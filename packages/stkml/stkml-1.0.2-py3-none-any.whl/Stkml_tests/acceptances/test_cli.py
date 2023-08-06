# coding=utf-8
import os
from click.testing import CliRunner
import unittest

from Stkml.Cli import cli
from Stkml_tests.acceptances.Fixtures import clone_fixture


class MainTest(unittest.TestCase):

    def setUp(self):
        pass


    def test_compile_exit_error_code_if_action_fails_not_0(self):
        # Assign
        runner = CliRunner()

        # Acts
        result = runner.invoke(cli, ['compile', '--input', '--backend', 'backend', '--output', 'outputfile'])

        # Assert
        self.assertNotEqual(result.exit_code, 0)

    # def test_compile_stackcore_should_generate_instance_file_when_stackml_architecture_is_valid(self):
    #     # Assign
    #     runner = CliRunner()
    #     with clone_fixture('empty_stackml_architecture') as working_directory:
    #         os.chdir(working_directory)
    #         stackml_architecture = '.'
    #         output_directory = 'output'
    #
    #         # Acts
    #         result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'stackcore',
    #                                      '--output', output_directory], input='y\n ')
    #
    #         # Assert
    #         ist_output_file = os.path.join(output_directory, 'Instance.ist.xml')
    #
    #         self.assertEqual(result.exit_code, 0, result)
    #         self.assertTrue(os.path.isfile(ist_output_file), f'the Instance file does not exists { ist_output_file }')
    #
    # def test_compile_stackcore_should_generate_initialization_file_when_stackml_architecture_is_valid(self):
    #     # Assign
    #     runner = CliRunner()
    #     with clone_fixture('empty_stackml_architecture') as working_directory:
    #         os.chdir(working_directory)
    #         stackml_architecture = '.'
    #         output_directory = 'output'
    #
    #         # Acts
    #         result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'stackcore',
    #                                      '--output', output_directory], input='y\n ')
    #
    #         # Assert
    #         ist_output_file = os.path.join(os.getcwd(), output_directory, 'Initialization.ini.xml')
    #
    #         self.assertEqual(result.exit_code, 0, result)
    #         self.assertTrue(os.path.isfile(ist_output_file),
    #                         f'the Initialization file does not exists { ist_output_file }')
    #
    #
    # def test_compile_stackcore_should_remove_output_folder_when_output_is_not_empty_and_user_accept(self):
    #     # Assign
    #     runner = CliRunner()
    #     with clone_fixture('non_empty_output_folder') as working_directory:
    #         os.chdir(working_directory)
    #         stackml_architecture = '.'
    #         output_directory = 'output'
    #
    #         # Acts
    #         result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'stackcore',
    #                                      '--output', output_directory], input='y\n')
    #
    #         # Assert
    #         output_content = os.path.join(os.getcwd(), output_directory, 'file.txt')
    #
    #         self.assertEqual(result.exit_code, 0, result)
    #         self.assertFalse(os.path.isfile(output_content),
    #                          f'the output directory is not be cleaned { output_content }')
    #
    # def test_compile_stackcore_should_not_remove_output_folder_when_output_is_not_empty_and_user_decline(self):
    #     # Assign
    #     runner = CliRunner()
    #     with clone_fixture('non_empty_output_folder') as working_directory:
    #         os.chdir(working_directory)
    #         stackml_architecture = '.'
    #         output_directory = 'output'
    #
    #         # Acts
    #         result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'stackcore',
    #                                      '--output', output_directory], input='N\n y\n output1')
    #
    #         # Assert
    #         output_content = os.path.join(os.getcwd(), output_directory, 'file.txt')
    #
    #         self.assertEqual(result.exit_code, 0, result)
    #
    #         self.assertTrue(os.path.isfile(output_content))
    #
    # def test_compile_stackcore_should_create_output_folder_when_output_is_not_found(self):
    #     # Assign
    #     runner = CliRunner()
    #     with clone_fixture('empty_stackml_architecture') as working_directory:
    #         os.chdir(working_directory)
    #         stackml_architecture = '.'
    #         output_directory = 'output'
    #
    #         # Acts
    #         result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'stackcore',
    #                                      '--output', output_directory], input='y\n ')
    #         # Assert
    #         output_content = os.path.join(os.getcwd(), output_directory)
    #
    #         self.assertEqual(result.exit_code, 0, result)
    #         self.assertTrue(os.path.isdir(output_content))

    def test_compile_should_show_error_when_input_file_does_not_exist(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('empty_stackml_architecture') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = 'StackMl_'
            output_file = 'output/test'

            # Acts
            result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'diagram',
                                         '--type', '1', '--output', output_file])

            # Assert
            self.assertEqual(result.exit_code, 2, result)
            self.assertEqual(result.output.split(stackml_architecture)[1],
                             f' doesn\'t exist\n', f'the input file {stackml_architecture}'
                                                   f' does not exist and the exception hase been raised ')

    def test_compile_should_show_error_when_backend_archeitecture_does_not_exist(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('empty_stackml_architecture') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = '.'
            output_directory = 'output'
            backend = 'backend'

            # Acts
            result = runner.invoke(cli, ['compile', '--input', stackml_architecture, backend])
            # Assert
            self.assertEqual(result.exit_code, 2, result)
            self.assertIn(f"Error: No such command \'{backend}\'.", result.output)


    def test_compile_should_show_error_when_input_file_is_not_well_formed(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('not_well_formed_stackml_architecture') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = '.'
            output_file = 'output/test'

            # Acts
            result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'diagram',
                                         '--type', '1', '--output', output_file])

            # Assert
            self.assertEqual(result.exit_code, 1, result)
            self.assertIn('YAML is not valid', result.output)

    def test_compile_should_show_error_when_input_file_does_not_respect_stackml_schema(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('not_valid_stackml_schema') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = '.'
            output_file = 'output/test'

            # Acts
            result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'diagram',
                                         '--type', '1', '--output', output_file])

            # Assert
            self.assertEqual(result.exit_code, 1, result)
            self.assertIn("Schema validation No", result.output)

    def test_check_should_show_error_when_input_file_does_not_exist(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('empty_stackml_architecture') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = 'StackMl_.xml'

            # Acts
            result = runner.invoke(cli, ['check', '--input', stackml_architecture])

            # Assert
            self.assertEqual(result.exit_code, 2, result)
            self.assertEqual(result.output.split(stackml_architecture)[1], f" doesn\'t exist\n")

    def test_check_should_show_error_when_input_file_is_not_well_formed(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('not_well_formed_stackml_architecture') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = '.'

            # Acts
            result = runner.invoke(cli, ['check', '--input', stackml_architecture])

            # Assert
            self.assertEqual(result.exit_code, 1, result)
            self.assertIn('YAML is not valid', result.output)


    def test_init_should_generate_stackml_file(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('stkml_project') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = 'Test'

            # Acts
            result = runner.invoke(cli, ['init', '--path', stackml_architecture], input=' y\n IoT System\nsys1\nuseCas1\n')

            # Assert
            stackml_file = os.path.join(stackml_architecture, 'main.stkml.yaml')

            self.assertEqual(result.exit_code, 0, result)
            self.assertTrue(os.path.isfile(stackml_file), f'the Stackml file does not exists { stackml_file }')


    def test_compile_diagram_should_generate_image_system_diagram(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('diagram_level_1') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = 'Test'
            output_file = 'img/test'

            # Acts
            result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'diagram',
                                         '--type', '1', '--output', output_file])

            # Assert
            output_file = f'{output_file}.png'
            self.assertEqual(result.exit_code, 0, result)
            self.assertTrue(os.path.isfile(output_file), f'the image file does not exists {output_file}')




    def test_compile_diagram_should_generate_image_for_topology_diagram(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('diagram_tpology') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = 'Test'
            output_file = 'img/test'

            # Acts
            result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'diagram',
                                         '--type', '2', '--output', output_file])

            # Assert
            output_file = f'{output_file}.png'
            self.assertEqual(result.exit_code, 0, result)
            self.assertTrue(os.path.isfile(output_file), f'the image file does not exists {output_file}')

    def test_compile_diagram_should_generate_map_for_topology_diagram(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('diagram_tpology') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = 'Test'
            output_file = 'img/test'

            # Acts
            result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'diagram',
                                         '--type', '3', '--output', output_file])

            # Assert
            output_file = f'{output_file}.html'
            self.assertEqual(result.exit_code, 0, result)
            self.assertTrue(os.path.isfile(output_file), f'the html file does not exists {output_file}')


    def test_compile_drawio_should_generate_drawio_file_for_architecture_diagram_level_1(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('diagram_level_1') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = 'Test'
            output_file = 'drawio/test'

            # Acts
            result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'drawio',
                                         '--level', '1', '--output', output_file])

            # Assert
            output_file = f'{output_file}.drawio'
            self.assertEqual(result.exit_code, 0, result)
            self.assertTrue(os.path.isfile(output_file), f'the drawio file does not exists {output_file}')

    def test_compile_drawio_should_generate_drawio_file_for_architecture_diagram_level_2(self):
        # Assign
        runner = CliRunner()
        with clone_fixture('diagram_level_2') as working_directory:
            os.chdir(working_directory)
            stackml_architecture = 'Test'
            output_file = 'drawio/test'

            # Acts
            result = runner.invoke(cli, ['compile', '--input', stackml_architecture, 'drawio',
                                         '--level', '2', '--output', output_file])

            # Assert
            output_file = f'{output_file}.drawio'
            self.assertEqual(result.exit_code, 0, result)
            self.assertTrue(os.path.isfile(output_file), f'the drawio file does not exists {output_file}')
