import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gtk
from renderer import Renderer
from texturemanager import TextureManager

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Hello World')

        widthBounds = Gtk.Adjustment(value=10, lower=1, upper=30, step_increment=1, page_increment=10, page_size=0)
        self.btn_tilewidth = Gtk.SpinButton()
        self.btn_tilewidth.set_adjustment(widthBounds)
        self.btn_tilewidth.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        heightBounds = Gtk.Adjustment(value=10, lower=1, upper=20, step_increment=1, page_increment=10, page_size=0)
        self.btn_tileheight = Gtk.SpinButton()
        self.btn_tileheight.set_adjustment(heightBounds)
        self.btn_tileheight.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)

        btn_apply = Gtk.Button(label='Apply new dimensions')
        btn_apply.connect('clicked', self.change_dimensions)

        ab = Gtk.ActionBar()
        ab.props.hexpand = True
        ab.pack_start(Gtk.Label(label='Width:'))
        ab.pack_start(self.btn_tilewidth)
        ab.pack_start(Gtk.Label(label='Height:'))
        ab.pack_start(self.btn_tileheight)
        ab.pack_end(btn_apply)

        self.img = Gtk.Image()
        self.img.props.halign = 1
        self.img.props.valign = 1
        self.img.props.margin = 0
        evbox_img = Gtk.EventBox()
        evbox_img.add(self.img)
        evbox_img.connect('button_press_event', self.img_click)

        sw = Gtk.ScrolledWindow()
        sw.add(evbox_img)
        sw.props.expand = True

        grid = Gtk.Grid()
        grid.props.expand = True
        grid.attach(sw, 0, 0, 5, 4)
        grid.attach(ab, 0, 4, 1, 5)

        btn_open = Gtk.Button(label='Open')
        btn_open.connect('clicked', self.tileset_open)

        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.pack_start(btn_open)

        self.add(grid)
        self.set_default_size(640, 480)
        self.set_titlebar(self.header)

        self.renderer = None
        self.ready = False

    def img_click(self, w, e):
        if e.type == Gdk.EventType.BUTTON_PRESS and self.ready:
            try:
                tileX, tileY = (int(e.x / 24), int(e.y / 24))
                self.renderer.setTile(tileX, tileY,
                        0 if self.renderer.getTile(tileX, tileY) == 1 else 1)
                self.img.set_from_pixbuf(self.renderer.getPixbuf())
            except KeyError:
                pass

    def tileset_open(self, w):
        chooser = Gtk.FileChooserNative(title='Open Tileset Folder',
                action=Gtk.FileChooserAction.SELECT_FOLDER,
                accept_label='Open', cancel_label='Cancel')
        result = chooser.run()
        if result == -3:
            texturemanager = TextureManager(chooser.get_filename())
            self.header.set_title(chooser.get_filename())
            self.init_renderer(tm=texturemanager)
        chooser.destroy()

    def change_dimensions(self, w):
        if self.ready:
            self.init_renderer()

    def init_renderer(self, tm=None):
        width = self.btn_tilewidth.get_value_as_int()
        height = self.btn_tileheight.get_value_as_int()
        self.renderer = Renderer(self.renderer, width, height, tm if tm is not None else self.renderer.texturemanager)
        self.img.set_from_pixbuf(self.renderer.getPixbuf())
        self.ready = True

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
