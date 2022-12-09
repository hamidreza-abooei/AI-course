# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    # fringe = problem.getSuccessors(problem.getStartState())
    # print("Selected next step:", fringe[0][0])
    # print("One step ahead: " ,problem.isGoalState(fringe[0][0]))
    # print("Start's successors:", problem.getSuccessors(fringe[0][0]))

    # According to the LIFO algorithm for DFS, we need Stack structure

    fringe = util.Stack()
    sequence = util.Stack()
    sequence.push((problem.getStartState(), 'Stop', 0))
    fringe.push(sequence)
    expand = fringe.pop()
    leaf = expand.pop()

    while (problem.isGoalState(leaf[0]) == False):
        successors = problem.getSuccessors(leaf[0])
        expand.push(leaf)
        for successor in successors:
            expanded_flag = False
            for leaves in expand.list:
                if (leaves[0] == successor[0]):
                    expanded_flag = True
                    break
            if (expanded_flag == False):
                # Find a new leaf
                expand.push(successor)
                # Deep copy
                expand_deep_copy = util.Stack()
                for i in expand.list:
                    expand_deep_copy.push(i)
                fringe.push(expand_deep_copy)
                expand.pop()  # prev line push successor in the end of extend. this line we reverse that

        expand = fringe.pop()
        leaf = expand.pop()

    final_sequence = []
    expand.push(leaf)
    flag_first = True
    for node in expand.list:
        if (flag_first):
            # Remove the first one because we add a leaf with beginig location, Stop Direction and zero cost.
            flag_first = False
            continue
        final_sequence.append(node[1])

    return final_sequence


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    sequence = util.Stack()
    sequence.push((problem.getStartState(), 'Stop', 0))
    fringe.push(sequence)
    expand = fringe.pop()
    leaf = expand.pop()
    expanded_nodes = []
    while (problem.isGoalState(leaf[0]) == False):
        expanded_flag = False
        for node in expanded_nodes:  # Remove nodes that been developed before
            if (node == leaf[0]):
                expanded_flag = True
        if (expanded_flag == False):
            successors = problem.getSuccessors(leaf[0])
            expanded_nodes.append(leaf[0])
            expand.push(leaf)
            for successor in successors:
                expanded_flag = False
                for leaves in expand.list:
                    if (leaves[0] == successor[0]):
                        expanded_flag = True
                        break

                if (expanded_flag == False):
                    # Find a new leaf
                    expand.push(successor)
                    # Deep copy
                    expand_deep_copy = util.Stack()
                    for i in expand.list:
                        expand_deep_copy.push(i)
                    fringe.push(expand_deep_copy)
                    expand.pop()  # prev line push successor in the end of extend. this line we reverse that

        expand = fringe.pop()
        leaf = expand.pop()

    final_sequence = []
    expand.push(leaf)
    flag_first = True
    for node in expand.list:
        if (flag_first):
            # Remove the first one because we add a leaf with beginig location, Stop Direction and zero cost.
            flag_first = False
            continue
        final_sequence.append(node[1])

    return final_sequence
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    fringe = util.PriorityQueue()
    sequence = util.Stack()
    sequence.push((problem.getStartState(), [], 0))
    fringe.push(sequence,problem.getCostOfActions([]))
    expand = fringe.pop()
    leaf = expand.pop()
    expanded_nodes = []
    while (problem.isGoalState(leaf[0]) == False):
        expanded_flag = False
        for node in expanded_nodes:  # Remove nodes that been developed before
            if (node == leaf[0]):
                expanded_flag = True
        if (expanded_flag == False):
            successors = problem.getSuccessors(leaf[0])
            expanded_nodes.append(leaf[0])
            expand.push(leaf)
            for successor in successors:
                expanded_flag = False
                for leaves in expand.list:
                    if (leaves[0] == successor[0]):
                        expanded_flag = True
                        break

                if (expanded_flag == False):
                    # Find a new leaf
                    expand.push(successor)
                    # Deep copy
                    expand_deep_copy = util.Stack()
                    actions = []
                    # flag_first = True
                    for i in expand.list:
                        expand_deep_copy.push(i)
                        actions.append(i[1])
                    actions.pop(0)
                    fringe.push(expand_deep_copy,problem.getCostOfActions(actions))
                    expand.pop()  # prev line push successor in the end of extend. this line we reverse that

        expand = fringe.pop()
        leaf = expand.pop()

    final_sequence = []
    expand.push(leaf)
    flag_first = True
    for node in expand.list:
        if (flag_first):
            # Remove the first one because we add a leaf with beginig location, Stop Direction and zero cost.
            flag_first = False
            continue
        final_sequence.append(node[1])

    return final_sequence
    # util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
