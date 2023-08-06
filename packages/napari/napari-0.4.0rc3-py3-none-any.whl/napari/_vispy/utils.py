from ..layers import Image, Points, Shapes, Surface, Tracks, Vectors
from ..utils import config
from .vispy_image_layer import VispyImageLayer
from .vispy_points_layer import VispyPointsLayer
from .vispy_shapes_layer import VispyShapesLayer
from .vispy_surface_layer import VispySurfaceLayer
from .vispy_tracks_layer import VispyTracksLayer
from .vispy_vectors_layer import VispyVectorsLayer

layer_to_visual = {
    Image: VispyImageLayer,
    Points: VispyPointsLayer,
    Shapes: VispyShapesLayer,
    Surface: VispySurfaceLayer,
    Vectors: VispyVectorsLayer,
    Tracks: VispyTracksLayer,
}

if config.async_loading:
    from ..layers.image.experimental.octree_image import OctreeImage
    from .experimental.vispy_tiled_image_layer import VispyTiledImageLayer

    # Put OctreeImage in front so we hit that before plain Image
    original = layer_to_visual.copy()
    layer_to_visual = {OctreeImage: VispyTiledImageLayer}
    layer_to_visual.update(original)


def create_vispy_visual(layer):
    """Create vispy visual for a layer based on its layer type.

    Parameters
    ----------
    layer : napari.layers._base_layer.Layer
        Layer that needs its property widget created.

    Returns
    -------
    visual : vispy.scene.visuals.VisualNode
        Vispy visual node
    """
    for layer_type, visual in layer_to_visual.items():
        if isinstance(layer, layer_type):
            return visual(layer)

    raise TypeError(
        f'Could not find VispyLayer for layer of type {type(layer)}'
    )
