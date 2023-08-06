"""QtAsync widget.
"""
import numpy as np
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtWidgets import QLabel, QVBoxLayout, QWidget

from ....layers.image import Image
from ....layers.image.experimental.octree_image import OctreeImage
from .qt_image_info import QtImageInfo, QtOctreeInfo
from .qt_test_image import QtTestImage


class QtRender(QWidget):
    """Dockable widget for render controls.

    Parameters
    ----------
    viewer : Viewer
        The napari viewer.
    layer : Optional[Layer]
        Show controls for this layer, or test image controls if no layer.
    """

    def __init__(self, viewer, layer=None):
        """Create our windgets.
        """
        super().__init__()
        self.viewer = viewer
        self.mini_map = None

        layout = QVBoxLayout()

        if isinstance(layer, Image):
            layout.addWidget(QtImageInfo(layer))

        if isinstance(layer, OctreeImage):
            layout.addWidget(QtOctreeInfo(layer))

            self.mini_map = QLabel()
            layout.addWidget(self.mini_map)

        layout.addStretch(1)
        layout.addWidget(QtTestImage(viewer))
        self.setLayout(layout)

        # if self.mini_map is not None:
        #    self._update_map()

    def _update_map(self):
        data = np.zeros((50, 50, 4), dtype=np.uint8)
        data[:, 25, :] = (255, 255, 255, 255)
        data[25, :, :] = (255, 255, 255, 255)

        image = QImage(
            data, data.shape[1], data.shape[0], QImage.Format_RGBA8888,
        )
        self.mini_map.setPixmap(QPixmap.fromImage(image))
