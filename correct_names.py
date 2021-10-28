import os

#destPath = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/test_shiyun_and_shanghai/preds_RESNET18SSD_ITER55000_PRIVATE_03MAY2021_PERSON_HEAD/"
srcPath = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/test_shiyun_and_shanghai/preds_aug16_ssd/"

for file in os.listdir(srcPath):
	os.rename(srcPath + file, srcPath + file.replace("_output", ""))

