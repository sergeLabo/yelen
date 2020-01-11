#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class WelcomeScreen(Screen):
    pass


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass


class ScreenManager(ScreenManager):
    pass


class CrimePrevention(BoxLayout):
    pass


class Actionbar_screenmanagerApp(App):
    title = 'Kivy ScreenManager & ActionBar Demo'

    def build(self):
        return CrimePrevention()


if __name__ == '__main__':
    Actionbar_screenmanagerApp().run()
