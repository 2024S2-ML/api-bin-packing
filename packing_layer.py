from rectpack import newPacker, PackingBin, PackingMode, GuillotineBlsfMinas, SkylineBl
from rectpack.geometry import Rectangle


class Packer:
    _packer_max = newPacker(mode=PackingMode.Offline, bin_algo=PackingBin.Global, rotation=False)
    _packer_gui = newPacker(mode=PackingMode.Offline, bin_algo=PackingBin.Global, rotation=False, pack_algo=GuillotineBlsfMinas)
    _packer_sky = newPacker(mode=PackingMode.Offline, bin_algo=PackingBin.Global, rotation=False, pack_algo=SkylineBl)
    bin: (int, int)

    def __init__(self, bin: (int, int)):
        self._packer_max.add_bin(bin[0], bin[1])
        self._packer_gui.add_bin(bin[0], bin[1])
        self._packer_sky.add_bin(bin[0], bin[1])
        self.bin = bin

    def add_rect(self, rect: (int, int, str)):
        self._packer_max.add_rect(rect[0], rect[1], rect[2])
        self._packer_gui.add_rect(rect[0], rect[1], rect[2])
        self._packer_sky.add_rect(rect[0], rect[1], rect[2])

    def add_many(self, rects: [Rectangle]):
        for rect in rects:
            self.add_rect(rect)

    def pack(self):
        self._packer_max.pack()
        self._packer_gui.pack()
        self._packer_sky.pack()

    def get_packer_max(self):
        return self._packer_max

    def get_packer_gui(self):
        return self._packer_gui

    def get_packer_sky(self):
        return self._packer_sky

