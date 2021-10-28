import os
pathLarge = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/raw/home/hooman/hs_datasets/fromProduction/crowd_pipeline/crowd_flow/test_videos/round1_selected_for_training_from_35-46_13-04_43-04/"

pathSmal1 = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/round1_first100/png/"
pathSmal2 = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/round2_100to200/png/"
pathSmal3 = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/round3/png/"

smallNames = {}

for img in os.listdir(pathSmal1):
	smallNames[img] = 1

for img in os.listdir(pathSmal2):
	smallNames[img] = 1

for img in os.listdir(pathSmal3):
	smallNames[img] = 1

print("\n found: ", len(smallNames), " in small")

count = 0
for img in os.listdir(pathLarge):
	if img not in smallNames:
		print("\n", img)
		count+=1

print("\n missing count: ", count)