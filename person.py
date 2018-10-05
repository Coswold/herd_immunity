import random
from virus import Virus

class Person(object):
	def __init__(self, is_vaccinated = None, _id = None, infected = None):
		self._id = _id
		self.is_vaccinated = is_vaccinated
		self.is_alive = True
		self.infected = infected

	def did_survive_infection(self):
		survive = random.uniform(0,1)

		if survive < self.infected.mortality_rate:
			self.is_alive = False
			self.infected = None
			return False

		else:
			self.is_vaccinated = True
			self.infected = None
			return True

def test_create_person():
	person = Person()
	assert person.is_vaccinated is None
	assert person.is_alive is True
	assert person.infected is None

def test_infection():
	ebola = Virus("ebola", 0.8, 0.25)
	person = Person(False, ebola)
	if person.did_survive_infection is False:
		assert person.is_alive is False
	elif person.did_survive_infection is True:
		assert person.is_vaccinated is True
		assert person.infected is None
	
