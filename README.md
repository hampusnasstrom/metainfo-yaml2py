# metainfo-yaml2py
A program for converting NOMAD metainfo YAML schemas into Python class definitions.

## Installation
metinfo-yaml2py is currently under development and for installing and contributing you should clone the repository and install the package in editable mode (`-e`) using:
```
$ pip install -e .
```
You can then run the program with:
```
$ metainfo-yaml2py <target file> <output directory>
```

## Example
Running `metainfo-yaml2py` on the following YAML file:
```yaml
definitions:
  name: Example
  sections:
    Activity:
      description: |
        A base class for any activity in relation to an enitity.
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
        A base class for any enitity which can be related to an activity.
```

Will create the follwing python file:
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

from nomad.metainfo import Package

m_package = Package(name='Example')


class Activity:
    '''A base class for any activity in relation to an enitity.'''
    start_time = Quantity(type=Datetime)

    end_time = Quantity(type=Datetime)


class Entity:
    '''A base class for any enitity which can be related to an activity.'''


m_package.__init_metainfo__()
```