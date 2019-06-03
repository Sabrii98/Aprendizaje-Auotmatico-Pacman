# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters

class NullGraphics:
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

    def printLineData(self, gameState):
    	# posicion de pacman
        columna_pacman = str(gameState.getPacmanPosition()[0])
        fila_pacman = str(gameState.getPacmanPosition()[1])
        # direccion de pacman
        dir_pacman = str(gameState.data.agentStates[0].getDirection())
        # numero de fantasmas
        num_fantasmas = str(gameState.getNumAgents() - 1)
        # posicion fantasma 1
        columna_fantasma_1 = str(gameState.getGhostPositions()[0][0])
        fila_fantasma_1 = str(gameState.getGhostPositions()[0][1])
        # posicion fantasma 2
        columna_fantasma_2 = str(gameState.getGhostPositions()[1][0])
        fila_fantasma_2 = str(gameState.getGhostPositions()[1][1])
        # posicion fantasma 3
        columna_fantasma_3 = str(gameState.getGhostPositions()[2][0])
        fila_fantasma_3 = str(gameState.getGhostPositions()[2][1])
        # posicion fantasma 4
        columna_fantasma_4 = str(gameState.getGhostPositions()[3][0])
        fila_fantasma_4 = str(gameState.getGhostPositions()[3][1])
        # distancia de manhattan al fantasma 1
        dist_1 = str(gameState.data.ghostDistances[0])
        # distancia de manhattan al fantasma 2
        dist_2 = str(gameState.data.ghostDistances[1])
        # distancia de manhattan al fantasma 3
        dist_3 = str(gameState.data.ghostDistances[2])
        # distancia de manhattan al fantasma 4
        dist_4 = str(gameState.data.ghostDistances[3])
        # puntos de comida restantes
        num_comida = str(gameState.getNumFood())
        #distancia de manhattan a la comida mas cercana
        dist_comida = str(gameState.getDistanceNearestFood())
        # var8 = str(gameState.getWalls()) #paredes del mapa

        res =  columna_pacman + ',' + fila_pacman + ',' + num_fantasmas + ',' + columna_fantasma_1 + ',' + fila_fantasma_1+ ',' + columna_fantasma_2 + ',' + fila_fantasma_2 + ',' + columna_fantasma_3 + ',' + fila_fantasma_3 + ',' + columna_fantasma_4 + ',' + fila_fantasma_4 + ',' + dist_1 + ',' + dist_2 + ',' + dist_3 + ',' + dist_4 + ',' + num_comida + ',' + dist_comida + ',' + dir_pacman + '\n'
        return res

from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
        
    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move
        
class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST

class BasicAgentAA(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        self.contMov = 0
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        print "---------------- TICK ", self.countActions, " --------------------------"
        # Dimensiones del mapa
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print "Width: ", width, " Height: ", height
        # Posicion del Pacman
        print "Pacman position: ", gameState.getPacmanPosition()
        # Acciones legales de pacman en la posicion actual
        print "Legal actions: ", gameState.getLegalPacmanActions()
        # Direccion de pacman
        print "Pacman direction: ", gameState.data.agentStates[0].getDirection()
        # Numero de fantasmas
        print "Number of ghosts: ", gameState.getNumAgents() - 1
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        print "Living ghosts: ", gameState.getLivingGhosts()
        # Posicion de los fantasmas
        print "Ghosts positions: ", gameState.getGhostPositions()
        # Direciones de los fantasmas
        print "Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Distancia de manhattan a los fantasmas
        print "Ghosts distances: ", gameState.data.ghostDistances
        # Puntos de comida restantes
        print "Pac dots: ", gameState.getNumFood()
        # Distancia de manhattan a la comida mas cercada
        print "Distance nearest pac dots: ", gameState.getDistanceNearestFood()
        # Paredes del mapa
        print "Map:  \n", gameState.getWalls()
        # Puntuacion
        print "Score: ", gameState.getScore()
        
    
    def chooseAction(self, gameState):
    	cont = 0
        position =  gameState.getPacmanPosition()
    	actions = gameState.getLegalPacmanActions()
    	ghostsPositions = gameState.getGhostPositions()
    	ghostsDistances = gameState.data.ghostDistances
    	for i in range(len(ghostsDistances)):
    		if ghostsDistances[i] < 0:
    			ghostsDistances.pop(i)
    			ghostsDistances.insert(i, 0)
    	ghostsDistancesSorted = sorted(ghostsDistances) #ordenar la lista de distancias 
    	for i in range(len(ghostsDistancesSorted)):
    		if ghostsDistancesSorted[i] == 0:
    			cont = cont + 1
    	pos = ghostsDistances.index(ghostsDistancesSorted[cont]) #elegir el indice correspondiente a la distancia mas pequena
    	destino = gameState.getGhostPositions()[pos]
        self.countActions = self.countActions + 1
        self.printInfo(gameState)
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman

        #El personaje se encuentra a la izquierda del fantasma
        if (position[0] < destino[0]):
        	#El personaje se encuentra debajo del fantasma
        	if(position[1] < destino[1]):
        		if(Directions.NORTH in legal): move = Directions.NORTH
        		else:
        			if (Directions.EAST in legal): move = Directions.EAST
	        		else:
	        			move_random = random.randint(0, 1)
	        			if(move_random == 0) and Directions.WEST in legal:  move = Directions.WEST
	        			if(move_random == 1) and Directions.SOUTH in legal:  move = Directions.SOUTH
        	#El personaje se encuentra encima del fantasma
        	if(position[1] > destino[1]):
        		if(Directions.SOUTH in legal): move = Directions.SOUTH
        		else:
        		 	if (Directions.EAST in legal): move = Directions.EAST
	        		else:
	        			move_random = random.randint(0, 1)
	        			if(move_random == 0) and Directions.WEST in legal:  move = Directions.WEST
	        			if(move_random == 1) and Directions.NORTH in legal:  move = Directions.NORTH
        	#El personaje se encuentra en la misma fila que el fantasma
        	if(position[1] == destino[1]):
        		if(Directions.EAST in legal):
        			move = Directions.EAST
        		else:
        			move_random = random.randint(0, 2)
        			if(move_random == 0) and Directions.WEST in legal:  move = Directions.WEST
        			if(move_random == 1) and Directions.NORTH in legal:  move = Directions.NORTH
        			if(move_random == 2) and Directions.SOUTH in legal:  move = Directions.SOUTH
        #El personaje se encuentra a la derecha del fantasma
        if(position[0] > destino[0]):
        	#El personaje se encuentra debajo del fantasma
        	if(position[1] < destino[1]):
        		if(Directions.NORTH in legal):
        			move = Directions.NORTH
        		else:
        			if(Directions.WEST in legal): 
        				move = Directions.WEST
	        		else:
	        			move_random = random.randint(0, 1)
	        			if(move_random == 0) and Directions.EAST in legal:  move = Directions.EAST
	        			if(move_random == 1) and Directions.SOUTH in legal:  move = Directions.SOUTH
        	#El personaje se encuentra encima del fantasma
        	if(position[1] > destino[1]):
        		if(Directions.SOUTH in legal):
        			move = Directions.SOUTH
        		else:
        			if(Directions.WEST in legal): 
        				move = Directions.WEST
	        		else:
	        			move_random = random.randint(0, 1)
	        			if(move_random == 0) and Directions.EAST in legal:  move = Directions.EAST
	        			if(move_random == 1) and Directions.NORTH in legal:  move = Directions.NORTH
        	#El personaje se encuentra en la misma fila que el fantasma
        	if(position[1] == destino[1]):
        		if(Directions.WEST in legal):
        			move = Directions.WEST
        		else:
        			move_random = random.randint(0, 2)
        			if(move_random == 0) and Directions.EAST in legal:  move = Directions.EAST
        			if(move_random == 1) and Directions.NORTH in legal:  move = Directions.NORTH
        			if(move_random == 2) and Directions.SOUTH in legal:  move = Directions.SOUTH
        #El personaje se encuentra en la misma columna que el fantasma
        if(position[0] == destino[0]):
        	#El personaje se encuentra debajo del fantasma
        	if(position[1] < destino[1]):
        		if Directions.NORTH in legal:
        			move = Directions.NORTH
        		else:
        			move_random = random.randint(0, 2)
        			if(move_random == 0) and Directions.WEST in legal:  
        				move = Directions.WEST
        			if(move_random == 1) and Directions.EAST in legal:  move = Directions.EAST
        			if(move_random == 2) and Directions.SOUTH in legal:  move = Directions.SOUTH
        	#El personaje se encuentra encima del fantasma
        	if (position[1] > destino[1]):
        		if Directions.SOUTH in legal:
        			move = Directions.SOUTH
        		else:
        			move_random = random.randint(0, 2)
        			if(move_random == 0) and Directions.WEST in legal:  
        				move = Directions.WEST
        			if(move_random == 1) and Directions.EAST in legal:  move = Directions.EAST
        			if(move_random == 2) and Directions.NORTH in legal:  move = Directions.NORTH

        self.contMov = self.contMov + 1
        varBoolean = 0
        if(self.contMov == 30):
            while varBoolean == 0:
                move_random = random.randint(0, 3)
                if(move_random == 0) and Directions.WEST in legal:
                    move = Directions.WEST
                    varBoolean = 1

                if(move_random == 1) and Directions.EAST in legal:
                    move = Directions.EAST
                    varBoolean = 1

                if(move_random == 2) and Directions.NORTH in legal:
                    move = Directions.NORTH
                    varBoolean = 1

                if(move_random == 3) and Directions.SOUTH in legal:
                    move = Directions.SOUTH
                    varBoolean = 1

            self.contMov = 0

        return move

    def printLineData(self, gameState):
        var1 = str(gameState.getPacmanPosition())
        var2 = str(gameState.getLegalPacmanActions())
        var3 = str(gameState.data.ghostDistances)
        res = 'Pacman position: ' + var1 + ', Legal pacman actions' + var2 + ', Ghosts distances: ' + var3 + '\n'
        return res
