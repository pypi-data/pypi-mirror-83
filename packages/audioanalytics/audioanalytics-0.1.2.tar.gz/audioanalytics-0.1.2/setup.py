import setuptools
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='audioanalytics',
      version='0.1.2',
      description='A python package to simplify the process of performing basic exploratory audio analysis and emotion detection',
      long_description='Components of the AudioAnalytics Package: 1) Extract Feature - It will return the feature values in a Dataframe. 2) Model_Load - It loads the model from backend.3) Predict - Predicts the Emotion by conducting the analysis of the provided audio.4) Summary Report - A report where probabilities are displayed of 4 Emotions.NOTE : THE AUDIO FILE INPUT FORMAT SHOULD BE .wav EXTENSION. ANY OTHER AUDIO FILE FORMAT IS NOT SUPPORTED FOR 0.1 VERSION. ',
      url='https://github.com/Paymanshus/audioanalytics',
      author='Pranav Kotak,Paymanshu Sharma,Shubh Lilani',
      license='MIT',
      include_package_data=True,
      package_data={
          'audioanalytics': ['model_85.h5', 'model_85.json']
      },
      packages=setuptools.find_packages(exclude=['tests']),
      zip_safe=False,
      install_requires=[ 
          "librosa>=0.8.0",
          "tensorflow>=2.2.0",
          "numpy>=1.19.1",
          "pandas>=1.0.4",
          "soundfile>=0.10.3.post1",
          "keras>=2.3.1",
          "importlib-resources>=3.2.0"
      ]
      )
