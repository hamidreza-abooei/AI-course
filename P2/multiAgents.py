# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"
        # print("All scores: ",gameState.getPacmanPosition() ,scores)
        # print("bestIndices: ",bestIndices)
        # print("LegalMoves: ", legalMoves)
        # print("choose index: ",chosenIndex,'\n')
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        width = newFood.width
        height = newFood.height
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]
        # print("startpos: ",newPos)
        # print("food: ",newFood)
        # print("gost states: ",newGhostStates)
        # print("new scared time: ",newScaredTimes[0])
        "*** YOUR CODE HERE ***"
        # print("successro game state: ",successorGameState.getScore())
        min_manhattan = width*height  # set a hig number
        newFoodList = newFood.asList()
        # print("foodlist",newFoodList)

        for foodpos in newFoodList:
            manhattandist = util.manhattanDistance(newPos, foodpos)
            if min_manhattan > manhattandist:
                min_manhattan = manhattandist
        if len(newFood.asList()) == 0:
            min_manhattan = 0
        # print("Min manhattan distance to food:",min_manhattan)
        min_manhattan_ghost = width*height
        for ghostState in newGhostStates:
            if ghostState.scaredTimer <= 1:
                manhattandist = util.manhattanDistance(
                    newPos, ghostState.getPosition())
                if min_manhattan_ghost > manhattandist:
                    min_manhattan_ghost = manhattandist
        # print("Min manhattan distance to Ghost:",min_manhattan_ghost)
        # score = 10/(min_manhattan+1) - 10/(min_manhattan_ghost+1) + 120/(len(newFoodList)+1)
        score = 10/(min_manhattan+1) - 20 / \
            (min_manhattan_ghost+1) - 10*len(newFoodList)
        # print("food")
        # sum_dist_foods = 0
        # for
        # evaluation_val =
        # print("score: ", score)
        # return successorGameState.getScore()
        return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class GamseStateMinimaxTree:
    '''This is an auxiliary class in order to make and save a tree structure.'''

    def __init__(self, gamestate, action, agentNumber, parent=None):
        '''Create a node '''
        self.gamestate = gamestate
        self.action = action
        self.agentNumber = agentNumber
        self.child = []
        self.parent = parent
        self.terminal = True

    def addchild(self, childGameState, childAction, childAgentNumber):
        '''Add new child to the current gamestateMinimaxTree'''
        self.terminal = False
        self.child.append(GamseStateMinimaxTree(
            childGameState, childAction, childAgentNumber, parent=self))

    def getGameState(self):
        return self.gamestate

    def getAction(self):
        return self.action

    def getChild(self):
        return self.child

    def getAgentNumber(self):
        return self.agentNumber

    def isTerminal(self):
        return self.terminal


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        gameStateTreeHead = GamseStateMinimaxTree(gameState, None, None)
        gameStateTreeFringe = [gameStateTreeHead]
        for idepth in range(self.depth):
            for agentNumber in range(gameState.getNumAgents()):
                nextFringe = []
                for gameStateTreeFringeItem in gameStateTreeFringe:
                    childs = self.takeOneRound(
                        gameStateTreeFringeItem, agentNumber)
                    for child in childs:
                        terminalFlag = False
                        if child.getGameState().isWin():
                            terminalFlag = True
                        if child.getGameState().isLose():
                            terminalFlag = True

                        if terminalFlag == False:
                            nextFringe.append(child)
                gameStateTreeFringe = nextFringe

        bestSequence = self.applyminimax(gameStateTreeHead)
        bestSequence.pop()
        nextMove = bestSequence.pop()
        bestAction = nextMove.getAction()

        return bestAction

    def takeOneRound(self, gameStateTree, agentNumber):
        gameState = gameStateTree.getGameState()
        legalMoves = gameState.getLegalActions(agentNumber)
        for legalMove in legalMoves:
            # Generate successor gamestate
            newGameState = gameState.generateSuccessor(agentNumber, legalMove)
            gameStateTree.addchild(newGameState, legalMove, agentNumber)

        return gameStateTree.getChild()

    def applyminimax(self, gamestateTree):
        if gamestateTree.isTerminal() == True:
            return [gamestateTree]
        children = gamestateTree.getChild()
        agentNumber = children[0].getAgentNumber()

        sequences = [self.applyminimax(child) for child in children]
        isPacman = False
        bestScore = float('inf')
        if agentNumber == 0:
            isPacman = True
            bestScore = -bestScore
        bestSequence = None
        # Min-Max sequence selection.
        for sequence in sequences:
            if isPacman:
                sequenceScore = self.evaluationFunction(
                    sequence[0].getGameState())
                if sequenceScore > bestScore:
                    bestScore = sequenceScore
                    bestSequence = sequence
            else:
                sequenceScore = self.evaluationFunction(
                    sequence[0].getGameState())
                if sequenceScore < bestScore:
                    bestScore = sequenceScore
                    bestSequence = sequence
        bestSequence.append(gamestateTree)
        return bestSequence


class MinimaxAlphaBeta:
    def __init__(self, gameState):
        self.gameState = gameState


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        v, action = self.treeBuilder(
            gameState, 0, 0, -float('inf'), float('inf'))
        return action
        util.raiseNotDefined()

    def treeBuilder(self, gameState, depth, agent, alpha, beta):
        numAgents = gameState.getNumAgents()
        if (depth >= self.depth-1) and (agent >= numAgents):   # Terminal
            # None is the best Action any node need to take to get the best res
            return self.evaluationFunction(gameState), None

        if gameState.isWin():       # Terminal
            return self.evaluationFunction(gameState), None

        if gameState.isLose():      # Terminal
            return self.evaluationFunction(gameState), None

        if (agent >= numAgents):
            agent = agent - numAgents
            depth = depth + 1

        # We don't need all the sequence. All we need to keep is the HEAD action
        if agent == 0:
            v, action = self.max_value(gameState, alpha, beta, depth, agent)
        else:
            v, action = self.min_value(gameState, alpha, beta, depth, agent)
        return v, action

    def max_value(self, state, alpha, beta, depth, agent):
        v = -float('inf')
        legalMoves = state.getLegalActions(agent)
        reserveBestLegalMove = None
        for legalMove in legalMoves:
            childGameState = state.generateSuccessor(agent, legalMove)
            successorVal, action = self.treeBuilder(
                childGameState, depth, agent + 1, alpha, beta)
            if v < successorVal:
                v = successorVal
                reserveBestLegalMove = legalMove
            if v > beta:
                return v, reserveBestLegalMove
            alpha = max(alpha, v)

        return v, reserveBestLegalMove

    def min_value(self, state, alpha, beta, depth, agent):
        v = +float('inf')
        legalMoves = state.getLegalActions(agent)
        reserveBestLegalMove = None
        for legalMove in legalMoves:
            childGameState = state.generateSuccessor(agent, legalMove)
            successorVal, action = self.treeBuilder(
                childGameState, depth, agent + 1, alpha, beta)
            if v > successorVal:
                v = successorVal
                reserveBestLegalMove = legalMove
            if v < alpha:
                return v, reserveBestLegalMove
            beta = min(beta, v)
        return v, reserveBestLegalMove


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    Don't forget to use pacmanPosition, foods, scaredTimers, ghostPositions!
    DESCRIPTION: <write something here so we know what you did>
    """

    pacmanPosition = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimers = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
