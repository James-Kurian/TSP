import numpy as np
startIndex = 5
parentOne = np.array([0,1,6,3,5,4,2])
parentTwo = np.array([0,5,6,1,3,2,4])
cities = [0,1,2,3,4,5,6]
#child one
leftOverIndices = [i for i in range(len(cities))]
childOne = np.zeros(len(cities))
childOne[startIndex] = parentOne[startIndex]

#numpy is weird
currIndex = np.where(parentTwo==parentOne[startIndex])[0][0]
while(currIndex!=startIndex):
    childOne[currIndex] = parentOne[currIndex]
    currIndex = np.where(parentTwo==parentOne[currIndex])[0][0]
    leftOverIndices.remove(currIndex)
for i in leftOverIndices:
    childOne[i] = parentTwo[i]


#child two
leftOverIndices = [i for i in range(len(cities))]
childTwo = np.zeros(len(cities))
childTwo[startIndex] = parentTwo[startIndex]
#numpy is weird
currIndex = np.where(parentOne==parentTwo[startIndex])[0][0]
while(currIndex!=startIndex):
    childTwo[currIndex] = parentTwo[currIndex]
    currIndex = np.where(parentOne==parentTwo[currIndex])[0][0]
    leftOverIndices.remove(currIndex)
for i in leftOverIndices:
    childTwo[i] = parentOne[i]
#add to pop
print(childOne)
print(childTwo)