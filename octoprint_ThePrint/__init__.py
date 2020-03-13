# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import os


class ThePrintPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.EventHandlerPlugin):

	def on_after_startup(self):
		self._logger.info("Pin of the light: 4")
		self._logger.info("Pin of the fan: 14")

	def on_event(self, event, payload):
		if event == "Connected":
			self._logger.info("Event '" + event + "' wurde ausgeloest")
			# Lampe an
			os.system("gpio -g mode 4 out")
		elif event == "Disconnected":
			self._logger.info("Event '" + event + "' wurde ausgeloest")
			# Lampe aus
			os.system("gpio -g mode 4 in")
		elif event == "PrintStarted" or event == "PrintResumed":
			self._logger.info("Event '" + event + "' wurde ausgeloest")
			# Bei Start Lüfter
			os.system("gpio -g mode 14 out")
		elif event == "PrintFailed" or event == "PrintCancelled" or event == "PrintPaused":
			self._logger.info("Event '" + event + "' wurde ausgeloest")
			# Lüfter aus
			os.system("gpio -g mode 14 in")

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			ThePrint=dict(
				displayName="ThePrint Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="KommissarKevin",
				repo="OctoPrint-ThePrint",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/KommissarKevin/OctoPrint-ThePrint/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "ThePrint"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = ThePrintPlugin()


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ThePrintPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
