import setuptools
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='audioanalytics',
      version='0.1',
      description='A python package to simplify the process of performing basic exploratory audio analysis and emotion detection',
      url='https://github.com/Paymanshus/audioanalytics',
      author='Pranav Kotak,Paymanshu Sharma,Shubh Lilani',
      license='MIT',
      include_package_data=True,
      package_data={
          'audioanalytics': ['models/model_85.h5', 'models/model_85.json']
      },
      packages=setuptools.find_packages(exclude=['tests']),
      zip_safe=False,
      install_requires=[ 
          "librosa>=0.8.0",
          "tensorflow>=2.2.0",
          "numpy>=1.19.1",
          "pandas>=1.0.4",
          "soundfile>=0.10.3.post1",
          "keras>=2.3.1"
      ]
      )
