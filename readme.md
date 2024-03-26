## **Deflect: Automatic Reflection Removal in Images**

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
