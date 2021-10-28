import os

srcPath = "/home/hooman/hs_datasets/car/MOT16/train/MOT16-02/deepSort_usingGt_detec5_keepAlive15_Affin0.008_temp/data_dupl/"
destPath = "/home/hooman/hs_datasets/car/MOT16/train/MOT16-02/deepSort_usingGt_detec5_keepAlive15_Affin0.008_temp/data/"


for file in os.listdir(srcPath):
	in_file = open(srcPath + file, "r")
	oldLines = in_file.readlines()
	in_file.close()

	frame_id_set = set()
	out_file = open(destPath + file,"w")

	for line in oldLines:
		sp = line.split(",")
		frame_id = sp[0] + "," + sp[1]
		if frame_id not in frame_id_set:
			out_file.write(line)
			frame_id_set.add(frame_id)

	out_file.close()

