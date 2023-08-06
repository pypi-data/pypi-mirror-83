import numpy as np
from   PIL   import Image
import copy 

class Fake_Camera():                                      
   
    def __init__(self, image = 'lena_color.jpg', colour = "c", background_colour = "b", 
                       size = (1000, 1000), add_noise = 0, pixel_move = 5):  
        """
        Library for creating a moving image on the screen.
        
        args:
            image             = ".jpg"        Image to be displayed
            colour            = "c" or "g"    for colour or grayscale
            backgroung_colour = "w", "b", "r" for white, black, random
            size              = (1000,1000)   Size of the Canvas
            add_noise         = "Yes", "No"   Add noise to the images
            pixel_move        = int()         How much pixels the image moves
        """
        
        self.image             = image
        self.colour            = colour
        self.background_colour = background_colour
        self.canvas_size       = size
        self.add_noise         = add_noise
        self.pixel_move        = pixel_move
        self.flip_sign         = 0
        self.image_config()
        self.background_config()
        self.canvas_config()
        if self.add_noise:       
            self.config_noise()

    def image_config(self):
        if  self.colour == "g":
            try:
                self.frame = np.asarray ( Image.open(self.image).convert('L') )
            except Exception:
                    print("Image does not exist in the current directory!")
                    return
            
        elif  self.colour == "c":
            try:
                self.frame = np.asarray ( Image.open(self.image) )
                self.frame = self.frame[...,[2,1,0]]
            except Exception:
                    print("Image does not exist in the current directory!")
                    return

    def background_config(self):
               
        if  self.colour == "g":
            if  self.background_colour == "r":
                self.canvas           = np.random.randint(1, 255, size = self.canvas_size, dtype='uint8') 
            if  self.background_colour == "w":
                self.canvas           = np.ones(self.canvas_size, dtype='uint8') * 255
            if  self.background_colour == "b":
                self.canvas           = np.zeros(self.canvas_size, dtype='uint8') 
        
        if  self.colour == "c":
            if  self.background_colour == "r":
                self.canvas           = np.random.randint(1, 255, size = self.canvas_size + (3,), dtype='uint8') 
            if  self.background_colour == "w":
                self.canvas           = np.ones(self.canvas_size + (3,), dtype='uint8') * 255
            if  self.background_colour == "b":
                self.canvas           = np.zeros(self.canvas_size + (3,), dtype='uint8')             
                        
    def canvas_config(self):
        
        self.upper_left_point_x = int( self.canvas.shape[0] / 4 )
        self.upper_left_point_y = int( self.canvas.shape[0] / 4 )
        
        self.canvas[ self.upper_left_point_x : self.upper_left_point_x + int( self.frame.shape[0] ),
                     self.upper_left_point_y : self.upper_left_point_y + int( self.frame.shape[1] ) ] =  self.frame
        
        self.limit_x_start =   int( self.upper_left_point_x / 2 ) 
        self.limit_x_end   = - int( self.upper_left_point_x / 2 )
        self.limit_y_start =   int( self.upper_left_point_x / 2 ) 
        self.limit_y_end   = - int( self.upper_left_point_x / 2 )
        
        self.canvas_view   = self.canvas[ self.limit_x_start : self.limit_x_end, self.limit_y_start : self.limit_y_end ]        
        self.old_start_x   = self.upper_left_point_x
        self.old_start_y   = self.upper_left_point_y     
        
    def config_noise(self):
        self.mean          = 0
        self.var           = 0.1
        self.sigma         = self.var **0.5  
        
    def add_noise_to_image(self, image ):
        
        if len(image.shape) == 2:
            row, col    = image.shape
            self.gauss  = np.random.normal( self.mean, self.sigma, (row, col) ) * 50
            self.gauss  = self.gauss.reshape( row, col )
        
        elif len(image.shape) == 3:
            row, col, ch    = image.shape
            self.gauss  = np.random.normal( self.mean, self.sigma, (row, col, ch) ) * 50
            self.gauss  = self.gauss.reshape( row, col, ch )
        
        self.gauss  = self.gauss.astype("uint8")
        noisy_image = image + self.gauss
        return noisy_image
        
    def read_fake_image(self):
    
        self.stepsize_x = np.random.randint(-self.pixel_move, self.pixel_move +1)
        self.stepsize_y = np.random.randint(-self.pixel_move, self.pixel_move +1)
     
        try:    
            new_start_x = min ( max (self.limit_x_start, self.old_start_x + self.stepsize_x), self.limit_x_start * 4 )
            new_start_y = min ( max (self.limit_y_start, self.old_start_y + self.stepsize_y), self.limit_y_start * 2 )
          
            self.old_start_x, self.old_start_y = new_start_x, new_start_y
            
            end_x   = new_start_x + int(self.frame.shape[0])
            end_y   = new_start_y + int(self.frame.shape[1])
           
            self.canvas_view =  self.canvas[ new_start_x : end_x, new_start_y : end_y ]
  
            if self.add_noise == 1:
                self.canvas_view = self.add_noise_to_image(self.canvas_view)

            # if np.random.uniform(low=0.0, high=1.0) < 0.05:
            #     start_y = int(noisy.shape[0]/2)
            #     noisy[:, start_y: ] = np.zeros( (noisy[:, start_y: ].shape[0], noisy[:, start_y: ].shape[1]), dtype='uint8' )
            
            if np.random.uniform( low =0.0, high= 1.0) < 0.01:
                self.flip_sign = self.flip_sign + 1
            
            if self.flip_sign % 2 == 0:
                return copy.deepcopy(self.canvas_view)
            
            elif self.flip_sign % 2 == 1:
                return  copy.deepcopy(np.fliplr(self.canvas_view))
            
        except Exception:
            print("Error Somewhere")
#-----------------------------------------------------------------------------#