import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
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

            BoxLayout:
                orientation: 'horizontal'

                Label:
                    size_hint: 0.25, None
                    text: 'Mejer'

                Label:
                    size_hint: 0.25, None
                    text: 'Zdzichu'

                Label:
                    size_hint: 0.25, None
                    text: '173'

                Button:
                    size_hint: 0.25, None
                    text: 'otwórz'
                    on_press: app.open_image()

            BoxLayout:
                orientation: 'horizontal'

                Label:
                    size_hint: 0.25, None
                    text: 'Ptok'

                Label:
                    size_hint: 0.25, None
                    text: 'Kacper'

                Label:
                    size_hint: 0.25, None
                    text: '180'

                Button:
                    size_hint: 0.25, None
                    text: 'otwórz'
                    on_press: app.open_image()

            BoxLayout:
                orientation: 'horizontal'

                Label:
                    size_hint: 0.25, None
                    text: 'Ufnal'

                Label:
                    size_hint: 0.25, None
                    text: 'Melania'

                Label:
                    size_hint: 0.25, None
                    text: '169'

                Button:
                    size_hint: 0.25, None
                    text: 'otwórz'
                    on_press: app.open_image()

            BoxLayout:
                orientation: 'horizontal'

                Label:
                    size_hint: 0.25, None
                    text: 'Cyroń'

                Label:
                    size_hint: 0.25, None
                    text: 'Marcin'

                Label:
                    size_hint: 0.25, None
                    text: '183'

                Button:
                    size_hint: 0.25, None
                    text: 'otwórz'
                    on_press: app.open_image()

<ImageViewScreen>:
    Button:
        text: 'Go back'
        on_press: root.manager.current = 'clients'
'''


# TODO can I reference objects in the layout directly from the app object?
class ClientListScreen(Screen):
    # TODO fill that table_box from sqlite. Might have to be made into a recycle view
    table_box = ObjectProperty()


class ImageViewScreen(Screen):
    # TODO fill that table_box from sqlite. Might have to be made into a recycle view
    table_box = ObjectProperty()


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
