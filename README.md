# Vesicle ground truth labelling assist using Napari

This code is designed to help with the labelling of vesicles using Napari. Once installed (see below for instructions), the code is run by simply navigating to the directory in terminal, ensuring the correct envrionment is being used and entering 'python run.py'. 

## Instructions For Use: 

Start by loading in the raw EM data that is to be labelled using dock widget 2 (see below for more details). This will create a Napari image layer entitled 'raw'. Next, tick both "pos" and "neg" in dock widget 5 and click "Clear centres". This will create two Napari label layers called "pos" and "neg". It is on these layers that the hand labelling is to be done. 

The user should then use Napari's in built labelling system to paint the centre of a vesicle, and then use the "**Compute GT**" functionality to draw the 3D spheres around these hand labelled centres. PC+ vesicles should be labelled on the "pos" layer, and PC- vesicles on the "neg" layer. The user should use different labels for each layer, and it is advised to use label 1 (red) for PC+ and label 2 (blue) for PC-. The brush size should also be restricted to not exceed the size of a vesicle -- it is advised to make it as small as possible. 

The user should use the widgets on the right hand side of the Napari screen for loading and saving data, and we summarise their function below.

### Dock widget 1
This widget is responsible for drawing the spheres around the hand labelled centres. The user can control the size of the corresponding vesicle using the "*vesicle diameter*" adjuster. The "*resolution*" adjusters should be set to the corresponding resolution of the raw EM image. Both the vesicle diameter and resolution are given in Angstroms (10nm = 1Å), though any unit can be used, as long as consistent -- the ratio between the numbers determines the number of voxels that should be labelled. 

The "*min distance*" adjuster is then used to control the minimum distance between distinct vesicle centres: vesicle centres must be at least $((2 \times \text{min distance}) +1)$ voxels away from each other to be considered separate vesicles. 

Once the above parameters are set, the user simply clicks "*Compute GT*" and the code will locate all labelled vesicle centres and draw the corresponding spheres around them. This will then be printed to screen as a new Napari labels layer with name "gt". 

### Dock widget 2 
This widget allows the user to load in the raw EM image they would like to label. This image must be stored in TIF format. The location of the file can either be typed manually into the box, or the "*Select file*" button can be used to navigate local folders. 

### Dock widget 3
This widget allows the user to load previously saved centre labels. As above, the pos and neg files are again required to be TIF files.

**WARNING**: loading new labels will replace the current label layers, so it is important to ensure your work is saved before clicking "Load".

### Dock widget 4 
This widget allows the user to choose the location they would like to save their label layers. Simply navigate to the chosen folder and click "Save centres". This will create two TIF files, pos.tif and neg.tif, which store the pos and neg labels. This saving process is compatible with the load method above. 

**WARNING**: if a pos.tif and/or neg.tif file exists in the chosen directory, saving the centres will overwrite these files. If the user wants to retain both label saves, it is suggested to use separate directories for each save. 

### Dock widget 5 
This allows you to clear the pos and neg napari label layers. This will also reset the sizes to match the size of the current raw EM image layer. If the user is changing the image they are labelling, they should save their current label layers, load in the new raw EM data and then clear both pos and neg to ensure the correct shape for the new image. Only the layers that are ticked within this widget will be cleared. 

## Installation instructions 
The code comes with a *setup.py* and *requirements.txt* file. These can be used to create a virtual conda environment to run the code from: 
- Ensure conda is intalled on the system
- Navigate to the directory in terminal / open the directory in VS Code or similiar.
- Run the command "conda create -p venv python==3.12.4 -y"
- Activate the conda environment as instructed
- Install the required packages using "pip install -r requirements.txt"
  
This should create a virtual environment (venv) that allows you to run the code. 
