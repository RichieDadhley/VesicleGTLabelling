import napari 
import numpy as np
import skimage 
import pathlib
from magicgui import magicgui
import os

# Load the napari viewer
viewer = napari.Viewer()

@magicgui(call_button='Load')
def load_raw(raw_data_path = pathlib.Path('path/to/raw.tif')) -> napari.types.LayerDataTuple:
    """
        Widget to allow the user to load in the raw data that is to be labelled. The data
        must be a TIF file, and the path to this file provided. This can either be entered
        manually, or using the dictionary navigation button.

        Clicking the 'Load' call button will load the provided TIF file into a Napari image 
        layer with name 'raw'.
    """

    raw_data = np.array([skimage.io.imread(raw_data_path)]) 
    # Check for stacks of images
    if (raw_data.shape[0] == 1):
        raw_data = raw_data[0,:]

    if 'raw' in viewer.layers:
        return (raw_data, {'name': 'raw'}, 'image')
    
    else: 
        raw = viewer.add_image(data = raw_data, name='raw')

@magicgui(save_location ={'mode': 'd'}, call_button='Run')
def preview_crop(
                shape_layer: 'napari.layers.Shapes',
                start_slice: int, 
                end_slice: int,
                name: str = 'cropped_image_name',
                save_location = pathlib.Path('save/location'),
                save: bool = False,
                preview: bool = False
                ):
    
    top_left = tuple(shape_layer.data[0][0])
    bottom_right = tuple(shape_layer.data[0][2])

    raw_layer = viewer.layers['raw']

    cropped_data = raw_layer.data[start_slice: end_slice, 
                                   int(top_left[1]): int(bottom_right[1]), 
                                   int(top_left[2]): int(bottom_right[2])]
    
    if preview == True:
        viewer.add_image(data=cropped_data, 
                         name=name, 
                         translate=(start_slice, top_left[1], top_left[2]),
                         colormap='green')

    if save == True:
        if not os.path.exists(f'{save_location}/{name}'):
            os.makedirs(f'{save_location}/{name}')

        skimage.io.imsave(f'{save_location}/{name}/{name}.tif', cropped_data)
        file = open(f'{save_location}/{name}/offset.txt', 'w')
        file.write(f'Image offset (to top-left): (z,y,x) = ({start_slice}, {top_left[1]}, {top_left[2]})')
        file.close()


viewer.window.add_dock_widget(load_raw)
viewer.window.add_dock_widget(preview_crop)

napari.run()