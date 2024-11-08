from rectpack import newPacker, PackingBin, PackingMode, GuillotineBlsfMinas, SkylineBl
from rectpack.geometry import Rectangle
from rectpack.packer import Packer


class Packer:
    _packer_max: Packer
    _packer_gui: Packer
    _packer_sky: Packer
    bin = None

    def __init__(self, bin: (int, int) = None,
                 packer_max = newPacker(mode=PackingMode.Offline, bin_algo=PackingBin.Global, rotation=False),
                 packer_gui = newPacker(mode=PackingMode.Offline, bin_algo=PackingBin.Global, rotation=False, pack_algo=GuillotineBlsfMinas),
                 packer_sky = newPacker(mode=PackingMode.Offline, bin_algo=PackingBin.Global, rotation=False, pack_algo=SkylineBl)
             ):

        self._packer_max = packer_max
        self._packer_sky = packer_sky
        self._packer_gui = packer_gui

        if bin is not None:
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

