import os

srcPath = "/home/hooman/hs_datasets/car/Track3_CityScale_MultiCamera_Vehicle_Tracking/AIC21_Track3_MTMC_Tracking/validation/S02/c009/mtsc/mtsc_deepsort_mask_rcnn.txt"
destPath = "/home/hooman/hs_datasets/car/Track3_CityScale_MultiCamera_Vehicle_Tracking/AIC21_Track3_MTMC_Tracking/validation/S02/c006/mtsc_deepsort_mask_rcnn_fromAuthors/mtsc_deepsort_mask_rcnn_hs_cam9.txt"


in_file = open(srcPath, "r")
out_file = open(destPath,"w")
oldLines = in_file.readlines()

for line in oldLines:
	sp = line.split(",")
	sp[0] = str( int(sp[0]) -1 )
	# newline = " ".join(sp)
	newline = "9 " + sp[1] + " " + sp[0] + " " + str(max(0, int(float(sp[2])))) + " " + str(max(0, int(float(sp[3])))) + " " + str(max(0, int(float(sp[4])))) + " " + str(max(0, int(float(sp[5])))) + " -1 -1\n"
	out_file.write(newline)

out_file.close()