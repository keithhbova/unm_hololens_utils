listOfTxtFiles = ["thermal_data_" + "{:05}".format(i) + ".jpg" for i in range(7431, 8254)]

with open("val2022.txt", "w") as file:
	for line in listOfTxtFiles:
		file.writelines("/home/firefighter/Desktop/development/datasets/yoloFlirData/images/val/" + str(line) + "\n")

listOfTxtFiles = ["thermal_data_" + "{:05}".format(i) + ".jpg" for i in range(0, 4954)]

with open("train2022.txt", "w") as file:
	for line in listOfTxtFiles:
		file.writelines("/home/firefighter/Desktop/development/datasets/yoloFlirData/images/train/" + str(line) + "\n")

listOfTxtFiles = ["thermal_data_" + "{:05}".format(i) + ".jpg" for i in range(4954,7431)]

with open("test2022.txt", "w") as file:
	for line in listOfTxtFiles:
		file.writelines("/home/firefighter/Desktop/development/datasets/yoloFlirData/images/test/" + str(line) + "\n")
