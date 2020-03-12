# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin


class ThePrintPlugin(octoprint.plugin.StartupPlugin):
    def on_after_startup(self):
        self._logger.info("Hello World!")

		##~~ Softwareupdate hook

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
__plugin_version__ = "1.0.0"
__plugin_description__ = "A quick \"Hello World\" example plugin for OctoPrint"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = ThePrintPlugin()

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ThePrintPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}



