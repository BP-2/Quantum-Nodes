## Simulation to calculate average noise across linear series of trusted nodes
## BP-2
from LinearFormula import *
from Node import *

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
