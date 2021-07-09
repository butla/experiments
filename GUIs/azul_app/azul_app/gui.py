# I don't like the "import *" in the example in the docs
import azul

css = """
    .__azul-native-label { font-size: 50px; }
"""

class DataModel:
    def __init__(self, counter):
        self.counter = counter

# model -> view
def my_layout_func(data, info):
    label = azul.Label("{}".format(data.counter))
    button = azul.Button("Update counter")
    button.set_on_click(data, my_on_click)

    dom = azul.Dom.body()
    dom.add_child(label.dom())
    dom.add_child(button.dom())

    return dom.style(azul.Css.from_string(css))

# model <- view
def my_on_click(data, info):
    data.counter += 1;

    # tell azul to call the my_layout_func again
    return azul.Update.RefreshDom


def main():
    model = DataModel(5)
    app = azul.App(model, azul.AppConfig(azul.LayoutSolver.Default))
    app.run(azul.WindowCreateOptions(my_layout_func))

# if name makes it nicer
if __name__ == '__main__':
    main()
