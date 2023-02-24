import random
import os

# Defines the paths to the JPG and TXT folders
pathToJPGFolder = "Monkey_Sorted/images"
pathToTXTFolder = "Monkey_Sorted/labels"

#Number of shuffles
numShuffles = 1000

# Get lists of all the JPG and TXT files in their respective folders
jpgFiles = [f for f in os.listdir(pathToJPGFolder) if f.endswith('.jpg')]
txtFiles = [f for f in os.listdir(pathToTXTFolder) if f.endswith('.txt')]

# Check that the number of JPG and TXT files match
assert len(jpgFiles) == len(txtFiles), "Number of JPG and TXT files doesn't match!"

# Shuffle the file names numShuffles times
for _ in range(numShuffles):
    random.shuffle(jpgFiles)
    random.shuffle(txtFiles)

# Sort the files based on the numbers in their names
jpgFiles = sorted(jpgFiles, key=lambda x: int(x.split("_")[-1].split(".")[0]), reverse=True)
txtFiles = sorted(txtFiles, key=lambda x: int(x.split("_")[-1].split(".")[0]), reverse=True)

# Rename the files to match their sorted order
for i, (jpgFile, txtFile) in enumerate(zip(jpgFiles, txtFiles)):
    os.rename(os.path.join(pathToJPGFolder, jpgFile), os.path.join(pathToJPGFolder, str("thermal_data_" + "{:05}".format(i) + ".jpg")))
    os.rename(os.path.join(pathToTXTFolder, txtFile), os.path.join(pathToTXTFolder, str("thermal_data_" + "{:05}".format(i) + ".txt")))

# Print a message indicating that the shuffling and sorting is finished
print("Shuffle & Sorting Is Complete")
