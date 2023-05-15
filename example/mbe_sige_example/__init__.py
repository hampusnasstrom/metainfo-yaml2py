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
from nomad.datamodel.metainfo.eln.ikz_mbe import GrowthRecipe
from nomad.parsing.tabular import TableData
from nomad.datamodel.metainfo.eln import Activity
from nomad.datamodel.metainfo.eln import Measurement
from nomad.datamodel.metainfo.eln import PublicationReference
import numpy as np
from nomad.metainfo import Datetime, Package, Quantity, Section, SubSection

m_package = Package(name='ELN for MBE SiGe')


class Substratepreparation(SubstratePreparation):
    '''Class autogenerated from yaml schema.'''
    m_def = Section()


class Substratecutting:
    '''Class autogenerated from yaml schema.'''
    m_def = Section()
    method = Quantity(type=str, default="Substrate Cutting")


class Growthrecipe(GrowthRecipe):
    '''Class autogenerated from yaml schema.'''
    m_def = Section()


class Calibrationdatesources(CalibrationDateSources):
    '''Class autogenerated from yaml schema.'''
    m_def = Section()


class Growthlog(GrowthLog):
    '''Class autogenerated from yaml schema.'''
    m_def = Section()


class Tasks(AFMmeasurement):
    '''Class autogenerated from yaml schema.'''
    m_def = Section()


class Afmmeasurements(TableData):
    '''Class autogenerated from yaml schema.'''
    m_def = Section(a_eln=None)
    data_file = Quantity(
        type=str, description='A reference to an uploaded .xlsx\n', a_tabular_parser={
            "comment": "#", "mode": "row", "target_sub_section": ["tasks"]}, a_browser={
            "adaptor": "RawFileAdaptor"}, a_eln={
                "component": "FileEditQuantity"}, default="#data/data_file")

    tasks = SubSection(section_def=Tasks)


class MbeExperiment:
    '''Class autogenerated from yaml schema.'''
    m_def = Section(
        a_eln={
            "hide": [
                "end_time",
                "lab_id",
                "location"]},
        a_template={
            "PublicationReference": {},
            "SubstratePreparation": {},
            "SubstrateCutting": {},
            "GrowthRecipe": {},
            "GrowthLog": {}})
    PublicationReference = SubSection(section_def=PublicationReference)
    SubstratePreparation = SubSection(section_def=Substratepreparation)
    SubstrateCutting = SubSection(section_def=Substratecutting)
    GrowthRecipe = SubSection(section_def=Growthrecipe)
    CalibrationDateSources = SubSection(section_def=Calibrationdatesources)
    GrowthLog = SubSection(section_def=Growthlog)
    AFMmeasurements = SubSection(section_def=Afmmeasurements)


class AFMmeasurement(Measurement, TableData):
    '''Class autogenerated from yaml schema.'''
    m_def = Section(a_eln=None)
    method = Quantity(type=str, default="AFM")


class Steps:
    '''Class autogenerated from yaml schema.'''
    m_def = Section(
        a_eln={
            "properties": {
                "order": [
                    "duration",
                    "ratio",
                    "step_number"]}})
    step_number = Quantity(
        type=int,
        description='sequential number of the step on going',
        a_eln={
            "component": "NumberEditQuantity"})

    ratio = Quantity(type=str, a_eln={"component": "StringEditQuantity"})

    duration = Quantity(
        type=np.float64,
        description='Duration of the current step in seconds',
        a_eln={
            "component": "NumberEditQuantity",
            "defaultDisplayUnit": "second"},
        unit="second")


class SubstratePreparation(Activity):
    '''Class autogenerated from yaml schema.'''
    m_def = Section(a_eln=None)
    method = Quantity(type=str, default="Substrate Preparation")

    steps = SubSection(section_def=Steps)


class GrowthRecipe(Activity, GrowthRecipe):
    '''Class autogenerated from yaml schema.'''
    m_def = Section(a_eln=None)


class GrowthLog(Activity, GrowthLog):
    '''Class autogenerated from yaml schema.'''
    m_def = Section(a_eln=None)


class CalibrationDateSources(Activity):
    '''Class autogenerated from yaml schema.'''
    m_def = Section(a_eln=None)
    source_material = Quantity(
        type=str, description='FILL THE DESCRIPTION', a_eln={
            "component": "StringEditQuantity"})

    calibration_date = Quantity(
        type=Datetime, description='FILL THE DESCRIPTION', a_eln={
            "component": "DateTimeEditQuantity"})


m_package.__init_metainfo__()
