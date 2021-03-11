# -*- coding: utf-8 -*-
"""
Complete this code for continuous optimization  problem

Please remove author name if generated by machine automatically
Keep you code anonymous

"""

# Use standard python package only.
import math
import numpy as np
import matplotlib as plt
from numpy import random





# MINIMUM GLOBAL VARIABLES TO BE USED
POPULATION_SIZE = 50 # Change POPULATION_SIZE to obtain better fitness.

GENERATIONS = 1000# Change GENERATIONS to obtain better fitness.
SOLUTION_FOUND = False

CORSSOVER_RATE = 0.8 # Change CORSSOVER_RATE  to obtain better fitness.
MUTATION_RATE = 0.2# Change MUTATION_RATE to obtain better fitness.

GENE_LENGTH = 4

UPPER_BOUND = 10
LOWER_BOUND = -10

# MINIMUM FUNCTIONS TO BE USED IN YOU COURSEWORK
def generate_population():

    population = []
    #population = random.uniform(LOWER_BOUND, UPPER_BOUND, size=(POPULATION_SIZE, GENE_LENGTH))
    population = random.randint(LOWER_BOUND, UPPER_BOUND, size=(POPULATION_SIZE, GENE_LENGTH))
    #population = np.round(population)
    #population = float(population)
    population = population.tolist()
  
    return population


def compute_fitness(individual):
    # fitness function used - sum squares function
    # using for a minimisation problem where the goal is to get 0
    n = len(individual)
    fitness = 0
    for j in range(0,n):
     
       fitness = fitness + (j+1)*individual[j]**2
    #print("right method\)
    return fitness

def compute_fitnessDixon(individual):
    # fitness function used - sum squares function
    # using for a minimisation problem where the goal is to get 0
    n = len(individual)
    fitness = 0
    for j in range(1,n):
       fitness =fitness+(j+1)*(2*individual[j]**2-individual[j-1])**2
    fitnes = fitness+(individual[0]-1)**2;
    return fitness

def compute_fitnessLevy(individual):
    n = len(individual)
    fitness = 0
    z= []
    for j in range(0,n):
       z.append(1+(individual[j]-1)/4)
    s = np.sin(np.pi*z[0])**2;
    for i in range(0,n-1):
        s = s+(z[i]-1)**2*(1+10*(np.sin(np.pi*z[i]+1))**2)
    fitness =  s+(z[n-1]-1)**2*(1+(np.sin(2*np.pi*z[n-1]))**2)
   # print ("ans " + str(fitness))
    return fitness


def compute_fitnessZakharov(individual):
    n = len(individual)
    fitness = 0
    sum1 = 0
    sum2 = 0
    for j in range(0,n):
        sum1 = sum1+individual[j] ** 2;
        sum2 = sum2+((j+1)*individual[j])/2;
    fitness = sum1 +sum2**2 + sum2**4;
    return fitness

def compute_fitnessPerm(individual):
    n = len(individual)
    b = 0.5
    fitness = 0
    j = np.arange( 1., n+1 )
    xbyj = np.fabs(individual) / j
    return sum([ sum( (j**k + b) * ((individual / j) ** k - 1) ) **2
             for k in j ])

def compute_fitnessAckley(individual):
    # ValueError if any NaN or Inf
    n = len(individual)
    a=20 
    b=0.2 
    c=2*np.pi
    sum1 = 0 
    sum2 = 0
    for i in range(0, n):
        sum1 = sum1 + individual[i]**2 
        sum2 = sum2 + np.cos( c * individual[i])
   
    return -a*np.exp( -b*np.sqrt( sum1 / n )) - np.exp( sum2 / n ) + a + np.exp(1)

def selection(population, method):
    # need to decide on an operation more appropriete
    individual = [] 
    for i in (population):
       if method == 0:
        individual.append(compute_fitness(i));
       elif method == 1:
        individual.append(compute_fitnessDixon(i));
       elif method == 2:
        individual.append(compute_fitnessLevy(i));
       elif method == 3:
        individual.append(compute_fitnessZakharov(i));
       elif method == 4:
        individual.append(compute_fitnessPerm(i));
       elif method == 5:
        individual.append(compute_fitnessAckley(i));
    return individual
    

def crossover(first_parent, second_parent):
    #implimenting single point crossover recombination
    individual = []
    crossProb = random.random() 
    if crossProb < CORSSOVER_RATE:
        pos = random.randint(0,GENE_LENGTH-1)
        individual.append(first_parent[:pos] +  second_parent[pos:])
        individual.append(first_parent[pos:] +  second_parent[:pos])
        return individual
    else:
        individual.append(first_parent)
        individual.append(second_parent)
        return individual
        


def mutation(individual):
    #need to glabalise the mutation bounds 
    # single bit point mutation
    if random.random() < MUTATION_RATE:
        posRng = random.randint(0,np.size(individual) -1)
        newMut = random.randint(LOWER_BOUND, UPPER_BOUND)
        #newMut = random.uniform(LOWER_BOUND, UPPER_BOUND)
        while newMut == individual[posRng]:
            newMut = random.randint(LOWER_BOUND, UPPER_BOUND)
        individual[posRng] = newMut
    return individual

def randSelc(fitness):
    parentsPos = []
    testFit = fitness.copy()
    testFit.sort()
    testFit2 = fitness.copy()
    testFit2.sort(reverse = True)
    for i in range(0,len(fitness)):
        posRng = random.uniform(0,sum(fitness));
        rngSum = 0
        found = False
        cnt = 0
        while found == False:
            rngSum = rngSum + testFit2[cnt]
            if rngSum >= posRng:
                parentsPos.append(fitness.index(testFit[cnt]))
                found = True
            cnt = cnt + 1
    return parentsPos

def findParents(fitness):
    #selection with to find values with lowest zeros 
    #creates a list with the indexs of the genes from greatest fitness to lowest fitness
     parentsIndex = []
     orderedVal = []     
     orderedVal = fitness.copy()
     orderedVal.sort()
   #  print( "best fitness" + str(orderedVal[0]) + "\n")
     for j in range (0, np.size(orderedVal)):
        for i in range(0,np.size(fitness)):
             if  fitness[i] == orderedVal[j]:
                 if i not in parentsIndex:
                    parentsIndex.append(i);
                    break;
     
     return parentsIndex


def next_generation(previous_population):
    fitness = selection(previous_population)
    parents = findParents(fitness)
    
    next_generation = []
    parentPos = 0;
    while parentPos < len(previous_population):
        children = crossover(previous_population[parents[parentPos]],previous_population[parents[parentPos + 1]])
        if children != None:
            next_generation.append(children[0])
            next_generation.append(children[1])
        parentPos = parentPos + 2
    
    mutatedPopulation = []
    for i in next_generation.copy():
         mutatedPopulation.append(mutation(i))
    #print (" next gen " + str(mutatedPopulation) + "\n")
    return mutatedPopulation


def bounds(type):
    global UPPER_BOUND
    global LOWER_BOUND
    if (type == 3):#Zakharov
        UPPER_BOUND = 10
        LOWER_BOUND = -5
    elif (type == 4): #perm
        UPPER_BOUND = GENE_LENGTH + 1
        LOWER_BOUND = -GENE_LENGTH
        
    elif (type == 5): #ackely 
        UPPER_BOUND = 30
        LOWER_BOUND = -15
    else: #sum squares, levy, dixon and price
        UPPER_BOUND = 10
        LOWER_BOUND = -10
   
def settings():
    global CORSSOVER_RATE
    global MUTATION_RATE 
    global GENE_LENGTH
    global POPULATION_SIZE
    global GENERATIONS
    complete = False
    while complete == False:
        print("what Crossover Rate do you want? \n")
        inp = input()
        CORSSOVER_RATE = float(inp)

        print("what Mutation Rate do you want? \n")
        inp = input()
        MUTATION_RATE = float(inp)

        print("what Gene Length do you want? \n")
        inp = input()
        GENE_LENGTH = float(inp)

        print("What Population Size do you want? \n")
        inp = input()
        POPULATION_SIZE = float(inp)

        print("How many Generation do you want? \n")
        inp = input()
        GENERATIONS = float(inp)
        complete = True

def cbaSettings():
    global CORSSOVER_RATE
    global MUTATION_RATE 
    global GENE_LENGTH
    global POPULATION_SIZE
    global GENERATIONS
    CORSSOVER_RATE = 1
    MUTATION_RATE = 0.025
    GENE_LENGTH = 50
    POPULATION_SIZE = 125
    GENERATIONS = 10000

def runGa(type):
    global SOLUTION_FOUND
    global LOWER_BOUND
    global UPPER_BOUND
    SOLUTION_FOUND = False
    selec = 2
    cbaSettings()
    bounds(type)
    print("type {}".format(type))
    currentGeneration = 0
    currentBest = 0
    currentBestFit = 90000000
    currentBestGen= 0
    population = generate_population()
    print("population{}\n".format(population))
    
    while (SOLUTION_FOUND == False): 
        fitness = selection(population,type)
        if selec == 1:
            parents = findParents(fitness)
        elif selec == 2:
            parents = randSelc(fitness)
        if fitness[parents[0]] < currentBestFit:
            currentBestFit = fitness[parents[0]]
            currentBest = population[parents[0]]
            currentBestGen = currentGeneration
        if 0 in fitness:
                SOLUTION_FOUND = True
                print ("The solution is " + str(population[fitness.index(0)]) + " in " + str(currentGeneration) + " generations\n")
        elif currentBestFit< 0.000000000001:
                SOLUTION_FOUND = True
                print ("The solution is " + str(currentBest) + " in " + str(currentGeneration) + " generations\n")
        elif currentGeneration >= GENERATIONS:
                print ("The solution was not found\n ")

                print("last population {}\n Last gen best fitness {}\n \n ".format(population, fitness[ parents[0]]))
                fitness.sort()
                print("fitness {}\n\n".format(fitness))
                print ("The closest solution is {} with a fitness of {} in gen {}\n".format(currentBest, currentBestFit , currentBestGen))
                break;
        next_generation = []
        parentPos = 0;
        while parentPos < len(population) - 1:
            children = crossover(population[parents[parentPos]],population[parents[parentPos + 1]])
            next_generation.append(children[0])
            next_generation.append(children[1])
            parentPos = parentPos + 2
    
        mutatedPopulation = []
        for i in next_generation.copy():
             mutatedPopulation.append(mutation(i))
        population = mutatedPopulation
        currentGeneration = currentGeneration + 1
    return currentBestGen

# USE THIS MAIN FUNCTION TO COMPLETE YOUR CODE - MAKE SURE IT WILL RUN FROM COMOND LINE   
def main(): 
    end = False
    print ("Welcome to continuous distribution gentic algorithm sim! \n") 
    print("Which problem do you want to solve?\nSum square = 1\nDixon and Price = 2\nLevy = 3\nZakharov = 4\nPerm = 5\nAckley = 6 \nExit = 0\n\nPlease input you selection below:\n")
    while end == False:
        inp = input()
        if inp == "1":
            result = []
            for i in range(0,10):
                result.append(runGa(0))
            print("final Result {}".format(result))
        elif inp == "2":
            runGa(1)
        elif inp == "3":
            result = []
            for i in range(0,10):
                result.append(runGa(2))
            print("final Result {}".format(result))
        elif inp == "4":
            result = []
            for i in range(0,10):
                result.append(runGa(3))
            
            print("final Result {}".format(result))
        elif inp == "5":
            runGa(4)
        elif inp == "6":
            result = []
            for i in range(0,10):
                result.append(runGa(5))
            print("final Result {}".format(result))
        elif inp == "7":
            print("test Fitness {}".format(int(compute_fitnessAckley([0,0]))))
        elif inp == "0":
            print("Thank you for using this sim\n")
            end =  True
        else:
            print("please type a valid input \n")

if __name__ == '__main__': 
    main() 
    