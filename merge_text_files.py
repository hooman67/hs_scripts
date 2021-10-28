import os

path2files = "/home/hooman/hs_datasets/fromProduction/car_reid/release1.0.0_2021-10-09_httpApi/try11_reportingInterval100_decision100/text_files/"
destPath = "/home/hooman/hs_datasets/fromProduction/car_reid/release1.0.0_2021-10-09_httpApi/try11_reportingInterval100_decision100/text_files/merged_results.txt"

out_file = open(destPath,"w")

for file in os.listdir(path2files):
	in_file = open(path2files + file, "r")
	lines = in_file.readlines()
	in_file.close()

	for line in lines:
		out_file.write(line)

out_file.close()

