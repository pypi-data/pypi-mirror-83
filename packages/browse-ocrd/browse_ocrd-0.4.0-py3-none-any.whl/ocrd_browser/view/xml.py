from gi.repository import GObject, GtkSource, Gtk

from typing import Optional, Tuple, Any

from ocrd_utils.constants import MIMETYPE_PAGE
from ocrd_models.ocrd_page import to_xml
from ocrd_browser.view import View
from ocrd_browser.view.base import FileGroupSelector, FileGroupFilter

GObject.type_register(GtkSource.View)


class ViewXml(View):
    """
    A view of the current PAGE-XML with syntax highlighting
    """

    label = 'PAGE-XML'

    def __init__(self, name: str, window: Gtk.Window):
        super().__init__(name, window)
        self.file_group: Tuple[Optional[str], Optional[str]] = (None, MIMETYPE_PAGE)
        # noinspection PyTypeChecker
        self.text_view: GtkSource.View = None
        # noinspection PyTypeChecker
        self.buffer: GtkSource.Buffer = None

    def build(self) -> None:
        super().build()
        self.add_configurator('file_group', FileGroupSelector(FileGroupFilter.PAGE))

        lang_manager = GtkSource.LanguageManager()
        style_manager = GtkSource.StyleSchemeManager()

        self.text_view = GtkSource.View(visible=True, vexpand=False, editable=False, monospace=True,
                                        show_line_numbers=True,
                                        width_request=400)
        self.buffer = self.text_view.get_buffer()
        self.buffer.set_language(lang_manager.get_language('xml'))
        self.buffer.set_style_scheme(style_manager.get_scheme('tango'))

        self.viewport.add(self.text_view)

    @property
    def use_file_group(self) -> str:
        return self.file_group[0]

    def config_changed(self, name: str, value: Any) -> None:
        super().config_changed(name, value)
        self.reload()

    def redraw(self) -> None:
        if self.current:
            self.text_view.set_tooltip_text(self.page_id)
            text = to_xml(self.current.pc_gts)
            # TODO: Crashes with big XML, as a workaround disable highlighting
            self.buffer.set_highlight_syntax(len(text) <= 50000)
            self.buffer.set_text(text)
        else:
            self.buffer.set_text('')

