import napari 
import numpy as np
import skimage 
import os 
from magicgui import magicgui
import pathlib

from src.groundtruth import GroundTruth

if __name__ == '__main__':

    # Load the napari viewer
    viewer = napari.Viewer()

    # Define our magicgui widget buttons
    
    @magicgui(call_button='Compute GT')
    def get_gt(
            vesicle_diameter = 300,
            resolution_z=60,
            resolution_y=60,
            resolution_x=60, 
            min_distance: int = 1) -> napari.types.LayerDataTuple:
        """
            Computes the ground truth labelling layer, from the pos and neg layers.
            The user sets the vesicle_diameter and the resolutions (in any consistent
            measurement unit) using the provided boxes. The minimum distance between 
            two labels to be considered independent vesicles is set using the min_distance
            input. 

            The ground truth label layer (called 'gt') is then generated by clicking the 
            "Compute GT" call button. 
        """
        
        pos = viewer.layers['pos']
        neg = viewer.layers['neg']
        ground_truth = GroundTruth(
                                pos_data = pos.data, 
                                neg_data = neg.data, 
                                vesicle_diameter = vesicle_diameter,
                                resolution = (resolution_z,resolution_y,resolution_x),
                                min_distance=min_distance)
        gt = ground_truth.compute_gt()

        # Return gt data as Napari label layer.
        return (gt, {'name': 'gt'}, 'labels')
    
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
    
    @magicgui(call_button='Load')
    def load_labels(pos_data_path = pathlib.Path('path/to/pos.tif'), 
                    neg_data_path = pathlib.Path('path/to/neg.tif')):
        
        """
            A widget to allow the user to load saved pos and neg label layers. Both the 
            pos and neg files should be TIF files, and the paths can be provided either
            manually or using dictionary navigation buttons. 

            Clicking the 'Load' button will load the provided TIF files into Napari as
            the pos and/or neg label layers. If these already exist, they will be overwritten.
        """
        
        try:
            pos_data = skimage.io.imread(pos_data_path)
            # Check to see if pos label layer already exists
            if 'pos' in viewer.layers:
                pos = viewer.layers['pos']
                pos.data = pos_data 
            else:
                pos = viewer.add_labels(data=pos_data, name='pos')
        except:
            if str(pos_data_path) == 'path/to/pos.tif' or str(pos_data_path) == '':
                # If the path is unaltered or left blank, do nothing. Safetly to not accidently 
                # overwrite pos layer if only want to load neg layer.
                pass
            else:
                raise FileExistsError('Pos data location provided not suitable. Please try again.')
        try:
            neg_data = skimage.io.imread(neg_data_path)
            # Check to see if neg label layer already exists
            if 'neg' in viewer.layers:
                neg = viewer.layers['neg']
                neg.data = neg_data 
            else: 
                neg = viewer.add_labels(data=neg_data, name='neg')
        except:
            if str(neg_data_path) == 'path/to/neg.tif' or str(neg_data_path) == '':
                # If the path is unaltered or left blank, do nothing. Safetly to not accidently 
                # overwrite neg layer if only want to load pos layer.
                pass
            else:
                raise FileExistsError('Neg data location provided not suitable. Please try again.')
    
    @magicgui(save_location ={'mode': 'd'}, call_button='Save centres')
    def save_centres(save_location = pathlib.Path('save/location')):
        """
            Widget to allow user to save their pos and neg label layers as TIF files. The 
            dictionary in which they wish to save their files is provided either manually, 
            or using the navigation button. 

            Clicking the 'Save centres' button will generate two files, pos.tif and neg.tif, 
            within the provided directory. Existing files with those names will be overwritten.
        """

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
        """
            A widget to allow the user to generate a clean pos and/or neg label layer. Only
            layers that have the corresponding tick box checked will be affected. This widget 
            can be used to generate the pos and neg label layers at the start, if previously 
            saved ones are not to be loaded. 
        """
        
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

    # Add widgets to napari window
    viewer.window.add_dock_widget(get_gt)
    viewer.window.add_dock_widget(load_raw)
    viewer.window.add_dock_widget(load_labels)
    viewer.window.add_dock_widget(save_centres)
    viewer.window.add_dock_widget(clear_centres)

    napari.run()


