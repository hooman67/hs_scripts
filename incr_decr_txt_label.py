import os

srcPath = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/test_shiyun_and_shanghai/temp/"
destPath = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/test_shiyun_and_shanghai/preds_aug16_ssd/"

for file in os.listdir(srcPath):
	in_file = open(srcPath + file, "r")
	out_file = open(destPath + file,"w")
	oldLines = in_file.readlines()

	for line in oldLines:
		sp = line.split(" ")
		sp[0] = str( int(sp[0]) -1 )
		newline = " ".join(sp)
		out_file.write(newline)

	out_file.close()

