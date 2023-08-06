# gaugan.py 
![](https://img.shields.io/pypi/l/gaugan?style=plastic) ![](https://img.shields.io/pypi/pyversions/gaugan?style=plastic)

A Python package providing an interface to NVIDIA's gauGAN project (http://nvidia-research-mingyuliu.com/gaugan/), which turns crude drawings into realistic images using AI.

## Installation
```pip install gaugan```

## Usage
```processImage(image = imageBytes, [style = 1], [url = 'http://12.34.56.78:90/'])```
Returns a bytes object of the processed image in JPG format.

### Parameters
###### ```image```
A bytes object of a PNG image containing a map (the drawing).
###### ```style``` (optional)
Valid values are 'random' or an integer. Default is 'random'.
###### ```url``` (optional)
An URL of a gauGAN server. Useful for bulk processing, as by default it gets a new URL every time ```processImage()``` is called. It is necessary because the URLs are changed periodically. You can get an URL from the ```getUrl()``` function.

### Example
```
import gaugan, PIL
from PIL import Image

with open('input.png', "rb") as fh:
    image = gaugan.processImage(fh.read())
    
PIL.Image.open(image).show()
```