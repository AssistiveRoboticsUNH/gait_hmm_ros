import statistics as st
from collections import namedtuple

DataEntry = namedtuple('DataEntry', \
                       'quatx quaty quatz quatw \
        gyrox gyroy gyroz \
        accelx accely accelz \
        compx compy compz \
        label \
        sequence'
                       )


class FullEntry:
    def __init__(self):
        self.features = []
        self.labels = []
        self.seq = []

    def add(self, entry):
        feat = [entry.quatx, entry.quaty, entry.quatz, entry.quatw, entry.gyrox, entry.gyroy, entry.gyroz, entry.accelx,
                entry.accely, entry.accelz, entry.compx, entry.compy, entry.compz]
        self.features.append(feat)
        self.labels.append(entry.label)
        self.seq.append(entry.sequence)

    def len(self):
        return len(self.features)


class DataParams:
    def __init__(self, **kwargs):
        self.data = kwargs.get('data', [])
        self.label = kwargs.get('label', -1)
        self.min = 0.0
        self.max = 0.0
        self.mean = 0.0
        self.stdev = 0.0
        self.variance = 0.0

    def calc_params(self):
        self.min = min(self.data)
        self.max = max(self.data)
        self.mean = sum(self.data) / float(len(self.data))
        self.stdev = st.stdev(self.data)
        self.variance = st.variance(self.data)


class ClassData:
    def __init__(self, **kwargs):
        self.quatx = DataParams(data=kwargs.get('quatx', []), label=kwargs.get('label', -1))
        self.quaty = DataParams(data=kwargs.get('quaty', []), label=kwargs.get('label', -1))
        self.quatz = DataParams(data=kwargs.get('quatz', []), label=kwargs.get('label', -1))
        self.quatw = DataParams(data=kwargs.get('quatw', []), label=kwargs.get('label', -1))
        self.gyrox = DataParams(data=kwargs.get('gyrox', []), label=kwargs.get('label', -1))
        self.gyroy = DataParams(data=kwargs.get('gyroy', []), label=kwargs.get('label', -1))
        self.gyroz = DataParams(data=kwargs.get('gyroz', []), label=kwargs.get('label', -1))
        self.accelx = DataParams(data=kwargs.get('accelx', []), label=kwargs.get('label', -1))
        self.accely = DataParams(data=kwargs.get('accely', []), label=kwargs.get('label', -1))
        self.accelz = DataParams(data=kwargs.get('accelz', []), label=kwargs.get('label', -1))
        self.compx = DataParams(data=kwargs.get('compx', []), label=kwargs.get('label', -1))
        self.compy = DataParams(data=kwargs.get('compy', []), label=kwargs.get('label', -1))
        self.compz = DataParams(data=kwargs.get('compz', []), label=kwargs.get('label', -1))

    def add(self, entry):
        self.quatx.data.append(entry.quatx)
        self.quaty.data.append(entry.quaty)
        self.quatz.data.append(entry.quatz)
        self.quatw.data.append(entry.quatw)
        self.gyrox.data.append(entry.gyrox)
        self.gyroy.data.append(entry.gyroy)
        self.gyroz.data.append(entry.gyroz)
        self.accelx.data.append(entry.accelx)
        self.accely.data.append(entry.accely)
        self.accelz.data.append(entry.accelz)
        self.compx.data.append(entry.compx)
        self.compy.data.append(entry.compy)
        self.compz.data.append(entry.compz)

    def calc_params(self):
        self.quatx.calc_params()
        self.quaty.calc_params()
        self.quatz.calc_params()
        self.quatw.calc_params()
        self.gyrox.calc_params()
        self.gyroy.calc_params()
        self.gyroz.calc_params()
