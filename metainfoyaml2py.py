import yaml
import os
import autopep8
import sys

def read_yaml(path: str) -> dict:
    """Help function for reading YAML file into dict using pyyaml."""
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def yaml2py(yaml_path: str, output_dir: str='') -> None:
    # Read the YAML file into dict and get the definitions key
    try:
        yaml_dict = read_yaml(yaml_path).get('definitions')
    except KeyError:
        raise ValueError('No "definitions" key found in YAML file.')
    # Get the standard contents from the 'standard_file_content.yaml' file
    content = read_yaml('standard_file_content.yaml')
    # Create output file with context manager
    with open(os.path.join(output_dir, '__init__.py'), 'w') as file:
        # Write the file content to string variable `code`
        code = content['header'] + '\n'
        code += content['imports'] + '\n'
        # Get the package name, defaults to YAML file name (without .schema.archive.yaml)
        package_name = yaml_dict.get('name', os.path.basename(yaml_path).split('/')[-1].split('.')[0])
        code += content['package_name'] % package_name + '\n'
        code += content['footer'] + '\n'
        # Clean up the code using autopep8
        cleaned_code = autopep8.fix_code(code, options={'aggressive': 2})
        # write the code to file
        file.write(cleaned_code)


def main(sys_args):
    yaml2py(*sys_args[1:])

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.exit("Please provide path to YAML file and optionally path to output directory.")
    main(sys.argv)
