#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin (send@mirko.pm)

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

import gi, sys, json, requests, logging
from datetime import datetime, timedelta
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# TODO: provide user setting to input personal APY key
API_KEY = "cb3a6fe9d9284af79a13661ff6191ea6"
headers = {'X-Auth-Token':API_KEY, 'X-Response-Control': 'minified'}

stylesheet = """
    @define-color colorPrimary #249C5F;
    @define-color textColorPrimary #f2f2f2;
    @define-color textColorPrimaryShadow #197949;
""";

class FootballDialog(Gtk.Dialog):

    def __init__(self, parent, message_log):
        Gtk.Dialog.__init__(self, "Warning", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 300)

        dialog_label = Gtk.Label()
        dialog_label.set_markup(
            "Something went wrong.\n"+
            "You can report what happened by creating a <a href='https://github.com/mirkobrombin/Football/issues/new'>new Issue</a>.\n"+
             "Attach the log below."
         )

        message_scroll = Gtk.ScrolledWindow()
        message_scroll.set_hexpand(True),message_scroll.set_vexpand(True)
        
        message_view = Gtk.TextView()
        message_buffer = message_view.get_buffer()
        message_buffer.set_text(message_log)
        message_scroll.add(message_view)
        
        content = self.get_content_area()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_border_width(20)
        box.add(dialog_label), box.add(message_scroll)
        
        content.add(box)
        self.show_all()

class Football(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Football")

        # set default variables values
        self.show_latest = False
        self.competition_id = 0

        # call methods
        self.header_bar()
        self.gen_competitions()
        self.gen_fixtures()
        
        # prepare box with scrollable treelist
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.add(self.treeview)
        self.box.add(self.scrollable_treelist)
        self.add(self.box)

        # lastest matches
        self.button_latest = Gtk.Button.new_from_icon_name("document-open-recent", Gtk.IconSize.LARGE_TOOLBAR)
        self.button_latest.set_property("tooltip-text", "Last 7 days")
        self.button_latest.connect("clicked", self.on_button_latest_clicked)
        self.hbar.pack_end(self.button_latest)

    def header_bar(self):
        self.hbar = Gtk.HeaderBar()
        self.hbar.set_show_close_button(True)
        self.hbar.props.title = "Football"
        self.set_titlebar(self.hbar)
        Gtk.StyleContext.add_class(self.hbar.get_style_context(), "FootballHeader")

    def gen_competitions(self):
        # get competitions JSON from API
        competitions = requests.get("http://api.football-data.org/v2/competitions",headers=headers)
        competitions_obj = json.loads(competitions.text)
        competitions_list = []
        
        # if competitions key not found, then probably reached the API limits
        try:
            self.competition_id = competitions_obj["competitions"][0]['area']['id']
        except(KeyError):
            dialog = FootballDialog(self, "API limits reached.")
            dialog.run()
            dialog.destroy()
            
        for c in competitions_obj["competitions"]:
            # TODO: provide user settings to set personal API key tier
            if c['plan'] == "TIER_ONE":
                competitions_list.append((c['id'], c['name']))
        
        # competitions selector
        self.competitions_liststore = Gtk.ListStore(int, str)
        for competition in competitions_list:
            self.competitions_liststore.append(list(competition))

        self.competitions_combo = Gtk.ComboBox.new_with_model_and_entry(self.competitions_liststore)
        self.competitions_combo.connect("changed", self.on_competitions_combo_changed)
        self.competitions_combo.set_entry_text_column(1)
        
        self.hbar.pack_start(self.competitions_combo)

    def gen_fixtures(self, competition_id=False, update=False):
        if competition_id != False:
            self.competition_id = competition_id
        
         # get fixtures JSON from API
        self.fixtures = requests.get(
            "http://api.football-data.org/v2/competitions/" + str(self.competition_id) + "/matches",headers=headers
        )
        self.fixtures_obj = json.loads(self.fixtures.text)
        self.fixtures_list = []
        
        # if requested scope not provide a matches key, then probably the API key do not have necessary permissions
        # TODO: if user defined a personal API key from user settings, then pop-up an alert with API restrictions
        try:
            for f in self.fixtures_obj['matches']:
                match_date = datetime.strptime(f['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
                match_results = str(f['score']['fullTime']['homeTeam'])+" - "+str(f['score']['fullTime']['awayTeam'])
                
                if f['status'] == "FINISHED":
                    match_status = "Finished"
                elif f['status'] == "TIMED":
                    match_status = "Timed"
                elif f['status'] == "SCHEDULED":
                    match_status = "Scheduled"
                
                self.fixtures_list.append((
                    f['homeTeam']['name'], 
                    f['matchday'],
                    match_results, 
                    f['awayTeam']['name'], match_status, match_date.strftime('%Y %B %d %H:%M')))
        except:
            dialog = FootballDialog(self, "This is not a mistake.\nPlease do not open an issue.\nThese are limits imposed by the API provider.")
            dialog.run(), dialog.destroy()

        # fixtures selector
        if update == False:
            self.fixtures_liststore = Gtk.ListStore(str, int, str, str, str, str)
            
            # create new filter for latest matches
            self.latest_filter = self.fixtures_liststore.filter_new()
            self.latest_filter.set_visible_func(self.set_latest_filter)
        else:
            self.fixtures_liststore.clear()
        
        for fixtures in self.fixtures_list:
            self.fixtures_liststore.append(list(fixtures))
        
        self.fixtures_sorted = Gtk.TreeModelSort(model=self.fixtures_liststore)
        self.fixtures_sorted.set_sort_column_id(1, Gtk.SortType.ASCENDING)
        self.treeview = Gtk.TreeView.new_with_model(self.latest_filter)
        
        for i, column_title in enumerate(["Home team", "Day", "Score", "Away team", "Status", "Date"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_reorderable(True)
            column.set_resizable(True)
            column.set_sort_column_id(i)
            self.treeview.append_column(column)
    
    def on_competitions_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            self.gen_fixtures(row_id, True)
        else:
            entry = combo.get_child()

    def set_latest_filter(self, model, iter, data):
        if self.show_latest == True:
            today = datetime.now()
            latest = today - timedelta(days=7) # Last 7 days
            col_date = datetime.strptime(model[iter][5], '%Y %B %d %H:%M')
            return col_date <= today and col_date >= latest
        return True

    def on_button_latest_clicked(self, widget):
        if self.show_latest == True:
            self.show_latest = False
            self.button_latest.set_property("tooltip-text", "Last 7 days")
        else:
            self.show_latest = True
            self.button_latest.set_property("tooltip-text", "Show all days")
        self.latest_filter.refilter()

style_provider = Gtk.CssProvider()
style_provider.load_from_data(bytes(stylesheet.encode()))
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
win = Football()
win.set_default_size(800, 600) 
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
