import os
############  THIS DOES NOT WORK###########################################################


# import xml.etree.ElementTree as ET

# xmlPath = "/home/hooman/hs_datasets/head_torso_related/shiyun_construction/00000.xml"

# tree = ET.parse(xmlPath)
# root = tree.getroot()

# # index2delete = []

# # for i in range(len(root)):
# # 	if root[i].tag == 'object':
# # 		if root[i][0].text == 'vest':
# # 			print(i)
# # 			index2delete.append(i)

# # print("len index2delete: ", len(index2delete))
# # for index in index2delete:
# # 	root.remove(root[index])
# # 	print("removed: ", index)
# # tree.write("/home/hooman/hs_datasets/head_torso_related/shiyun_construction/output.xml")

# for objectt in root.iter('object'):
# 	if objectt[0] == 'vest':
# 		tree.remove(objectt)
# 		# parent=objectt.getparent()
# 		# parent.remove(objectt)

# tree.write("/home/hooman/hs_datasets/head_torso_related/shiyun_construction/output.xml")
####################################################################################################


################################THIS WORKS ###############################################
'''
xmlPath = "/home/hooman/hs_datasets/head_torso_related/shiyun_construction/00000.xml"

in_file = open(xmlPath, "r")
out_file = open("/home/hooman/hs_datasets/head_torso_related/shiyun_construction/output.xml","w")
oldLines = in_file.readlines()
newLines = []

i = 0
while( i < len(oldLines)-1 ):
	if "vest" in oldLines[i+1]:
		i = i + 12
	else:
		if 'hat' in oldLines[i]:
			newLines.append( oldLines[i].replace('hat', 'head') )
		elif 'noHat' in oldLines[i]:
			newLines.append( oldLines[i].replace('noHat', 'head') )
		else:
			newLines.append( oldLines[i] )
		
		i = i + 1

		

newLines.append(oldLines[-1])

out_file.writelines(newLines)
'''
####################################################################################################

####################################################################################################
#this removes vest, NoVast classes and changes hat, NoHat to head.

path2Input = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/round3/Annotations_vest-hat_xml/"
path2Output = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/round3/Annotations_person-head_xml/"

for fileName in os.listdir(path2Input):
	in_file = open(path2Input + fileName, "r")

	oldLines = in_file.readlines()
	newLines = []

	i = 0
	while( i < len(oldLines)-1 ):
		if ("vest" in oldLines[i+1]) or ("noVest" in oldLines[i+1]) or ("Vest" in oldLines[i+1]) or ("NoVest" in oldLines[i+1])  :
			i = i + 12
		else:
			if 'noHat' in oldLines[i]:
				newLines.append( oldLines[i].replace('noHat', 'head') )
			elif 'NoHat' in oldLines[i]:
				newLines.append( oldLines[i].replace('NoHat', 'head') )
			elif 'Hat' in oldLines[i]:
				newLines.append( oldLines[i].replace('Hat', 'head') )
			elif 'hat' in oldLines[i]:
				newLines.append( oldLines[i].replace('hat', 'head') )
			else:
				newLines.append( oldLines[i] )
			
			i = i + 1

	newLines.append(oldLines[-1])

	out_file = open(path2Output + fileName,"w")
	out_file.writelines(newLines)

####################################################################################################

####################################################################################################
#this corrects the paths
'''
path2Input = "/home/hooman/hs_datasets/head_torso_related/shiyun_construction/training_data_may2020/Test/Annotations_head_person/"
path2Output = "/home/hooman/hs_datasets/head_torso_related/shiyun_construction/training_data_may2020/Test/cor/"

for fileName in os.listdir(path2Input):
	in_file = open(path2Input + fileName, "r")
	out_file = open(path2Output + fileName,"w")

	oldLines = in_file.readlines()

	for line in oldLines:
		if "jovision_5class" in line:
			out_file.writelines(line.replace("/home/maharshi/caffe-ssd/data/jovision_5class/jovision_data/Train", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch1":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch1", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch2":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch2", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch3":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch3", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch4":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch4", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch5":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch5", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch6":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch6", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch7":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch7", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch8":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch8", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch9":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch9", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch10":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch10", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
		elif "batch11":
			out_file.writelines(line.replace("/home/victorz/Desktop/Shiyun labelling/batch11", "/home/maharshi/Vitis-AI/models/AI-Model-Zoo/caffe-xilinx/jobs/crowdFlow-resnet-ssd-560dp_training/data/training_data_may2020/Train"))
'''
####################################################################################################