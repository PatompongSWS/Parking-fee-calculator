import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.button import Label, Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder

# Load file screen
#Builder.load_file('Calculator.kv')

class CalcGridLayout(GridLayout):

    def calculate(self, calculation):
        if calculation:
            try:
                self.display.text = str(eval(calculation))
            except Exception:
                self.display.text = "Error"

class CalculatorApp(App):

    def build(self):
        return CalcGridLayout()

Calculator = CalculatorApp()
Calculator.run()
