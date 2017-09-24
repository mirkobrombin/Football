#!/usr/bin/env python
'''
   Copyright 2017 Mirko Brombin (brombinmirko@gmail.com)

   This file is part of Football.

    Football is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Football is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Football.  If not, see <http://www.gnu.org/licenses/>.
'''

import gi
import sys
import json
import requests
gi.require_version('Granite', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Granite, Gtk, Gdk

API_KEY = "cb3a6fe9d9284af79a13661ff6191ea6"
headers = {'X-Auth-Token':API_KEY, 'X-Response-Control': 'minified'}

class Football(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Football")
        
        self.header_bar()

        #grid
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.gen_competitions()
        self.gen_fixtures("446")

        #setting up the layout
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)

        #paned
        self.paned = Gtk.Paned()
        self.paned.add1(self.grid)
        self.add(self.paned)
        
        #hbox
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.add(self.competitions_combo)
        self.hbar.pack_start(self.hbox)

    def header_bar(self):
        self.hbar = Gtk.HeaderBar()
        self.hbar.set_show_close_button(True)
        self.hbar.props.title = "Football"
        self.set_titlebar(self.hbar)
        Gtk.StyleContext.add_class(self.hbar.get_style_context(), "FootballHeader")

    def gen_competitions(self):
        #competition json
        competitions = requests.get("http://api.football-data.org/v1/competitions",headers=headers)
        competitions_obj = json.loads(competitions.text)
        competitions_list = []
        for c in competitions_obj:
            try:
                competitions_list.append((c['id'], c['caption']))
            except(KeyError):
                print("Error for JSON: " + str(f))

        #competition selector
        self.competitions_liststore = Gtk.ListStore(int, str)
        for competition in competitions_list:
            self.competitions_liststore.append(list(competition))

        self.competitions_combo = Gtk.ComboBox.new_with_model_and_entry(self.competitions_liststore)
        self.competitions_combo.connect("changed", self.on_competitions_combo_changed)
        self.competitions_combo.set_entry_text_column(1)

    def gen_fixtures(self, competition_id, update=False):
         #fixtures json
        self.fixtures = requests.get(
            "http://api.football-data.org/v1/competitions/" + str(competition_id) + "/fixtures",headers=headers
        )
        self.fixtures_obj = json.loads(self.fixtures.text)
        print("N of fixtures: " + str(self.fixtures_obj['count']))
        self.fixtures_list = []
        for f in self.fixtures_obj['fixtures']:
            try:
                self.fixtures_list.append((
                    f['homeTeamName'], 
                    str(f['result']['goalsHomeTeam'])+" - "+str(f['result']['goalsAwayTeam']), 
                    f['awayTeamName'], f['date'], f['status']))
            except(KeyError):
                print("Error for JSON: " + str(f))

        #fixtures selector
        if update == False:
            self.fixtures_liststore = Gtk.ListStore(str, str, str, str, str)
        else:
            self.fixtures_liststore.clear()
        for fixtures in self.fixtures_list:
            self.fixtures_liststore.append(list(fixtures))
        self.fixtures_filter = self.fixtures_liststore.filter_new()
        self.treeview = Gtk.TreeView.new_with_model(self.fixtures_filter)
        for i, column_title in enumerate(["Home team", "Results", "Away team", "Date", "Status"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
    
    def on_competitions_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            self.gen_fixtures(row_id, True)
            print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())

win = Football()
win.set_default_size(820, 600) 
win.connect("delete-event", Gtk.main_quit)
'''style_provider = Gtk.CssProvider()
style_provider.load_from_path("./style.css")
 
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)'''
win.show_all()
Gtk.main()
