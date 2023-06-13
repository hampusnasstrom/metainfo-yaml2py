# metainfo-yaml2py
A program for converting NOMAD metainfo YAML schemas into Python class definitions.

## Installation
`metainfo-yaml2py` is not yet on PyPI but you can install the latest version using:
```sh
pip install git+https://github.com/hampusnasstrom/metainfo-yaml2py.git
```
You can then run the program with:

```
$ metainfo-yaml2py <target file>
```

### For development
`metainfo-yaml2py` is currently under development and for installing and contributing you should clone the repository and install the package in editable mode (`-e`) using:
```
pip install -e .
```

## Example
Running `metainfo-yaml2py` on the following YAML file (with the `-n` flag):
```yaml:example/example.schema.archive.yaml
```

Will create the following python file:
```python:example/__init__.py
```

## Command Line Interface
```sh
metainfo-yaml2py --help
usage: metainfo-yaml2py [-h] [-o OUTPUT_DIR] [-n] [-p] yaml_path

positional arguments:
  yaml_path             The path to the YAML schema that should be converted to Python
                        classes.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The path to the output directory of the conversion. Defaults to
                        the current directory.
  -n, --normalizers     Add empty normalizers to all class definitions.
  -p, --plugin          Create all the necessary files for a nomad plugin.
```