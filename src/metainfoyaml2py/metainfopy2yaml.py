'''
metainfpy2yaml module
'''

import os
import argparse
import importlib.util
import json
import yaml
from types import ModuleType

def m_package_to_yaml(module: ModuleType, output_dir: str=None) -> None:
    '''
    Convert the metainfo package to a YAML schema.
    '''
    yaml_dict = {
        'definitions': {
            'sections': {},
        },
    }
    m_package = module.m_package
    for section in m_package['section_definitions']:
        yaml_dict['definitions']['sections'][section.name] = json.loads(
            getattr(module, section.name).m_to_json())
    file_name = 'schema.archive.yaml'
    if output_dir:
        file_name = os.path.join(output_dir, file_name)
    with open(file_name, 'w') as file:
        yaml.dump(yaml_dict, file)


def py2yaml(python_path: str, output_dir: str) -> None:
    '''
    Convert Python class definitions
    to YAML schema definitions.
    '''
    module = python_path.split('/')[-1].split('.')[0]
    spec=importlib.util.spec_from_file_location(module, python_path)
    
    schema_package = importlib.util.module_from_spec(spec)
    
    spec.loader.exec_module(schema_package)
    
    schema_dict = json.loads(schema_package.m_package.m_to_json())
    print(json.dumps(schema_dict, indent=2))


def main() -> None:
    '''
    Main function for running the metainfo Python class definition to YAML parser.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'python_path',
        help='The path to the Python classes that should be converted to YAML schema.',
    )
    parser.add_argument(
        '-o',
        '--output_dir',
        default='',
        help=('The path to the output directory of the conversion. '
              'Defaults to the current directory.'),
    )
    args = parser.parse_args()
    py2yaml(
        python_path=args.python_path,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
