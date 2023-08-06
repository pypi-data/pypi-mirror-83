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

This file initialises the application and contains key utility
classes.
"""
import configparser
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets  # WebEngine must be imported here before QApp init

from . import resources


__version__ = '1.0.1 Private'


class Configuration(configparser.ConfigParser):
    """A class providing persistent configuration ... All data is stored on memory until program shutdown, when it is written to
    backing storage automatically."""
    path = os.path.join('cache', 'wingman.cfg')

    def __init__(self):
        configparser.ConfigParser.__init__(self, allow_no_value=True)
        self.optionxform = str  # override default behaviour of converting all keys to lowercase

        try:
            self.read_file(open(self.path))  # .read will not raise an error if the file doesn't exist
            assert {'paths', 'urls'}.issubset(self.sections())
        except FileNotFoundError or AssertionError:
            self.createDefault()
        self.createShortcuts()

    def save(self, *path):
        if not path:
            path = self.path

        with open(path, 'w') as fh:
            self.write(fh)

    def export(self, path):
        self.save(path)

    def createDefault(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)  # create cache directory if it doesn't already exist
        # load default file from resources
        file = QtCore.QFile(':/config/default')
        file.open(QtCore.QIODevice.ReadOnly | QtCore.QFile.Text)
        default = QtCore.QTextStream(file).readAll()
        self.read_string(default)
        self.save()

    def getlist(self, section, option):
        """Return a list stored as a newline delimited value.
        Analogous to the superclass methods getboolean, getint, etc."""
        value = self.get(section, option)
        return list(filter(None, (x.strip() for x in value.splitlines())))

    def createShortcuts(self):
        # todo move this to init and then reinit instead of calling this when nec
        # define some useful path constants
        paths = self['paths']
        self.INSTALL = paths['winstall'] if IS_WIN else paths['linstall']
        self.MYGAMES = paths['wmygames'] if IS_WIN else paths['lmygames']
        self.DSACE = self.fpath('Freelancer', 'DSAce.log', root=self.MYGAMES)
        self.LAUNCHERACCS = self.fpath('Discovery', 'launcheraccounts.xml', root=self.MYGAMES)
        self.NAVMAP = self['urls']['navmap']

    def fpath(self, *subpaths, root=None):
        """
        A convenient method which constructs an absolute from a given subpath, relative to root, which should be one of the path
        shortcuts mentioned above.
        """
        if not root:
            root = self.INSTALL
        return os.path.join(root, *subpaths)

    def createShared(self, path):
        """Create a symlink to the cache directory at `path`"""
        assert os.path.isdir('cache')
        os.rename('cache', '_cache')
        os.symlink(path, 'cache')

    def revertShared(self):
        assert os.path.islink('cache')
        os.remove('cache')
        os.rename('_cache', 'cache')


class Icons:
    """Set the icons of the interface depending on whether the background colour is light (meaning that dark icons should be used)
    or dark (meaning that light icons should be used)"""
    monoChrome = ['universemap', 'jump', 'expand', 'open', 'cc']

    def __init__(self):
        prefix = ':/dark/' if self.determineLuminescence() else ':/light/'

        for icon in self.monoChrome:
            setattr(self, icon, QtGui.QIcon(prefix + icon))

        self.main = QtGui.QIcon(':/general/main')  # todo: make static class
        self.navmap = QtGui.QIcon(':/general/navmap')
        self.merchant = QtGui.QIcon(':/general/merchant')
        self.roster = QtGui.QIcon(':/general/roster')

        # Linux only:
        self.open = QtGui.QIcon.fromTheme('document-save')
        self.copy = QtGui.QIcon.fromTheme('edit-copy')

    @staticmethod
    def determineLuminescence(threshold=200) -> bool:
        """Determine whether this platform has a light or dark theme by testing the background colour of a push
        button."""
        button = QtWidgets.QPushButton()
        colour = button.palette().color(button.backgroundRole())
        brightness = sum(colour.getRgb()) / 3
        return brightness > threshold


try:
    import flair
    IS_WIN = flair.IS_WIN
    IS_ADMIN = flair.IS_ADMIN
except ImportError:
    IS_WIN = False
    IS_ADMIN = False


plugin = QtCore.QPluginLoader('/home/biqqles/.local/lib/python3.7/site-packages/PyQt5/Qt/plugins/platformthemes/KDEPlasmaPlatformTheme.so')
print(plugin.load())
QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Style::Breeze'))


app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(':/general/main'))

# platform specific initialisation
if IS_WIN:
    font = app.font()
    font.setFamily('Segoe UI')
    font.setPointSizeF(font.pointSize() * 1.2)
    app.setFont(font)
from PyQt5 import Qt
print('version', Qt.QT_VERSION_STR)

    # switch cwd to directory and add to path (workaround for potential problems after running after install)
    # abspath = os.path.abspath(__file__)
    # dname = os.path.dirname(abspath)
    # os.chdir(dname)
    # sys.path.insert(0, dname)


icons = Icons()
config = Configuration()


if QtWidgets.QStyleFactory.keys() == ['Windows', 'Fusion']:
    print('Warning: native Qt style not available. Defaulting to Fusion - the application may not render correctly.'
          ' To fix this, install the PyQt5 packages from your distro\'s repos, not pip')
