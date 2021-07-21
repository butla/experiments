# sample taken from https://wiki.wxpython.org/Getting%20Started

import wx

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 300))

        self.build_menu()
        self.build_main_screen()

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

        label = wx.StaticText(panel, label= 'Testowy element tekstowy')
        text_intput = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        button = wx.Button(panel, label='Testowy guzik śćółżź')

        # arguments: box.Add(wx.Window window, integer proportion=0, integer flag = 0, integer border = 0)
        vbox.Add(label, 0, wx.ALL, 5)
        vbox.Add(text_intput, 3, wx.ALL | wx.EXPAND, 5)
        # adding empty space
        vbox.Add((-1, 25))
        vbox.Add(button, 0, wx.ALL, 5)

        panel.SetSizer(vbox)

app = wx.App(False)
frame = MainWindow(None, "Sample editor")
frame.Show()

app.MainLoop()
