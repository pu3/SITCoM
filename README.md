## Sitcom Python Package
The `sitcom` Python package is a collection of utilities designed to quickly analyze some properties of coronal dynamics.SiRGraF Integrated Tool for Coronal dynaMics (SITCoM) is based on Simple Radial Gradient Filter (SiRGraF) used to filter the radial gradient in the white-light coronagraph images and bring out dynamic structures. SITCoM has been developed in Python and integrated with SunPy which enables the user to pass the white-light coronagraph data to the tool and generate radially filtered output with an option to save in various formats as required. The outputs can be viewed in Cartesian and polar coordinate systems. We have implemented the functionality of tracking the transients such as coronal mass ejections (CMEs), outflows, plasma blobs etc. using height-time plots and derive their kinematics. In addition, SITCoM also supports oscillation and waves studies such as for streamer waves. This is done by creating a distance-time plot at a user-defined location (artificial slice) and fitting a sinusoidal function to derive the properties: of time period, amplitude, and damping (if any) which could be used for seismology. We provide the provision to manually or automatically select the data points to be used for fitting.

### Installation

You can install the `sitcom` package using pip:

```
pip install sitcom
```
For Linux users, existence of the "xcb" library is essential. That can be installed with :
```
sudo apt-get install libxcb-xinerama0
```

### Usage

The `sitcom` package currently can be used by typing the following in the terminal:

```
python3 -m sitcom
```
### Contributing

If you'd like to contribute to the `sitcom` package, please email us on the provided email addresses.

### License

The `sitcom` package is released under the MIT License. See the LICENSE file for more information.
