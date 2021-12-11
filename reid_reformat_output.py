import os, shutil
from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, required=True, help="Path to folder containing gallery and result_images folders")
    return parser.parse_args()

def reformat(pathSrc):
	pathDst = pathSrc + "reformatted_results/"
	resultPath = pathSrc + "result_images/"
	galPath = pathSrc + "gallery/"

	os.mkdir(pathDst)

	for track in os.listdir(resultPath):
		for tracklet in os.listdir(resultPath + track):
			shutil.copy(galPath + tracklet + "/car.jpg", pathDst + track + "_" + tracklet + ".jpg")


if __name__ == '__main__':
    args = get_args()
    reformat(args.input_path)