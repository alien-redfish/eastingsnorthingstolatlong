# mapping

This has only been tested on Linux.

A Python3 program to run a GUI to convert eastings and northings to latitude and longitude.

The first tab allows for the user to input an eastings and northing, upon convert this is turned into a latitude and longitude and a Google Map link is provided. There is also a button to Map the latitude and longitude using open street maps. This is displayed in the tab.

The second tab allows the user to find a .csv file on their local machine, choose the eastings and northing columns and then, by pressing the convert button, output a new file with the latitude and longitude columns added and converted from teh eastings and northings.

# requirements

As well as Python3 and PyQt5 the following are needed to be installed:

sudo pip3 install PyQt5

sudo pip3 install OSGridConverter

sudo pip3 install PyQtWebEngine

sudo pip3 install folium

If you get an error about sip then please run sudo pip3 install PyQt5-sip -U

# To run

cd to extracted directory and run python3 screen.py
