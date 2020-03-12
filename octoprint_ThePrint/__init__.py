# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class ThePrintPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.SettingsPlugin, octoprint.plugin.EventHandlerPlugin):

	def on_after_startup(self):
		self._logger.info("Pin of the light: %s" % self._settings.get(["pinLight"]))
		self._logger.info("Pin of the fan: %s" % self._settings.get(["pinFan"]))

	def get_settings_defaults(self):
		return dict(pinLight=4, pinFan=17)

	def get_template_vars(self):
		return dict(pinLight=self._settings.get(["pinLight"]), pinFan=self._settings.get(["pinFan"]))

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def on_event(self, event, payload):
		if event == "Connected":
			self._logger.info("Event '" + event + "' wurde ausgeloest")
			# Lampe an
			relais_light_gpio = int(self._settings.get(["pinLight"]))
			GPIO.setup(relais_light_gpio, GPIO.OUT)  # GPIO Modus zuweisen
			GPIO.output(relais_light_gpio, GPIO.HIGH)  # an
		elif event == "Disconnected":
			self._logger.info("Event '" + event + "' wurde ausgeloest")
			# Lampe aus
			relais_light_gpio = int(self._settings.get(["pinLight"]))
			GPIO.setup(relais_light_gpio, GPIO.OUT)  # GPIO Modus zuweisen
			GPIO.output(relais_light_gpio, GPIO.LOW)  # aus
		elif event == "PrintStarted" or event == "PrintResumed":
			self._logger.info("Event '" + event + "' wurde ausgeloest")
			# Bei Start Lüfter
			relais_fan_gpio = int(self._settings.get(["pinFan"]))
			GPIO.setup(relais_fan_gpio, GPIO.OUT)  # GPIO Modus zuweisen
			GPIO.output(relais_fan_gpio, GPIO.HIGH)  # an
		elif event == "PrintFailed" or event == "PrintCancelled" or event == "PrintPaused":
			self._logger.info("Event '" + event + "' wurde ausgeloest")
			# Lüfter aus
			relais_fan_gpio = int(self._settings.get(["pinFan"]))
			GPIO.setup(relais_fan_gpio, GPIO.OUT)  # GPIO Modus zuweisen
			GPIO.output(relais_fan_gpio, GPIO.LOW)  # aus

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
