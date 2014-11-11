from gettext import gettext

import sys
sys.path.append("C:/Python27/Lib/site-packages/")
from gi.repository import Gtk
import pygame

import sugar3.activity.activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton

sys.path.append('..')	#Import sugargame package from top-level directory
import sugargame.canvas

import matter

class MatterActivity(sugar3.activity.activity.Activity):
	#Initializes the activity
	def __init__(self, handle):
		super(matteractivity, self).__init__(handle)

		self.paused = False

		#Setup activity stuff
		self.build_toolar()
		self._pygamecanvas = sugargame.canvas.PygameCanvas(self)

		#Note that set_canvas implicitly calls read_file when resuming from journal
		self.set_canvas(self._pygamecanvas)
		self._pygamecanvas.grab_focus()

		#Create instance of game
		self.game = MatterGame.MatterGame()

		#self.game.run is called whtn the activity constructor returns
		self._pygamecanvas.run_pygame(self.game.run)


	#Sets upthe sugar activity toolbar
	def build_toolbar(self):
		toolbar_box = ToolbarBox()
		self.set_toolbar_box(toolbar_box)
		toolbar_box.show()
		
		activity_button = ActivityToolbarButton(self)
		toolbar_box.toolbar.insert(activity_button, -1)
		activity_button.show()

		#Play/Pause button
		stop_play = ToolButton('media-playback-stop')
		stop_play.set_tooltip(gettext("Stop"))
		stop_play.set_accelerator(gettext('<ctrl>space'))
		stop_play.connect('clicked', self._stop_play_cb)
		
		toolbar_box.toolbar.insert(stop_play, -1)
		stop_play.show()

		#Separator
		separator = Gtk.SeparatorToolItem()
		separator.props.draw = False
		separator.set_expand(True)
		
		toolbar_box.toolbar.insert(separator, -1)
		separator.show()

		#Stop button
		stop_button = StopButton(self)
		toolbar_box.toolbar.insert(stop_button, -1)
		stop_button.show()

	#Pauses or unpauses the activity
	def _stop_play_cb(self, button):
		self.paused = not self.paused
		self.game.paused = self.paused

		#Update button to show next action
		if(self.paused):
			button.set_icon('media-playback-start')
			button.set_tooltip(gettext("Start"))
		else:
			button.set_icon('media-playback-stop')
			button.set_tooltip(gettext("Stop"))

	def read_file(self, file_path):
		self.game.read_file(file_path)
	
	def write_file(self, file_path):
		self.game.write_file(file_path)
