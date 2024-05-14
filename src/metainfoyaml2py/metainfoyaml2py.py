'''
metainfoyaml2py module
'''

import argparse
import os
import shutil
import json
from typing import Any, Iterable
import warnings
import re

import toml
import yaml
import autopep8
import autoflake

from pkg_resources import resource_filename

resource_path = resource_filename(__name__, 'resources')


def _to_camel_case(input_string: str) -> str:
    '''
    Help function for converting sub section names to CamelCase.

    Args:
        input_string (str): The input string with space, -, _, or CamelCase for separation.

    Returns:
        str: The input converted to CamelCase.
    '''
    matches = re.finditer(
        r'.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',
        input_string,
    )
    words = []
    for match in matches:
        words += match.group(0).replace("-", " ").replace("_", " ").split()
    return ''.join(word[:1].upper() + word[1:] for word in words)


def _to_snake_case(input_string: str) -> str:
    '''
    Help function for converting package name to snake_case.

    Args:
        input_string (str): The input string with space, -, _, or CamelCase for separation.

    Returns:
        str: The input converted to snake_case.
    '''
    matches = re.finditer(
        r'.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',
        input_string,
    )
    words = []
    for match in matches:
        words += match.group(0).replace("-", " ").replace("_", " ").split()
    return '_'.join(word.lower() for word in words)


def set_nested(mapping: dict, nested_key: list, value: Any) -> None:
    '''
    Helper function for setting a nested value in a dict.

    Args:
        mapping (dict): The nested dictionary.
        nested_key (list): A list of the nested keys from outer to inner.
        value (Any): The value to set.

    Returns:
        _type_: The nested dictionary with the set value.
    '''
    _nested_dict = mapping.copy()
    _keys = nested_key.copy()
    key = _keys.pop(0)
    if len(_keys) == 0:
        _nested_dict[key] = value
        return _nested_dict
    else:
        _nested_dict[key] = set_nested(_nested_dict.get(key, {}), _keys, value)
        return _nested_dict


def read_yaml(path: str) -> dict:
    '''
    Help function for reading YAML file into dict using pyyaml.

    Args:
        path (str): The path to the YAML file including the `.yaml` extension.

    Returns:
        dict: Dictionary representation of the YAML file.
    '''
    with open(path, 'r', encoding="utf8") as file:
        return yaml.safe_load(file)
    

def update_mapping_file(path: str, nested_keys: Iterable[list], values: Iterable) -> None:
    '''
    Help function for updating a nested key value in a yaml or toml file.

    Args:
        path (str): The path to the file.
        nested_keys (Iterable[list]): An iterable of lists with the nested keys as items.
        values (Iterable): An iterable of the values corresponding to the keys.

    Raises:
        ValueError: For unsupported file endings.
    '''
    with open(path, 'r', encoding='utf-8') as fh:
        if path.endswith('.yaml'):
            mapping = yaml.safe_load(fh)
        elif path.endswith('.toml'):
            mapping = toml.load(fh)
        else:
            raise ValueError(f'Unsupported file ending for: {path}')
    for nested_key, value in zip(nested_keys, values):
        mapping = set_nested(mapping=mapping, nested_key=nested_key, value=value)
    with open(path, 'w', encoding='utf-8') as fh:
        if path.endswith('.yaml'):
            yaml.dump(mapping, fh)
        elif path.endswith('.toml'):
            toml.dump(mapping, fh)

def parse_annotation(section_dict: dict) -> str:
    '''
    Parse all m_annotations into python variables which are prepended by "a_".

    Args:
        section_dict (dict): The yaml dictionary for the MSection containing the
        annotations.

    Returns:
        str: The m_annotations as a str of python variables.
    '''
    code = ""
    for annotation_type, annotation in section_dict.pop("m_annotations", {}).items():
        code += f"        a_{annotation_type}={json.dumps(annotation, indent=4)},\n"
    return code


def parse_quantity(quantity_name: str, quantity_dict: dict) -> str:
    '''
    Parse the content of metainfo quantity into Python instance.

    Args:
        quantity_name (str): The name of the quantity.
        quantity_dict (dict): A dictionary representation for the YAML content for the 
        quantity to be parsed.

    Returns:
        str: The instantiated quantity variable of the parsed quantity as python code.

    Raises:
        ValueError: If the YAML file is not a valid NOMAD metainfo schema.
    '''
    code = ""
    code += f"{quantity_name} = Quantity(\n"
    try:
        quantity_type = quantity_dict.pop('type')
    except KeyError as exc:
        raise ValueError(f'No "type" key found in quantity {quantity_name}.') from exc
    if isinstance(quantity_type, dict):
        if quantity_type['type_kind'] == 'Enum':
            quantity_type = f"MEnum({quantity_type['type_data']})"
        else:
            raise ValueError('Unknown type_kind in quantity.')
    elif quantity_type == 'string':
        quantity_type = 'str'
    elif quantity_type == 'integer':
        quantity_type = 'int'
    elif quantity_type == 'boolean':
        quantity_type = 'bool'
    code += f"        type={quantity_type.replace('#/','')},\n"
    if "description" in quantity_dict:
        description = quantity_dict.pop('description')
        if description.endswith('\n'):
            description = description[:-1].replace('\n', '\n        ')
            code += f"        description='''\n        {description}\n        ''',\n"
        else:
            code += f"        description='{description}',\n"
    code += parse_annotation(quantity_dict)
    for keyword, value in quantity_dict.items():
        indent = 4
        if isinstance(value, list):
            indent = None
        code += f"        {keyword}={json.dumps(value, indent=indent)},\n"
    code += "    )\n"
    return code


def parse_section(section_name: str, section_dict: dict) -> str:
    '''
    Parse the content of a metainfo section into a Python class.

    Args:
        section_name (str): The name of the section.
        section_dict (dict): A dictionary representation of the YAML content for the 
        section to be parsed.

    Returns:
        str: The class definition of the parsed section as python code.
    '''
    code = ""
    # Recursive definition of subsections
    sub_sections_code = ''
    sub_sections_dict = section_dict.pop("sub_sections", {})
    for sub_section, kwargs in sub_sections_dict.items():
        camel_name = _to_camel_case(sub_section)
        sub_section_def = kwargs.pop("section")
        if isinstance(sub_section_def, dict):
            code += parse_section(
                section_name=camel_name,
                section_dict=sub_section_def,
            ) + '\n'
        elif sub_section_def.startswith('nomad'):
            modules = sub_section_def.split('.')
            camel_name = modules.pop()
            code = f'from {".".join(modules)} import (\n    {camel_name},\n)' + '\n' + code
        elif sub_section_def.startswith('#/'):
            camel_name = sub_section_def[2:]
        elif '.' not in sub_section_def:
            camel_name = sub_section_def
        else:
            warnings.warn(f"Unable to import subsection: {sub_section}.")
        sub_sections_code += f'    {sub_section} = SubSection(\n'
        sub_sections_code += f'        section_def={camel_name},\n'
        sub_sections_code += parse_annotation(kwargs)
        for keyword, arg in kwargs.items():
            sub_sections_code += f'        {keyword}={json.dumps(arg, indent=4)},\n'
        sub_sections_code += ')\n'
    # Inheritance from base sections
    base_sections = []
    base_section_list = section_dict.pop("base_sections", [])
    if "base_section" in section_dict:
        base_section_list.append(section_dict.pop("base_section"))
    for base_section in base_section_list:
        base_section = base_section.replace('#/','')
        if not '.' in base_section:
            base_sections.append(base_section)
        elif base_section.startswith('nomad'):
            modules = base_section.split('.')
            base_class = modules.pop()
            code = f'from {".".join(modules)} import {base_class}' + '\n' + code
            base_sections.append(base_class)
        else:
            warnings.warn(f"Unable to inherit from referenced base section: {base_section}.")
    if 'ArchiveSection' not in base_sections:
        base_sections.append('ArchiveSection')
    base_classes = ""
    if len(base_sections) > 0:
        base_classes = f"({','.join(base_sections)})"
    # Description as docstring
    description = section_dict.pop(
        'description', 'Class autogenerated from yaml schema.')
    if description[-1] == '\n':
        description = description[:-1]
    code += f"class {section_name}{base_classes}:\n    '''"
    description = description.replace('\n', '\n    ')
    code += f"\n    {description}\n    '''\n"
    # Pop quantities
    quantities = section_dict.pop('quantities', {})
    code += "    m_def = Section(\n" 
    code += parse_annotation(section_dict)
    # Add remaining keys in section dictionary as keyword arguments to section definition
    for keyword in section_dict:
        code += f"        {keyword}={json.dumps(section_dict.get(keyword), indent=4)},\n"
    if code.endswith('\n'):
        code = code[:-1]
    code += ')\n'
    for quantity in quantities:
        code += '    ' + \
            parse_quantity(quantity_name=quantity,
                           quantity_dict=quantities[quantity])
    # Sub section references
    code += sub_sections_code
    return code


def create_plugin(location: str, package_name: str) -> str:
    '''
    Function for creating a nomad plugin package at a given location.

    Args:
        location (str): The location where the nomad plugin folder will be created.
        package_name (str): The name of the package.

    Returns:
        str: The location with filename where the schema should be placed.
    '''
    snake_package_name = _to_snake_case(package_name)
    plugin_loc = os.path.join(location, snake_package_name + '_plugin')
    shutil.copytree(
        src=os.path.join(resource_path, 'standard_plugin_content'),
        dst=plugin_loc,
    )
    os.rename(
        src=os.path.join(plugin_loc, 'src', 'plugin_name'),
        dst=os.path.join(plugin_loc, 'src', snake_package_name),
    )
    update_mapping_file(
        path=os.path.join(plugin_loc, 'src', snake_package_name, 'nomad_plugin.yaml'),
        nested_keys=(['name'],),
        values=(package_name,)
    )
    update_mapping_file(
        path=os.path.join(plugin_loc, 'pyproject.toml'),
        nested_keys=(['project','name'],),
        values=(snake_package_name,)
    )
    update_mapping_file(
        path=os.path.join(plugin_loc, 'nomad.yaml'),
        nested_keys=(['plugins','options','schemas/example','python_package'],),
        values=(snake_package_name,)
    )
    return os.path.join(plugin_loc, 'src', snake_package_name, 'schema.py')


def yaml2py(yaml_path: str, output_dir: str = '', normalizers: bool = False,
            plugin: bool = False) -> None:
    '''
    Function for parsing a NOMAD metainfo YAML schema into a python file of class definitions.

    Args:
        yaml_path (str): The path to the YAML file including the `.yaml` extension
        output_dir (str, optional): The output directory where the python file is saved.
        Defaults to ''.
        normalizers (bool, optional): Whether to add empty normalizers or not.
        Defaults to False.
        plugin (bool, optional): Whether or not to create the files needed for a NOMAD plugin.
        Defaults to False.

    Raises:
        ValueError: If the YAML file is not a valid NOMAD metainfo schema.
    '''
    # Read the YAML file into dict and get the definitions key
    try:
        yaml_dict = read_yaml(yaml_path).get('definitions')
    except KeyError as exc:
        raise ValueError('No "definitions" key found in YAML file.') from exc
    # Get the standard contents from the 'standard_file_content.yaml' file
    content = read_yaml(os.path.join(
        resource_path, 'standard_file_content.yaml'))
    # Get the package name, defaults to YAML file name (without
    # .schema.archive.yaml)
    file_name = os.path.basename(yaml_path).split("/")[-1].split('.')[0]
    package_name = yaml_dict.get('name', file_name)
    if plugin:
        output_file = create_plugin(output_dir, package_name)
    else:
        output_file = os.path.join(output_dir, f'{file_name}.py')
    # Create output file with context manager
    with open(output_file, 'w', encoding="utf8") as file:
        # Write the file content to string variable `code`
        code = content['imports'] + '\n'
        code += content['package_name'] % package_name + '\n'
        sections = yaml_dict.get('sections', {})
        for section in sections:
            section_dict = sections[section]
            code += parse_section(
                section_name=section,
                section_dict=section_dict,
            ) + '\n'
            if normalizers:
                code += (
                    '    ' +
                    content['normalizer'].replace('\n','\n    ') % (section, section) +
                    '\n'
                )
                if plugin:
                    test_loc = os.path.join(
                        output_dir,
                        _to_snake_case(package_name) + '_plugin',
                        'tests'
                    )
                    test_file = os.path.join(
                        test_loc,'data',f'test_{_to_snake_case(section)}.archive.yaml'
                    )
                    with open(test_file, 'w') as fh:
                        yaml.dump(
                            {
                                'data': {
                                    'm_def': f'{_to_snake_case(package_name)}.{section}'
                                }
                            },
                            fh
                        )
        code += content['footer'] + '\n'
        code = content['header'] + '\n' + code
        code = code.replace('true', 'True')
        code = code.replace('false', 'False')
        code = code.replace('null', 'None')
        # Clean up the code using autopep8 and autoflake
        flake8_cleaned_code = autoflake.fix_code(
            code, remove_all_unused_imports=True)
        cleaned_code = autopep8.fix_code(
            flake8_cleaned_code, options={'aggressive': 2, 'max_line_length': 90})
        # write the code to file
        file.write(cleaned_code)


def main() -> None:
    '''
    Main function for running the metainfo YAML to Python class definition parser.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'yaml_path',
        help='The path to the YAML schema that should be converted to Python classes.',
    )
    parser.add_argument(
        '-o',
        '--output_dir',
        default='',
        help=('The path to the output directory of the conversion. '
              'Defaults to the current directory.'),
    )
    parser.add_argument(
        '-n',
        '--normalizers',
        action='store_true',
        help='Add empty normalizers to all class definitions.',
    )
    parser.add_argument(
        '-p',
        '--plugin',
        action='store_true',
        help='Create all the necessary files for a nomad plugin.',
    )
    args = parser.parse_args()
    yaml2py(
        yaml_path=args.yaml_path,
        output_dir=args.output_dir,
        normalizers=args.normalizers,
        plugin=args.plugin,
    )


if __name__ == "__main__":
    main()
