import pathlib
import xml.etree.ElementTree
import numpy as np
from . import reg


class VersaRawMetadata(reg.Metadata):

    def __init__(self, path):
        self.path = pathlib.Path(path).resolve()
        self._init_metadata()

    def _init_metadata(self):
        tree = xml.etree.ElementTree.parse(str(self.path / 'ScanData_Position.xml'))
        positions_map = {}
        image_paths = {}
        depth = int(tree.find('ImageDimensions/Depth').text)
        th = int(tree.find('ImageDimensions/Height').text)
        tw = int(tree.find('ImageDimensions/Width').text)
        rx = float(tree.find('Resolution/X').text)
        ry = float(tree.find('Resolution/Y').text)
        assert np.allclose(rx, ry, rtol=1e-3)
        assert depth == 24
        self._num_channels = 3
        for frame in tree.findall('Frames/Frame'):
            assert len(frame.findall('Component')) == 1
            n = int(frame.find('Number').text)
            series = n - 1
            x = float(frame.find('X').text)
            y = float(frame.find('Y').text)
            filename = f"Image_{n}.raw"
            # Hack to ignore missing .raw files.
            if not (self.path / filename).exists():
                continue
            positions_map[n] = [y, x]
            image_paths[series] = filename
        self.image_paths = [path for series, path in sorted(image_paths.items())]
        positions = [pos for series, pos in sorted(positions_map.items())]
        self._positions = np.array(positions, np.float64) / rx
        self._tile_size = np.array([th, tw], np.int64)
        self._pixel_size = rx

    @property
    def _num_images(self):
        return len(self._positions)

    @property
    def num_channels(self):
        return self._num_channels

    @property
    def pixel_size(self):
        return self._pixel_size

    @property
    def pixel_dtype(self):
        return np.dtype(np.uint8)

    def tile_size(self, i):
        return self._tile_size

    def image_path(self, series):
        return self.path / self.image_paths[series]


class VersaRawReader(reg.Reader):

    def __init__(self, path, allow_missing=True):
        self.metadata = VersaRawMetadata(path)
        self.path = pathlib.Path(path)
        self.allow_missing = allow_missing

    def read(self, series, c):
        nc = self.metadata.num_channels
        shape = tuple(self.metadata.tile_size(series))
        path = self.metadata.image_path(series)
        if path.exists():
            raw = np.fromfile(str(path), dtype=self.metadata.pixel_dtype)
            img = raw[(nc - c - 1) : : nc].reshape(shape)
        else:
            if self.allow_missing:
                img = np.zeros(shape, dtype=self.metadata.pixel_dtype)
            else:
                raise FileNotFoundError(f"No such file: '{path}'")
        return img
