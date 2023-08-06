from distutils.core import setup

long_description = """Code Example:

>>> import cv2 as cv
>>> from fake_camera import Fake_Camera  # import the class
>>> fake_cam_object = Fake_Camera()      # create an instance of the class
>>> while True:
       canvas_view = fake_cam_object.read_fake_image()   #call the new image from the fake camera
       cv.imshow("Moving Image", canvas_view)       
       time.sleep(1/10)
       if cv.waitKey(1) & 0xFF == ord('q'):                                    
           break
"""

setup(
  name = 'fake-camera',         # How you named your package folder (MyLib)
  packages = ['fake_camera'],   # Chose the same as "name"
  version = '0.9',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Camera Simulator. It creates a moving image in the screen.',   # Give a short description about your library
  long_description = long_description,
  author = 'fjolublar',                   # Type in your name
  url = 'https://github.com/fjolublar/fake_camera',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/fjolublar/fake_camera/archive/v_0.9.tar.gz',    # I explain this later on
  keywords = ['Fake Camera', 'Moving Image', 'Camera Simulator'],   # Keywords that define your package best
  install_requires=['Pillow', 'numpy'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
  ],
)
