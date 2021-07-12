"""
My first application
"""
import sys
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class BeewareTogaTestApp(toga.App):
    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            'Your name: ',
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            'Say Hello!',
            on_press=self.say_hello,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        import ptpython
        print(ptpython.__file__)

    def say_hello(self, widget):
        self.main_window.info_dialog(
            'Hi there!',
            "Hello, {}".format(self.name_input.value)
        )


def main():
    return BeewareTogaTestApp()
