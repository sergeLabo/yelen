#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#######################################################################
# Copyright (C) La Labomedia January 2020
#
# This file is part of Yelen.

# Yelen is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Yelen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Yelen.  If not, see <https://www.gnu.org/licenses/>.
#######################################################################

"""
Icon icon_labo.png
Splash screen logo-1280-720.jpg
Screen Manager
Menu Bar avec icône, ..
Inspiré de
    shorturl.at/bhIZ5
    soit
    https://stackoverflow.com/questions/55482899/how-to-add-an-action-bar-in-
    kivy-using-screenmanager-widget

Excécuté sur PC avec
    KIVY_METRICS_FONTSCALE=2.5 python3 main.py
    pour simuler le dpi du tel
"""

__version__ = '0.54'

"""
0.54 10sp
"""

# De la bibliothèque standard, ne pas les ajouter dans buildozer.spec
import os, sys
import textwrap
import urllib.request
from urllib.error import HTTPError, URLError

# ajouter certifi dans les requirements de buildozer.spec
import certifi
# Here's all the magic !
os.environ['SSL_CERT_FILE'] = certifi.where()

# ajouter beautifulsoup4 et lxml dans les requirements de buildozer.spec
# BeautifulSoup utilise lxml comme parser par défaut
from bs4 import BeautifulSoup

# Pour kivy
# ajouter kivy dans les requirements de buildozer.spec
import kivy
kivy.require('1.11.1')

# Pour mon PC
if sys.platform == 'linux':
    from kivy.core.window import Window
    # Pour simuler l'écran de mon tél fait 1280*720
    k = 0.8
    WS = (int(720*k), int(1280*k))
    Window.size = WS

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock


class RecentsModifications:

    def __init__(self):

        self.url = "https://ressources.labomedia.org/modifications_recentes"

        self.recents_mdifications_page = self.download_page(self.url)

        if self.recents_mdifications_page:
            # L'attribut à appeler
            self.modifs_list = self.get_liste_modifs(self.recents_mdifications_page)
        else:
            self.modifs_list = ["urllib.request.urlopen error"]*100

    def download_page(self, url):
        """Télécharge la page à l'url."""

        page = None
        try:
            page = urllib.request.urlopen(url)
            page = page.read().decode("utf-8")
            # Ajout d'un EOF
            page += "\n"
        except HTTPError as e:
                print("HTTP Error:", e.code)
                page = None
        except URLError as e:
                print("URL Error:", e.reason)
                page = None

        return page

    def get_liste_modifs(self, page):
        """on fait la soupe, puis on cherche les lignes:
        <a class="wikilink1" href="/amipo_weekend_reboot" title="amipo_weekend_reboot">
        Weekend reboot de l'AMIPO
        </a>
        """

        soup = BeautifulSoup(page, features="lxml")
        # #print(soup.prettify())

        # Seulement les lignes avec <a class="wikilink1" ...
        aaaa = soup.find_all("a", class_="wikilink1")

        # Parcours des lignes, elles ont toutes "title",
        # pour ne garder que les lignes sans "tag"
        modifs_list = []
        for title_line in aaaa:
             if "tag:" not in title_line['title']:
                # #print("Page:", title_line.text)
                modifs_list.append(title_line.text)

        return modifs_list

class Screen2(Screen):
    # #def __init__(self, **kwargs):
        # #super().__init__(**kwargs)
    pass

class Screen1(Screen):
    # #def __init__(self, **kwargs):
        # #super().__init__(**kwargs)
    pass

class MainScreen(Screen):
    # #def __init__(self, **kwargs):
        # #super().__init__(**kwargs)
    pass

class ScreenManager(ScreenManager):
    pass

class Yelen(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        text = self.get_modifs()

        # #self.app.text = "Sans request\n"*100
        self.app.text = text

        print(self.app.text[:50])

    def get_modifs(self, *args):
        modifs = RecentsModifications().modifs_list
        print("Nombre de lignes de RecentsModifications:", len(modifs))
        text = ""
        a = 0
        for line in modifs:
            # Seulement 40 lignes, sinon le scroll bug
            if a < 40:
                line = textwrap.fill(line, 25)
                text += line + "\n\n"
                a += 1
            else:
                break
        # print(len(text)) 1659
        return text

class YelenApp(App):
    """Cet objet est app dans le kv"""

    text = StringProperty("Mon Texte Mon Texte Mon Texte Mon Texte Mon Texte Mon Texte \n"*100)

    def build(self):
        # Le self permet d'accéder dans Yelen à app dans le kv !
        return Yelen(self)

    def build_config(self, config):

        config.setdefaults('kivy',
                            { 'log_level': 'debug',
                              'log_name': 'yelen_%y-%m-%d_%_.txt',
                              'log_dir': '/sdcard',
                              'log_enable': '1'})

        config.setdefaults('postproc',
                            { 'double_tap_time': 250,
                              'double_tap_distance': 20})


if __name__ == '__main__':
    YelenApp().run()
