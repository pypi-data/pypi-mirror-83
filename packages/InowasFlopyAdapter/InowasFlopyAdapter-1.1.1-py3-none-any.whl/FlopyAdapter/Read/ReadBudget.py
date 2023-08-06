import os
from flopy.utils.mflistfile import MfListBudget


class ReadBudget:
    _filename = None

    def __init__(self, workspace):
        for file in os.listdir(workspace):
            if file.endswith(".list"):
                self._filename = os.path.join(workspace, file)
        pass

    def read_times(self):
        try:
            mf_list = MfListBudget(self._filename)
            if mf_list.get_times():
                return mf_list.get_times()
            else:
                return []
        except:
            return []

    def read_budget_by_totim(self, totim=0, incremental=False):
        try:
            mf_list = MfListBudget(self._filename)
            budget = mf_list.get_data(totim=totim, incremental=incremental)
            values = {}
            for x in budget:
                param = str(x[2].decode('UTF-8'))
                values[param] = float(str(x[1]))
            return values
        except:
            return []

    def read_budget_by_idx(self, idx=0, incremental=False):
        try:
            mf_list = MfListBudget(self._filename)
            budget = mf_list.get_data(idx=idx, incremental=incremental)
            values = {}
            for x in budget:
                param = str(x[2].decode('UTF-8'))
                values[param] = float(str(x[1]))
            return values
        except:
            return []

    def read_budget_by_kstpkper(self, kstpkper=(0, 0), incremental=False):
        try:
            mf_list = MfListBudget(self._filename)
            budget = mf_list.get_data(kstpkper=kstpkper, incremental=incremental)
            values = {}
            for x in budget:
                param = str(x[2].decode('UTF-8'))
                values[param] = float(str(x[1]))
            return values
        except:
            return []
