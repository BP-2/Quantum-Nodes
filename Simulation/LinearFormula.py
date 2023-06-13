## Linear Formula
## BP-2

## Break up initial noise into two parts, we will iterate over these fractional representations of our good and bad bits

## To begin, we will take .04 and 1-.04 to yield a pair of (.04, and .96) or (bad, good)
def linear_formula(startingNode):
  noiseLinearPair = [startingNode.arcs[0].noise, 1 - startingNode.arcs[0].noise]
  #print(startingNode.arcs[0].noise)
  ## Next, we must calculate the effects of the ensuing noisy channel
  ## However, if a bit is reflipped, that is no longer considered "bad", and can be moved back to the good position.  If a good value is flipped, it is moved to bad.
  jumpNode = startingNode.nextNodes[0]
  
  ## performing formula over each node
  while jumpNode.isFinalNode == False:
    print(jumpNode.arcs[0].noise)
    print(jumpNode.name)
    badDiff = noiseLinearPair[0] * jumpNode.arcs[0].noise
    goodDiff = noiseLinearPair[1] * jumpNode.arcs[0].noise

    noiseLinearPair[0] -= badDiff
    noiseLinearPair[0] += goodDiff
    noiseLinearPair[1] -= goodDiff
    noiseLinearPair[1] += badDiff
    #print("Bad: " + str(noiseLinearPair[0]) + " Good: " + str(noiseLinearPair[1]))

    jumpNode = jumpNode.nextNodes[0]
  
  #print("Bad: " + str(noiseLinearPair[0]) + " Good: " + str(noiseLinearPair[1]))
  #print("Bad = Qtavg")
  return noiseLinearPair

## overloaded function with a previous value, in case you do not want the full path
def linear_formula_indexed(startingNode, previous):
  noiseLinearPair = [previous, 1 - previous]
  #print(startingNode.arcs[0].noise)
  ## Next, we must calculate the effects of the ensuing noisy channel
  ## However, if a bit is reflipped, that is no longer considered "bad", and can be moved back to the good position.  If a good value is flipped, it is moved to bad.
  jumpNode = startingNode
  ## performing formula over each node
  while jumpNode.isFinalNode == False:
    # print(jumpNode.arcs[0].noise)
    # print(jumpNode.name)
    badDiff = noiseLinearPair[0] * jumpNode.arcs[0].noise
    goodDiff = noiseLinearPair[1] * jumpNode.arcs[0].noise

    noiseLinearPair[0] -= badDiff
    noiseLinearPair[0] += goodDiff
    noiseLinearPair[1] -= goodDiff
    noiseLinearPair[1] += badDiff
    #print("Bad: " + str(noiseLinearPair[0]) + " Good: " + str(noiseLinearPair[1]))

    jumpNode = jumpNode.nextNodes[0]
  
  #print("Bad: " + str(noiseLinearPair[0]) + " Good: " + str(noiseLinearPair[1]))
  #print("Bad = Qtavg")
  return noiseLinearPair