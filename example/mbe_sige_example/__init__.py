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

from nomad.datamodel.metainfo.eln.ikz_mbe import GrowthLog
from nomad.parsing.tabular import TableData
from nomad.datamodel.metainfo.eln import PublicationReference
from nomad.datamodel.metainfo.eln import Measurement
from nomad.datamodel.metainfo.eln import Activity
from nomad.datamodel.metainfo.eln.ikz_mbe import GrowthRecipe
import numpy as np
from nomad.metainfo import (
    Package,
    Quantity,
    SubSection,
    Datetime,
    Section,
)
from nomad.datamodel.data import (
    ArchiveSection,
)

m_package = Package(name='ELN for MBE SiGe')


class GrowthRecipe(Activity, GrowthRecipe, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
        a_eln=None,
    )


class SubstratePreparation(SubstratePreparation, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
    )


class SubstrateCutting(ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
    )
    method = Quantity(
        type=str,
        default="Substrate Cutting",
    )


class GrowthRecipe(GrowthRecipe, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
    )


class CalibrationDateSources(CalibrationDateSources, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
    )


class GrowthLog(GrowthLog, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
    )


class Tasks(AFMmeasurement, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
    )


class AFMmeasurements(TableData, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
        a_eln=None,
    )
    data_file = Quantity(
        type=str,
        description='''
        A reference to an uploaded .xlsx
        ''',
        a_tabular_parser={
            "comment": "#",
            "mode": "row",
            "target_sub_section": [
                "tasks"
            ]
        },
        a_browser={
            "adaptor": "RawFileAdaptor"
        },
        a_eln={
            "component": "FileEditQuantity"
        },
        default="#data/data_file",
    )
    tasks = SubSection(
        section_def=Tasks,
        repeats=True,
    )


class MbeExperiment(ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
        a_eln={
            "hide": [
                "end_time",
                "lab_id",
                "location"
            ]
        },
        a_template={
            "PublicationReference": {},
            "SubstratePreparation": {},
            "SubstrateCutting": {},
            "GrowthRecipe": {},
            "GrowthLog": {}
        },
    )
    PublicationReference = SubSection(
        section_def=PublicationReference,
        a_eln=None,
        repeats=True,
    )
    SubstratePreparation = SubSection(
        section_def=SubstratePreparation,
    )
    SubstrateCutting = SubSection(
        section_def=SubstrateCutting,
    )
    GrowthRecipe = SubSection(
        section_def=GrowthRecipe,
    )
    CalibrationDateSources = SubSection(
        section_def=CalibrationDateSources,
    )
    GrowthLog = SubSection(
        section_def=GrowthLog,
    )
    AFMmeasurements = SubSection(
        section_def=AFMmeasurements,
    )


class AFMmeasurement(Measurement, TableData, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
        a_eln=None,
    )
    method = Quantity(
        type=str,
        default="AFM",
    )


class Steps(ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
        a_eln={
            "properties": {
                "order": [
                    "duration",
                    "ratio",
                    "step_number"
                ]
            }
        },
    )
    step_number = Quantity(
        type=int,
        description='sequential number of the step on going',
        a_eln={
            "component": "NumberEditQuantity"
        },
    )
    ratio = Quantity(
        type=str,
        a_eln={
            "component": "StringEditQuantity"
        },
    )
    duration = Quantity(
        type=np.float64,
        description='Duration of the current step in seconds',
        a_eln={
            "component": "NumberEditQuantity",
            "defaultDisplayUnit": "second"
        },
        unit="second",
    )


class SubstratePreparation(Activity, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
        a_eln=None,
    )
    method = Quantity(
        type=str,
        default="Substrate Preparation",
    )
    steps = SubSection(
        section_def=Steps,
        repeats=True,
    )


class GrowthLog(Activity, GrowthLog, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
        a_eln=None,
    )


class CalibrationDateSources(Activity, ArchiveSection):
    '''
    Class autogenerated from yaml schema.
    '''
    m_def = Section(
        a_eln=None,
    )
    source_material = Quantity(
        type=str,
        description='FILL THE DESCRIPTION',
        a_eln={
            "component": "StringEditQuantity"
        },
    )
    calibration_date = Quantity(
        type=Datetime,
        description='FILL THE DESCRIPTION',
        a_eln={
            "component": "DateTimeEditQuantity"
        },
    )


m_package.__init_metainfo__()
