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
"""Voice setting tab on settings window"""
import json
from configparser import ConfigParser
import gi
from .settings import SettingsWindow
gi.require_version("Gtk", "3.0")
# pylint: disable=wrong-import-position,wrong-import-order
from gi.repository import Gtk, Gdk, Pango


class VoiceSettingsWindow(SettingsWindow):
    """Voice setting tab on settings window"""

    def __init__(self, overlay):
        SettingsWindow.__init__(self)
        self.overlay = overlay
        self.set_size_request(400, 200)
        self.connect("destroy", self.close_window)
        self.connect("delete-event", self.close_window)
        self.placement_window = None
        self.align_x = None
        self.align_y = None
        self.bg_col = None
        self.fg_col = None
        self.tk_col = None
        self.mt_col = None
        self.avatar_size = None
        self.icon_spacing = None
        self.text_padding = None
        self.font = None
        self.square_avatar = None
        self.only_speaking = None
        self.highlight_self = None
        self.icon_only = None
        self.monitor = None
        self.vert_edge_padding = None
        self.horz_edge_padding = None
        self.floating = None
        self.order = None
        self.init_config()

        self.create_gui()

    def present_settings(self):
        """
        Show tab
        """
        self.show_all()
        if not self.floating:
            self.align_x_widget.show()
            self.align_y_widget.show()
            self.align_monitor_widget.show()
            self.align_placement_widget.hide()
        else:
            self.align_x_widget.hide()
            self.align_y_widget.hide()
            self.align_monitor_widget.show()
            self.align_placement_widget.show()

    def read_config(self):
        """
        Read 'main' section of the config file
        """
        config = ConfigParser(interpolation=None)
        config.read(self.config_file)
        self.align_x = config.getboolean("main", "rightalign", fallback=True)
        self.align_y = config.getint("main", "topalign", fallback=1)
        self.bg_col = json.loads(config.get(
            "main", "bg_col", fallback="[0.0,0.0,0.0,0.5]"))
        self.fg_col = json.loads(config.get(
            "main", "fg_col", fallback="[1.0,1.0,1.0,1.0]"))
        self.tk_col = json.loads(config.get(
            "main", "tk_col", fallback="[0.0,0.7,0.0,1.0]"))
        self.mt_col = json.loads(config.get(
            "main", "mt_col", fallback="[0.6,0.0,0.0,1.0]"))
        self.avatar_size = config.getint("main", "avatar_size", fallback=48)
        self.icon_spacing = config.getint("main", "icon_spacing", fallback=8)
        self.text_padding = config.getint("main", "text_padding", fallback=6)
        self.font = config.get("main", "font", fallback=None)
        self.square_avatar = config.getboolean(
            "main", "square_avatar", fallback=False)
        self.only_speaking = config.getboolean(
            "main", "only_speaking", fallback=False)
        self.highlight_self = config.getboolean(
            "main", "highlight_self", fallback=False)
        self.icon_only = config.getboolean(
            "main", "icon_only", fallback=False)
        self.monitor = config.get("main", "monitor", fallback="None")
        self.vert_edge_padding = config.getint(
            "main", "vert_edge_padding", fallback=0)
        self.horz_edge_padding = config.getint(
            "main", "horz_edge_padding", fallback=0)
        self.floating = config.getboolean("main", "floating", fallback=False)
        self.floating_x = config.getint("main", "floating_x", fallback=0)
        self.floating_y = config.getint("main", "floating_y", fallback=0)
        self.floating_w = config.getint("main", "floating_w", fallback=400)
        self.floating_h = config.getint("main", "floating_h", fallback=400)
        self.order = config.getint("main", "order", fallback=0)

        # Pass all of our config over to the overlay
        self.overlay.set_align_x(self.align_x)
        self.overlay.set_align_y(self.align_y)
        self.overlay.set_bg(self.bg_col)
        self.overlay.set_fg(self.fg_col)
        self.overlay.set_tk(self.tk_col)
        self.overlay.set_mt(self.mt_col)
        self.overlay.set_avatar_size(self.avatar_size)
        self.overlay.set_icon_spacing(self.icon_spacing)
        self.overlay.set_text_padding(self.text_padding)
        self.overlay.set_square_avatar(self.square_avatar)
        self.overlay.set_only_speaking(self.only_speaking)
        self.overlay.set_highlight_self(self.highlight_self)
        self.overlay.set_icon_only(self.icon_only)
        self.overlay.set_monitor(self.get_monitor_index(
            self.monitor), self.get_monitor_obj(self.monitor))
        self.overlay.set_vert_edge_padding(self.vert_edge_padding)
        self.overlay.set_horz_edge_padding(self.horz_edge_padding)
        self.overlay.set_order(self.order)

        self.overlay.set_floating(
            self.floating, self.floating_x, self.floating_y, self.floating_w, self.floating_h)

        if self.font:
            desc = Pango.FontDescription.from_string(self.font)
            size = desc.get_size()
            if not desc.get_size_is_absolute():
                size = size / Pango.SCALE
            self.overlay.set_font(desc.get_family(), size)

    def save_config(self):
        """
        Write settings out to the 'main' section of the config file
        """
        config = ConfigParser(interpolation=None)
        config.read(self.config_file)
        if not config.has_section("main"):
            config.add_section("main")

        config.set("main", "rightalign", "%d" % (int(self.align_x)))
        config.set("main", "topalign", "%d" % (self.align_y))
        config.set("main", "bg_col", json.dumps(self.bg_col))
        config.set("main", "fg_col", json.dumps(self.fg_col))
        config.set("main", "tk_col", json.dumps(self.tk_col))
        config.set("main", "mt_col", json.dumps(self.mt_col))
        config.set("main", "avatar_size", "%d" % (self.avatar_size))
        config.set("main", "icon_spacing", "%d" % (self.icon_spacing))
        config.set("main", "text_padding", "%d" % (self.text_padding))
        if self.font:
            config.set("main", "font", self.font)
        config.set("main", "square_avatar", "%d" % (int(self.square_avatar)))
        config.set("main", "only_speaking", "%d" % (int(self.only_speaking)))
        config.set("main", "highlight_self", "%d" % (int(self.highlight_self)))
        config.set("main", "icon_only", "%d" % (int(self.icon_only)))
        config.set("main", "monitor", self.monitor)
        config.set("main", "vert_edge_padding", "%d" %
                   (self.vert_edge_padding))
        config.set("main", "horz_edge_padding", "%d" %
                   (self.horz_edge_padding))
        config.set("main", "floating", "%s" % (int(self.floating)))
        config.set("main", "floating_x", "%s" % (self.floating_x))
        config.set("main", "floating_y", "%s" % (self.floating_y))
        config.set("main", "floating_w", "%s" % (self.floating_w))
        config.set("main", "floating_h", "%s" % (self.floating_h))
        config.set("main", "order", "%s" % (self.order))

        with open(self.config_file, 'w') as file:
            config.write(file)

    def create_gui(self):
        """
        Prepare the gui
        """
        box = Gtk.Grid()

        # Font chooser
        font_label = Gtk.Label.new("Font")
        font = Gtk.FontButton()
        if self.font:
            font.set_font(self.font)
        font.connect("font-set", self.change_font)

        # Colours
        bg_col_label = Gtk.Label.new("Background colour")
        bg_col = Gtk.ColorButton.new_with_rgba(
            Gdk.RGBA(self.bg_col[0], self.bg_col[1], self.bg_col[2], self.bg_col[3]))
        fg_col_label = Gtk.Label.new("Text colour")
        fg_col = Gtk.ColorButton.new_with_rgba(
            Gdk.RGBA(self.fg_col[0], self.fg_col[1], self.fg_col[2], self.fg_col[3]))
        tk_col_label = Gtk.Label.new("Talk colour")
        tk_col = Gtk.ColorButton.new_with_rgba(
            Gdk.RGBA(self.tk_col[0], self.tk_col[1], self.tk_col[2], self.tk_col[3]))
        mt_col_label = Gtk.Label.new("Mute colour")
        mt_col = Gtk.ColorButton.new_with_rgba(
            Gdk.RGBA(self.mt_col[0], self.mt_col[1], self.mt_col[2], self.mt_col[3]))
        bg_col.set_use_alpha(True)
        fg_col.set_use_alpha(True)
        tk_col.set_use_alpha(True)
        mt_col.set_use_alpha(True)
        bg_col.connect("color-set", self.change_bg)
        fg_col.connect("color-set", self.change_fg)
        tk_col.connect("color-set", self.change_tk)
        mt_col.connect("color-set", self.change_mt)

        # Avatar size
        avatar_size_label = Gtk.Label.new("Avatar size")
        avatar_adjustment = Gtk.Adjustment.new(
            self.avatar_size, 8, 128, 1, 1, 8)
        avatar_size = Gtk.SpinButton.new(avatar_adjustment, 0, 0)
        avatar_size.connect("value-changed", self.change_avatar_size)

        # Monitor & Alignment
        align_label = Gtk.Label.new("Overlay Location")

        align_type_box = Gtk.HBox()
        align_type_edge = Gtk.RadioButton.new_with_label(
            None, "Anchor to edge")
        align_type_floating = Gtk.RadioButton.new_with_label_from_widget(
            align_type_edge, "Floating")
        if self.floating:
            align_type_floating.set_active(True)
        align_type_box.add(align_type_edge)
        align_type_box.add(align_type_floating)

        monitor_store = Gtk.ListStore(str)
        display = Gdk.Display.get_default()
        if "get_n_monitors" in dir(display):
            for i in range(0, display.get_n_monitors()):
                monitor_store.append([display.get_monitor(i).get_model()])
        monitor = Gtk.ComboBox.new_with_model(monitor_store)
        monitor.set_active(self.get_monitor_index(self.monitor))
        monitor.connect("changed", self.change_monitor)
        renderer_text = Gtk.CellRendererText()
        monitor.pack_start(renderer_text, True)
        monitor.add_attribute(renderer_text, "text", 0)

        align_x_store = Gtk.ListStore(str)
        align_x_store.append(["Left"])
        align_x_store.append(["Right"])
        align_x = Gtk.ComboBox.new_with_model(align_x_store)
        align_x.set_active(True if self.align_x else False)
        align_x.connect("changed", self.change_align_x)
        renderer_text = Gtk.CellRendererText()
        align_x.pack_start(renderer_text, True)
        align_x.add_attribute(renderer_text, "text", 0)

        align_y_store = Gtk.ListStore(str)
        align_y_store.append(["Top"])
        align_y_store.append(["Middle"])
        align_y_store.append(["Bottom"])
        align_y = Gtk.ComboBox.new_with_model(align_y_store)
        align_y.set_active(self.align_y)
        align_y.connect("changed", self.change_align_y)
        renderer_text = Gtk.CellRendererText()
        align_y.pack_start(renderer_text, True)
        align_y.add_attribute(renderer_text, "text", 0)

        align_placement_button = Gtk.Button.new_with_label("Place Window")

        align_type_edge.connect("toggled", self.change_align_type_edge)
        align_type_floating.connect("toggled", self.change_align_type_floating)
        align_placement_button.connect("pressed", self.change_placement)

        self.align_x_widget = align_x
        self.align_y_widget = align_y
        self.align_monitor_widget = monitor
        self.align_placement_widget = align_placement_button

        # Icon spacing
        icon_spacing_label = Gtk.Label.new("Icon Spacing")
        icon_spacing_adjustment = Gtk.Adjustment.new(
            self.icon_spacing, 0, 64, 1, 1, 0)
        icon_spacing = Gtk.SpinButton.new(icon_spacing_adjustment, 0, 0)
        icon_spacing.connect("value-changed", self.change_icon_spacing)

        # Text padding
        text_padding_label = Gtk.Label.new("Text Padding")
        text_padding_adjustment = Gtk.Adjustment.new(
            self.text_padding, 0, 64, 1, 1, 0)
        text_padding = Gtk.SpinButton.new(text_padding_adjustment, 0, 0)
        text_padding.connect("value-changed", self.change_text_padding)

        # Edge padding
        vert_edge_padding_label = Gtk.Label.new("Vertical Edge Padding")
        vert_edge_padding_adjustment = Gtk.Adjustment.new(
            self.vert_edge_padding, 0, 1000, 1, 1, 0)
        vert_edge_padding = Gtk.SpinButton.new(
            vert_edge_padding_adjustment, 0, 0)
        vert_edge_padding.connect(
            "value-changed", self.change_vert_edge_padding)

        horz_edge_padding_label = Gtk.Label.new("Horizontal Edge Padding")
        horz_edge_padding_adjustment = Gtk.Adjustment.new(
            self.horz_edge_padding, 0, 1000, 1, 1, 0)
        horz_edge_padding = Gtk.SpinButton.new(
            horz_edge_padding_adjustment, 0, 0)
        horz_edge_padding.connect(
            "value-changed", self.change_horz_edge_padding)

        # Avatar shape
        square_avatar_label = Gtk.Label.new("Square Avatar")
        square_avatar = Gtk.CheckButton.new()
        square_avatar.set_active(self.square_avatar)
        square_avatar.connect("toggled", self.change_square_avatar)

        only_speaking_label = Gtk.Label.new("Display Speakers Only")
        only_speaking = Gtk.CheckButton.new()
        only_speaking.set_active(self.only_speaking)
        only_speaking.connect("toggled", self.change_only_speaking)

        highlight_self_label = Gtk.Label.new("Highlight Self")
        highlight_self = Gtk.CheckButton.new()
        highlight_self.set_active(self.highlight_self)
        highlight_self.connect("toggled", self.change_highlight_self)

        # Display icon only
        icon_only_label = Gtk.Label.new("Display Icon Only")
        icon_only = Gtk.CheckButton.new()
        icon_only.set_active(self.icon_only)
        icon_only.connect("toggled", self.change_icon_only)

        # Order avatars
        order_label = Gtk.Label.new("Order Avatars By")
        order_store = Gtk.ListStore(str)
        order_store.append(["Alphabetically"])
        order_store.append(["ID"])
        order_store.append(["Last Spoken"])
        order = Gtk.ComboBox.new_with_model(order_store)
        order.set_active(self.order)
        order.connect("changed", self.change_order)
        renderer_text = Gtk.CellRendererText()
        order.pack_start(renderer_text, True)
        order.add_attribute(renderer_text, "text", 0)

        box.attach(font_label, 0, 0, 1, 1)
        box.attach(font, 1, 0, 1, 1)
        box.attach(bg_col_label, 0, 1, 1, 1)
        box.attach(bg_col, 1, 1, 1, 1)
        box.attach(fg_col_label, 0, 2, 1, 1)
        box.attach(fg_col, 1, 2, 1, 1)
        box.attach(tk_col_label, 0, 3, 1, 1)
        box.attach(tk_col, 1, 3, 1, 1)
        box.attach(mt_col_label, 0, 4, 1, 1)
        box.attach(mt_col, 1, 4, 1, 1)
        box.attach(avatar_size_label, 0, 5, 1, 1)
        box.attach(avatar_size, 1, 5, 1, 1)
        box.attach(align_label, 0, 6, 1, 5)
        box.attach(align_type_box, 1, 6, 1, 1)
        box.attach(monitor, 1, 7, 1, 1)
        box.attach(align_x, 1, 8, 1, 1)
        box.attach(align_y, 1, 9, 1, 1)
        box.attach(align_placement_button, 1, 10, 1, 1)
        box.attach(icon_spacing_label, 0, 11, 1, 1)
        box.attach(icon_spacing, 1, 11, 1, 1)
        box.attach(text_padding_label, 0, 12, 1, 1)
        box.attach(text_padding, 1, 12, 1, 1)
        box.attach(vert_edge_padding_label, 0, 13, 1, 1)
        box.attach(vert_edge_padding, 1, 13, 1, 1)
        box.attach(horz_edge_padding_label, 0, 14, 1, 1)
        box.attach(horz_edge_padding, 1, 14, 1, 1)
        box.attach(square_avatar_label, 0, 15, 1, 1)
        box.attach(square_avatar, 1, 15, 1, 1)
        box.attach(only_speaking_label, 0, 16, 1, 1)
        box.attach(only_speaking, 1, 16, 1, 1)
        box.attach(highlight_self_label, 0, 17, 1, 1)
        box.attach(highlight_self, 1, 17, 1, 1)
        box.attach(icon_only_label, 0, 18, 1, 1)
        box.attach(icon_only, 1, 18, 1, 1)
        box.attach(order_label, 0, 19, 1, 1)
        box.attach(order, 1, 19, 1, 1)

        self.add(box)

    def change_font(self, button):
        """
        Font settings changed
        """
        font = button.get_font()
        desc = Pango.FontDescription.from_string(font)
        size = desc.get_size()
        if not desc.get_size_is_absolute():
            size = size / Pango.SCALE
        self.overlay.set_font(desc.get_family(), size)

        self.font = desc.to_string()
        self.save_config()

    def change_bg(self, button):
        """
        Background colour changed
        """
        colour = button.get_rgba()
        colour = [colour.red, colour.green, colour.blue, colour.alpha]
        self.overlay.set_bg(colour)

        self.bg_col = colour
        self.save_config()

    def change_fg(self, button):
        """
        Text colour changed
        """
        colour = button.get_rgba()
        colour = [colour.red, colour.green, colour.blue, colour.alpha]
        self.overlay.set_fg(colour)

        self.fg_col = colour
        self.save_config()

    def change_tk(self, button):
        """
        Talking colour changed
        """
        colour = button.get_rgba()
        colour = [colour.red, colour.green, colour.blue, colour.alpha]
        self.overlay.set_tk(colour)

        self.tk_col = colour
        self.save_config()

    def change_mt(self, button):
        """
        Mute colour changed
        """
        colour = button.get_rgba()
        colour = [colour.red, colour.green, colour.blue, colour.alpha]
        self.overlay.set_mt(colour)

        self.mt_col = colour
        self.save_config()

    def change_avatar_size(self, button):
        """
        Avatar size setting changed
        """
        self.overlay.set_avatar_size(button.get_value())

        self.avatar_size = button.get_value()
        self.save_config()

    def change_icon_spacing(self, button):
        """
        Inter-icon spacing changed
        """
        self.overlay.set_icon_spacing(button.get_value())

        self.icon_spacing = int(button.get_value())
        self.save_config()

    def change_text_padding(self, button):
        """
        Text padding changed
        """
        self.overlay.set_text_padding(button.get_value())

        self.text_padding = button.get_value()
        self.save_config()

    def change_vert_edge_padding(self, button):
        """
        Vertical padding changed
        """
        self.overlay.set_vert_edge_padding(button.get_value())

        self.vert_edge_padding = button.get_value()
        self.save_config()

    def change_horz_edge_padding(self, button):
        """
        Horizontal padding changed
        """
        self.overlay.set_horz_edge_padding(button.get_value())

        self.horz_edge_padding = button.get_value()
        self.save_config()

    def change_square_avatar(self, button):
        """
        Square avatar setting changed
        """
        self.overlay.set_square_avatar(button.get_active())

        self.square_avatar = button.get_active()
        self.save_config()

    def change_only_speaking(self, button):
        """
        Show only speaking users setting changed
        """
        self.overlay.set_only_speaking(button.get_active())

        self.only_speaking = button.get_active()
        self.save_config()

    def change_highlight_self(self, button):
        """
        Highlight self setting changed
        """
        self.overlay.set_highlight_self(button.get_active())

        self.highlight_self = button.get_active()
        self.save_config()

    def change_icon_only(self, button):
        """
        Icon only setting changed
        """
        self.overlay.set_icon_only(button.get_active())

        self.icon_only = button.get_active()
        self.save_config()

    def change_order(self, button):
        """
        Order user setting changed
        """
        self.overlay.set_order(button.get_active())

        self.order = button.get_active()
        self.save_config()
