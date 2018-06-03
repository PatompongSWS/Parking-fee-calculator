import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.core.window import Window
from dateutil import parser
import datetime

# json databases
storeTime = JsonStore('TimeParking.json')
storeStat = JsonStore('Statistics.json')


# Load file screen
Builder.load_file('Parking.kv')

# Declare both screens
class HomeScreen(Screen):

   def onFocus(self, dt):
      self.ids.entry.focus = True
   
   def resetTextInput(self, dt):
      self.ids.entry.text = ""

   def FocusTextInput(self):
      # call onFocus() in 0.2s
      Clock.schedule_once(self.onFocus, 0.2)

   def removeText(self):
      if self.ids.entry.text != "":
         
         # cut last character
         self.ids.entry.text = (self.ids.entry.text)[:-1]
         
      self.FocusTextInput()

   def enterText(self):
      if self.ids.entry.text != "":

         now = datetime.datetime.now()
         
         # if found document to calculate the money
         if storeTime.exists(self.ids.entry.text):
            
            past = parser.parse(storeTime[self.ids.entry.text]['time'])
            
            # subtrac time and convert to hour unit
            hours = int(self.subtracTime(now , past))

            # calculate money
            money = self.calculateMoney(hours)

            # change format date
            date = '{:%d/%m/%Y}'.format(now)
            
            # keep start time to index and store document
            storeStat[storeTime[self.ids.entry.text]['time']] = {
               'end': str(now),'hours': hours,'money': money, 'date': str(date)
            }
            
            # delete current document
            storeTime.delete(self.ids.entry.text)
            print "calculate Fee"

            # show parking time and Fee
            self.ids.entry.text = "Parking Time: " + str(hours) + "   Fee: " + str(money)

            # reset text input in 2s
            Clock.schedule_once(self.resetTextInput, 2)

         else:

            # insert new document
            storeTime[str(self.ids.entry.text)] = {'time': str(now)}
            print "insert barcode"

            # show insert status
            self.ids.entry.text = "The Barcode Inserted"

            # reset text input in 2s
            Clock.schedule_once(self.resetTextInput, 2)
            
      self.FocusTextInput()
   
   def subtracTime(self, now, past):

      # subtrac time and convert to hour unit
      return (now - past).total_seconds()//3600

   def calculateMoney(self, hours):
      if hours <= 1:
         return 0
      elif hours <= 3:
         return (hours - 1) * 20
      else:
         return 40 + ((hours - 3) * 25)
   
class AmountOfCarScreen(Screen):
   
   def getAmountOfCar(self):
      
      now = '{:%d/%m/%Y}'.format(datetime.datetime.now())
      
      # count car
      count = 0
      for key in storeStat:
         # compare date
         if storeStat[key]['date'] == str(now):
            count = count + 1

      # display amount of car
      self.ids.amountOfCar.text = "Amount of Car: " + str(count)

class AmountOfMoneyScreen(Screen):

   def getMoney(self):
      
      now = '{:%d/%m/%Y}'.format(datetime.datetime.now())

      # sum money
      totalMoney = 0
      for key in storeStat:
         print storeStat[key]['date']
         # compare date
         if storeStat[key]['date'] == now:
            totalMoney = totalMoney + storeStat[key]['money']
      
      # display money
      self.ids.totalMoney.text = "Total: " + str(totalMoney)

# Create the screen manager
sm = ScreenManager()
sm.add_widget(HomeScreen(name='Home'))
sm.add_widget(AmountOfCarScreen(name='AmountOfCar'))
sm.add_widget(AmountOfMoneyScreen(name='AmountOfMoney'))

class ParkingApp(App):

   def build(self):
      return sm


if __name__ == '__main__':
    ParkingApp().run()
