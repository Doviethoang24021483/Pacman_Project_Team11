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
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()

        for ghostState in newGhostStates : 
              disToGhost = util.manhattanDistance(newPos, ghostState.getPosition())
              if disToGhost < 1:
                  return -999999
              elif disToGhost < 3:
                  score -= 40.0 / disToGhost 
        # 3. Tìm hạt đậu gần nhất và cộng điểm thưởng nghịch đảo

        foodList = newFood.asList()

        if len(foodList) > 0:

            minFoodDist = min([util.manhattanDistance(newPos, foodPos) for foodPos in foodList])

            score += 10.0 / minFoodDist


        if action == 'Stop':

            score -= 10
        
        return score

def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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
        bestScore = float('-inf')
        bestAction = None
        numAgents = gameState.getNumAgents()

        for action in gameState.getLegalActions(self.index):
            successor = gameState.generateSuccessor(self.index, action)
            score = self.minimax(successor, 1, self.depth, numAgents)
            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction
    
    def minimax(self, gameState: GameState, agentIndex, depth, numAgents):
        if  depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        actions = gameState.getLegalActions(agentIndex)

        nextAgentIndex = (agentIndex + 1) % numAgents
        nextDepth = depth - 1 if nextAgentIndex == 0 else depth     # mỗi khi quay lại Pacman, giảm độ sâu đi 1

        if agentIndex == 0:                                         # Pacman (max)
            bestScore = float('-inf')
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                score = self.minimax(successor, nextAgentIndex, nextDepth, numAgents)
                bestScore = max(bestScore, score)
            return bestScore
        else:                                                       # Ghost (min)
            bestScore = float('inf')
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                score = self.minimax(successor, nextAgentIndex, nextDepth, numAgents)
                bestScore = min(bestScore, score)
            return bestScore

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestScore = float('-inf')
        bestAction = None
        alpha = float('-inf')
        beta = float('inf')

        actions = gameState.getLegalActions(self.index)

        for action in actions:
            successor = gameState.generateSuccessor(self.index, action)
            score = self.alphabeta(successor, 1, self.depth, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(alpha, bestScore)

        return bestAction
    
    def alphabeta(self, gameState: GameState, agentIndex, depth, alpha, beta):
        if  depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        numAgents = gameState.getNumAgents()
        actions = gameState.getLegalActions(agentIndex)
        nextAgentIndex = (agentIndex + 1) % numAgents
        nextDepth = depth - 1 if nextAgentIndex == 0 else depth    

        if agentIndex == 0:            
            v = float('-inf')
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = max(v, self.alphabeta(successor, nextAgentIndex, nextDepth, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)                            
            return v
        else:
            v = float('inf')
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = min(v, self.alphabeta(successor, nextAgentIndex, nextDepth, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)                            
            return v  

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestScore = float('-inf')
        bestAction = None
        numAgents = gameState.getNumAgents()

        for action in gameState.getLegalActions(self.index):
            successor = gameState.generateSuccessor(self.index, action)
            score = self.expectimax(successor, 1, self.depth, numAgents)
            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction
    def expectimax(self, gameState: GameState, agentIndex, depth, numAgents):
        if  depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agentIndex)

        nextAgentIndex = (agentIndex + 1) % numAgents
        nextDepth = depth - 1 if nextAgentIndex == 0 else depth     # mỗi khi quay lại Pacman, giảm độ sâu đi 1

        if agentIndex == 0:                                         # Pacman (max)
            bestScore = float('-inf')
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                score = self.expectimax(successor, nextAgentIndex, nextDepth, numAgents)
                bestScore = max(bestScore, score)
            return bestScore
        else:                                                       # Ghost (min)
            total_bestscore = 0
            probability = 1/len(actions)
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                total_bestscore += self.expectimax(successor, nextAgentIndex, nextDepth, numAgents)
            return total_bestscore*probability

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()
    walls = currentGameState.getWalls()

    distMap = bfsPreCompute(walls,pos)

    if foodList:
        avg_x = sum([f[0] for f in foodList]) / len(foodList)
        avg_y = sum([f[1] for f in foodList]) / len(foodList)

        dist_to_center = abs(pos[0] - avg_x) + abs(pos[1] - avg_y)

        score += 1.0 / (dist_to_center + 0.1)

        minFoodDist = min(distMap.get(f, 999) for f in foodList)
        score += 1.0 / (minFoodDist + 0.1)
    score -= 10 * len(foodList)
    score -= 20 * len(capsules)
    for gs in ghostStates:
        ghostPos = gs.getPosition()

        ghostCell = (int(ghostPos[0]), int(ghostPos[1]))
        d = distMap.get(ghostCell, 999)
        if gs.scaredTimer == 0:
            if d <= 1:
                score -= 9999
            else:
                score -= 2.0 / d
        else:
            if d <= gs.scaredTimer:
                score += 100.0 / (d + 0.1)
    
    return score
    
def riskAwareEvaluationFunction(currentGameState: GameState):
    """
    Risk-aware evaluation function.

    DESCRIPTION: Extension of betterEvaluationFunction:
        1. Add a risk multiplier that decreases as the number of remaining food decreases.
        2. Penalizes states with fewer legal moves when ghosts are nearby.
        3. Penalizes states where Pacman is close to multiple active ghosts.
    """

    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    numFood = len(foodList)
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()
    walls = currentGameState.getWalls()

    distMap = bfsPreCompute(walls,pos)

    risk_multiplier = 1.0
    if numFood <= 3:
        risk_multiplier = 0.25 # Chấp nhận rủi ro cao khi sắp thắng
    elif numFood <= 10:
        risk_multiplier = 0.5 # Chấp nhận rủi ro vừa phải khi còn ít hạt đậu

    if foodList:
        avg_x = sum([f[0] for f in foodList]) / len(foodList)
        avg_y = sum([f[1] for f in foodList]) / len(foodList)
        dist_to_center = abs(pos[0] - avg_x) + abs(pos[1] - avg_y) # Khoảng cách đến trung tâm các hạt đậu
        score += 1.0 / (dist_to_center + 0.1)

        minFoodDist = min(distMap.get(f, 999) for f in foodList)
        score += 10.0 / (minFoodDist + 0.1)

    score -= 10 * numFood # Phạt dựa trên số lượng hạt đậu còn lại
    score -= 20 * len(capsules) # Phạt nhiều hơn đối với capsule

    active_ghost_dist = []

    for gs in ghostStates:
        ghostPos = gs.getPosition()
        ghostCell = (int(ghostPos[0]), int(ghostPos[1]))
        d = distMap.get(ghostCell, 999)

        if gs.scaredTimer == 0:
            active_ghost_dist.append(d)
            if d <= 1:
                score -= 9999
            elif d <= 5:
                score -= (2.0 / d) * risk_multiplier # Mức phạt tùy vào giai đoạn game
        else:
            if d <= gs.scaredTimer:
                score += 100.0 / (d + 0.1)

    active_ghost_dist.sort()

    legalMoves = currentGameState.getLegalActions(0)
    numMoves = len(legalMoves)

    if numMoves <= 2:
        if active_ghost_dist:
            closest_ghost = active_ghost_dist[0]
            if closest_ghost <= 3:
                score -= 500 * risk_multiplier # Rủi ro có ma ở gần và ít lựa chọn di chuyển

    if len(active_ghost_dist) >= 2:
        closest = active_ghost_dist[0]
        second_closest = active_ghost_dist[1]
        if closest < 5 and second_closest < 5:
            score -= 1000 * risk_multiplier # Rủi ro bị kẹp giữa 2 con ma

    return score

# Helper function for betterEvaluationFunction
dist = {}
def bfsPreCompute(walls,pos):
    if pos in dist:
        return dist[pos]
    
    queue = util.Queue()

    start_pos = pos
    queue.push(start_pos)
    
    visited = {}
    visited[start_pos] = 0
    
    while queue.isEmpty() == False:
        curr = queue.pop()
        
        for(dx, dy) in [(0,1),(1,0),(-1,0),(0,-1)]:
            next = (curr[0] + dx, curr[1] + dy)
            if next not in visited and not walls[next[0]][next[1]]:
                visited[next] = visited[curr] + 1
                queue.push(next)
    
    dist[pos] = visited
    return dist[pos]
        
# Abbreviation
better = betterEvaluationFunction
