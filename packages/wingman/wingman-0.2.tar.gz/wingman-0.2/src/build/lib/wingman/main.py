"""
Copyright © 2016-2017, 2020 biqqles.

This file is part of Wingman.

Wingman is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Wingman is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Wingman.  If not, see <http://www.gnu.org/licenses/>.

This file contains the application's entry point - main().
"""
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import flint as fl

from . import app, config, icons, IS_WIN
from . import dialogues
from .windows.main import layout
from .dialogues import expandedmap, configurepaths
from .windows.main.navmap.navmap import Navmap
from .windows.main.merchant.merchant import Merchant
from .windows.main.roster.roster import Accounts

global mainWindow


# todo move paths dialog to own file

def onFirstRun():
    config['general']['firstrun'] = False


def main():
    """Main application entry point."""
    global mainWindow
    mainWindow = layout.MainWindow()

    firstRun = config['general'].getboolean('firstrun')

    # todo: get paths here

    if firstRun:
        onFirstRun()

    if IS_WIN:
        fl.paths.set_install_path(r"C:\Users\user\Desktop\Freelancer\Eclipse 2.1")
    else:
        fl.paths.set_install_path("/run/media/biqqles/Acer/Users/user/Desktop/Freelancer/Eclipse 2.1/")

    expmap = expandedmap.ExpandedMap()
    nav = Navmap(mainWindow, expmap)
    mer = Merchant(mainWindow, expmap, nav)
    acc = Accounts(mainWindow)

    mainWindow.dependents()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
