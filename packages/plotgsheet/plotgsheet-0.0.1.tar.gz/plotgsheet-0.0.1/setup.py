from setuptools import setup, find_packages
setup(

name="plotgsheet",
version="0.0.1",
description="This Package is used to Plot diff-diff Graph from Google Sheet.",
long_description = "This Package is used to Plot diff-diff Graph from Google Sheet with diff-diff Color. you can also change the Axis Labels as well as Plot Type, Graph Title. In this Package Graph Image will Automatically Saved in your woking Directory",
author="Ashok Kumar Meghvanshi",
author_email="ashokmeghvanshi04@gmail.com",
packages=['plotgsheet'],
install_requires=['pandas>=1.1.0',
                  'gspread>=3.5.0',
                  'matplotlib>=3.3.0']
)
