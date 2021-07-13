"""
My first application
"""
import sys
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.images import Image

# from https://github.com/beeware/toga/blob/master/examples/table/table/app.py
bee_movies = [
    ('The Secret Life of Bees', '2008', '7.3', 'Drama'),
    ('Bee Movie', '2007', '6.1', 'Animation, Adventure, Comedy'),
    ('Bees', '1998', '6.3', 'Horror'),
    ('The Girl Who Swallowed Bees', '2007', '7.5', 'Short'),
    ('Birds Do It, Bees Do It', '1974', '7.3', 'Documentary'),
    ('Bees: A Life for the Queen', '1998', '8.0', 'TV Movie'),
    ('Bees in Paradise', '1944', '5.4', 'Comedy, Musical'),
    ('Keeper of the Bees', '1947', '6.3', 'Drama')
]


class BeewareTogaTestApp(toga.App):
    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self._prepare_main_box()
        self.main_window.show()

        # this is testing for using external Python dependencies
        # import ptpython
        # print(ptpython.__file__)

    def _prepare_main_box(self):
        container = toga.OptionContainer()

        self.table = toga.Table(
            headings=['Title', 'Year', 'Genre', 'Rating'],
            data=bee_movies,
            style=Pack(flex=1, padding_right=5),
            multiple_select=False,
        )

        open_image_button = toga.Button(
            'Open Image',
            on_press=self._open_image,
            style=Pack(padding=5)
        )
        self.image_view = toga.ImageView(style=Pack(flex=1))
        image_view_box = toga.Box(
            children=[open_image_button, self.image_view],
            style=Pack(direction=COLUMN),
        )

        container.add('Table', self.table)
        container.add('Image page', image_view_box)

        main_box = toga.Box(style=Pack(direction=COLUMN))
        main_box.add(container)

        return main_box

    def _open_image(self, source_button):
        # TODO no idea how to draw on an image...
        # free-form GUI object placement would help, or Canvas with a background
        try:
            selected_file = self.main_window.open_file_dialog('Open image file')
        except ValueError:
            print('no image chosen')
            return
        self.image_view.image = Image(selected_file)


def main():
    return BeewareTogaTestApp()
