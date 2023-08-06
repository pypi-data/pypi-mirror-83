## Stkml-cli
![continuous_integration](https://github.com/Stackitect/stackml-cli/workflows/continuous_integration/badge.svg)
![publish_to_Pypi](https://github.com/Stackeo-io/stackml-cli/workflows/publish_to_Pypi/badge.svg)
[![PyPI package](https://badge.fury.io/py/stkml.svg)](https://pypi.python.org/pypi/stkml/)
[![downloads](https://img.shields.io/pypi/dm/stkml.svg)](https://pypistats.org/packages/stkml)


STKML is an open-source IoT stack coding language developed by Stackeo and INRIA for both industry and academic research. STKML allows you to describe an IoT system globally and then to detail its different entities and their relationships in a simple way. Thus IoT teams can quickly visualize and verify the principles of the end-to-end architecture, create simulation or reproducible test scenarios for the sizing and forecasting of the non-functional properties of a connected system or an IoT solution. end to end before its large-scale deployment. STKML also allows vendors to create libraries of IoT product models and architecture patterns for integration into an architectural design.

A set of tools associated with STKML (enriched online editor, transpilators, diagramming tools, topology checking tools, model libraries) are being developed to support developers in assisted coding and compilation of their models. components and architecture in order to automatically generate models, their documentation or the associated simulation or deployment scenarios. The user can thus contribute to the Stacker community, by creating, reusing and manipulating frameworks and architectural templates and models of IoT system components.

The implementation is compatible with python3.6

## Usage

1. Installation of application

```bash
pip install stkml
```

2. Run the application

You can run the application with the following command

```bash
stkml

Usage: stkml [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help  Show this message and exit.

Commands:
  check    check stkml file architecture
  compile  compile stkml file using a specific backend
  init     initialize a stkml project

Usage: stkml compile [OPTIONS] COMMAND [ARGS]...

  compile stkml file using a specific backend

Options:
  -i, --input TEXT                the file to compile
  -d, --disable-syntax-verification
                                  ignore syntax verification
  -h, --help                      Show this message and exit.

Commands:
  diagram    compile stkml file for
  drawio     compile stkml file for drawio




Usage: stkml compile diagram [OPTIONS]

  compile stkml file for diagram

  Example:     stkml compile -i architecture.stkml diagram -t 1 -o img

Options:
  -t, --type [1|2|3]  the diagram type {Architecture ,Topology or Map}
                      [required]

  -i, --icons TEXT    the icon folder {it contains [Node_Id].png files}
  -o, --output TEXT   the output file  [required]
  -h, --help          Show this message and exit.



Usage: stkml compile drawio [OPTIONS]

  compile stkml file for Drawio

  Example:     stkml compile -i architecture.stkml Drawio -l 1 -o Drawio

Options:
  -l, --level [1|2]  the diagram view level {System View or Layer View}
                     [required]

  -i, --icons TEXT   the icon folder {it contains [Node_Id].png files}
  -o, --output TEXT  the output file  [required]
  -h, --help         Show this message and exit.




stkml check --input architecture

Usage: stkml check [OPTIONS]

  check stkml project

Options:
  -i, --input TEXT               the stkml project to check
  --disable-syntax-verification  ignore syntax verification
  --help                         Show this message and exit.


stkml init

Usage: stkml init [OPTIONS]

  initialize a stkml project

Options:
  -i, --input TEXT    the file to compile to stkml
  -b, --backend TEXT  the file backend [drawio]
  -p, --path TEXT     the stkml project directory
  -h, --help          Show this message and exit.


```

3. Configure the Ide

  See the [stkml documentation](https://stkml.stackeo.io/rst/developer_guide/index.html#configure-the-ide)

4. Diagram Examples
    -   System Diagram
          ```
          stkml compile -i Examples/example.stkml diagram -t 1 -o Examples/results/diagram/Type1/level1 --icons Examples/icons/
          ```
          Result :
          ![](https://stkml.stackeo.io/_images/level1.png)

    -   Deployment Topology Diagram
          ```
          stkml compile -i Examples/example.stkml diagram -t 2 -o Examples/results/Type2/diagram/level1 --icons Examples/icons/
          ```
          Result :
          ![](https://stkml.stackeo.io/_images/level11.png)

    -   Deployment Map
          ```
          stkml compile -i Examples/example.stkml diagram -t 3 -o Examples/results/Type2/diagram/level2.html --icons Examples/icons/
          ```
          Result :

           [![](https://stkml.stackeo.io/_static/results/type3.png)](https://stkml.stackeo.io/_static/results/level2_2.html)




4. Drawio Examples

    - level 1 :
      ```
      stkml compile -i Examples/example.stkml drawio -l 1 -o Examples/results/Type1/level1
      ```
      Result :
      [![](https://stkml.stackeo.io/_static/results/level1.png)](https://stkml.stackeo.io/_static/results/level1.html)

    - level 2 :
      ```
      stkml compile -i Examples/example.stkml drawio -l 2 -o Examples/results/Type1/level2
      ```
      Result :
      [![](https://stkml.stackeo.io/_static/results/level2.png)](https://stkml.stackeo.io/_static/results/level2.html)
