## **Deflect: Automatic Reflection Removal in Images**

## Update Log:

### April 7 + 8

Developed pseudocode level understanding of the algorithm + what should be the plan of action for the project

#### How and Why It Works:
- Frequency Domain Processing
    -  By transforming the image into the frequency domain using DCT, the algorithm can more easily separate components based on their frequency characteristics, i.e., reflections might have different frequency properties compared to the main image content.
- Convex Optimization
    - The algorithm leverages optimization techniques to differentiate between the actual image and the reflection. This is based on the assumption that reflections can be modeled differently from the main content in the frequency domain.
- Gradient and Laplacian
    - These operations help in identifying edges and textures, aiding in the separation process by highlighting areas of the image affected by reflections.
- Normalization and Scaling
    - Ensures that the output image maintains a visual consistency with the original in terms of brightness and contrast.

```python 

class FastReflectionRemoval:
    Initialize with parameters like h, lambda, mu
    
    function remove_reflection(image):
        # Step 1: Preprocessing
        Convert image to frequency domain using DCT
        
        # Step 2: Reflection Removal Core
        For each frequency component:
            Apply convex optimization to separate reflection from actual image content
            This might involve using the gradient and Laplacian operations to distinguish features
        
        # Step 3: Reconstruction
        Convert the processed frequency domain back to spatial domain using Inverse DCT
        
        # Step 4: Postprocessing
        Normalize and scale the image back to its original range
        
        return the reflection-free image

# Utility Functions (e.g., for file handling and image normalization)
class FileWriter:
    functions for saving images, handling directories, etc.

```

### Apil 6

After reading and analyzing, will be going ahead with implementing [this](https://arxiv.org/pdf/1903.03889.pdf) algorithm.


### April 4
Implemented [ICA](ICA.py) and [Averging](averaging.py) to test some algorithms for reflection removal


> This is the final project proposal for CS2364 - Computational Photography and Graphics (Spring 2024)

## Summary:

Deflect intends to be a tool for removing reflection from uploaded images.This project leverages both traditional image processing techniques, such as averaging and filtering, and advanced deep learning models to identify and subtract reflection components from images.

The final product will (hopefully) be a website where users can upload photos with unwanted reflections (e.g., through windows), and the system will process and return the cleaned images.

## Task List:

#### Core Objectives:

1. **Literature Review and Algorithm Selection**: Study existing methods for reflection removal, focusing on averaging techniques for simple scenarios and deep learning models for complex cases.
2. **Development of Image Processing Backend**: Implement a basic image processing algorithm for reflection removal using averaging and filtering techniques in Python, using libraries like OpenCV.

#### Nice-to-Haves (If Time Permits):

1. **Integration of Deep Learning Model**: Select and train a deep learning model suitable for reflection removal on more complex images. Consider pre-trained models or datasets available for fine-tuning.
2. **Web Application Development**: Develop webapp (NextJS frontend, Flask Backend) that allows users to upload images and view the results.