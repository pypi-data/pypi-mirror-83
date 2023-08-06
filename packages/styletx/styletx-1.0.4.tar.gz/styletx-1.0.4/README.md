# StyleTx
**StyleTx** is a python project that applies effects of an image to another image using machine learning.

## Installation
You can install the StyleTx package using the command given below

```
pip3 install styletx
```

## Requirements
Requires Python >=3.8

Required packages are specified in [requirements.txt](https://github.com/dinesh-GDK/StyleTx/blob/master/requirements.txt) file, which you can install using

```
pip3 install -r requirements.txt
```

`torch` and `torchvision` versions in `requirements.txt` are CPU only, if you want to use the GPU versions that suit your hardware requirements visit this [link](https://pytorch.org/).


## Implementation

```python
# import necessary packages
from styletx import StyleTransfer
from PIL import Image
import matlibplot.pyplot as plt

# import the images
content_image = Image.open('path/filename')
style_image = Image.open('path/filename')

# implement StyleTransfer
output_image = StyleTransfer(content_image, style_image, alpha=1, beta=10, epochs=500)

# display the results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
ax1.imshow(content_image)
ax2.imshow(output_image)
plt.show()
```
The above code will apply the effects of the `style_image` to `content_image`.

# Inputs
`content_image` - a PIL object\
`style_image` - a PIL object\
`alpha` - a positive integer\
`beta` - a positive integer\
`epochs` - a positive integer

By default `alpha` = 1, `beta` = 10 and `epochs` = 500.
You can play around these values to get desired output image.

## Example
![](https://raw.githubusercontent.com/dinesh-GDK/StyleTx/master/images/Result.png)

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/dinesh-GDK/StyleTx/blob/master/LICENSE.txt)

## Resources
- The complete theory behind the **StyleTransfer** can be found in this [link](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf).

- https://github.com/udacity/deep-learning-v2-pytorch/tree/master/style-transfer
