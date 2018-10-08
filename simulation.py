import random, sys
random.seed(42)
from person import Person
from virus import Virus
from logger import Logger

class Simulation(object):
	
	def __init__(self, population_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num, initial_infected=1):
		self.population_size = (population_size)
		self.population = []
		self.next_id = 0
		self.vacc_percentage = (vacc_percentage)
		self.total_infected = (initial_infected)
		self.total_dead = 0
		self.current_infected = (initial_infected)
		self.virus_name = virus_name
		self.mortality_rate = (mortality_rate)
		self.repro_num = basic_repro_num
		self.newly_infected = []
		self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(virus_name, population_size, vacc_percentage, initial_infected)
		self.virus = Virus(self.virus_name, self.mortality_rate, self.repro_num)
		self.create_population(initial_infected, self.virus)
		self.logger = Logger(self.file_name)
		self.logger.write_metadata(self.population_size, self.vacc_percentage, self.virus_name, self.mortality_rate, self.repro_num)

	def create_population(self, initial_infected, virus):
		i = 0
		while i <  initial_infected:
			self.population.append(Person(False, self.next_id, self.virus))
			i += 1
			self.next_id += 1
		while i < self.population_size:
			vacc = random.uniform(0, 1)
			if vacc < self.vacc_percentage:
				self.population.append(Person(True, self.next_id))
			else:
				self.population.append(Person(False, self.next_id))
			i += 1
			self.next_id += 1
		print(len(self.population))

	def _simulation_should_continue(self):
		if self.total_dead > self.population_size - 1:
			return False
		for i in self.population:
			if i.infected != None:
				return True
		return False

	def run(self):
		should_continue = self._simulation_should_continue()
		time_step_counter = 0
		while should_continue == True:
			self.time_step()
			time_step_counter += 1
			should_continue = self._simulation_should_continue()
		for stuff in self.population:
			print(stuff.is_alive, stuff.infected)
		print('The simulation has ended after {} turns.'.format(time_step_counter))
		self.logger.log_ending_stats(self.total_dead, time_step_counter)

	def time_step(self):
		for person in self.population:
			if person.infected != None and person.is_alive == True:
				interactions = 0
				while interactions < 99:
					random_p = self.population[random.randint(0, len(self.population)) - 1]
					if random_p.is_alive == True and random_p._id != person._id:
						self.interaction(person, random_p)
						interactions += 1
		self.death()
		#print("stuff")
		self._infect_newly_infected()

	def interaction(self, person, random_person):
		assert person.is_alive == True
		assert random_person.is_alive == True
		infect = float(random.uniform(0, 1))
		print(infect, self.repro_num)
		if infect < self.repro_num and random_person.is_vaccinated == False and random_person.infected == None:
			self.newly_infected.append(random_person._id)
			self.logger.log_interaction(person, random_person, True, random_person.is_vaccinated)
		else:
			self.logger.log_interaction(person, random_person, False, random_person.is_vaccinated)

	def _infect_newly_infected(self):
		if len(self.newly_infected) > 0:
			for _id in self.newly_infected:
				for person in self.population:
					if _id == person._id:
						person.infected = self.virus
		self.newly_infected = []

	def death(self):
		for person in self.population:
			if person.infected != None and person.is_alive == True:
				if person.did_survive_infection() == True:
					self.logger.log_infection_survival(person, False)
				else:
					self.total_dead += 1
					self.logger.log_infection_survival(person, True)

if __name__ == "__main__":
	params = sys.argv[1:]
	pop_size = int(params[0])
	vacc_percentage = float(params[1])
	virus_name = str(params[2])
	mortality_rate = float(params[3])
	basic_repro_num = float(params[4])
	if len(params) == 6:
		initial_infected = int(params[5])
	else:
		initial_infected = 1
	simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num, initial_infected)
	simulation.run()
			
