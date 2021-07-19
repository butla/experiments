import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.label import Label

KV = '''
FloatLayout:
    BoxLayout:
        size_hint: .5, .5
        pos_hint: {'center': (.5, .5)}

        orientation: 'vertical'

        TextInput:
            text: app.text
            on_text: app.text = self.text
            id: input_box

        Slider:
            min: 0
            max: 100
            value: app.number
            on_value: app.number = self.value

        Button:
            text: 'Jakiś guzik żółć A'
            canvas:
                Color:
                    rgba: 1, .3, .8, .5
                Line:
                    points: [(15, 30), (300, 150)]

        Button:
            text: input_box.text
'''

# TODO make the app async
class MyApp(App):
    number = NumericProperty()
    text = StringProperty()

    def build(self):
        return Builder.load_string(KV)



# TODO load the kv file and try changing some widget's canvas
# MyWidget:
#     canvas:
#         Color:
#             rgba: 1, .3, .8, .5
#         Line:
#             points: zip(self.data.x, self.data.y)
if __name__ == '__main__':
    MyApp().run()
