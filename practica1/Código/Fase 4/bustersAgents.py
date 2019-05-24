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
import sys
from wekaI import Weka

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
        self.instanciaAnterior = ""
        self.accionAnteriorAnterior = 0
        # WEKA
        self.weka = Weka()
        self.weka.start_jvm()

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

        # POSICION DE PACMAN
        columna_pacman = str(gameState.getPacmanPosition()[0])
        fila_pacman = str(gameState.getPacmanPosition()[1])
        
        # NUMERO DE FANTASMAS (SIEMPRE ES 4 ES IRRELEVANTE)
        num_fantasmas = str(gameState.getNumAgents() - 1)
        
        # NUMERO DE FANTASMAS VIVOS
        num_fantasmas_vivos = 0
        for fantasma in gameState.getLivingGhosts():
            if fantasma: 
                num_fantasmas_vivos = num_fantasmas_vivos + 1
        num_fantasmas_vivos = str(num_fantasmas_vivos)
        # num_fantasmas_vivos = sum([int(g) for g in gameState.getLivingGhosts()])
        
        # POSICION FANTASMA 1
        columna_fantasma_1 = str(gameState.getGhostPositions()[0][0])
        fila_fantasma_1 = str(gameState.getGhostPositions()[0][1])
        
        # POSICION FANTASMA 2
        columna_fantasma_2 = str(gameState.getGhostPositions()[1][0])
        fila_fantasma_2 = str(gameState.getGhostPositions()[1][1])
        
        # POSICION FANTASMA 3
        columna_fantasma_3 = str(gameState.getGhostPositions()[2][0])
        fila_fantasma_3 = str(gameState.getGhostPositions()[2][1])
        
        # POSICION FANTASMA 4
        columna_fantasma_4 = str(gameState.getGhostPositions()[3][0])
        fila_fantasma_4 = str(gameState.getGhostPositions()[3][1])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 1
        dist_1 = str(gameState.data.ghostDistances[0])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 2
        dist_2 = str(gameState.data.ghostDistances[1])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 3
        dist_3 = str(gameState.data.ghostDistances[2])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 4
        dist_4 = str(gameState.data.ghostDistances[3])
        
        # ORDENAR LISTA DE DISTANCIAS
        cont = 0
        ghostsDistances = gameState.data.ghostDistances
        for i in range(len(ghostsDistances)):
            if ghostsDistances[i] < 0:
                ghostsDistances.pop(i)
                ghostsDistances.insert(i, -1)
        ghostsDistancesSorted = sorted(ghostsDistances) # ORDENAR LA LISTA DE DISTANCIAS 
        for i in range(len(ghostsDistancesSorted)):
            if ghostsDistancesSorted[i] == -1:
                cont = cont + 1
        pos = ghostsDistances.index(ghostsDistancesSorted[cont]) # ELEGIR EL INDICE CORRESPONDIENTE A LA DISTANCIA MAS PEQUENA
        
        #POSICION FANTASMA MAS CERCANO
        columna_fantasma_mas_cercano = str(gameState.getGhostPositions()[pos][0])
        fila_fantasma_mas_cercano = str(gameState.getGhostPositions()[pos][1])

        # DISTANCIA EN COLUMNAS AL FANTASMA MAS CERCANO
        dist_columna_fantasma_cercano = str(abs((gameState.getPacmanPosition()[0])-(gameState.getGhostPositions()[pos][0])))
        # DISTANCIA EN FILAS AL FANTASMA MAS CERCANO
        dist_fila_fantasma_cercano = str(abs((gameState.getPacmanPosition()[1])-(gameState.getGhostPositions()[pos][1])))
        #DISTANCIA DE MANHATTAN AL FANTASMA MAS CERCANO
        dist_fantasma_cercano = str((abs((gameState.getPacmanPosition()[0])-(gameState.getGhostPositions()[pos][0])))+(abs((gameState.getPacmanPosition()[1])-(gameState.getGhostPositions()[pos][1]))))

        # PUNTOS DE COMIDA RESTANTES
        num_comida = str(gameState.getNumFood())
        
        # DISTANCIA DE MANHATTAN A LA COMIDA MAS CERCANA
        dist_comida = str(gameState.getDistanceNearestFood())

        # PAREDES
        isWallNorth = str(gameState.getWalls()[gameState.getPacmanPosition()[0]][gameState.getPacmanPosition()[1]+1])
        isWallSouth = str(gameState.getWalls()[gameState.getPacmanPosition()[0]][gameState.getPacmanPosition()[1]-1])
        isWallEast = str(gameState.getWalls()[gameState.getPacmanPosition()[0]+1][gameState.getPacmanPosition()[1]])
        isWallWest = str(gameState.getWalls()[gameState.getPacmanPosition()[0]-1][gameState.getPacmanPosition()[1]])

        # DISTANCIAS A LAS PAREDES MAS CERCANAS
        aux_columna_pacman = gameState.getPacmanPosition()[0]
        aux_fila_pacman = gameState.getPacmanPosition()[1]
        aux_columna = gameState.getWalls()[aux_columna_pacman]
        lista_columna = []
        lista_norte = []
        lista_sur = []
        aux_cont = -1
        for valor in aux_columna:
        	aux_cont = aux_cont + 1
        	if(valor == True):
        		lista_columna.append(aux_cont)
        for numero in lista_columna:
        	if(numero < aux_fila_pacman):
        		lista_sur.append(numero)
        	if(numero > aux_fila_pacman):
        		lista_norte.append(numero)
        pos_North_cercano = sorted(lista_norte)[0] # lista norte nos quedamos con el mas pequeno
        pos_South_cercano = sorted(lista_sur, reverse = True)[0] # lista sur nos quedamos con el mas grande
        distNorth = str(abs(pos_North_cercano - aux_fila_pacman))
        distSouth = str(abs(pos_South_cercano - aux_fila_pacman))
    
        lista_fila = []
        lista_este = []
        lista_oeste = []
        num_columna = -1
        num_fila = -1
        lista_mapa = []
        for valor in gameState.getWalls():
        	lista_mapa.append(valor)
        # imprime las columnas de 0 a x
        # i representa la columna
        # j representa la fila
        # almacenamos la columna en la que se encuentran las paredes, la fila es la misma que la del pacman
        for i in range(len(lista_mapa)):
        	for j in range(len(lista_mapa[i])):
        		if(lista_mapa[i][j] == True and j == aux_fila_pacman):
        			lista_fila.append(i)
        for numero in lista_fila:
        	if(numero < aux_columna_pacman):
        		lista_oeste.append(numero)
        	if(numero > aux_columna_pacman):
        		lista_este.append(numero)
        pos_East_cercano = sorted(lista_este)[0] # lista este nos quedamos con el mas pequeno
        pos_West_cercano = sorted(lista_oeste, reverse = True)[0] # lista oeste nos quedamos con el mas grande
        distEast = str(abs(pos_East_cercano - aux_columna_pacman))
        distWest = str(abs(pos_West_cercano - aux_columna_pacman))


        # PUNTUACION
        score = str(gameState.getScore())
        
        # DIRECCION DE PACMAN
        dir_pacman = str(gameState.data.agentStates[0].getDirection())
        

        if dist_1 == "None":
        	dist_1 = "-1"
        if dist_2 == "None":
        	dist_2 = "-1"
        if dist_3 == "None":
        	dist_3 = "-1"
        if dist_4 == "None":
        	dist_4 = "-1"
        if dist_comida == "None":
        	dist_comida = "-1" 

        if(self.accionAnteriorAnterior != 0):
            x = [num_fantasmas_vivos,dist_columna_fantasma_cercano,dist_fila_fantasma_cercano,dist_fantasma_cercano,dist_comida,isWallNorth,isWallSouth,isWallEast,isWallWest,distNorth,distSouth,distEast,distWest,self.accionAnteriorAnterior]
            a = self.weka.predict("./J48_1_4.model", x, "./training_tutorial1.arff")
            self.accionAnteriorAnterior = dir_pacman 
        else:
            x = [num_fantasmas_vivos,dist_columna_fantasma_cercano,dist_fila_fantasma_cercano,dist_fantasma_cercano,dist_comida,isWallNorth,isWallSouth,isWallEast,isWallWest,distNorth,distSouth,distEast,distWest,self.accionAnteriorAnterior]
            a = self.weka.predict("./J48_1_4.model", x, "./training_tutorial1.arff")
            self.accionAnteriorAnterior = dir_pacman

        legal = gameState.getLegalActions(0) ##Legal position from the pacman

        if(a in legal):
            print ("LA ACCION EXISTE")
            return a
        else:
        	print("RANDOM")
        	move = Directions.STOP
        	move_random = random.randint(0, 3)
        	if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        	if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        	if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        	if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        	return move


class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)
        self.instanciaAnterior = 0
        self.accionAnterior = 0
        self.accionAnteriorAnterior = 0

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

    def printLineData(self, gameState):
        # POSICION DE PACMAN
        columna_pacman = str(gameState.getPacmanPosition()[0])
        fila_pacman = str(gameState.getPacmanPosition()[1])
        
        # NUMERO DE FANTASMAS (SIEMPRE ES 4 ES IRRELEVANTE)
        num_fantasmas = str(gameState.getNumAgents() - 1)
        
        # NUMERO DE FANTASMAS VIVOS
        num_fantasmas_vivos = 0
        for fantasma in gameState.getLivingGhosts():
            if fantasma: 
                num_fantasmas_vivos = num_fantasmas_vivos + 1
        num_fantasmas_vivos = str(num_fantasmas_vivos)
        # num_fantasmas_vivos = sum([int(g) for g in gameState.getLivingGhosts()])
        
        # POSICION FANTASMA 1
        columna_fantasma_1 = str(gameState.getGhostPositions()[0][0])
        fila_fantasma_1 = str(gameState.getGhostPositions()[0][1])
        
        # POSICION FANTASMA 2
        columna_fantasma_2 = str(gameState.getGhostPositions()[1][0])
        fila_fantasma_2 = str(gameState.getGhostPositions()[1][1])
        
        # POSICION FANTASMA 3
        columna_fantasma_3 = str(gameState.getGhostPositions()[2][0])
        fila_fantasma_3 = str(gameState.getGhostPositions()[2][1])
        
        # POSICION FANTASMA 4
        columna_fantasma_4 = str(gameState.getGhostPositions()[3][0])
        fila_fantasma_4 = str(gameState.getGhostPositions()[3][1])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 1
        dist_1 = str(gameState.data.ghostDistances[0])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 2
        dist_2 = str(gameState.data.ghostDistances[1])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 3
        dist_3 = str(gameState.data.ghostDistances[2])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 4
        dist_4 = str(gameState.data.ghostDistances[3])
        
        # ORDENAR LISTA DE DISTANCIAS
        cont = 0
        ghostsDistances = gameState.data.ghostDistances
        for i in range(len(ghostsDistances)):
            if ghostsDistances[i] < 0:
                ghostsDistances.pop(i)
                ghostsDistances.insert(i, -1)
        ghostsDistancesSorted = sorted(ghostsDistances) # ORDENAR LA LISTA DE DISTANCIAS 
        for i in range(len(ghostsDistancesSorted)):
            if ghostsDistancesSorted[i] == -1:
                cont = cont + 1
        pos = ghostsDistances.index(ghostsDistancesSorted[cont]) # ELEGIR EL INDICE CORRESPONDIENTE A LA DISTANCIA MAS PEQUENA
        
        #POSICION FANTASMA MAS CERCANO
        columna_fantasma_mas_cercano = str(gameState.getGhostPositions()[pos][0])
        fila_fantasma_mas_cercano = str(gameState.getGhostPositions()[pos][1])

        # DISTANCIA EN COLUMNAS AL FANTASMA MAS CERCANO
        dist_columna_fantasma_cercano = str(abs((gameState.getPacmanPosition()[0])-(gameState.getGhostPositions()[pos][0])))
        # DISTANCIA EN FILAS AL FANTASMA MAS CERCANO
        dist_fila_fantasma_cercano = str(abs((gameState.getPacmanPosition()[1])-(gameState.getGhostPositions()[pos][1])))
        #DISTANCIA DE MANHATTAN AL FANTASMA MAS CERCANO
        dist_fantasma_cercano = str((abs((gameState.getPacmanPosition()[0])-(gameState.getGhostPositions()[pos][0])))+(abs((gameState.getPacmanPosition()[1])-(gameState.getGhostPositions()[pos][1]))))

        # PUNTOS DE COMIDA RESTANTES
        num_comida = str(gameState.getNumFood())
        
        # DISTANCIA DE MANHATTAN A LA COMIDA MAS CERCANA
        dist_comida = str(gameState.getDistanceNearestFood())

        # PAREDES
        isWallNorth = str(gameState.getWalls()[gameState.getPacmanPosition()[0]][gameState.getPacmanPosition()[1]+1])
        isWallSouth = str(gameState.getWalls()[gameState.getPacmanPosition()[0]][gameState.getPacmanPosition()[1]-1])
        isWallEast = str(gameState.getWalls()[gameState.getPacmanPosition()[0]+1][gameState.getPacmanPosition()[1]])
        isWallWest = str(gameState.getWalls()[gameState.getPacmanPosition()[0]-1][gameState.getPacmanPosition()[1]])

        # DISTANCIAS A LAS PAREDES MAS CERCANAS
        aux_columna_pacman = gameState.getPacmanPosition()[0]
        aux_fila_pacman = gameState.getPacmanPosition()[1]
        aux_columna = gameState.getWalls()[aux_columna_pacman]
        lista_columna = []
        lista_norte = []
        lista_sur = []
        aux_cont = -1
        for valor in aux_columna:
        	aux_cont = aux_cont + 1
        	if(valor == True):
        		lista_columna.append(aux_cont)
        for numero in lista_columna:
        	if(numero < aux_fila_pacman):
        		lista_sur.append(numero)
        	if(numero > aux_fila_pacman):
        		lista_norte.append(numero)
        pos_North_cercano = sorted(lista_norte)[0] # lista norte nos quedamos con el mas pequeno
        pos_South_cercano = sorted(lista_sur, reverse = True)[0] # lista sur nos quedamos con el mas grande
        distNorth = str(abs(pos_North_cercano - aux_fila_pacman))
        distSouth = str(abs(pos_South_cercano - aux_fila_pacman))
    
        lista_fila = []
        lista_este = []
        lista_oeste = []
        num_columna = -1
        num_fila = -1
        lista_mapa = []
        for valor in gameState.getWalls():
        	lista_mapa.append(valor)
        # imprime las columnas de 0 a x
        # i representa la columna
        # j representa la fila
        # almacenamos la columna en la que se encuentran las paredes, la fila es la misma que la del pacman
        for i in range(len(lista_mapa)):
        	for j in range(len(lista_mapa[i])):
        		if(lista_mapa[i][j] == True and j == aux_fila_pacman):
        			lista_fila.append(i)
        for numero in lista_fila:
        	if(numero < aux_columna_pacman):
        		lista_oeste.append(numero)
        	if(numero > aux_columna_pacman):
        		lista_este.append(numero)
        pos_East_cercano = sorted(lista_este)[0] # lista este nos quedamos con el mas pequeno
        pos_West_cercano = sorted(lista_oeste, reverse = True)[0] # lista oeste nos quedamos con el mas grande
        distEast = str(abs(pos_East_cercano - aux_columna_pacman))
        distWest = str(abs(pos_West_cercano - aux_columna_pacman))


        # PUNTUACION
        score = str(gameState.getScore())
        
        # DIRECCION DE PACMAN
        dir_pacman = str(gameState.data.agentStates[0].getDirection())
        

        if dist_1 == "None":
        	dist_1 = "-1"
        if dist_2 == "None":
        	dist_2 = "-1"
        if dist_3 == "None":
        	dist_3 = "-1"
        if dist_4 == "None":
        	dist_4 = "-1"
        if dist_comida == "None":
        	dist_comida = "-1"

        cabecera = False

        try: 
        	fichero = open("info.arff", "a+")
        	#print "EL FICHERO EXISTE"
        	palabra = "@RELATION"
        	lineas = fichero.readlines()
        	if lineas[0] == "@RELATION pacman\n":
        		#print "EXISTE LA CABECERA"
        		cabecera = True
        	fichero.close()
        except:
        	#print "EL FICHERO NO EXISTE"
        	fichero = open("info.arff", "a+")
        	fichero.write("@RELATION pacman\n\n@ATTRIBUTE columna_pacman NUMERIC\n@ATTRIBUTE fila_pacman NUMERIC\n@ATTRIBUTE num_fantasmas NUMERIC\n@ATTRIBUTE num_fantasmas_vivos NUMERIC\n@ATTRIBUTE columna_fantasma_1 NUMERIC\n@ATTRIBUTE fila_fantasma_1 NUMERIC\n@ATTRIBUTE columna_fantasma_2 NUMERIC\n@ATTRIBUTE fila_fantasma_2 NUMERIC\n@ATTRIBUTE columna_fantasma_3 NUMERIC\n@ATTRIBUTE fila_fantasma_3 NUMERIC\n@ATTRIBUTE columna_fantasma_4 NUMERIC\n@ATTRIBUTE fila_fantasma_4 NUMERIC\n@ATTRIBUTE dist_1 NUMERIC\n@ATTRIBUTE dist_2 NUMERIC\n@ATTRIBUTE dist_3 NUMERIC\n@ATTRIBUTE dist_4 NUMERIC\n@ATTRIBUTE columna_fantasma_mas_cercano NUMERIC\n@ATTRIBUTE fila_fantasma_mas_cercano NUMERIC\n@ATTRIBUTE dist_columna_fantasma_cercano NUMERIC\n@ATTRIBUTE dist_fila_fantasma_cercano NUMERIC\n@ATTRIBUTE dist_fantasma_cercano NUMERIC\n@ATTRIBUTE num_comida NUMERIC\n@ATTRIBUTE dist_comida NUMERIC\n@ATTRIBUTE isWallNorth {False, True}\n@ATTRIBUTE isWallSouth {False, True}\n@ATTRIBUTE isWallEast {False, True}\n@ATTRIBUTE isWallWest {False, True}\n@ATTRIBUTE distNorth NUMERIC\n@ATTRIBUTE distSouth NUMERIC\n@ATTRIBUTE distEast NUMERIC\n@ATTRIBUTE distWest NUMERIC\n@ATTRIBUTE score NUMERIC\n@ATTRIBUTE dir_anterior_pacman {Stop, East, West, North, South}\n@ATTRIBUTE dir_pacman {Stop, East, West, North, South}\n@ATTRIBUTE next_score NUMERIC\n\n@DATA\n")
        	cabecera = True
        	fichero.close()

        if(cabecera == True):
            if(self.accionAnteriorAnterior != 0):
                if (self.instanciaAnterior != 0):
                	# self.accionAnteriorAnterior = dir_pacman
                	fichero = open("info.arff", "a+")
                	fichero.write(self.instanciaAnterior + ',' + self.accionAnteriorAnterior + ',' + self.accionAnterior + ',' + score + '\n')
                	fichero.close()
                	self.accionAnteriorAnterior = self.accionAnterior
                	self.instanciaAnterior = columna_pacman + ',' + fila_pacman + ',' + num_fantasmas + ',' + num_fantasmas_vivos + ',' + columna_fantasma_1 + ',' + fila_fantasma_1+ ',' + columna_fantasma_2 + ',' + fila_fantasma_2 + ',' + columna_fantasma_3 + ',' + fila_fantasma_3 + ',' + columna_fantasma_4 + ',' + fila_fantasma_4 + ',' + dist_1 + ',' + dist_2 + ',' + dist_3 + ',' + dist_4 + ',' + columna_fantasma_mas_cercano + ',' + fila_fantasma_mas_cercano + ',' + dist_columna_fantasma_cercano + ',' + dist_fila_fantasma_cercano + ','+  dist_fantasma_cercano + ',' + num_comida + ',' + dist_comida + ',' + isWallNorth + ',' + isWallSouth + ',' + isWallEast + ',' + isWallWest + ',' + distNorth + ',' + distSouth + ',' + distEast + ',' + distWest + ',' + score
                	self.accionAnterior = dir_pacman
                else:
                	self.instanciaAnterior = columna_pacman + ',' + fila_pacman + ',' + num_fantasmas + ',' + num_fantasmas_vivos + ',' + columna_fantasma_1 + ',' + fila_fantasma_1+ ',' + columna_fantasma_2 + ',' + fila_fantasma_2 + ',' + columna_fantasma_3 + ',' + fila_fantasma_3 + ',' + columna_fantasma_4 + ',' + fila_fantasma_4 + ',' + dist_1 + ',' + dist_2 + ',' + dist_3 + ',' + dist_4 + ',' + columna_fantasma_mas_cercano + ',' + fila_fantasma_mas_cercano + ',' + dist_columna_fantasma_cercano + ',' + dist_fila_fantasma_cercano + ','+  dist_fantasma_cercano + ',' + num_comida + ',' + dist_comida + ',' + isWallNorth + ',' + isWallSouth + ',' + isWallEast + ',' + isWallWest + ',' + distNorth + ',' + distSouth + ',' + distEast + ',' + distWest + ',' + score
                	self.accionAnterior = dir_pacman
            else:
            	self.accionAnteriorAnterior = dir_pacman

            
        	
       

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
    	self.countActions = self.countActions + 1
        self.printInfo(gameState)
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

    	dist_manhattan = []

    	#para cada fantasmas calculamos la distancia de manhattan
    	for i in gameState.getGhostPositions():
    		dist_manhattan.append(self.distancer.getDistance(gameState.getPacmanPosition(), i))
    	#ordenar la lista y coger la distancia mas pequena
    	dist_manhattan_menor = sorted(dist_manhattan)[0]

    	for i in range(len(dist_manhattan)):
            if dist_manhattan[i] == dist_manhattan_menor:
            	pos = gameState.getGhostPositions()[i]

    	dist_acciones = []

    	for accion in gameState.getLegalActions():
    		dist_acciones.append(self.distancer.getDistance(Actions.getSuccessor(gameState.getPacmanPosition(), accion), pos))

    	dist_accion_menor = sorted(dist_acciones)[0]

    	for i in range(len(dist_acciones)):
            if dist_acciones[i] == dist_accion_menor:
            	return gameState.getLegalActions()[i]

    def printLineData(self, gameState):
        # POSICION DE PACMAN
        columna_pacman = str(gameState.getPacmanPosition()[0])
        fila_pacman = str(gameState.getPacmanPosition()[1])
        
        # NUMERO DE FANTASMAS (SIEMPRE ES 4 ES IRRELEVANTE)
        num_fantasmas = str(gameState.getNumAgents() - 1)
        
        # NUMERO DE FANTASMAS VIVOS
        num_fantasmas_vivos = 0
        for fantasma in gameState.getLivingGhosts():
            if fantasma: 
                num_fantasmas_vivos = num_fantasmas_vivos + 1
        num_fantasmas_vivos = str(num_fantasmas_vivos)
        # num_fantasmas_vivos = sum([int(g) for g in gameState.getLivingGhosts()])
        
        # POSICION FANTASMA 1
        columna_fantasma_1 = str(gameState.getGhostPositions()[0][0])
        fila_fantasma_1 = str(gameState.getGhostPositions()[0][1])
        
        # POSICION FANTASMA 2
        columna_fantasma_2 = str(gameState.getGhostPositions()[1][0])
        fila_fantasma_2 = str(gameState.getGhostPositions()[1][1])
        
        # POSICION FANTASMA 3
        columna_fantasma_3 = str(gameState.getGhostPositions()[2][0])
        fila_fantasma_3 = str(gameState.getGhostPositions()[2][1])
        
        # POSICION FANTASMA 4
        columna_fantasma_4 = str(gameState.getGhostPositions()[3][0])
        fila_fantasma_4 = str(gameState.getGhostPositions()[3][1])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 1
        dist_1 = str(gameState.data.ghostDistances[0])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 2
        dist_2 = str(gameState.data.ghostDistances[1])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 3
        dist_3 = str(gameState.data.ghostDistances[2])
        
        # DISTANCIA DE MANHATTAN AL FANTASMA 4
        dist_4 = str(gameState.data.ghostDistances[3])
        
        # ORDENAR LISTA DE DISTANCIAS
        cont = 0
        ghostsDistances = gameState.data.ghostDistances
        for i in range(len(ghostsDistances)):
            if ghostsDistances[i] < 0:
                ghostsDistances.pop(i)
                ghostsDistances.insert(i, -1)
        ghostsDistancesSorted = sorted(ghostsDistances) # ORDENAR LA LISTA DE DISTANCIAS 
        for i in range(len(ghostsDistancesSorted)):
            if ghostsDistancesSorted[i] == -1:
                cont = cont + 1
        pos = ghostsDistances.index(ghostsDistancesSorted[cont]) # ELEGIR EL INDICE CORRESPONDIENTE A LA DISTANCIA MAS PEQUENA
        
        #POSICION FANTASMA MAS CERCANO
        columna_fantasma_mas_cercano = str(gameState.getGhostPositions()[pos][0])
        fila_fantasma_mas_cercano = str(gameState.getGhostPositions()[pos][1])

        # DISTANCIA EN COLUMNAS AL FANTASMA MAS CERCANO
        dist_columna_fantasma_cercano = str(abs((gameState.getPacmanPosition()[0])-(gameState.getGhostPositions()[pos][0])))
        # DISTANCIA EN FILAS AL FANTASMA MAS CERCANO
        dist_fila_fantasma_cercano = str(abs((gameState.getPacmanPosition()[1])-(gameState.getGhostPositions()[pos][1])))
        #DISTANCIA DE MANHATTAN AL FANTASMA MAS CERCANO
        dist_fantasma_cercano = str((abs((gameState.getPacmanPosition()[0])-(gameState.getGhostPositions()[pos][0])))+(abs((gameState.getPacmanPosition()[1])-(gameState.getGhostPositions()[pos][1]))))

        # PUNTOS DE COMIDA RESTANTES
        num_comida = str(gameState.getNumFood())
        
        # DISTANCIA DE MANHATTAN A LA COMIDA MAS CERCANA
        dist_comida = str(gameState.getDistanceNearestFood())

        # PAREDES
        isWallNorth = str(gameState.getWalls()[gameState.getPacmanPosition()[0]][gameState.getPacmanPosition()[1]+1])
        isWallSouth = str(gameState.getWalls()[gameState.getPacmanPosition()[0]][gameState.getPacmanPosition()[1]-1])
        isWallEast = str(gameState.getWalls()[gameState.getPacmanPosition()[0]+1][gameState.getPacmanPosition()[1]])
        isWallWest = str(gameState.getWalls()[gameState.getPacmanPosition()[0]-1][gameState.getPacmanPosition()[1]])

        # DISTANCIAS A LAS PAREDES MAS CERCANAS
        aux_columna_pacman = gameState.getPacmanPosition()[0]
        aux_fila_pacman = gameState.getPacmanPosition()[1]
        aux_columna = gameState.getWalls()[aux_columna_pacman]
        lista_columna = []
        lista_norte = []
        lista_sur = []
        aux_cont = -1
        for valor in aux_columna:
        	aux_cont = aux_cont + 1
        	if(valor == True):
        		lista_columna.append(aux_cont)
        for numero in lista_columna:
        	if(numero < aux_fila_pacman):
        		lista_sur.append(numero)
        	if(numero > aux_fila_pacman):
        		lista_norte.append(numero)
        pos_North_cercano = sorted(lista_norte)[0] # lista norte nos quedamos con el mas pequeno
        pos_South_cercano = sorted(lista_sur, reverse = True)[0] # lista sur nos quedamos con el mas grande
        distNorth = str(abs(pos_North_cercano - aux_fila_pacman))
        distSouth = str(abs(pos_South_cercano - aux_fila_pacman))
    
        lista_fila = []
        lista_este = []
        lista_oeste = []
        num_columna = -1
        num_fila = -1
        lista_mapa = []
        for valor in gameState.getWalls():
        	lista_mapa.append(valor)
        # imprime las columnas de 0 a x
        # i representa la columna
        # j representa la fila
        # almacenamos la columna en la que se encuentran las paredes, la fila es la misma que la del pacman
        for i in range(len(lista_mapa)):
        	for j in range(len(lista_mapa[i])):
        		if(lista_mapa[i][j] == True and j == aux_fila_pacman):
        			lista_fila.append(i)
        for numero in lista_fila:
        	if(numero < aux_columna_pacman):
        		lista_oeste.append(numero)
        	if(numero > aux_columna_pacman):
        		lista_este.append(numero)
        pos_East_cercano = sorted(lista_este)[0] # lista este nos quedamos con el mas pequeno
        pos_West_cercano = sorted(lista_oeste, reverse = True)[0] # lista oeste nos quedamos con el mas grande
        distEast = str(abs(pos_East_cercano - aux_columna_pacman))
        distWest = str(abs(pos_West_cercano - aux_columna_pacman))


        # PUNTUACION
        score = str(gameState.getScore())
        
        # DIRECCION DE PACMAN
        dir_pacman = str(gameState.data.agentStates[0].getDirection())
        

        if dist_1 == "None":
        	dist_1 = "-1"
        if dist_2 == "None":
        	dist_2 = "-1"
        if dist_3 == "None":
        	dist_3 = "-1"
        if dist_4 == "None":
        	dist_4 = "-1"
        if dist_comida == "None":
        	dist_comida = "-1"

        cabecera = False

        try: 
        	fichero = open("info.arff", "a+")
        	#print "EL FICHERO EXISTE"
        	palabra = "@RELATION"
        	lineas = fichero.readlines()
        	if lineas[0] == "@RELATION pacman\n":
        		#print "EXISTE LA CABECERA"
        		cabecera = True
        	fichero.close()
        except:
        	#print "EL FICHERO NO EXISTE"
        	fichero = open("info.arff", "a+")
        	fichero.write("@RELATION pacman\n\n@ATTRIBUTE columna_pacman NUMERIC\n@ATTRIBUTE fila_pacman NUMERIC\n@ATTRIBUTE num_fantasmas NUMERIC\n@ATTRIBUTE num_fantasmas_vivos NUMERIC\n@ATTRIBUTE columna_fantasma_1 NUMERIC\n@ATTRIBUTE fila_fantasma_1 NUMERIC\n@ATTRIBUTE columna_fantasma_2 NUMERIC\n@ATTRIBUTE fila_fantasma_2 NUMERIC\n@ATTRIBUTE columna_fantasma_3 NUMERIC\n@ATTRIBUTE fila_fantasma_3 NUMERIC\n@ATTRIBUTE columna_fantasma_4 NUMERIC\n@ATTRIBUTE fila_fantasma_4 NUMERIC\n@ATTRIBUTE dist_1 NUMERIC\n@ATTRIBUTE dist_2 NUMERIC\n@ATTRIBUTE dist_3 NUMERIC\n@ATTRIBUTE dist_4 NUMERIC\n@ATTRIBUTE columna_fantasma_mas_cercano NUMERIC\n@ATTRIBUTE fila_fantasma_mas_cercano NUMERIC\n@ATTRIBUTE dist_columna_fantasma_cercano NUMERIC\n@ATTRIBUTE dist_fila_fantasma_cercano NUMERIC\n@ATTRIBUTE dist_fantasma_cercano NUMERIC\n@ATTRIBUTE num_comida NUMERIC\n@ATTRIBUTE dist_comida NUMERIC\n@ATTRIBUTE isWallNorth {False, True}\n@ATTRIBUTE isWallSouth {False, True}\n@ATTRIBUTE isWallEast {False, True}\n@ATTRIBUTE isWallWest {False, True}\n@ATTRIBUTE distNorth NUMERIC\n@ATTRIBUTE distSouth NUMERIC\n@ATTRIBUTE distEast NUMERIC\n@ATTRIBUTE distWest NUMERIC\n@ATTRIBUTE score NUMERIC\n@ATTRIBUTE dir_anterior_pacman {Stop, East, West, North, South}\n@ATTRIBUTE dir_pacman {Stop, East, West, North, South}\n@ATTRIBUTE next_score NUMERIC\n\n@DATA\n")
        	cabecera = True
        	fichero.close()

        if(cabecera == True):
            if(self.accionAnteriorAnterior != 0):
                if (self.instanciaAnterior != 0):
                	# self.accionAnteriorAnterior = dir_pacman
                	fichero = open("info.arff", "a+")
                	fichero.write(self.instanciaAnterior + ',' + self.accionAnteriorAnterior + ',' + self.accionAnterior + ',' + score + '\n')
                	fichero.close()
                	self.accionAnteriorAnterior = self.accionAnterior
                	self.instanciaAnterior = columna_pacman + ',' + fila_pacman + ',' + num_fantasmas + ',' + num_fantasmas_vivos + ',' + columna_fantasma_1 + ',' + fila_fantasma_1+ ',' + columna_fantasma_2 + ',' + fila_fantasma_2 + ',' + columna_fantasma_3 + ',' + fila_fantasma_3 + ',' + columna_fantasma_4 + ',' + fila_fantasma_4 + ',' + dist_1 + ',' + dist_2 + ',' + dist_3 + ',' + dist_4 + ',' + columna_fantasma_mas_cercano + ',' + fila_fantasma_mas_cercano + ',' + dist_columna_fantasma_cercano + ',' + dist_fila_fantasma_cercano + ','+  dist_fantasma_cercano + ',' + num_comida + ',' + dist_comida + ',' + isWallNorth + ',' + isWallSouth + ',' + isWallEast + ',' + isWallWest + ',' + distNorth + ',' + distSouth + ',' + distEast + ',' + distWest + ',' + score
                	self.accionAnterior = dir_pacman
                else:
                	self.instanciaAnterior = columna_pacman + ',' + fila_pacman + ',' + num_fantasmas + ',' + num_fantasmas_vivos + ',' + columna_fantasma_1 + ',' + fila_fantasma_1+ ',' + columna_fantasma_2 + ',' + fila_fantasma_2 + ',' + columna_fantasma_3 + ',' + fila_fantasma_3 + ',' + columna_fantasma_4 + ',' + fila_fantasma_4 + ',' + dist_1 + ',' + dist_2 + ',' + dist_3 + ',' + dist_4 + ',' + columna_fantasma_mas_cercano + ',' + fila_fantasma_mas_cercano + ',' + dist_columna_fantasma_cercano + ',' + dist_fila_fantasma_cercano + ','+  dist_fantasma_cercano + ',' + num_comida + ',' + dist_comida + ',' + isWallNorth + ',' + isWallSouth + ',' + isWallEast + ',' + isWallWest + ',' + distNorth + ',' + distSouth + ',' + distEast + ',' + distWest + ',' + score
                	self.accionAnterior = dir_pacman
            else:
            	self.accionAnteriorAnterior = dir_pacman