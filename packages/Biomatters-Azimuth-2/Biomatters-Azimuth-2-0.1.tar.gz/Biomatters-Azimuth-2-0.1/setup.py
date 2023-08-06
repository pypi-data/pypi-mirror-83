# from Cython.Build import cythonize
from setuptools import setup


setup(name='Biomatters-Azimuth-2',
      version='0.1',
      author='Nicolo Fusi and Jennifer Listgarten',
      author_email="fusi@microsoft.com, jennl@microsoft.com",
      description=("Machine Learning-Based Predictive Modelling of CRISPR/Cas9 guide efficiency"),
      packages=["azimuth", "azimuth.features", "azimuth.models", "azimuth.tests"],
      package_data={'azimuth': ['saved_models/*.*', 'data/*.*']},
      install_requires=['scipy<0.17', 'numpy<1.17', 'nose', 'scikit-learn>=0.17.1,<0.18', 'pandas<0.25', 'biopython<=1.76'],
      license="BSD",
      # ext_modules=cythonize("ssk_cython.pyx"),
      )
