import numpy as np
from   PIL   import Image

class Fake_Camera():                                      
   
    def __init__(self, image = 'lena_color.jpg', black_white = 1, size = (1000, 1000), add_noise = 1):  
        
        self.image            = image
        self.black_white      = black_white
        self.canvas_size      = size
        self.add_noise        = add_noise
        self.flip_sign        = 0
        self.pixel_move       = 5
        self.main_config()

    def main_config(self):
        
        self.canvas           = np.random.randint(1, 255, size = self.canvas_size, dtype='uint8')  
        try:
            self.frame = np.asarray ( Image.open("lena_color.jpg").convert('L') )

        except Exception:
            self.frame        = np.random.randint(1, 255, size = self.canvas_size, dtype='uint8')  
        
        if  self.black_white == 1:
            self.config_black_white()
  
        if self.add_noise:       
            self.config_noise()
             
    def config_black_white(self):
        
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
        self.noise_start   = np.zeros( ( self.canvas_view.shape[0],self.canvas_view.shape[1] ), np.uint8 )
        self.mean          = 0
        self.var           = 0.1
        self.sigma         = self.var **0.5  
        
    def add_noise_to_image(self, image):
        row, col    = image.shape
        self.gauss  = np.random.normal( self.mean, self.sigma, (row, col) ) * 50
        self.gauss  = self.gauss.reshape( row, col )
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
                return self.canvas_view 
            
            elif self.flip_sign % 2 == 1:
                return np.fliplr(self.canvas_view)
            
        except Exception:
            print("Error Somewhere")
#---------------------------------------------------------------------------------------------------------------------------#   