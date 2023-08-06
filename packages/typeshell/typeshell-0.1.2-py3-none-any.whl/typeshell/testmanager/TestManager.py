from os import system
from random import sample
from time import perf_counter
from typeshell.testmanager import prompts
import pytyper

class TestManager:
	def __init__(self):
		self.prompts = {'proverbs':prompts.PROVERBS,
						'shakespeare':prompts.SHAKESPEARE}
		self.stats = []
		self.averages = {}

	def generate_prompts(self, count, prompt_type):
		if prompt_type not in list(self.prompts.keys()):
			raise(KeyError(f'Invalid prompt name: {prompt_type}'))

		prompt_count = len(self.prompts[prompt_type])
		if count > prompt_count:
			raise(ValueError(f'Specified {count} prompts, but only {prompt_count} exist.'))
		if count < 1:
			raise(ValueError(f'Specified {count} out of range.'))
		prompt_pool = self.prompts[prompt_type]
		return sample(prompt_pool, count)

	def begin_test(self, count, prompt_type):
		prompts = self.generate_prompts(count, prompt_type)
		session_data = []
		for prompt in prompts:
			seconds, user_input = self.prompt_input(prompt)
			"""
			Using TestData (pytyper) to store data for each typing test.
			"""
			td = pytyper.TestData(prompt, user_input, seconds)
			session_data.append(td)
		"""
		Using SessionData (pytyper) to store necessary data for typing session
		"""
		session = pytyper.SessionData(tests=session_data)
		self.averages = session.averages
		for test in session.get_tests():
			self.stats.append(test.alphastats)

	def prompt_input(self, prompt):
		system('clear')
		print(prompt)
		start = perf_counter()
		user_input = input()
		finish = perf_counter()
		return finish-start, user_input
