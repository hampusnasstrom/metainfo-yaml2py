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

from structlog.stdlib import (
    BoundLogger,
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

m_package = Package(name='Example Schema')


class Activity(ArchiveSection):
    '''
    A base class for any activity in relation to an entity.
    '''
    m_def = Section()
    start_time = Quantity(
        type=Datetime,
        description='The starting date and time of the activity.\n',
        a_eln={
            "component": "DateTimeEditQuantity"})
    end_time = Quantity(
        type=Datetime,
        description='The ending date and time of the activity.\n',
        a_eln={
            "component": "DateTimeEditQuantity"})

    def normalize(self, archive, logger: BoundLogger) -> None:
        '''
        The normalizer for the `Activity` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super(Activity, self).normalize(archive, logger)


class Entity(ArchiveSection):
    '''
    A base class for any entity which can be related to an activity.
    '''
    m_def = Section()

    def normalize(self, archive, logger: BoundLogger) -> None:
        '''
        The normalizer for the `Entity` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        '''
        super(Entity, self).normalize(archive, logger)


m_package.__init_metainfo__()
