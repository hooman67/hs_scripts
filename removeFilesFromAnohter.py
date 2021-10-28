import os
pathIm = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/round4_600/jpg/"
# pathXml = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/shiyun_project/Train/Annotations_head_person/"
pathTxt = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/round4_600/Annotations_person-head_yolo/"

# pathYolo = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/shiyun_project/Train/jpegWithYoloLabels_looseHatsRemoved/"

# c_xml = 0 
# imgs = os.listdir(pathIm)
# for imgXml in os.listdir(pathXml):
# 	if(imgXml.replace("xml", "jpg") not in imgs):
# 		# print(pathXml + imgXml)
# 		# c_xml +=1
# 		os.remove(pathXml + imgXml)

# print("\n\n\n")

c_txt = 0
texts = os.listdir(pathTxt)
for imgName in os.listdir(pathIm):
	if(imgName.replace("jpg", "txt") not in texts):
		print(pathTxt + imgName.replace("jpg", "txt"))
		c_txt +=1
		os.remove(pathIm + imgName)

print("\n\nx_txt: ", c_txt)


# print("\n\n\n")

# c_xml = 0 
# imgs = os.listdir(pathIm)
# for imgXml in os.listdir(pathYolo):
# 	if( imgXml not in imgs):
# 		# print(pathYolo + imgXml)
# 		# c_xml +=1
# 		os.remove(pathYolo + imgXml)

# print("\n\n", c_xml)