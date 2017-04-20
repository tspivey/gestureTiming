import globalPluginHandler
import speech
import ui
import time
import addonHandler

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	scriptCategory = _("Gesture Timing")

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.patched = False
		self.old_speak = None
		self.last_gesture_time = 0

	def script_toggleGestureTiming(self, gesture):
		synth = speech.getSynth()
		if self.patched:
			synth.speak = self.old_speak
			self.patched = False
			ui.message("gesture timing off")
			self.last_gesture_time = 0
		else:
			ui.message("gesture timing on")
			self.old_speak = synth.speak
			synth.speak = self.speak
			self.patched = True
	script_toggleGestureTiming.__doc__ = _("Time the difference between gestures and speech.")

	def getScript(self, gesture):
		if not self.patched:
			return globalPluginHandler.GlobalPlugin.getScript(self, gesture)
		res = globalPluginHandler.GlobalPlugin.getScript(self, gesture)
		self.last_gesture_time = time.time()
		return res

	def speak(self, speechSequence):
		if self.last_gesture_time == 0:
			return self.old_speak(speechSequence)
		t = time.time()-self.last_gesture_time
		t *= 1000.0
		t = u"%d ms " % int(t)
		speechSequence.insert(0, t)
		self.last_gesture_time = 0
		return self.old_speak(speechSequence)

	__gestures = {
		"kb:nvda+shift+f12": "toggleGestureTiming",
	}
