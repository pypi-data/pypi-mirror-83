"""
This module is an intermediate layer between flopy version 3.2
and the inowas-modflow-configuration format.

Author: Ralf Junghanns
EMail: ralf.junghanns@gmail.com
"""

from FlopyAdapter.MfPackages.BasAdapter import BasAdapter
from FlopyAdapter.MfPackages.ChdAdapter import ChdAdapter
from FlopyAdapter.MfPackages.DisAdapter import DisAdapter
from FlopyAdapter.MfPackages.DrnAdapter import DrnAdapter
from FlopyAdapter.MfPackages.FhbAdapter import FhbAdapter
from FlopyAdapter.MfPackages.GhbAdapter import GhbAdapter
from FlopyAdapter.MfPackages.HobAdapter import HobAdapter
from FlopyAdapter.Statistics.HobStatistics import HobStatistics
from FlopyAdapter.MfPackages.LpfAdapter import LpfAdapter
from FlopyAdapter.MfPackages.MfAdapter import MfAdapter
from FlopyAdapter.MfPackages.NwtAdapter import NwtAdapter
from FlopyAdapter.MfPackages.OcAdapter import OcAdapter
from FlopyAdapter.MfPackages.PcgAdapter import PcgAdapter
from FlopyAdapter.MfPackages.RchAdapter import RchAdapter
from FlopyAdapter.MfPackages.EvtAdapter import EvtAdapter
from FlopyAdapter.MfPackages.RivAdapter import RivAdapter
from FlopyAdapter.Read.ReadBudget import ReadBudget
from FlopyAdapter.Read.ReadConcentration import ReadConcentration
from FlopyAdapter.Read.ReadDrawdown import ReadDrawdown
from FlopyAdapter.Read.ReadHead import ReadHead
from FlopyAdapter.MfPackages.UpwAdapter import UpwAdapter
from FlopyAdapter.MfPackages.WelAdapter import WelAdapter
from FlopyAdapter.MfPackages.LmtAdapter import LmtAdapter

from FlopyAdapter.MpPackages.MpAdapter import MpAdapter
from FlopyAdapter.MpPackages.BasAdapter import BasAdapter
from FlopyAdapter.MpPackages.SimAdapter import SimAdapter

from FlopyAdapter.MtPackages.MtAdapter import MtAdapter
from FlopyAdapter.MtPackages.AdvAdapter import AdvAdapter
from FlopyAdapter.MtPackages.BtnAdapter import BtnAdapter
from FlopyAdapter.MtPackages.DspAdapter import DspAdapter
from FlopyAdapter.MtPackages.GcgAdapter import GcgAdapter
from FlopyAdapter.MtPackages.LktAdapter import LktAdapter
from FlopyAdapter.MtPackages.PhcAdapter import PhcAdapter
from FlopyAdapter.MtPackages.RctAdapter import RctAdapter
from FlopyAdapter.MtPackages.SftAdapter import SftAdapter
from FlopyAdapter.MtPackages.SsmAdapter import SsmAdapter
from FlopyAdapter.MtPackages.TobAdapter import TobAdapter
from FlopyAdapter.MtPackages.UztAdapter import UztAdapter
from FlopyAdapter.SwtPackages.SwtAdapter import SwtAdapter
from FlopyAdapter.SwtPackages.VdfAdapter import VdfAdapter
from FlopyAdapter.SwtPackages.VscAdapter import VscAdapter


class InowasFlopyCalculationAdapter:
    """The Flopy Class"""

    _version = None
    _uuid = None

    _model = None

    _report = ''
    _success = False

    mf_package_order = [
        'mf', 'dis', 'bas', 'bas6',
        'chd', 'evt', 'drn', 'fhb', 'ghb', 'hob', 'rch', 'riv', 'wel',
        'lpf', 'upw', 'pcg', 'nwt', 'oc', 'lmt', 'lmt6'
    ]

    mt_package_order = [
        'mt', 'btn', 'adv', 'dsp', 'gcg', 'ssm', 'lkt',
        'phc', 'rct', 'sft', 'tob', 'uzt'
    ]

    swt_package_order = [
        # Modflow
        'swt', 'dis', 'bas', 'bas6', 'riv', 'wel', 'rch', 'chd', 'ghb', 'hob',
        'lpf', 'upw', 'pcg', 'nwt', 'oc', 'lmt', 'lmt6',
        # Mt3D
        'btn', 'adv', 'dsp', 'gcg', 'ssm', 'lkt', 'phc', 'rct', 'sft', 'tob', 'uzt',
        # Seawat                                         
        'vdf', 'vsc'
    ]

    mp_package_order = [
        'mp', 'bas', 'sim'
    ]

    def __init__(self, version, data, uuid):
        self._mf_data = data.get('mf')
        self._mp_data = data.get('mp')
        self._mt_data = data.get('mt')
        self._swt_data = data.get('swt')
        self._version = version
        self._uuid = uuid

        # Model calculation if Seawat is enabled
        if self._swt_data is not None:
            package_data = {
                **self._mf_data,
                **self._mt_data,
                **self._swt_data,
                'packages': self._mf_data['packages'] + self._mt_data['packages'] + self._swt_data['packages']
            }

            package_content = self.read_packages(package_data)
            self.create_model(self.swt_package_order, package_content)
            self.write_input_model(self._model)
            self._success, report = self.run_model(self._model, model_type='swt')
            self._report += report

            if 'hob' in self._mf_data['packages']:
                print('Calculate hob-statistics and write to file %s.hob.stat' % uuid)
                self.run_hob_statistics(self._model)

            return

        # Normal Modflow calculation
        if self._mf_data is not None:
            package_content = self.read_packages(self._mf_data)
            self.create_model(self.mf_package_order, package_content)
            self.write_input_model(self._model)
            self.success, report = self.run_model(self._model, model_type='mf')
            self._report += report

            if 'hob' in self._mf_data['packages']:
                print('Calculate hob-statistics and write to file %s.hob.stat' % uuid)
                self.run_hob_statistics(self._model)

            # Mt3d calculation
            if self._mt_data is not None:
                package_content = self.read_packages(self._mt_data)
                self.create_model(self.mt_package_order, package_content)
                self.write_input_model(self._model)
                self._success, report = self.run_model(self._model, model_type='mt')
                self._report += report

            # ModPath6 calculation
            if self._mp_data is not None:
                package_content = self.read_packages(self._mp_data)
                self.create_model(self.mp_package_order, package_content)
                self.write_input_model(self._model)
                self._success, report = self.run_model(self._model, model_type='mp')
                self._report += report

    @staticmethod
    def read_packages(data):
        package_content = {}
        for package in data['packages']:
            print('Read Flopy package data: %s' % package)
            package_content[package.lower()] = data[package]
        return package_content

    def create_model(self, package_order, package_content):
        for package in package_order:
            if package in package_content:
                print('Create Flopy Package: %s' % package)
                self.create_package(package, package_content[package])

    @staticmethod
    def write_input_model(model):
        print('Write input files.')
        model.write_input()

    @staticmethod
    def run_model(model, model_type):
        normal_msg = 'normal termination'
        if model_type == 'mt':
            normal_msg = 'Program completed'

        print('Run model.')
        print('Model nam-file: %s.' % model.namefile)
        print('Model executable: %s.' % model.exe_name)
        success, report = model.run_model(report=True, silent=True, normal_msg=normal_msg)
        return success, ' \n'.join(str(e) for e in report)

    @staticmethod
    def run_hob_statistics(model):
        model_ws = model.model_ws
        name = model.name

        print('Calculate hob-statistics for model %s' % name)
        HobStatistics(model_ws, name).write_to_file()

    def check_model(self):
        if self._model is not None:
            self._model.check()
        if self._model is not None:
            self._model.check()

    def create_package(self, name, content):

        # Modflow packages
        if name == 'mf':
            self._model = MfAdapter(content).get_package()
        if name == 'dis':
            DisAdapter(content).get_package(self._model)
        if name == 'drn':
            DrnAdapter(content).get_package(self._model)
        if name == 'bas' or name == 'bas6':
            BasAdapter(content).get_package(self._model)
        if name == 'lpf':
            LpfAdapter(content).get_package(self._model)
        if name == 'upw':
            UpwAdapter(content).get_package(self._model)
        if name == 'pcg':
            PcgAdapter(content).get_package(self._model)
        if name == 'nwt':
            NwtAdapter(content).get_package(self._model)
        if name == 'oc':
            OcAdapter(content).get_package(self._model)
        if name == 'riv':
            RivAdapter(content).get_package(self._model)
        if name == 'wel':
            WelAdapter(content).get_package(self._model)
        if name == 'rch':
            RchAdapter(content).get_package(self._model)
        if name == 'evt':
            EvtAdapter(content).get_package(self._model)
        if name == 'chd':
            ChdAdapter(content).get_package(self._model)
        if name == 'fhb':
            FhbAdapter(content).get_package(self._model)
        if name == 'ghb':
            GhbAdapter(content).get_package(self._model)
        if name == 'hob':
            HobAdapter(content).get_package(self._model)
        if name == 'lmt':
            LmtAdapter(content).get_package(self._model)

        # MT3D packages
        if name == 'mt':
            self._model = MtAdapter(content).get_package(self._model)
        if name == 'adv':
            AdvAdapter(content).get_package(self._model)
        if name == 'btn':
            BtnAdapter(content).get_package(self._model)
        if name == 'dsp':
            DspAdapter(content).get_package(self._model)
        if name == 'gcg':
            GcgAdapter(content).get_package(self._model)
        if name == 'lkt':
            LktAdapter(content).get_package(self._model)
        if name == 'phc':
            PhcAdapter(content).get_package(self._model)
        if name == 'rct':
            RctAdapter(content).get_package(self._model)
        if name == 'sft':
            SftAdapter(content).get_package(self._model)
        if name == 'ssm':
            SsmAdapter(content).get_package(self._model)
        if name == 'tob':
            TobAdapter(content).get_package(self._model)
        if name == 'uzt':
            UztAdapter(content).get_package(self._model)

        # ModPath packages
        if name == 'mp':
            self._model = MpAdapter(content).get_package()
        if name == 'mpbas':
            self._model = BasAdapter(content).get_package(self._model)
        if name == 'mpsim':
            self._model = SimAdapter(content).get_package(self._model)

        # Seawat packages
        if name == 'swt':
            self._model = SwtAdapter(content).get_package()
        if name == 'vdf':
            VdfAdapter(content).get_package(self._model)
        if name == 'vsc':
            VscAdapter(content).get_package(self._model)

    def response(self):
        key = 'mf'
        if 'MF' in self._mf_data:
            key = 'MF'

        budgets = ReadBudget(self._mf_data[key]['model_ws'])
        concentrations = ReadConcentration(self._mf_data[key]['model_ws'])
        drawdowns = ReadDrawdown(self._mf_data[key]['model_ws'])
        heads = ReadHead(self._mf_data[key]['model_ws'])

        return {
            'budgets': budgets.read_times(),
            'concentrations': concentrations.read_times(),
            'drawdowns': drawdowns.read_times(),
            'heads': heads.read_times(),
            'number_of_layers': heads.read_number_of_layers()
        }

    def success(self):
        return self._success

    def response_message(self):
        return self._report
