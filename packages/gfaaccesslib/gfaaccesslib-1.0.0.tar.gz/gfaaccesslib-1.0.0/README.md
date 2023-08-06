# Python gfa access library - pygfalib
Python implementation of the interface library to the GFA


## Adding new commands

## Declare command

On gfaaccesslib.commands add a new command class which inherits from CommandBase

On __init__ which arguments are used and added to the JSON object

## Add interface

On gfaaccesslib.gfaaccess add a new method which uses the command you just added on gfaaccesslib.commands

## Server endpoint

Check documentation on gfaserver on how to add new commands 


# guiqwt plotting

To install guiqwt:

  sudo -H pip3 install guidata
  sudo -H pip3 install guiqwt
  sudo -H pip3 install h5py

On older versions of Ubuntu I had to manually uninstall python3-pyqt5 and python3-sip due to a systemError and download  latests versions of PyQt5 and sip from riverbank, compile and install it.

To do so it needs:
  sudo apt-get install libqt5svg5 libqt5svg5-dev qt5-qmake qt5-default
