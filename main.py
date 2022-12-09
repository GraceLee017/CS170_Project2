# I followed Dr. Keogh's pseudocode from the Project 2 Briefing slides
import csv
import pandas as pd
import numpy as np
import copy
import time

def crossValidation(df1, current, addFeature):
    #Make all unnecessary columns 0
    tempData = copy.deepcopy(df1)
    for i in range(1,len(tempData[0])):
        if (i != addFeature) and (i not in current):
            for k in range(len(tempData)):
                tempData[k][i] = 0

    numCorrect = 0
    for index in range(len(tempData)):
        classifyObj = tempData[index][1:]
        label = tempData[index][0]
        NNDistance = np.inf
        NNlocation = np.inf

        for index1 in range(len(tempData)):
            if index != index1:
                distance = np.linalg.norm(classifyObj-tempData[index1][1:])
                if distance < NNDistance:
                    NNDistance = distance
                    NNlocation = index1
                    NNlabel = tempData[NNlocation][0]
        if label == NNlabel:
            numCorrect += 1
    accuracy = numCorrect/len(tempData)
    return accuracy


def ForwardSelection(array):
    start = time.time()
    setFeatures = []
    bestFeatures = []
    theBest = 0
    for index in range(1,len(array[0])):
        print('On the ' + str(index) + 'th level of the search tree')
        feature_added = 0
        bestAccuracy = 0
        for index1 in range(1,len(array[0])):
            if index1 not in setFeatures:
                print('-- Considering adding the ' + str(index1) + 'th feature')
                accuracy = crossValidation(array, setFeatures, index1) #change index1+1 to index1
                print('Accuracy is ' + str(accuracy))
                if accuracy > bestAccuracy:
                    bestAccuracy = accuracy
                    feature_added = index1
                
        if theBest < bestAccuracy:
            theBest = bestAccuracy
            bestFeatures.append(feature_added)     
        setFeatures.append(feature_added)
        
        print('On level ' + str(index) + ', feature ' + str(feature_added) + ' with accuracy ' + str(bestAccuracy) + ' was added to current set')

    print('The current set is ' + str(setFeatures))
    print('The set with the best accuracy is ' + str(bestFeatures) + ' with accuracy ' + str(theBest))
    print('It took ' + str(f'{(time.time() - start):.2f}') + 'secs')

def BackwardElimination(array):
    start = time.time()
    setFeatures = []
    bestFeatures = []
    theBest = 0

    for i in (range(1,len(array[0]))):
        setFeatures.append(i)
        bestFeatures.append(i)

    print(setFeatures)
    #prints accuracy for all
    accuracy = RemCrossValidation(array, setFeatures) #change index1+1 to index1
    print('Accuracy is ' + str(accuracy))
    
    for index in range(1,len(array[0])):
        print('On the ' + str(index) + 'th level of the search tree')
        feature_added = 0
        bestAccuracy = 0
        for index1 in range(1,len(array[0])):
            if index1 not in setFeatures:
                print('-- Considering adding the ' + str(index1) + 'th feature')
                accuracy = RemCrossValidation(array, setFeatures) #change index1+1 to index1
                print('Accuracy is ' + str(accuracy))
                if accuracy > bestAccuracy:
                    bestAccuracy = accuracy
                    feature_added = index1
                
        if theBest < bestAccuracy:
            theBest = bestAccuracy
            bestFeatures.append(feature_added)     
        setFeatures.append(feature_added)
        
        print('On level ' + str(index) + ', feature ' + str(feature_added) + ' with accuracy ' + str(bestAccuracy) + ' was added to current set')

    print('The current set is ' + str(setFeatures))
    print('The set with the best accuracy is ' + str(bestFeatures) + ' with accuracy ' + str(theBest))
    print('It took ' + str(f'{(time.time() - start):.2f}') + 'secs')    


def RemCrossValidation(df1, current):
    #Make all unnecessary columns 0
    tempData = copy.deepcopy(df1)
    for i in range(1,len(tempData[0])):
        if (i not in current):
            for k in range(len(tempData)):
                tempData[k][i] = 0

    numCorrect = 0
    for index in range(len(tempData)):
        classifyObj = tempData[index][1:]
        label = tempData[index][0]
        NNDistance = np.inf
        NNlocation = np.inf

        for index1 in range(len(tempData)):
            if index != index1:
                # distance = np.sqrt(sum(pow(classifyObj- tempData[index1][1:],2)))
                distance = np.linalg.norm(classifyObj-tempData[index1][1:])
                if distance < NNDistance:
                    NNDistance = distance
                    NNlocation = index1
                    NNlabel = tempData[NNlocation][0]
        if label == NNlabel:
            numCorrect += 1
    accuracy = numCorrect/len(tempData)
    return accuracy



file =  input("Which file do you want to test: ")
search = input ("1. Forward Selection \n2. Backward Elimination \nWhich algorithm do you want to run: ")

while search != '1' and search != '2':
    search = input ("1. Forward Selection \n2. Backward Elimination \nWhich algorithm do you want to run: ")

df = pd.read_csv(file, sep="  ", header = None, engine = 'python')
array = df.iloc[:,:].values

if (search == '1'):
    ForwardSelection(array)
else:
    BackwardElimination(array)