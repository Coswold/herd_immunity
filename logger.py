class Logger(object):
	def __init__(self, file_name):
		self.file_name = file_name

	def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
		self.file = open(self.file_name, "w+")
		self.file.write("Population Size: {}\tVaccination Percentage: {}\tVirus Name: {}\tMortality Rate: {}\tReproduction: {}\n".format(pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num))
		self.file.close()

	def log_interaction(self, person1, person2, did_infect = None, person2_vacc = None, person2_sick= None):
		self.file = open(self.file_name, "a")
		self.file.write("Interaction between patient {} and citizen{}\nCitizen {} Vaccinated: {}\n".format(person1._id, person2._id, person2._id, person2_vacc))
		if did_infect == True:
			self.file.write("Infection was spread\n")
		self.file.close()

	def log_infection_survival(self, person, did_die_from_infection):
		self.file = open(self.file_name, "a")
		if did_die_from_infection == True:
			self.file.write("Patient {} was killed from infection\n".format(person._id))
		else:
			self.file.write("Patient {} survived the infection\n".format(person._id))
		self.file.close()
