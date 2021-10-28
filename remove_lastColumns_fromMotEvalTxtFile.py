import os
from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, required=True, help="Path to the prediction file output by the worker")
    parser.add_argument('-o', '--output_path', type=str, default=None, help="Path to the converted prediciton file")
    parser.add_argument('-fo', '--frame_offset', type=int, default=1, help="Frame offest to be applied")
    return parser.parse_args()

def convert(input_path, output_path=None, frame_offset=1):
    if not os.path.exists(input_path):
        raise ValueError("Input file not found: %s" % input_path)

    if input_path[-4:] !='.txt':
        raise ValueError("Input format not supported: %s" % input_path)

    if output_path is None:
        output_path = input_path[:-4] + '_converted.txt'
    else:
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

    lines_in = []
    with open(input_path, 'r') as f:
        lines_in = f.readlines()
    
    with open(output_path, 'w') as f:
        for line in lines_in:
            line_ele = line.split(" ")
            line_out = "%s %s %d %s %s %s %s -1 -1\n" % (
                line_ele[0], line_ele[1],
                int(line_ele[2]) + frame_offset, 
                line_ele[3], line_ele[4], line_ele[5], line_ele[6])
            f.write(line_out)
    return 

if __name__ == '__main__':
    args = get_args()
    convert(args.input_path, args.output_path,args.frame_offset)


