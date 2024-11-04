import numpy as np
import skimage 
import scipy.ndimage

class GroundTruth():
     
    def __init__(self,
                 pos_data, 
                 neg_data,
                 vesicle_diameter: int,
                 resolution: tuple, 
                 offset = (0,0,0), 
                 background_label = 0, 
                 num_classes = 3, 
                 axes =['z','y','x'], 
                 min_distance = 1):

        self.pos_data = pos_data
        self.neg_data = neg_data
        self.voxel_size = resolution
        self.offset = offset
        self.background_label = background_label
        self.num_classes = num_classes
        self.axes = axes 
        self.balls = {}
        self.min_distance = min_distance

        diameter = np.array([vesicle_diameter, vesicle_diameter, vesicle_diameter])
        self.kernel_shape = np.ceil(diameter/self.voxel_size)
        
    def find_centres(self, data):

        kernel = skimage.morphology.ball(100).astype(np.float64) 
        kernel = skimage.transform.resize(kernel, self.kernel_shape).astype(np.float64)

        # Convolve the prediction with a spherical kernel
        data_convolved = scipy.ndimage.convolve(data*5, kernel)

        # Find the indices for the peak local maxima
        centre_indices = skimage.feature.peak_local_max(
                                                    data_convolved, 
                                                    min_distance = self.min_distance, 
                                                    labels= skimage.measure.label(data)
                                                    )

        

        return centre_indices
    
    def draw_ball(self, array, location, label=1):

        diameter = self.kernel_shape
        diameter = tuple(int(x) for x in diameter)
        # Check to see if we already have a ball of this size
        if diameter not in self.balls:
            ball = skimage.morphology.ball(100, dtype=bool)
            ball = skimage.transform.resize(
                                            ball, 
                                            diameter, 
                                            order=0, 
                                            anti_aliasing=False).astype(bool) 
            self.balls[diameter] = ball
        
        else: 
            ball = self.balls[diameter]

        
        # Check for ball going past the boundary and trim ball accordingly. 
        slices_list = []
        ball_slices_list = []
        for loc, d, boundary, ball_shape in zip(location, diameter, array.shape, ball.shape):
            ball_start = (loc - d//2)
            ball_end = (loc - d//2 +d) 
            ball_trim_start = 0 
            ball_trim_end = ball_shape 

            if (ball_start < 0):
                ball_trim_start = -1*ball_start
                ball_start = 0
            if (ball_end > boundary):
                ball_trim_end = boundary - ball_end 
                ball_end = boundary
            
            slices_list.append(slice(ball_start, ball_end))
            ball_slices_list.append(slice(ball_trim_start, ball_trim_end))
        
        slices = tuple(slices_list)
        ball_slices = tuple(ball_slices_list)

        # Go to ball location in array and set values to label
        view = array[slices]
        sliced_ball = ball[ball_slices]
        view[sliced_ball] = label

    def compute_gt(self):

        hand_labelled_data = self.pos_data + self.neg_data

        self.ground_truth = np.zeros(hand_labelled_data.shape, dtype=np.int64)

        vesicle_centres = self.find_centres(data = hand_labelled_data)
        print(vesicle_centres)
        for i in range (len(vesicle_centres)):
            loc = tuple(vesicle_centres[i])
            # print(hand_labelled_data[loc])
            self.draw_ball(array=self.ground_truth, location=loc, label=hand_labelled_data[loc])

        return self.ground_truth