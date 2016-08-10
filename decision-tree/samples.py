class PlayBasketballDecision:
	"""
	make a decision wether to play basketball
	"""

	@staticmethod
	def createTrainSamples():
	    """
	    outlook->  0: sunny | 1: overcast | 2: rain
	    temperature-> 0: hot | 1: mild | 2: cool
	    humidity-> 0: high | 1: normal
	    windy-> 0: false | 1: true 
	    """
	    dataSet = [[0, 0, 0, 0, 'N'], 
	               [0, 0, 0, 1, 'N'], 
	               [1, 0, 0, 0, 'Y'], 
	               [2, 1, 0, 0, 'Y'], 
	               [2, 2, 1, 0, 'Y'], 
	               [2, 2, 1, 1, 'N'], 
	               [1, 2, 1, 1, 'Y']]
	    labels = ['outlook', 'temperature', 'humidity', 'windy']
	    return dataSet, labels

	@staticmethod
	def createTestSamples():
	    """
	    outlook->  0: sunny | 1: overcast | 2: rain
	    temperature-> 0: hot | 1: mild | 2: cool
	    humidity-> 0: high | 1: normal
	    windy-> 0: false | 1: true 
	    """
	    testSet = [[0, 1, 0, 0], 
	               [0, 2, 1, 0], 
	               [2, 1, 1, 0], 
	               [0, 1, 1, 1], 
	               [1, 1, 0, 1], 
	               [1, 0, 1, 0], 
	               [2, 1, 0, 1]]
	    return testSet

class JoinAsMemberDecision:
	'''
	estimate the probility of a user pay to join a member system
	'''
	def createTrainData():
	    my_data=[['slashdot','USA','yes',18,'None'],
	            ['google','France','yes',23,'Premium'],
	            ['digg','USA','yes',24,'Basic'],
	            ['kiwitobes','France','yes',23,'Basic'],
	            ['google','UK','no',21,'Premium'],
	            ['(direct)','New Zealand','no',12,'None'],
	            ['(direct)','UK','no',21,'Basic'],
	            ['google','USA','no',24,'Premium'],
	            ['slashdot','France','yes',19,'None'],
	            ['digg','USA','no',18,'None'],
	            ['google','UK','no',18,'None'],
	            ['kiwitobes','UK','no',19,'None'],
	            ['digg','New Zealand','yes',12,'Basic'],
	            ['slashdot','UK','no',21,'None'],
	            ['google','UK','yes',18,'Basic'],
	            ['kiwitobes','France','yes',19,'Basic']]

	    my_labels = ['source', 'country', 'clicked faq or not', 'age']
	    return (my_data, my_labels)