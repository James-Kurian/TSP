import numpy as np
import math
from line_profiler import LineProfiler
cities = [(550.0, 250.0), (548.4229402628955, 275.06664671286086), (543.7166322257262, 299.737977432971), (535.9552971776502, 323.6249105369356), (525.2613360087728, 346.35073482034306), (511.8033988749895, 367.55705045849464), (495.7937254842823, 386.90942118573776), (477.484797949738, 404.1026485551578), (457.16535899579935, 418.865585100403), (435.15585831301456, 430.9654104932039), (411.8033988749895, 440.21130325903073), (387.476262917145, 446.4574501457377), (362.55810390586277, 449.6053456856543), (337.4418960941374, 449.6053456856543), (312.5237370828552, 446.45745014573777), (288.1966011250106, 440.21130325903073), (264.84414168698555, 430.96541049320393), (242.8346410042007, 418.865585100403), (222.51520205026205, 
404.1026485551579), (204.20627451571767, 386.9094211857377), (188.19660112501046, 367.5570504584946), (174.73866399122724, 346.35073482034295), (164.04470282234968, 323.62491053693543), (156.28336777427373, 299.7379774329708), (151.5770597371044, 275.06664671286063), (150.0, 249.99999999999974), (151.57705973710446, 224.93335328713889), (156.28336777427384, 200.26202256702874), (164.04470282234985, 176.37508946306409), (174.73866399122747, 153.6492651796566), (188.19660112501074, 132.44294954150504), (204.206274515718, 113.09057881426193), (222.51520205026236, 95.89735144484192), (242.83464100420105, 81.13441489959675), (264.8441416869859, 69.0345895067959), (288.196601125011, 59.78869674096913), (312.5237370828556, 53.54254985426218), (337.4418960941379, 50.394654314345644), (362.5581039058633, 50.39465431434573), (387.47626291714556, 53.542549854262376), (411.80339887499014, 59.7886967409695), (435.1558583130152, 69.03458950679641), (457.1653589957999, 81.13441489959737), (477.48479794973855, 95.89735144484266), (495.79372548428285, 113.09057881426284), (511.80339887498997, 132.44294954150607), (525.2613360087731, 153.64926517965773), (535.9552971776507, 176.37508946306525), (543.7166322257265, 200.26202256702996), (548.4229402628957, 224.93335328714014)]
adjacencyMatrix = []
for pos in cities:
    distances = []
    for pos2 in cities:
        distances.append( math.sqrt( ((pos2[0]-pos[0])**2) + ((pos2[1]-pos[1])**2))  )
    adjacencyMatrix.append(distances)
adMatrix = adjacencyMatrix
arr = [i for i in range(len(cities))]
pop = np.array(
        [
            np.random.permutation(arr) for x in range(1000)
        ]
    )
initPop = pop.copy()
print(len(cities))




#random city pos
# for i in range(numCities):
#     cities.append((math.ceil(np.random.rand()*700), math.ceil(np.random.rand()*500)))

#circular city pos

#gen adjacency matrix





def localSearch():
        # k-opt
        # swapping does not work if there are less than 4 cities (but like why would you even run that...)
        if (len(cities) > 3):
            for i in range(len(pop)):
                chrom = pop[i].copy()
                best = chrom.copy()
                lowestCost = np.sum([adMatrix[best[i]][best[i+1]] for i in range(len(best)-1)])
                for _ in range(len(chrom)-2):
                    vOneIndex = 0
                    vTwoIndex = 1
                    excludeIndex = 2
                    cost = adMatrix[chrom[vOneIndex]][chrom[vTwoIndex]]
                    vThreeIndex = findLowerCostExclude(chrom, chrom[vTwoIndex], cost, chrom[excludeIndex])
                    newChrom = chrom
                    hasChanged = True
                    while (vThreeIndex != -1 and hasChanged):
                        newChrom = np.array(makeArr(newChrom, vOneIndex, vTwoIndex, vThreeIndex))
                        newCost = isLower(newChrom, lowestCost) 
                        if (newCost):
                            best = newChrom
                            lowestCost = newCost
                        cost = adMatrix[newChrom[vOneIndex]][newChrom[vTwoIndex]]
                        newVThreeIndex = findLowerCostExclude(newChrom, newChrom[vTwoIndex], cost, newChrom[excludeIndex])
                        hasChanged = newVThreeIndex != vThreeIndex
                        vThreeIndex = newVThreeIndex
                    chrom = np.roll(chrom, -1)
                chrom = np.roll(chrom, -2)
                pop[i] = best

def isLower(chrom, compareCost):
    totalCost = 0
    for i in range(len(chrom)-1):
        totalCost += adMatrix[chrom[i]][chrom[i+1]]
        if (totalCost > compareCost):
            return False
    return totalCost

def makeArr(chrom, vOneIndex, vTwoIndex, vThreeIndex):
    arr = [chrom[vOneIndex]]
    arr = np.append(arr, np.flip(chrom[vTwoIndex:vThreeIndex]))
    arr = np.append(arr, chrom[vThreeIndex:])
    return arr

    # arr = chrom[vThreeIndex:]
    # arr = np.append(arr, chrom[vOneIndex])
    # arr = np.append(np.flip(chrom[vTwoIndex:vThreeIndex]), arr)
    # arr = np.roll(arr, 1)

    # arr = [chrom[vOneIndex]]
    # index = vOneIndex
    # while (index != vThreeIndex):
    #     index = (index-1)%len(chrom)
    #     arr.append(chrom[index])

    # index = vTwoIndex
    # while (index != vThreeIndex):
    #     arr.append(chrom[index])
    #     index = (index+1)%len(chrom)



def findLowerCostExclude(chrom, vertex, cost, exclude):
    for v in range(len(adMatrix)):
        if (chrom[v] != vertex and chrom[v] != exclude and adMatrix[vertex][chrom[v]] < cost):
            return v;
    return -1;
lp = LineProfiler()
test = lp(localSearch)
test()
lp.print_stats()