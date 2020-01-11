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

__version__ = '0.70'

"""
0.70 avec size en option
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


class RecentChanges:

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
    pass

class Screen1(Screen):
    pass

class MainScreen(Screen):
    pass

class ScreenManager(ScreenManager):
    pass

class Yelen(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        # Récup sur le wiki des modifications récentes
        self.modifs = RecentChanges().modifs_list
        # ou
        # #modifs = ["Veni vedi vici, alea jacta est, Factum fieri infectum non potest. Julius Caesar "]*100
        print("Nombre de lignes de RecentChanges:", len(self.modifs))

        # text et font_size sont définis dans le kv comme attributs de app
        # il faut définir:
        #     self.app.text et self.app.font_size_sp
        self.font_size = int(self.app.config["font"]["font_size"])
        self.font_size_sp = str(self.font_size) + "sp"
        self.app.text = ""

        self.format_text()

    def format_text(self):
        """Recalcule self.font_size et self.font_size_sp,
        redéfinit self.app.text, self.app.font_size, self.app.font_size_sp
        """
        self.font_size = int(self.app.config["font"]["font_size"])
        self.font_size_sp = str(self.font_size) + "sp"

        chars_nb, maxi = self.get_chars_nb_maxi()

        text = ""
        a = 0
        for line in self.modifs:
            if a < maxi:
                line = textwrap.fill(line, chars_nb)
                text += line + "\n\n"
                a += 1
            else:
                break

        self.app.font_size = self.font_size
        self.app.font_size_sp = self.font_size_sp
        self.app.text = text

    def get_chars_nb_maxi(self):
        """Droite avec coeff a, b
        chars_nb
            si 10 --> 60
            si 40 --> 15
            a= -0.67 b= 46.7
        maxi
            20 pour 40
            80 pour 10
            a= -2 b= 100
        """

        chars_nb = 75 - 1.5*self.font_size
        chars_nb = int(chars_nb)
        print("Nombre de caractères par ligne:", chars_nb)

        maxi = 100 - 2*self.font_size
        print("Nombre de lignes maxi:", maxi)

        return chars_nb, maxi


class YelenApp(App):
    """Cet objet est app dans le kv"""

    text = StringProperty("toto\n"*100)
    font_size_sp = StringProperty("10sp")

    def build(self):
        # Le self permet d'accéder dans Yelen à app dans le kv !

        return Yelen(self)

    def on_start(self):

        self.root.format_text()

    def build_config(self, config):
        print("build_config")
        config.setdefaults("font", {"font_size": 20, "unit": "sp" })

    def build_settings(self, settings):
        print("build_settings")
        data = '''[ { "type": "title", "title":"Taille des textes"},

                    { "type": "numeric",
                      "title": "Taille des textes",
                      "desc": "De 10 à 40",
                      "section": "font",
                      "key": "font_size"},

                    { "type": "string",
                      "title": "Taille de la police en:",
                      "desc": "sp ou dp",
                      "section": "font",
                      "key": "unit"}
                      ]'''
        settings.add_json_panel('Configuration de Yelen', self.config, data=data)

    def on_config_change(self, config, section, key, value):
        """Faire des
        print(dir(self)) puis print(dir(self.toto)) avec des 'toto' astucieux
        pour trouver: self.root.format_text()
        """

        if config is self.config:  # du joli python rigoureux
            token = (section, key)

            # Font size
            if token == ('font', 'font_size'):
                value = int(value)
                if value < 0: value = 0
                if value > 40: value = 40
                print("Nouvelle taille de police:", value)
                self.root.format_text()


if __name__ == '__main__':
    YelenApp().run()


        # ## Actualisation toutes les secondes
        # #self.event = Clock.schedule_interval(self.update, 1)

    # #def update(self, dt):
        # #self.app.text = self.get_modifs()
        # #self.get_font_size()
        # #print(self.font_size_sp)
        # #self.app.font_size_sp = self.font_size_sp
