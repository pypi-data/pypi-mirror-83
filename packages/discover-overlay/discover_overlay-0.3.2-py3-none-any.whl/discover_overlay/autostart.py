#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""A class to assist auto-start"""
import os
import logging
try:
    from xdg.BaseDirectory import xdg_config_home, xdg_data_home
except ModuleNotFoundError:
    from xdg import XDG_CONFIG_HOME as xdg_config_home
    from xdg import XDG_DATA_HOME as xdg_data_home


class Autostart:
    """A class to assist auto-start"""

    def __init__(self, app_name):
        if not app_name.endswith(".desktop"):
            app_name = "%s.desktop" % (app_name)
        self.app_name = app_name
        self.auto_locations = [os.path.join(
            xdg_config_home, 'autostart/'), '/etc/xdg/autostart/']
        self.desktop_locations = [os.path.join(
            xdg_data_home, 'applications/'), '/usr/share/applications/']
        self.auto = self.find_auto()
        self.desktop = self.find_desktop()
        logging.info("Autostart info : desktop %s auto %s",
                     self.desktop, self.auto)

    def find_auto(self):
        """Check all known locations for auto-started apps"""
        for path in self.auto_locations:
            file = os.path.join(path, self.app_name)
            if os.path.exists(file):
                return file
        return None

    def find_desktop(self):
        """Check all known locations for desktop apps"""
        for path in self.desktop_locations:
            file = os.path.join(path, self.app_name)
            if os.path.exists(file):
                return file
        return None

    def set_autostart(self, enable):
        """Set or Unset auto-start state"""
        if enable and not self.auto:
            # Enable
            directory = os.path.join(xdg_config_home, 'autostart')
            self.auto = os.path.join(directory, self.app_name)
            os.symlink(self.desktop, self.auto)
        elif not enable and self.auto:
            # Disable
            if os.path.islink(self.auto):
                os.remove(self.auto)

    def is_auto(self):
        """Check if it's already set to auto-start"""
        return True if self.auto else False
