import os
import math
import subprocess

pathToJPGFolder = "Monkey_Sorted/images"
pathToTXTFolder = "Monkey_Sorted/labels"


jpgFiles = [f for f in os.listdir(pathToJPGFolder) if f.endswith('.jpg')]
txtFiles = [f for f in os.listdir(pathToTXTFolder) if f.endswith('.txt')]

jpgFiles.sort()
txtFiles.sort()

sizeOfDataset:int = len(jpgFiles)
sizeOfTrain:int = int(math.floor(0.6 * sizeOfDataset))
sizeOfTest:int = int(math.floor(0.3 * sizeOfDataset))
sizeOfVal:int = sizeOfDataset - sizeOfTrain - sizeOfTest


print(str(sizeOfTrain), str(sizeOfTest), str(sizeOfVal))

trainingIndexes = [i for i in range(sizeOfTrain)]
testingIndexes = [(i + sizeOfTrain) for i in range(sizeOfTest)]
valIndexes = [(i + sizeOfTrain + sizeOfTest) for i in range(sizeOfVal)]


namesOfFilesInTrainingFolder = [str("thermal_data_" + "{:05}".format(i)) for i in trainingIndexes]
namesOfFilesInTestingFolder = [str("thermal_data_" + "{:05}".format(i)) for i in testingIndexes]
namesOfFilesInValFolder = [str("thermal_data_" + "{:05}".format(i)) for i in valIndexes]

os.makedirs("NewDataset")
os.makedirs("NewDataset/images")
os.makedirs("NewDataset/labels")
os.makedirs("NewDataset/images/train")
os.makedirs("NewDataset/images/test")
os.makedirs("NewDataset/images/val")
os.makedirs("NewDataset/labels/train")
os.makedirs("NewDataset/labels/test")
os.makedirs("NewDataset/labels/val")



for i in range(len(trainingIndexes)):
    jpgTarget = pathToJPGFolder + "/" + jpgFiles[i]
    destination = "NewDataset/images/train/" + namesOfFilesInTrainingFolder[i] + ".jpg"
    print(f"{jpgTarget}\t{destination}")
    subprocess.call(f"cp {jpgTarget} {destination}",shell=True)



    txtTarget = pathToTXTFolder + "/" + txtFiles[i]
    destination = "NewDataset/labels/train/" + namesOfFilesInTrainingFolder[i] + ".txt"
    print(f"{txtTarget}\t{destination}")
    subprocess.call(f"cp {txtTarget} {destination}",shell=True)



for i in range(len(testingIndexes)):
    jpgTarget = pathToJPGFolder + "/" + jpgFiles[i + sizeOfTrain]
    destination = "NewDataset/images/test/" + namesOfFilesInTestingFolder[i] + ".jpg"
    print(f"{jpgTarget}\t{destination}")
    subprocess.call(f"cp {jpgTarget} {destination}",shell=True)

    txtTarget = pathToTXTFolder + "/" + txtFiles[i + sizeOfTrain]
    destination = "NewDataset/labels/test/" + namesOfFilesInTestingFolder[i] + ".txt"
    print(f"{txtTarget}\t{destination}")
    subprocess.call(f"cp {txtTarget} {destination}",shell=True)


for i in range(len(valIndexes)):
    jpgTarget = pathToJPGFolder + "/" + jpgFiles[i + sizeOfTrain + sizeOfTest]
    destination = "NewDataset/images/val/" + namesOfFilesInValFolder[i] + ".jpg"
    print(f"{jpgTarget}\t{destination}")
    subprocess.call(f"cp {jpgTarget} {destination}",shell=True)


    txtTarget = pathToTXTFolder + "/" + txtFiles[i + sizeOfTrain + sizeOfTest]
    destination = "NewDataset/labels/val/" + namesOfFilesInValFolder[i] + ".txt"
    print(f"{txtTarget}\t{destination}")
    subprocess.call(f"cp {txtTarget} {destination}",shell=True)

print(sizeOfDataset)
