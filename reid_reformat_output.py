import os, shutil
from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, required=True, help="Path to folder containing gallery and result_images folders")
    parser.add_argument('-t', '--type', type=str, required=True, help="0 for normal 1 for shenzen")
    return parser.parse_args()

def reformat(pathSrc):
	pathDst = pathSrc + "reformatted_results/"
	resultPath = pathSrc + "result_images/"
	galPath = pathSrc + "gallery/"

	os.mkdir(pathDst)

	for track in os.listdir(resultPath):
		for tracklet in os.listdir(resultPath + track):
			shutil.copy(galPath + tracklet + "/car.jpg", pathDst + track + "_" + tracklet + ".jpg")

def reformat_shenzen(pathSrc):
	pathDst = pathSrc + "reformatted_results/"
	resultPath = pathSrc + "result_images/"

	os.mkdir(pathDst)

	for track in os.listdir(resultPath):
		for tracklet in os.listdir(resultPath + track):
			shutil.copy(resultPath + track + "/" + tracklet + "/car.jpg", pathDst + track + "_" + tracklet + ".jpg")

if __name__ == '__main__':
    args = get_args()
    if args.type == "0":
    	reformat(args.input_path)
    elif args.type == "1":
    	reformat_shenzen(args.input_path)
    else:
    	print("\n\n***\nERROR wrong conversion type specified. You passed: ", args.type, "\n***\n\n")