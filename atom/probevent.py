
class AperiodicBooleanState:
	def __init__(self, true_timeconst=None, false_timeconst=None, trigger=0, initstate=0):
		self.state = initstate >= 0.5
		self.val = initstate
		self.trigger = trigger
		self.on_change = None
		self.true_timeconst = true_timeconst
		self.false_timeconst = false_timeconst

	def set_on_change_handle(self, cbl):
		self.on_change = cbl

	def serve(self, curstate, deltatime):
		timeconst = self.true_timeconst if curstate else self.false_timeconst 
		curval = 1 if curstate else 0
		if timeconst is None:
			self.val = curval
		else:
			self.val += (deltatime / timeconst) * (curval - self.val)

		if (self.state is False and self.val > 0.5 + self.trigger):
			self.state = True
			if self.on_change: 
				self.on_change(self.state)

		elif (self.state is True and self.val < 0.5 - self.trigger):
			self.state = False
			if self.on_change: 
				self.on_change(self.state)

	def __str__(self):
		return str(self.val)