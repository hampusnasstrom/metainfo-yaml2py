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

import numpy as np
from nomad.metainfo import MEnum, Package, Quantity

m_package = Package(name='Electronic Lab Notebook example schema')


class Chemical:
    '''This is an example description for Chemical.
A description can contain **markdown** markup and TeX formulas, like $\\sum\\limits_{i=0}^{n}$.'''
    form = Quantity(type=MEnum(['crystalline solid', 'powder']), a_eln={
                    "component": "EnumEditQuantity"})

    cas_number = Quantity(type=str, a_eln={"component": "StringEditQuantity"})

    ec_number = Quantity(type=str, a_eln={"component": "StringEditQuantity"})


class Instrument:
    '''Class autogenerated from yaml schema.'''


class Process:
    '''Class autogenerated from yaml schema.'''
    instrument = Quantity(
        type=Instrument, a_eln={
            "component": "ReferenceEditQuantity"})


class pvd_evaporation:
    '''Class autogenerated from yaml schema.'''
    data_file = Quantity(
        type=str,
        description='A reference to an uploaded .csv produced by the PVD evaporation instruments\ncontrol software.\n',
        a_eln={
            "component": "FileEditQuantity"})

    time = Quantity(type=np.float64, shape=['*'], unit='s')

    chamber_pressure = Quantity(type=np.float64, shape=['*'], unit='mbar')

    substrate_temperature = Quantity(
        type=np.float64, shape=['*'], unit='kelvin')


class hotplate_annealing:
    '''Class autogenerated from yaml schema.'''
    set_temperature = Quantity(
        type=np.float64, unit='K', a_eln={
            "component": "NumberEditQuantity"})

    duration = Quantity(
        type=np.float64, unit='s', a_eln={
            "component": "NumberEditQuantity"})


class processes:
    '''Class autogenerated from yaml schema.'''


class Sample:
    '''Class autogenerated from yaml schema.'''
    name = Quantity(type=str, a_eln={"component": "StringEditQuantity"})

    tags = Quantity(type=MEnum(['internal', 'collaboration', 'project', 'other']), shape=[
                    '*'], a_eln={"component": "AutocompleteEditQuantity"})

    chemicals = Quantity(
        type=Chemical,
        shape=['*'],
        a_eln={
            "component": "ReferenceEditQuantity"})

    substrate_type = Quantity(type=MEnum(['Fused quartz glass', 'SLG', 'other']), a_eln={
                              "component": "RadioEnumEditQuantity"})

    substrate_thickness = Quantity(
        type=np.float64, unit='m', a_eln={
            "component": "NumberEditQuantity"})

    sample_is_from_collaboration = Quantity(
        type=bool, a_eln={"component": "BoolEditQuantity"})


m_package.__init_metainfo__()
