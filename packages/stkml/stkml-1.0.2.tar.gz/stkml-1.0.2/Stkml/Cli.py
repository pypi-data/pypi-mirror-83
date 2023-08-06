#Copyright STACKEO - INRIA 2020
# pylint: disable=redefined-builtin

from __future__ import print_function

import json
import os
import sys
import shutil

import click
import requests

from jinja2 import Environment, FileSystemLoader

from Stkml.Diagram.Map.RegionNotFound import RegionNotFound
from Stkml.Drawio import DrawIO
from Stkml.Stkml import Stkml, StkmlSyntaxicErrorList, ModelException, WarningList
from Stkml.Diagram import  StkmlDiagram
from Stkml import MODULE_DIR, __version__
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


CONTEXT_SETTINGS = {'help_option_names':['-h', '--help']}
ICONS = os.path.join(MODULE_DIR, 'templates/diagram/resources/')
@click.group()
@click.version_option(__version__)
def cli():
    latest_version = get_stackml_latest_version()
    if latest_version:
        if __version__ != latest_version:
            click.secho(f"""[WARN] deprecated stackml@{__version__}: stackml@<{latest_version}\
is no longer maintained. Upgrade to stackml@^{latest_version} using\
"pip install --upgrade stackml" """,
                        fg='yellow')

@click.command('check', help='check stackml project', context_settings=CONTEXT_SETTINGS)
@click.option('--input', '-i', 'stackmlfile', help='the stackml project to check')
@click.option('--disable-syntax-verification', '-d', help='ignore syntax verification', is_flag=True)
def check(stackmlfile: str, disable_syntax_verification: bool) -> None:
    stackml, _ = create_stackml(stackmlfile)
    try:
        check_stackml(stackml, disable_syntax_verification)
    except click.ClickException as error:
        click.secho(f"[ERROR] {error}", fg='red')
        sys.exit(1)
    else:
        click.secho("[SUCCESS] File checked successfully", fg='green')


@click.group('compile', help='compile Stackml file using a specific backend',
             context_settings=CONTEXT_SETTINGS)
@click.option('--input', '-i', 'stackmlfile', help='the file to compile')
@click.option('--disable-syntax-verification', '-d', help='ignore syntax verification', is_flag=True)
@click.pass_context
def compile(ctx: click.Context, stackmlfile: str, disable_syntax_verification: bool) -> None:
    if stackmlfile:
        stackml, working_dir = create_stackml(stackmlfile)
        try:
            check_stackml(stackml, disable_syntax_verification)
        except click.ClickException as error:
            click.secho(f"[ERROR] {error}", fg='red')
            sys.exit(1)
        else:
            try:
                stackml.create_architecture()
            except ModelException as error:
                click.secho(f"[ERROR] {error} ", fg='red')
                sys.exit(1)
            else:
                ctx.ensure_object(dict)
                ctx.obj['Stackml'] = stackml
                ctx.obj['working_dir'] = working_dir

@click.command('diagram', short_help='compile Stackml file for diagram', context_settings=CONTEXT_SETTINGS)
@click.option('--type', '-t', 'type', help='the diagram type {Architecture ,Topology or Map}',
              required=True, type=click.Choice(['1', '2', '3']))
@click.option('--icons', '-i', 'icons', default=ICONS, help='the icon folder {it contains [Node_Id].png files}')
@click.option('--output', '-o', 'outputfile', required=True, help='the output file')
@click.pass_context
def diagram(ctx: click.Context, type: str, icons: str, outputfile: str) -> None:
    """
    compile Stackml file for diagram

    Example:
    \b
        Stackml compile -i architecture.stkml diagram -t 1 -o img
    """
    if which('dot'):
        stackml = ctx.obj['Stackml']
        working_dir = ctx.obj['working_dir']
        outputfile = os.path.join(working_dir, outputfile)
        diagram_ = StkmlDiagram(icons=icons)
        try:
            result = diagram_.diagram_from_stackml(type_=int(type),
                                                   stackml=stackml, output=outputfile)
        except FileNotFoundError as error:
            click.secho(f"[ERROR] {error} ", fg='red')
        except RegionNotFound as error:
            click.secho(f"[ERROR] {error} ", fg='red')
        else:
            if result:
                click.secho(result.rstrip().replace('Warning:', '[WARN]'), fg='yellow')
            click.secho("[SUCCESS] Compilation completed successfully", fg='green')
    else:
        click.secho("""[WARN] failed to execute 'dot',
                    make sure the Graphviz 'https://www.graphviz.org/' executables are on your systems' PATH""",
                    fg='yellow')


@click.command('drawio', short_help='compile Stackml file for Drawio', context_settings=CONTEXT_SETTINGS)
@click.option('--level', '-l', 'level', help='the diagram view level {System View or Layer View}', required=True,
              type=click.Choice(['1', '2']))
@click.option('--icons', '-i', 'icons', default=ICONS, help='the icon folder {it contains [Node_Id].png files}')
@click.option('--output', '-o', 'outputfile', required=True, help='the output file')
@click.pass_context
def drawio(ctx: click.Context, level: str, icons: str, outputfile: str) -> None:
    """
    compile Stackml file for Drawio

    Example:
    \b
        Stackml compile -i architecture.stkml Drawio -l 1 -o Drawio
    """

    stackml = ctx.obj['Stackml']
    working_dir = ctx.obj['working_dir']
    outputfile = os.path.join(working_dir, outputfile)
    template_dir = os.path.join(MODULE_DIR, 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    drawio_ = DrawIO(default_icons=ICONS, icons=icons)
    erreur = drawio_.from_stackml(stackml)
    if erreur:
        click.secho(f"[Error] {erreur} ", fg='red')
        sys.exit(1)
    warnings = drawio_.generate_drawio_diagram(output=outputfile, env=env, level=int(level))
    if len(warnings) > 0:
        for warn in warnings:
            click.secho(f"[WARN] {warn} ", fg='yellow')

    click.secho("[SUCCESS] Compilation completed successfully", fg='green')



@click.command('init', help='initialize a Stackml project', context_settings=CONTEXT_SETTINGS)
@click.option('--input', '-i', 'file', help='the file to compile to Stackml', type=str, default=None)
@click.option('--backend', '-b', 'backend', help='the file backend', type=str, default=None)
@click.option('--path', '-p', 'stackmldir', type=str, help='the Stackml project directory', default='.')
def init(stackmldir: str, file: str, backend: str) -> None:
    working_dir = os.path.realpath(os.getcwd())
    #project_dir = os.path.join(working_dir, stackmldir)
    project_dir = check_folder_empty(working_dir, stackmldir)
    if project_dir:
        template_dir = os.path.join(MODULE_DIR, 'templates')
        stackml = Stkml()
        stackml.topology.name = click.prompt('Enter the system Name', type=str)
        stackml.topology.type = '' #click.prompt('Enter the system type', type=str)
        stackml.topology.usecase = click.prompt('Enter the system use case', type=str)
        env = Environment(loader=FileSystemLoader(template_dir))
        if file and backend:
            if backend == 'Drawio':
                file = os.path.join(working_dir, file)
                drawio_ = DrawIO(ICONS, ICONS)
                drawio_.create_drawio(file)
                stackml.from_drawio(drawio_)
        output = stackml.generate_files(environment=env)
        outputfile = os.path.join(project_dir, 'main.stkml.yaml')
        with open(outputfile, 'w') as stackml_file:
            stackml_file.write(output)
        click.secho("[SUCCESS] Stackml project initialized successfully", fg='green')


def check_stackml(stackml, disable_syntax_verification) -> bool:
    try:
        stackml.check_stackml_project()
    except Exception as error:
        raise click.ClickException(f'YAML is not valid, {stackml.stackmlfile} {error}')
    else:
        click.secho("[INFO] YAML is valid", fg='blue')
        if disable_syntax_verification:
            click.secho("[INFO] Ignore syntax verification", fg='blue')
        else:
            try:
                warn = stackml.validate_stackml_project()
            except FileNotFoundError as error:
                raise click.ClickException(f'{error} not found')
            except Exception as error:
                raise click.ClickException(f'Schema validation No\n {error}')
            else:
                if not warn:
                    click.secho("[INFO] Schema validation Ok", fg='blue')
                else:
                    click.secho(f"[WARN] {warn}", fg='yellow')


def create_stackml(stackml_folder):
    working_dir = os.path.realpath(os.getcwd())
    stackml_folder = os.path.join(working_dir, stackml_folder)
    if not os.path.isdir(stackml_folder):
        raise click.BadParameter(message=f'{stackml_folder} doesn\'t exist', param=stackml_folder, param_hint='--input')
    if not os.path.isfile(os.path.join(stackml_folder, 'main.stkml.yaml')):
        raise click.BadParameter(message=f'{os.path.join(stackml_folder,"main.stkml.yaml") } doesn\'t exist',
                                 param=stackml_folder, param_hint='--input')
    stackml = Stkml(stackml_folder)
    return stackml, working_dir

def check_folder_empty(working_dir, outputdir):
    output_dir = os.path.join(working_dir, outputdir)
    if os.path.isdir(output_dir):
        if len(os.listdir(outputdir)) != 0:
            click.secho(f"[WARN] {output_dir} is not empty", fg='yellow')
            if click.confirm('Do you want to delete its content', abort=False):
                shutil.rmtree(output_dir)
                os.makedirs(output_dir)
                return output_dir
            return None
        return output_dir
    if click.confirm(f'{output_dir} Does not existe, do you want to create it', abort=False):
        os.makedirs(output_dir)
        return output_dir
    return None


def which(program):
    return shutil.which(program)

def get_stackml_latest_version() -> str or None:
    try:
        request = requests.get('https://pypi.org/pypi/stkml/json')
    except requests.exceptions.ConnectionError :
        pass
    else:
        version = None
        if request.status_code == 200:
            stackml_pypi = json.loads(request.content.decode("utf-8"))
            version = list(stackml_pypi['releases'].keys())[-1]
        request.close()
        return version

cli.add_command(check)
cli.add_command(compile)
cli.add_command(init)
compile.add_command(diagram)
compile.add_command(drawio)
if __name__ == '__main__':
    cli()
