import numpy as np
import math

class MA:
    def __init__(self, cities, startingCityIndex, crossRate, mutationRate, maxIterations, popSize, maxLocalSearchJump, neighbourSize, localSearchIterations, adMatrix, printGenerations):
        self.crossRate = crossRate
        self.mutationRate = mutationRate
        self.startingCityIndex = startingCityIndex
        self.maxIterations = maxIterations
        self.bestChrom = None
        self.maxFit = -float("inf")
        self.currGen = 0
        self.popSize = popSize
        self.maxLocalSearchJump = maxLocalSearchJump
        self.neighbourSize = neighbourSize
        self.localSearchIterations = localSearchIterations
        self.cities = cities
        self.pop = self.initPop()
        self.adMatrix = adMatrix
        self.printGenerations = printGenerations

    def runIterations(self, stepSize):
        if (self.printGenerations and self.currGen==0):
            print("Gen 0:")
            print(self.pop)

        if (self.currGen < self.maxIterations):
            for i in range(stepSize):
                weights = self.fitness()
                self.cycleCrossover(weights)
                self.mutate()
                # self.localSearch()
                self.currGen+=1
                if (self.printGenerations):
                    print("Gen " + str(self.currGen) + ":")
                    print(self.pop)
    #converted
    def initPop(self):
        arr = [i for i in range(len(self.cities))]
        # arr.remove(self.startingCityIndex)
        return np.array(
            [
                # np.concatenate(
                #     ([self.startingCityIndex], np.random.permutation(arr))) for x in range(self.popSize
                # )
                
                np.random.permutation(arr) for x in range(self.popSize)
                
            ]
        )

    def fitness(self):
        fitness = np.array([])

        for chrom in self.pop:
            chromFit = np.sum([self.adMatrix[chrom[i]][chrom[i+1]] for i in range(len(chrom)-1)])
            #don't questions it 👀
            chromFit = 10000000/chromFit
            fitness = np.append(fitness, chromFit)
        
        sum = np.sum(fitness)
        return (fitness)/sum
    
    def cycleCrossover(self, weights):
        newPop = []
        for doCross in np.random.rand(math.ceil(len(self.pop)/2)) <= self.crossRate:
            #np.random.choice takes two arguments. First, an array of elems to choose. Second, an array with weights with respect to the first array. Effectivley this selection acts like a roulette wheel
            parentOne = self.pop[np.random.choice(range(len(self.pop)), p=weights)]
            parentTwo  = self.pop[np.random.choice(range(len(self.pop)), p=weights)]

            startIndex = int(np.random.rand()*len(self.cities))
            if (doCross):
                #child one
                leftOverIndices = [i for i in range(len(self.cities))]
                childOne = np.zeros(len(self.cities))
                childOne[startIndex] = parentOne[startIndex]
                #numpy is weird
                currIndex = np.where(parentTwo==parentOne[startIndex])[0][0]
                leftOverIndices.remove(currIndex)
                while(currIndex!=startIndex):
                    childOne[currIndex] = parentOne[currIndex]
                    currIndex = np.where(parentTwo==parentOne[currIndex])[0][0]
                    leftOverIndices.remove(currIndex)
                for i in leftOverIndices:
                    childOne[i] = parentTwo[i]


                #child two
                leftOverIndices = [i for i in range(len(self.cities))]
                childTwo = np.zeros(len(self.cities))
                childTwo[startIndex] = parentTwo[startIndex]
                #numpy is weird
                currIndex = np.where(parentOne==parentTwo[startIndex])[0][0]
                leftOverIndices.remove(currIndex)
                while(currIndex!=startIndex):
                    childTwo[currIndex] = parentTwo[currIndex]
                    currIndex = np.where(parentOne==parentTwo[currIndex])[0][0]
                    leftOverIndices.remove(currIndex)
                for i in leftOverIndices:
                    childTwo[i] = parentOne[i]
                #add to pop
                newPop.extend([childOne, childTwo])
            else:
                newPop.extend([parentOne,parentTwo])


        if (len(self.pop)%2==1):
            newPop.pop()
        self.pop = np.array(newPop, dtype=np.int32)
    
    def mutate(self):
        for chrom in self.pop:
            if (self.mutationRate >= np.random.rand()):
                randomCityIndex = np.random.randint(len(chrom))
                randomCityIndex2 = np.random.randint(len(chrom))
                store = chrom[randomCityIndex]
                chrom[randomCityIndex] = chrom[randomCityIndex2]
                chrom[randomCityIndex2] = store
        

    def localSearch(self):
        for i in range(len(self.pop)):
            val = int(self.pop[i], 2)
            iterations = 0
            while(iterations < self.localSearchIterations):
                neighbours = self.getNeighbours(val)
                val = self.findBest(neighbours, val)
                iterations+=1
            self.pop[i]=bin(val).replace("0b","").zfill(self.strLength)
    
    def getNeighbours(self, val):
        arr = []
        for i in range(self.neighbourSize):
            add = np.random.randint(0,2)
            if (add == 1):
                arr.append(val + math.ceil(np.random.rand()*self.maxLocalSearchJump))
            else:
                arr.append(val - math.ceil(np.random.rand()*self.maxLocalSearchJump))
        return arr
    
    def getBest(self):
        bestChrom = self.pop[0]
        maxFit = np.sum([self.adMatrix[bestChrom[i]][bestChrom[i+1]] for i in range(len(bestChrom)-1)])
        for chrom in self.pop:
            chromFit = np.sum([self.adMatrix[chrom[i]][chrom[i+1]] for i in range(len(chrom)-1)])
            if (chromFit < maxFit):
                maxFit = chromFit
                bestChrom = chrom
        return bestChrom
                
        
 

    def getPop(self):
        return self.pop
    
    def getBestChrom(self):
        return self.bestChrom