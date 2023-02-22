listOfTxtFiles = ["thermal_data_" + "{:05}".format(i) + ".jpg" for i in range(1200, 1800)]

with open("val2022.txt", "w") as file:
	for line in listOfTxtFiles:
		file.writelines("/home/keithhbova/Desktop/development/datasets/yoloFlirData/images/val/" + str(line) + "\n")
		
listOfTxtFiles = ["thermal_data_" + "{:05}".format(i) + ".jpg" for i in range(1800, 6000)]

with open("train2022.txt", "w") as file:
	for line in listOfTxtFiles:
		file.writelines("/home/keithhbova/Desktop/development/datasets/yoloFlirData/images/train/" + str(line) + "\n")
		
listOfTxtFiles = ["thermal_data_" + "{:05}".format(i) + ".jpg" for i in range(1200)]

with open("test2022.txt", "w") as file:
	for line in listOfTxtFiles:
		file.writelines("/home/keithhbova/Desktop/development/datasets/yoloFlirData/images/test/" + str(line) + "\n")
