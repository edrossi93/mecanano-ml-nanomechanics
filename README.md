# MecaNano Summer School 2025 – Tutorial on Machine Learning for Nanomechanics

Welcome to the hands-on repository for the **MecaNano Summer School in Kassel**.

This tutorial introduces key machine learning techniques applied to materials science and nanomechanics. Through a series of Jupyter notebooks, participants will learn how to apply classification, regression, object detection, and dimensionality reduction to problems such as nanoindentation analysis and microstructural image interpretation.

## Topics Covered

- Convolutional Neural Networks (CNNs) for handwriting recognition (MNIST)
- Deep learning on nanoindentation load–depth curves
- Object detection in microscopy images with YOLO
- Curve fitting of mechanical behavior (regression)

## Repository Structure

mecanano-ml-nanomechanics-tutorial/
├── data/                       # Sample datasets (curves, images)
├── notebooks/                 # Tutorial Jupyter notebooks
├── scripts/                   # Utility functions and model loaders
├── models/                    # Pretrained models
├── environment.yml            # Conda environment definition
├── LICENSE                    # Licensing information
└── README.md                  # This file

## Getting Started (Locally)

To set up the environment:

conda env create -f environment.yml  
conda activate ml-nano  
jupyter lab

## Try It Online (Binder)

You can also run the tutorial directly in your browser using Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/edrossi93/mecanano-ml-nanomechanics-tutorial/HEAD)

## Contact

For any questions, contact:

Edoardo Rossi  
Assistant Professor, Università degli Studi Roma Tre  
edoardo.rossi@uniroma3.it

© 2025 – MecaNano Summer School – All rights reserved.
