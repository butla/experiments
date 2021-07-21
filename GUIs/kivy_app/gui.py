import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
import kivy.graphics
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager

KV = '''
<ClientListScreen>:
    BoxLayout:
        orientation: 'vertical'
        table_box: table_box

        BoxLayout:
            orientation: 'horizontal'

            Label:
                size_hint: 0.25, None
                text: 'Nazwisko'

            Label:
                size_hint: 0.25, None
                text: 'Imię'

            Label:
                size_hint: 0.25, None
                text: 'wzrost'

            Label:
                size_hint: 0.25, None
                text: 'Akcje'


        BoxLayout:
            orientation: 'vertical'
            id: table_box

            PersonRow:
                last_name: 'Mejer'
                first_name: 'Zdzichu'
                height_: 173

            PersonRow:
                last_name: 'Ptok'
                first_name: 'Kacper'
                height_: 180

            PersonRow:
                last_name: 'Ufnal'
                first_name: 'Melania'
                height_: 169

            PersonRow:
                last_name: 'Cyroń'
                first_name: 'Marcin'
                height_: 183

<ImageViewScreen>:
    BoxLayout:
        orientation: 'vertical'

        Button:
            text: 'Go back'
            size_hint: 1, 0.15
            on_press: root.manager.current = 'clients'

        ImageCanvas:
            source: '../hippo.jpg'

<PersonRow>:
    id: person

    BoxLayout:
        orientation: 'horizontal'

        Label:
            size_hint: 0.25, None
            text: person.last_name

        Label:
            size_hint: 0.25, None
            text: person.first_name

        Label:
            size_hint: 0.25, None
            text: str(person.height_)

        Button:
            size_hint: 0.25, None
            text: 'otwórz'
            on_press: app.open_image()
'''


# TODO can I reference objects in the layout directly from the app object?
class ClientListScreen(Screen):
    # TODO fill that table_box from sqlite. Might have to be made into a recycle view
    table_box = ObjectProperty()


class ImageViewScreen(Screen):
    # TODO fill that table_box from sqlite. Might have to be made into a recycle view
    table_box = ObjectProperty()

    # an example of how to use file chooser is in Kivy repo: kivy/examples/RST_Editor/main.py

class PersonRow(BoxLayout):
    last_name = StringProperty()
    first_name = StringProperty()
    height_ = NumericProperty()

class ImageCanvas(Image):
    def on_touch_down(self, touch):
        # TODO limit the processing to touches on the image
        with self.canvas:
            kivy.graphics.Color(0, 0.7, 0)
            dot_size = 20
            dot_position = (touch.pos[0] - dot_size//2, touch.pos[1] - dot_size//2)
            kivy.graphics.Ellipse(pos=dot_position, size=(dot_size, dot_size))
        print(touch, touch.button, 'mouse button')


# TODO make the app async
class MyApp(App):

    def build(self):
        Builder.load_string(KV)

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(ClientListScreen(name='clients'))
        self.screen_manager.add_widget(ImageViewScreen(name='image_view'))

        return self.screen_manager

    def open_image(self):
        self.screen_manager.current = 'image_view'


if __name__ == '__main__':
    MyApp().run()
