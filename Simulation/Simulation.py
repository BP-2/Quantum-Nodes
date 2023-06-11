## Simulation to calculate average noise across linear series of trusted nodes
## BP-2
import copy
from LinearFormula import *
## Establish node system
## Going to establish node class, this is for higher level abstraction throughout program
## Each node object has a series of arcs branching from it
class Node:
    def __init__(self, name="", arcs=None, isFinalNode=False, travelled=False, nextNodes=None):
        if arcs is None:
            arcs = []
        if nextNodes is None:
            nextNodes = []
        self.name = name
        self.arcs = arcs
        self.isFinalNode = isFinalNode
        self.travelled = travelled
        self.nextNodes = nextNodes

## Each arc object has a level of quantum noise
class Arc:
    def __init__(self, noise):
        self.noise = noise

## Now lets create an example linear model

## A - .04 -> T - .03 -> T - .5 -> B

## Begin with node A (Alice)
A = Node("A")
T1 = Node("T1")
T2 = Node("T2")
B = Node("B", isFinalNode=True)

# Create arcs and connect nodes
arc1 = Arc(0.04)
A.arcs.append(arc1)
A.nextNodes.append(T1)

arc2 = Arc(0.03)
T1.arcs.append(arc2)
T1.nextNodes.append(T2)

arc3 = Arc(0.5)
T2.arcs.append(arc3)
T2.nextNodes.append(B)

## node iterator
jumpNode = A

i = 0 #counter
while jumpNode.isFinalNode == False:
  print("node " + jumpNode.name + ": " + str(jumpNode.arcs[0].noise))
  jumpNode = jumpNode.nextNodes[0]
  i += 1


## Let's use our formula to calculate the noise
linear_formula(A)




## User interface for Linear Function
## BP-2

## Allow user to construct path of nodes with noises
## Calculate average total noise
## Calculate noise at node i



print("Welcome to the Trusted Quantum Nodes Noise Simulation!")
numNodes = input("How many trusted nodes are in your network path?")


## starting node
startNode = Node("startNode", [])
## ending node
endNode = Node("endNode", [], True)

## node as iterator
jumpNodeEx = startNode
## increment variable
i = 0

## The following loop iterates over each node to be added and creates it and adds correct arc with passed noise values
while i < int(numNodes):
  ## node to be connected
  connectNode = Node("T", [])
  ## append new node
  jumpNodeEx.nextNodes.append(connectNode)
  arcNoise = float(input("Please input noise % of arc " + str(i+1)))
  ## convert to decimal from percent
  arcNoise /= 100
  ## add arcs and go to next node
  addArc = Arc(arcNoise)
  jumpNodeEx.arcs.append(addArc)
  jumpNodeEx = jumpNodeEx.nextNodes[0]
  i += 1

## This is because you will always have one more arc than nodes
arcNoise = float(input("Please input noise % of arc " + str(i+1)))
arcNoise /= 100
addArc = Arc(arcNoise)
jumpNodeEx.arcs.append(addArc)
jumpNodeEx.nextNodes.append(endNode)

print("Approximate noise percent of path: " + str(linear_formula(startNode)[0]))
