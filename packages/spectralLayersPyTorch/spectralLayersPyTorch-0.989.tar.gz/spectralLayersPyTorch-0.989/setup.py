"""
 Created by Narayan Schuetz at 14/11/2018
 University of Bern
 
 This file is subject to the terms and conditions defined in
 file 'LICENSE.txt', which is part of this source code package.
"""
import os

from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="spectralLayersPyTorch",
    version="0.989",
    description="PyTorch NN based trainable spectral linear layers",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Angela Botros & Narayan Schuetz",
    author_email="narayan.schuetz@artorg.unibe.ch",
    license="MIT",
    packages=["spectral"],
    zip_safe=False,
    install_requires=["torch", "numpy"],
)
