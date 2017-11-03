import numpy as np 
import theano
import theano.tensor as T
import lasagne
import sys

class FeatureRepresenter:
	"""
	Get the feature representation of the data for giving
	as input to Block1
	"""
	
	def __init__(self,num_p,num_q,k_ability=3,k_difficulty=3,num_dimensions=2):
		"""
		k_ability - number of buckets for ability
		k_difficulty - number of buckets for difficulty
		num_p - rows in the matrix
		num_q - columns in the matrix
		num_dimensions - 2 for 2D matrix, etc.
		"""
		self.k_ability = k_ability
		self.k_difficulty = k_difficulty
		self.num_dimensions = num_dimensions
		self.num_participants = num_p 
		self.num_questions = num_q
		
	def get_average_ability_2d(self):
		"""
		Get average ability in 2D case
		"""
		abilities = []
		for i in range(0,self.num_participants):
			correct_count = 0
			for j in range(0,self.num_questions):
				if self.current_proposals[j] == self.input_data[i][j]:
					correct_count += 1
			ability = float(correct_count)/self.num_questions
			abilities.append((ability,i))
		abilities = np.array(abilities)
		return abilities
	
	def get_average_difficulty_2d(self):
		"""
		Get average difficulty in 2D case
		"""
		difficulties = []
	#	print np.shape(self.input_data)
		for i in range(0,self.num_questions):
			correct_count = 0
			for j in range(0,self.num_participants):
				if self.current_proposals[i] == self.input_data[j][i]:
					correct_count += 1
			difficulty = 1-float(correct_count)/self.num_participants
			difficulties.append((difficulty,i))
		difficulties = np.array(difficulties)
		return difficulties
		
	def get_buckets(self,attribute,k):
		"""
		Get k buckets for the attribute list given in ascending order
		"""
		attribute = attribute.tolist()
		attribute.sort(key=lambda x:x[0])
		attribute_step_size = len(attribute)/k
		for i in range(0,k):
			current_bucket = attribute[i*attribute_step_size:min((i+1)*attribute_step_size,len(attribute))]
			for j in range(0,len(current_bucket)):
				current_bucket[j][1] = int(current_bucket[j][1])
			yield current_bucket	
			
	def get_ability_in_bucket(self,ability_bucket):
		"""
		Get the ability in the bucket ability_bucket
		"""
		difficulties = []
		for i in range(0,self.num_questions):
			correct_count = 0	
			for j in range(0,len(ability_bucket)):
				if self.current_proposals[i] == self.input_data[ability_bucket[j][1]][i]:
					correct_count += 1
			difficulty = 1-float(correct_count)/len(ability_bucket)
			difficulties.append((difficulty,i))
		difficulties = np.array(difficulties)
		return difficulties
		
	def get_difficulty_in_bucket(self,difficulty_bucket):
		"""
		Get the difficulty in the bucket difficulty_bucket
		"""
		abilities = []
	#	print np.shape(self.input_data)
	#	print np.shape(self.current_proposals)
	#	print len(difficulty_bucket)
	#	print difficulty_bucket
		for i in range(0,self.num_participants):
			correct_count = 0	
			for j in range(0,len(difficulty_bucket)):
		#		print i, j
		#		print difficulty_bucket[j][1]
				if self.current_proposals[difficulty_bucket[j][1]] == self.input_data[i][difficulty_bucket[j][1]]:
					correct_count += 1
			ability = float(correct_count)/len(difficulty_bucket)
			abilities.append((ability,i))
		abilities = np.array(abilities)
		return abilities
		
	def generate_features_2d(self,input_data,current_proposals):
		"""
		Generate the feature input given the data and current proposed
		answer sheet
		"""
		assert len(np.shape(input_data)) == self.num_dimensions
		assert len(current_proposals) == self.num_questions
		self.input_data = input_data
		self.current_proposals = current_proposals
		self.abilities = self.get_average_ability_2d()
		self.difficulties = self.get_average_difficulty_2d()
		abilities_bucket_wise = []
		difficulties_bucket_wise = []
		for ability_bucket in self.get_buckets(self.abilities[:],self.k_ability):
			difficulties_bucket_wise.append(self.get_ability_in_bucket(ability_bucket))
		for difficulty_bucket in self.get_buckets(self.difficulties[:],self.k_difficulty):
			abilities_bucket_wise.append(self.get_difficulty_in_bucket(difficulty_bucket))
		self.abilities_bucket_wise = np.array(abilities_bucket_wise)
		self.difficulties_bucket_wise = np.array(difficulties_bucket_wise)				
		
	def get_features_2d_element(self,person,question):
		"""
		Get a particular value in the generated feature matrix
		"""
		feature_list = []
		print self.abilities
		print self.difficulties
		print self.abilities_bucket_wise
		print self.difficulties_bucket_wise
		print len(self.abilities_bucket_wise)
		print len(self.abilities_bucket_wise[0])
		print len(self.abilities_bucket_wise[0][0])
	#	sys.exit(0)
		feature_list.append(self.abilities[person][0])
		for i in range(0,self.k_difficulty):
			feature_list.append(self.abilities_bucket_wise[i][person][0])
		feature_list.append(self.difficulties[question][0])
		for i in range(0,self.k_ability):
			feature_list.append(self.difficulties_bucket_wise[i][question][0])
		feature_list = np.array(feature_list)
		return feature_list
		
	def get_features_2d(self):
		"""
		Get the feature list by flattring the feature matrix
		"""
		features_list = []
		labels_list = []
		for i in range(0,self.num_participants):
			for j in range(0,self.num_questions):
				features_list.append(self.get_features_2d_element(i,j))
				labels_list.append(self.current_proposals[j])
		features_list = np.array(features_list)
		labels_list = np.array(labels_list)
		return features_list, labels_list

class FeatureRepresenter_3D:
	"""
	Get the feature representation of the data for giving
	as input to Block1
	"""
	
	def __init__(self,num_p,num_q,num_o,k_ability=3,k_qdifficulty=3,k_odifficulty=3):
		"""
		k_ability - number of buckets for ability
		k_difficulty - number of buckets for difficulty
		num_p - rows in the matrix
		num_q - columns in the matrix
		num_dimensions - 2 for 2D matrix, etc.
		"""
		self.k_ability = k_ability
		self.k_qdifficulty = k_qdifficulty
		self.k_odifficulty = k_odifficulty
		self.num_dimensions = 3
		self.num_participants = num_p 
		self.num_questions = num_q
		self.num_options = num_o
		
	def get_average_ability_3d(self):
		"""
		Get average ability in 3D case
		"""
		abilities = []
		for i in range(0,self.num_participants):
			correct_count = 0
			for j in range(0,self.num_questions):
				for k in range(0,self.num_options):
					if self.current_proposals[j][k] == self.input_data[i][j][k]:
						correct_count += 1
			ability = float(correct_count)/(self.num_questions*self.num_options)
#			print ability
		#	print correct_count
		#	sys.exit(0)
			abilities.append((ability,i))
		abilities = np.array(abilities)
		return abilities
	
	def get_average_qdifficulty_3d(self):
		"""
		Get average difficulty in 3D case
		"""
		qdifficulties = []
	#	print np.shape(self.input_data)
		for i in range(0,self.num_questions):
			qdifficulty = 0
			for j in range(0,self.num_options):
				index_arr = np.intersect1d(np.where(self.odifficulties[:,1] == i),np.where(self.odifficulties[:,2] == j))
				assert len(index_arr) == 1
				qdifficulty += self.odifficulties[index_arr[0]][0]
			qdifficulty = qdifficulty / float(self.num_options)
			qdifficulties.append((difficulty,i))
		qdifficulties = np.array(qdifficulties)
		return qdifficulties
		
	def get_average_odifficulty_3d(self):
		"""
		Get average difficulty in 3D case
		"""
		odifficulties = []
	#	print np.shape(self.input_data)
		for i in range(0,self.num_questions):
			for j in range(0,self.num_options):
				correct_count = 0
				for k in range(0,self.num_participants):
					if self.current_proposals[i][j] == self.input_data[k][i][j]:
						correct_count += 1
				odifficulty = 1-float(correct_count)/self.num_participants
				odifficulties.append((odifficulty,i,j))
		odifficulties = np.array(odifficulties)
		return odifficulties
		
	def get_buckets(self,attribute,k):
		"""
		Get k buckets for the attribute list given in ascending order
		"""
		attribute = attribute.tolist()
	#	attribute = [[8,2],[10,1],[3,3]]
		attribute.sort(key=lambda x:x[0])
#		print attribute
		attribute_step_size = len(attribute)/k
		for i in range(0,k):
			current_bucket = attribute[i*attribute_step_size:min((i+1)*attribute_step_size,len(attribute))]
			for j in range(0,len(current_bucket)):
				current_bucket[j][1] = int(current_bucket[j][1])
				if len(current_bucket[j]) == 3:
					current_bucket[j][2] = int(current_bucket[j][2])
#			print current_bucket
	#		sys.exit(0)
			yield current_bucket	
			
	def get_ability_in_bucket(self,ability_bucket):
		"""
		Get the ability in the bucket ability_bucket
		"""
		odifficulties = []
#		print ability_bucket
	#	sys.exit(0)
		for i in range(0,self.num_questions):
			for j in range(0,self.num_options):
				correct_count = 0	
				for k in range(0,len(ability_bucket)):
#					print i, j
#					print ability_bucket
#					print self.current_proposals
				#	sys.exit(0)
					if self.current_proposals[i][j] == self.input_data[ability_bucket[k][1]][i][j]:
						correct_count += 1
				odifficulty = 1-float(correct_count)/len(ability_bucket)
				odifficulties.append((odifficulty,i,j))
		odifficulties = np.array(odifficulties)
		return odifficulties
		
	def get_odifficulty_in_bucket(self,odifficulty_bucket):
		"""
		Get the difficulty in the bucket difficulty_bucket
		"""
		abilities = []
	#	print np.shape(self.input_data)
	#	print np.shape(self.current_proposals)
	#	print len(difficulty_bucket)
#		print odifficulty_bucket
	#	sys.exit(0)
		for i in range(0,self.num_participants):
			correct_count = 0	
			for j in range(0,len(odifficulty_bucket)):
		#		print i, j
		#		print difficulty_bucket[j][1]
#				print len(odifficulty_bucket)
			#	sys.exit(0)
				if self.current_proposals[odifficulty_bucket[j][1]][odifficulty_bucket[j][2]] == self.input_data[i][odifficulty_bucket[j][1]][odifficulty_bucket[j][2]]:
					correct_count += 1
			ability = float(correct_count)/len(odifficulty_bucket)
#			print ability
#			print correct_count
	#		sys.exit(0)
			abilities.append((ability,i))
		abilities = np.array(abilities)
		return abilities
		
	def generate_features_3d(self,input_data,current_proposals):
		"""
		Generate the feature input given the data and current proposed
		answer sheet
		"""
		assert len(np.shape(input_data)) == self.num_dimensions
	#	assert len(current_proposals.shape) == 2
		print current_proposals.shape
	#	sys.exit(0)
		assert len(current_proposals) == self.num_questions
		assert len(current_proposals[0]) == self.num_options
		self.input_data = input_data
		self.current_proposals = current_proposals
		self.abilities = self.get_average_ability_3d()
		self.odifficulties = self.get_average_odifficulty_3d()
#		print self.abilities 
#		print self.odifficulties 
	#	sys.exit(0)
	#	self.qdifficulties = self.get_average_qdifficulty_3d()
		abilities_bucket_wise = []
		qdifficulties_bucket_wise = []
		odifficulties_bucket_wise = []
		for ability_bucket in self.get_buckets(self.abilities[:],self.k_ability):
#			print ability_bucket
			odifficulties_bucket_wise.append(self.get_ability_in_bucket(ability_bucket))
		for odifficulty_bucket in self.get_buckets(self.odifficulties[:],self.k_odifficulty):
			abilities_bucket_wise.append(self.get_odifficulty_in_bucket(odifficulty_bucket))
		self.abilities_bucket_wise = np.array(abilities_bucket_wise)
		self.odifficulties_bucket_wise = np.array(odifficulties_bucket_wise)			
		
	def get_features_3d_element(self,person,question,option):
		"""
		Get a particular value in the generated feature matrix
		"""
		feature_list = []
#		print self.abilities
#		print self.odifficulties
#		print self.abilities_bucket_wise
#		print self.odifficulties_bucket_wise
#		print len(self.abilities_bucket_wise)
#		print len(self.abilities_bucket_wise[0])
#		print len(self.abilities_bucket_wise[0][0])
#		sys.exit(0)
		feature_list.append(self.abilities[person][0])
		for i in range(0,self.k_odifficulty):
	#		print i
			feature_list.append(self.abilities_bucket_wise[i][person][0])
	#		print question
	#		print self.num_questions
	#		print option
	#		print question*self.num_options+option
		feature_list.append(self.odifficulties[question*self.num_options+option][0])
		for i in range(0,self.k_ability):
			feature_list.append(self.odifficulties_bucket_wise[i][question*self.num_options+option][0])
		feature_list = np.array(feature_list)
		return feature_list
		
	def get_features_3d(self):
		"""
		Get the feature list by flattening the feature matrix
		"""
		features_list = []
		labels_list = []
		for i in range(0,self.num_participants):
			for j in range(0,self.num_questions):
				for k in range(0,self.num_options):
					features_list.append(self.get_features_3d_element(i,j,k))
					labels_list.append(self.current_proposals[j][k])
		features_list = np.array(features_list)
		labels_list = np.array(labels_list)
		return features_list, labels_list	
		
if __name__ == "__main__":
	feature = FeatureRepresenter(3,3,1,1,2)
	feature = FeatureRepresenter_3D(3,2,3,2,3,1)
	feature.generate_features_3d([[[1,1,0],[1,1,0]],[[1,0,1],[0,1,0]],[[1,1,1],[0,1,1]]],[[1,0,0],[0,1,0]])
	print feature.get_features_3d_element(1,1,1)
#	feature.generate_features_2d([[1,0,0],[0,1,0],[1,1,0]],[1,0,1])
#	print feature.get_features_2d_element(1,1)
	print "Defined Feature Creator for DeepAgg"
