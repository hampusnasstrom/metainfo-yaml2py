# metainfo-yaml2py
A program for converting NOMAD metainfo YAML schemas into Python class definitions.

Running on the following YAML file:
```yaml
definitions:
  name: Example
  sections:
    Activity:
      description: |
        A base class for any activity in relation to an enitity.
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

from nomad.metainfo import (
    MSection,
    Package,
    Quantity,
    SubSection,
    MEnum,
    Reference,
    Datetime,
    Section)
from nomad.datamodel.data import EntryData, ArchiveSection

m_package = Package(name='Example')


class Activity:
    '''A base class for any activity in relation to an enitity.'''
    pass


class Entity:
    '''A base class for any enitity which can be related to an activity.'''
    pass


m_package.__init_metainfo__()
```