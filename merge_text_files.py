import os
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, required=True, help="Path to the prediction file output by the worker")
    return parser.parse_args()

def mergeFiles(path2files):
	destPath = "/".join(path2files.split("/")[:-2]) + "/merged_results.txt"

	out_file = open(destPath,"w")
	alreadyAddedHeader = False

	for file in os.listdir(path2files):
		in_file = open(path2files + file, "r")
		lines = in_file.readlines()
		in_file.close()

		for line in lines:
			if "cameraId" not in line:
				out_file.write(line)
			elif not alreadyAddedHeader:
				alreadyAddedHeader = True
				

	out_file.close()


if __name__ == '__main__':
    args = get_args()
    mergeFiles(args.input_path)

