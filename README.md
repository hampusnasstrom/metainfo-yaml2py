![](https://github.com/hampusnasstrom/metainfo-yaml2py/actions/workflows/publish.yml/badge.svg)
![](https://img.shields.io/pypi/pyversions/metainfoyaml2py)
![](https://img.shields.io/pypi/l/metainfoyaml2py)
![](https://img.shields.io/pypi/v/metainfoyaml2py)

# metainfo-yaml2py
A program for converting NOMAD metainfo YAML schemas into Python class definitions.

## Installation
`metainfo-yaml2py` can be installed from PyPI using pip:
```sh
pip install metainfoyaml2py
```
You can then run the program with:

```
metainfo-yaml2py <target file>
```

### For development
`metainfo-yaml2py` is currently under development and for installing and contributing you should clone the repository and install the package in editable mode (`-e`) using:
```
pip install -e .
```

## Example
Running `metainfo-yaml2py` on the following YAML file (with the `-n` flag):
```yaml
definitions:
  name: Example Schema
  sections:
    Activity:
      description: |
        A base class for any activity in relation to an entity.
        This docstring can span multiple lines.
      quantities:
        start_time:
          description: |
            The starting date and time of the activity.
          type: Datetime
          m_annotations:
            eln:
              component: DateTimeEditQuantity
        end_time:
          description: |
            The ending date and time of the activity.
          type: Datetime
          m_annotations:
            eln:
              component: DateTimeEditQuantity
    Entity:
      description: |
        A base class for any entity which can be related to an activity.
```

Will create the following python file:
```python
#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from nomad.datamodel.data import ArchiveSection
from typing import (
    TYPE_CHECKING,
)
from nomad.metainfo import (
    Package,
    Quantity,
    Datetime,
    Section,
)
from nomad.datamodel.data import (
    ArchiveSection,
)
if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

m_package = Package(name='Example Schema')


class Activity(ArchiveSection):
    '''
    A base class for any activity in relation to an entity.
    This docstring can span multiple lines.
    '''
    m_def = Section()
    start_time = Quantity(
        type=Datetime,
        description='''
        The starting date and time of the activity.
        ''',
        a_eln={
            "component": "DateTimeEditQuantity"
        },
    )
    end_time = Quantity(
        type=Datetime,
        description='''
        The ending date and time of the activity.
        ''',
        a_eln={
            "component": "DateTimeEditQuantity"
        },
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `Activity` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super().normalize(archive, logger)


class Entity(ArchiveSection):
    '''
    A base class for any entity which can be related to an activity.
    '''
    m_def = Section()

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        '''
        The normalizer for the `Entity` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super().normalize(archive, logger)


m_package.__init_metainfo__()

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
