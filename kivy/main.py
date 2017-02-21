from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


Config.set('graphics', 'width', '250')
Config.set('graphics', 'height', '300')

Builder.load_string('''
<TextInverter>:
    input_widget: input_widget
    text_widget: text_widget

    orientation: 'vertical'
    padding: 20

    TextInput:
        id: input_widget
        text: 'Write here...'
    Label:
        id: text_widget
        text: 'Bla, bla'
    Button:
        text: 'Invert text'
        on_press: root.invert_text()
        size_hint_y: .5
''')


class TextInverter(BoxLayout):
    input_widget = ObjectProperty(None)
    text_widget = ObjectProperty(None)

    def invert_text(self):
        self.text_widget.text = self.input_widget.text[::-1]


class TextInverterApp(App):
    def build(self):
        return TextInverter()


if __name__ == '__main__':
    TextInverterApp().run()
