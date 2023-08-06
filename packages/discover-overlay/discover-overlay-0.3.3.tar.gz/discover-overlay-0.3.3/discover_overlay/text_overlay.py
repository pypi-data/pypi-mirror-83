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
"""Overlay window for text"""
import logging
import time
import re
import cairo
import gi
from .image_getter import get_surface, draw_img_to_rect, get_aspected_size
from .overlay import OverlayWindow
gi.require_version("Gtk", "3.0")
gi.require_version('PangoCairo', '1.0')
# pylint: disable=wrong-import-position,wrong-import-order
from gi.repository import Pango, PangoCairo


class TextOverlayWindow(OverlayWindow):
    """Overlay window for voice"""

    def __init__(self, discover):
        OverlayWindow.__init__(self)
        self.discover = discover
        self.text_spacing = 4
        self.content = []
        self.text_font = None
        self.text_size = 13
        self.text_time = None
        self.show_attach = None
        self.popup_style = None
        # 0, 0, self.text_size, self.text_size)
        self.pango_rect = Pango.Rectangle()
        self.pango_rect.width = self.text_size * Pango.SCALE
        self.pango_rect.height = self.text_size * Pango.SCALE

        self.connected = True
        self.bg_col = [0.0, 0.6, 0.0, 0.1]
        self.fg_col = [1.0, 1.0, 1.0, 1.0]
        self.attachment = {}

        self.image_list = []
        self.img_finder = re.compile(r"`")
        self.set_title("Discover Text")

    def set_text_time(self, timer):
        """
        Set the duration that a message will be visible for.
        """
        self.text_time = timer

    def set_text_list(self, tlist, altered):
        """
        Update the list of text messages to show
        """
        self.content = tlist
        if altered:
            self.redraw()

    def set_fg(self, fg_col):
        """
        Set default text colour
        """
        self.fg_col = fg_col
        self.redraw()

    def set_bg(self, bg_col):
        """
        Set background colour
        """
        self.bg_col = bg_col
        self.redraw()

    def set_show_attach(self, attachment):
        """
        Set if attachments should be shown inline
        """
        self.show_attach = attachment
        self.redraw()

    def set_popup_style(self, boolean):
        """
        Set if message disappear after a certain duration
        """
        self.popup_style = boolean

    def set_font(self, name, size):
        """
        Set font used to render text
        """
        self.text_font = name
        self.text_size = size
        self.pango_rect = Pango.Rectangle()
        self.pango_rect.width = self.text_size * Pango.SCALE
        self.pango_rect.height = self.text_size * Pango.SCALE
        self.redraw()

    def make_line(self, message):
        """
        Decode a recursive JSON object into pango markup.
        """
        ret = ""
        if isinstance(message, list):
            for inner_message in message:
                ret = "%s%s" % (ret, self.make_line(inner_message))
        elif isinstance(message, str):
            ret = message
        elif message['type'] == 'strong':
            ret = "<b>%s</b>" % (self.make_line(message['content']))
        elif message['type'] == 'text':
            ret = self.sanitize_string(message['content'])
        elif message['type'] == 'link':
            ret = "<u>%s</u>" % (self.make_line(message['content']))
        elif message['type'] == 'emoji':
            if 'surrogate' in message:
                # ['src'] is SVG URL
                # ret = msg
                ret = message['surrogate']
            else:
                ### Add Image ###
                url = ("https://cdn.discordapp.com/emojis/%s.png?v=1" %
                       (message['emojiId']))
                img = {"url": url}
                self.image_list.append(img)
                ret = "`"
        elif (message['type'] == 'inlineCode' or
              message['type'] == 'codeBlock' or
              message['type'] == 'blockQuote'):
            ret = "<span font_family=\"monospace\" background=\"#0004\">%s</span>" % (
                self.make_line(message['content']))
        elif message['type'] == 'u':
            ret = "<u>%s</u>" % (self.make_line(message['content']))
        elif message['type'] == 'em':
            ret = "<i>%s</i>" % (self.make_line(message['content']))
        elif message['type'] == 's':
            ret = "<s>%s</s>" % (self.make_line(message['content']))
        elif message['type'] == 'channel':
            ret = self.make_line(message['content'])
        elif message['type'] == 'mention':
            ret = self.make_line(message['content'])
        elif message['type'] == 'br':
            ret = '\n'
        else:
            logging.error("Unknown text type : %s", message["type"])
        return ret

    def recv_attach(self, identifier, pix):
        """
        Called when an image has been downloaded by image_getter
        """
        self.attachment[identifier] = pix
        self.redraw()

    def overlay_draw(self, _w, context, data=None):
        """
        Draw the overlay
        """
        self.context = context
        context.set_antialias(cairo.ANTIALIAS_GOOD)
        (width, height) = self.get_size()
        # Make background transparent
        context.set_source_rgba(0.0, 0.0, 0.0, 0.0)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.save()
        if self.is_wayland:
            # Special case!
            # The window is full-screen regardless of what the user has selected. Because Wayland
            # We need to set a clip and a transform to imitate original behaviour

            width = self.width
            height = self.height
            context.translate(self.pos_x, self.pos_y)
            context.rectangle(0, 0, width, height)
            context.clip()

        current_y = height
        tnow = time.time()
        for line in reversed(self.content):
            if self.popup_style and tnow - line['time'] > self.text_time:
                break
            out_line = ""
            self.image_list = []

            col = "#fff"
            if 'nick_col' in line and line['nick_col']:
                col = line['nick_col']
            for in_line in line['content']:
                out_line = "%s%s" % (out_line, self.make_line(in_line))
            if line['attach'] and self.show_attach:
                attachment = line['attach'][0]
                url = attachment['url']
                extension = attachment['filename']
                extension = extension.rsplit(".", 1)[1]
                extension = extension.lower()
                if extension in ['jpeg', 'jpg', 'png', 'gif']:
                    if url in self.attachment:
                        current_y = self.draw_attach(current_y, url)
                    else:
                        get_surface(self.recv_attach,
                                    url,
                                    url, None)
                else:
                    logging.warning("Unknown file extension '%s'", extension)
                # cy = self.draw_text(cy, "%s" % (line['attach']))
            message = "<span foreground='%s'>%s</span>: %s" % (self.sanitize_string(col),
                                                               self.sanitize_string(
                                                                   line["nick"]),
                                                               out_line)
            current_y = self.draw_text(current_y, message)
            if current_y <= 0:
                # We've done enough
                break
        if self.is_wayland:
            context.restore()

    def draw_attach(self, pos_y, url):
        """
        Draw an attachment
        """
        if url in self.attachment and self.attachment[url]:
            pix = self.attachment[url]
            image_width = min(pix.get_width(), self.width)
            image_height = min(pix.get_height(), (self.height * .7))
            (_ax, _ay, _aw, aspect_height) = get_aspected_size(
                pix, image_width, image_height)
            self.col(self.bg_col)
            self.context.rectangle(0, pos_y - aspect_height,
                                   self.width, aspect_height)

            self.context.fill()
            self.context.set_operator(cairo.OPERATOR_OVER)
            _new_w, new_h = draw_img_to_rect(
                pix, self.context, 0, pos_y - image_height, image_width, image_height, aspect=True)
            return pos_y - new_h
        return pos_y

    def draw_text(self, pos_y, text):
        """
        Draw a text message, returning the Y position of the next message
        """
        layout = self.create_pango_layout(text)
        layout.set_markup(text, -1)
        attr = layout.get_attributes()

        layout.set_width(Pango.SCALE * self.width)
        layout.set_spacing(Pango.SCALE * 3)
        if self.text_font:
            font = Pango.FontDescription(
                "%s %s" % (self.text_font, self.text_size))
            layout.set_font_description(font)
        _tw, text_height = layout.get_pixel_size()
        self.col(self.bg_col)
        self.context.rectangle(0, pos_y - text_height, self.width, text_height)
        self.context.fill()
        self.context.set_operator(cairo.OPERATOR_OVER)
        self.col(self.fg_col)

        self.context.move_to(0, pos_y - text_height)
        PangoCairo.context_set_shape_renderer(
            self.get_pango_context(), self.render_custom, None)

        text = layout.get_text()
        count = 0

        for loc in self.img_finder.finditer(text):
            idx = loc.start()

            if len(self.image_list) <= count:
                break  # We fucked up. Who types ` anyway
            # url = self.imgList[count]

            attachment = Pango.attr_shape_new_with_data(
                self.pango_rect, self.pango_rect, count, None)
            attachment.start_index = idx
            attachment.end_index = idx + 1
            attr.insert(attachment)
            count += 1
        layout.set_attributes(attr)

        PangoCairo.show_layout(self.context, layout)
        return pos_y - text_height

    def render_custom(self, ctx, shape, path, _data):
        """
        Draw an inline image as a custom emoticon
        """
        key = self.image_list[shape.data]['url']
        if key not in self.attachment:
            get_surface(self.recv_attach,
                        key,
                        key, None)
            return
        pix = self.attachment[key]
        (pos_x, pos_y) = ctx.get_current_point()
        draw_img_to_rect(pix, ctx, pos_x, pos_y - self.text_size, self.text_size,
                         self.text_size, path=path)
        return True

    def sanitize_string(self, string):
        """
        Sanitize a text message so that it doesn't intefere with Pango's XML format
        """
        string = string.replace("&", "&amp;")
        string = string.replace("<", "&lt;")
        string = string .replace(">", "&gt;")
        string = string.replace("'", "&#39;")
        string = string.replace("\"", "&#34;")
        return string
