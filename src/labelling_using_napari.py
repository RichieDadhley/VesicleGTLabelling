import napari 
import numpy as np
import skimage 
import os 
from magicgui import magicgui
import pathlib

from src.groundtruth import GroundTruth

if __name__ == '__main__':

    viewer = napari.Viewer()
    
    @magicgui(call_button='Compute GT')
    def get_gt(
            vesicle_diameter = 300,
            resolution_z=60,
            resolution_y=60,
            resolution_x=60, 
            min_distance: int = 1) -> napari.types.LayerDataTuple:
        
        pos = viewer.layers['pos']
        neg = viewer.layers['neg']
        ground_truth = GroundTruth(
                                pos_data = pos.data, 
                                neg_data = neg.data, 
                                vesicle_diameter = vesicle_diameter,
                                resolution = (resolution_z,resolution_y,resolution_x),
                                min_distance=min_distance)
        gt = ground_truth.compute_gt()
        return (gt, {'name': 'gt'}, 'labels')
    
    @magicgui(call_button='Load')
    def load_raw(raw_data_path = pathlib.Path('path/to/raw.tif')) -> napari.types.LayerDataTuple:
        raw_data = np.array([skimage.io.imread(raw_data_path)]) 
        # Check for stacks of images
        if (raw_data.shape[0] == 1):
            raw_data = raw_data[0,:]

        if 'raw' in viewer.layers:
            return (raw_data, {'name': 'raw'}, 'image')
        
        else: 
            raw = viewer.add_image(data = raw_data, name='raw')
    
    @magicgui(call_button='Load')
    def load_labels(pos_data_path = pathlib.Path('path/to/pos.tif'), 
                    neg_data_path = pathlib.Path('path/to/neg.tif')):
        
        try:
            pos_data = skimage.io.imread(pos_data_path)
            if 'pos' in viewer.layers:
                pos = viewer.layers['pos']
                pos.data = pos_data 
            else:
                pos = viewer.add_labels(data=pos_data, name='pos')
        except:
            if str(pos_data_path) == 'path/to/pos.tif' or str(pos_data_path) == '':
                pass
            else:
                raise FileExistsError('Pos data location provided not suitable. Please try again.')
        try:
            neg_data = skimage.io.imread(neg_data_path)
            if 'neg' in viewer.layers:
                neg = viewer.layers['neg']
                neg.data = neg_data 
            else: 
                neg = viewer.add_labels(data=neg_data, name='neg')
        except:
            if str(neg_data_path) == 'path/to/neg.tif' or str(neg_data_path) == '':
                pass
            else:
                raise FileExistsError('Neg data location provided not suitable. Please try again.')
    
    @magicgui(call_button='Save centres')
    def save_centres(save_location = pathlib.Path('save/location')):

        pos = viewer.layers['pos']
        neg = viewer.layers['neg']

        if not os.path.exists(save_location):
            os.makedirs(save_location)

        pos_data = pos.data
        neg_data = neg.data.astype(np.uint16)

        skimage.io.imsave(f'{save_location}/pos.tif', pos_data)
        skimage.io.imsave(f'{save_location}/neg.tif', neg_data)
            
    @magicgui(call_button='Clear centres')
    def clear_centres(Pos: bool = False, 
                      Neg: bool = False):
        
        raw_layer = viewer.layers['raw']
        if Pos == True:
            if 'pos' in viewer.layers:
                pos = viewer.layers['pos']
                pos.data = np.zeros(raw_layer.data.shape, dtype=np.int64)
            else:
                pos = viewer.add_labels(data = np.zeros(raw_layer.data.shape, dtype=np.int64), name='pos')

        if Neg == True:
            if 'neg' in viewer.layers:
                neg = viewer.layers['neg']
                neg.data = np.zeros(raw_layer.data.shape, dtype=np.int64)
            else: 
                neg = viewer.add_labels(data = np.zeros(raw_layer.data.shape, dtype=np.int64), name='neg')

            
    viewer.window.add_dock_widget(get_gt)
    viewer.window.add_dock_widget(load_raw)
    viewer.window.add_dock_widget(load_labels)
    viewer.window.add_dock_widget(save_centres)
    viewer.window.add_dock_widget(clear_centres)

    napari.run()


