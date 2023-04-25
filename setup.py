from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='sitcom',
    version='1.4.1',
    packages=['sitcom'],
    url='https://github.com/pu3/SITCoM',
    license='LICENSE',
    author='Purvi Udhwani, Arpit Shrivastava, Ritesh Patel',
    author_email='purviaries@aries.res.in,arpits@aries.res.in,ritesh.sophy@gmail.com',
    description='SITCoM: SiRGraF Integrated Tool for Coronal dynaMics',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',
    install_requires=[
        'PyQt5>=5.15.0,<6.0.0,','opencv-python','numpy>=1.21.0','matplotlib>=3.5.3','scikit-image>=0.19.3','sunpy>=4.0.5','astropy>=5.1'
    ],
    package_dir={'sitcom': 'sitcom'},
    package_data={'sitcom': ['data/*','icon/*','load/*','font/lato/*','*.md']},
    include_package_data=True
)
