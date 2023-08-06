import codecs
import os
import sys

try:
    from setuptools import setup
except:
  from distutils.core import setup
import shutil


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

long_des = read("README.rst")
    
platforms = ['linux/Windows']
classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',


]

install_requires = [
    'numpy>=1.17.0',
    'matplotlib',
    'scipy>=1.4.1',
    "opencv-python",
    "tqdm",
    "prettytable",
]

# old method to install template

auth_home = os.path.join(os.path.expanduser('~'),".detmetric/template")
if not os.path.exists(auth_home):
  os.makedirs(auth_home)
shutil.copy("./template/report.md",os.path.join(auth_home,"report.md"))

if not os.path.exists(os.path.join(auth_home,'static')):
  os.makedirs(os.path.join(auth_home,'static'))

statics = [shutil.copy(os.path.join("./template/static",file),os.path.join(os.path.join(auth_home,'static'),file)) for file in os.listdir("./template/static")]

setup(name='detmetric',
      version='0.2.0',
      description='Object Detection Metric in Computer Vision',
      long_description=long_des,
      py_modules=['detcivar','detmet','BoundingBox',"BoundingBoxes","detutils","detmdreport"],
      author = "Xu Jing",  
      author_email = "274762204@qq.com" ,
      url = "https://github.com/DataXujing/detmetric" ,
      license="MIT License",
      platforms=platforms,
      classifiers=classifiers,
      install_requires=install_requires,
      keywords="object detection",
      # data_files=[(auth_home,["./template/report.md"]),(os.path.join(auth_home,'static'),statics)]
      )   
      