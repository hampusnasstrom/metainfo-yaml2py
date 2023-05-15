'''
metainfoyaml2py module
'''

import argparse
import os
import json
import warnings
import re

import yaml
import autopep8
import autoflake

from pkg_resources import resource_filename

resource_path = resource_filename(__name__, 'resources')


def _to_camel_case(input_string: str) -> str:
    '''Help function for converting sub section names to CamelCase.

    Args:
        input_string (str): The input string with space, - or _ for separation.

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


def read_yaml(path: str) -> dict:
    '''Help function for reading YAML file into dict using pyyaml.

    Args:
        path (str): The path to the YAML file including the `.yaml` extension.

    Returns:
        dict: Dictionary representation of the YAML file.
    '''
    with open(path, 'r', encoding="utf8") as file:
        return yaml.safe_load(file)


def parse_annotation(section_dict: dict) -> str:
    '''
    Parse all m_annotations into python variables which are prepended by "a_".

    Args:
        section_dict (dict): The yaml dictionary for the MSection containing the
        annotations.

    Returns:
        str: The m_annotations as a str of python variables.
    '''
    code = ", "
    for annotation_type, annotation in section_dict.pop("m_annotations", {}).items():
        code += f"a_{annotation_type}={json.dumps(annotation)}, "
    return code


def parse_quantity(quantity_name: str, quantity_dict: dict) -> str:
    '''Parse the content of metainfo quantity into Python instance.

    Args:
        quantity_name (str): The name of the quantity.
        quantity_dict (dict): A dictionary representation for the YAML content for the quantity to
        be parsed.

    Returns:
        str: The instantiated quantity variable of the parsed quantity as python code.

    Raises:
        ValueError: If the YAML file is not a valid NOMAD metainfo schema.
    '''
    code = ""
    code += f"{quantity_name} = Quantity("
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
    code += "type=" + quantity_type.replace('#/','')
    if "description" in quantity_dict:
        code += ", description=" + "'" + \
            quantity_dict.pop('description').replace('\n', '\\n') + "'"
    code += parse_annotation(quantity_dict)[:-2]
    for keyword, value in quantity_dict.items():
        code += f", {keyword}={json.dumps(value)}"
    code += ")\n"
    return code


def parse_section(section_name: str, section_dict: dict) -> str:
    '''Parse the content of a metainfo section into a Python class.

    Args:
        section_name (str): The name of the section.
        section_dict (dict): A dictionary representation of the YAML content for the section to be
        parsed.

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
            code = f'from {".".join(modules)} import {camel_name}' + '\n' + code
        else:
            warnings.warn(f"Unable to import subsection: {sub_section}.")
        sub_sections_code += f'    {sub_section} = SubSection(section_def={camel_name}'
        sub_sections_code += parse_annotation(kwargs)[:-2]
        for keyword, arg in kwargs.items():
            sub_sections_code += f', {keyword}={json.dumps(arg)}'
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
    base_classes = ""
    if len(base_sections) > 0:
        base_classes = f"({','.join(base_sections)})"
    # Description as docstring
    description = section_dict.pop(
        'description', 'Class autogenerated from yaml schema.')
    if description[-1] == '\n':
        description = description[:-1]
    code += f"class {section_name}{base_classes}:\n    '''{description}'''\n    pass\n"
    # Pop quantities
    quantities = section_dict.pop('quantities', {})
    code += "    m_def = Section(" + parse_annotation(section_dict)[2:]
    # Add remaining keys in section dictionary as keyword arguments to section definition
    for keyword in section_dict:
        code += f"{keyword}={json.dumps(section_dict.get(keyword))}, "
    if code.endswith(', '):
        code = code[:-2]
    code += ')\n'
    for quantity in quantities:
        code += '    ' + \
            parse_quantity(quantity_name=quantity,
                           quantity_dict=quantities[quantity])
    # Sub section references
    code += sub_sections_code
    return code


def yaml2py(yaml_path: str, output_dir: str = '', normalizers: bool = False,
            plugin: bool = False) -> None:
    '''Function for parsing a NOMAD metainfo YAML schema into a python file of class definitions.

    Args:
        yaml_path (str): The path to the YAML file including the `.yaml` extension
        output_dir (str, optional): The output directory where the `__init__.py` file is saved.
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
    # Create output file with context manager
    with open(os.path.join(output_dir, '__init__.py'), 'w', encoding="utf8") as file:
        # Write the file content to string variable `code`
        code = content['imports'] + '\n'
        # Get the package name, defaults to YAML file name (without
        # .schema.archive.yaml)
        file_name = os.path.basename(yaml_path).split("/")[-1]
        package_name = yaml_dict.get('name', file_name.split('.')[0])
        code += content['package_name'] % package_name + '\n'
        sections = yaml_dict.get('sections', {})
        for section in sections:
            section_dict = sections[section]
            code += parse_section(
                section_name=section,
                section_dict=section_dict,
            ) + '\n'
        code += content['footer'] + '\n'
        code = content['header'] + '\n' + code
        code = code.replace('true', 'True')
        code = code.replace('false', 'False')
        code = code.replace('null', 'None')
        # Clean up the code using autopep8 and autoflake
        flake8_cleaned_code = autoflake.fix_code(
            code, remove_all_unused_imports=True)
        cleaned_code = autopep8.fix_code(
            flake8_cleaned_code, options={'aggressive': 2})
        # write the code to file
        file.write(cleaned_code)
        if normalizers:
            raise NotImplementedError
        if plugin:
            raise NotImplementedError


def main() -> None:
    '''Main function for running the metainfo YAML to Python class definition parser.
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
