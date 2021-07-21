# sample taken from https://wiki.wxpython.org/Getting%20Started

import wx
import wx.lib.mixins.listctrl


class AutoWidthListCtrl(wx.ListCtrl, wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin):

    def __init__(self, parent, *args, **kw):
        wx.ListCtrl.__init__(self, parent, wx.ID_ANY, style=wx.LC_REPORT)
        wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin.__init__(self)


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 300))

        self.build_menu()
        # self.build_main_screen()
        self.build_main_screen_with_table()

        # center the window on the screen
        self.Center()

    def build_menu(self):
        filemenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # A Statusbar in the bottom of the window. Displays hits for the menu bar, for example.
        self.CreateStatusBar()

    def build_main_screen(self):
        # Panel makes jumping around with Tab work
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(panel, label='Testowy element tekstowy')
        text_intput = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        button = wx.Button(panel, label='Testowy guzik śćółżź')

        # arguments: box.Add(wx.Window window, integer proportion=0, integer flag = 0, integer border = 0)
        vbox.Add(label, 0, wx.ALL, 5)
        vbox.Add(text_intput, 3, wx.ALL | wx.EXPAND, 5)
        # adding empty space
        vbox.Add((-1, 25))
        vbox.Add(button, 0, wx.ALL, 5)

        panel.SetSizer(vbox)

    def build_main_screen_with_table(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(panel, label='Double-click any row to open an image')

        self.list = AutoWidthListCtrl(panel, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Last name', width=140)
        self.list.InsertColumn(1, 'First name', width=140)
        self.list.InsertColumn(2, 'Height', width=60)

        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.open_image_view)

        vbox.Add(label, 0)
        vbox.Add(self.list, 0, wx.EXPAND, 10)
        panel.SetSizer(vbox)

        data = [
            ('Mejer', 'Zdzichu', 173),
            ('Ptok', 'Kacper', 180),
            ('Ufnal', 'Melania', 169),
            ('Cyroń', 'Marcin', 183),
        ]

        for row_number, row in enumerate(data):
            # this can fail returning -1, theoretically
            self.list.InsertItem(row_number, row[0])
            for column_number, cell in enumerate(row[1:], 1):
                self.list.SetItem(row_number, column_number, str(row[column_number]))

    def open_image_view(self, event):
        image_view = ImageView(self, 'Image view')
        image_view.Show()


class ImageView(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(500, 500))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.bitmap = wx.Bitmap('../hippo.jpg')

        self.SetSize(self.bitmap.GetWidth(), self.bitmap.GetHeight())

        self.image_widget = wx.StaticBitmap(panel, bitmap=self.bitmap)
        # This might not work on a Mac according to
        # https://stackoverflow.com/questions/63972761/how-can-i-receive-mouse-events-on-a-wxpython-staticbitmap
        self.image_widget.Bind(wx.EVT_LEFT_DOWN, self.image_click)
        vbox.Add(self.image_widget)

        panel.SetSizer(vbox)
        self.Center()

    def image_click(self, event):
        print('Image clicked!', event.x, event.y)
        dc = wx.MemoryDC(self.bitmap)
        dc.SetPen(wx.Pen(wx.RED, 1))
        dc.DrawCircle(event.x, event.y, 5)
        self.image_widget.SetBitmap(self.bitmap)



def main():
    app = wx.App(False)
    frame = MainWindow(None, "WxPython test app")
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()
