# Script to convert yolo annotations to voc format

# Sample format
# <annotation>
#     <folder>_image_fashion</folder>
#     <filename>brooke-cagle-39574.png</filename>
#     <size>
#         <width>1200</width>
#         <height>800</height>
#         <depth>3</depth>
#     </size>
#     <segmented>0</segmented>
#     <object>
#         <name>head</name>
#         <pose>Unspecified</pose>
#         <truncated>0</truncated>
#         <difficult>0</difficult>
#         <bndbox>
#             <xmin>549</xmin>
#             <ymin>251</ymin>
#             <xmax>625</xmax>
#             <ymax>335</ymax>
#         </bndbox>
#     </object>
# <annotation>
import os
# import xml.etree.cElementTree as ET
from lxml import etree as ET
from PIL import Image

### This should always be current working directory.
ANNOTATIONS_DIR_PREFIX = "./"
### Which also means that this scipt should be with the .txt annotations.


DESTINATION_DIR = "/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/round3/Annotations_vest-hat_xml/"

# CLASS_MAPPING = {
# # This is class wise mapping. Please see your labelmap.prototxt file to write this dictionary.
#     '0': 'Head',
#     '1': 'Torso',
#     '2': 'Person',
#     # Add your remaining classes here.
# }

CLASS_MAPPING = {
    '0': 'background',
    '1': 'person',
    '2': 'noVest',
    '3': 'vest',
    '4': 'noHat',
    '5': 'hat',
    # Add your remaining classes here.
}


def create_root(file_prefix, width, height):
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "images"
    ET.SubElement(root, "filename").text = "{}.png".format(file_prefix)

    ET.SubElement(root, "path").text = "dataset_split/TrainOrTest"
    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "Unknown"
        # <path>PICTURE_DATA/Test</path>
    	# <source>
    	# 	<database>Unknown</database>
    	# </source>
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    tree.write("{}/{}.xml".format(DESTINATION_DIR, file_prefix),pretty_print=True)
    # tree.write("{}/{}.xml".format(DESTINATION_DIR, file_prefix))


def read_file(file_path):
    file_prefix = file_path.split(".txt")[0]
    image_file_name = "{}.png".format(file_prefix)
    img = Image.open("{}/{}".format("/home/hooman/hs_datasets/head_torso_related/shanghai_expo_head_person/round2_100to200/png/", image_file_name))
    w, h = img.size
    with open(file_path, 'r') as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            xmin_fin = int(center_x - (bbox_width / 2))
            xmax_fin = int(center_x + (bbox_width / 2))
            ymin_fin = int(center_y - (bbox_height / 2))
            ymax_fin = int(center_y + (bbox_height / 2))
            if xmin_fin <= 0:
                xmin_fin = 1
            if xmax_fin > w:
                xmax_fin = w
            if ymin_fin <= 0:
                ymin_fin = 1
            if ymax_fin > h:
                ymax_fin = h
            voc.append(xmin_fin)
            voc.append(ymin_fin)
            voc.append(xmax_fin)
            voc.append(ymax_fin)
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels)
    print("Processing complete for file: {}".format(file_path))


def start():
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for filename in os.listdir(ANNOTATIONS_DIR_PREFIX):
        if filename.endswith('txt'):
            read_file(filename)
        else:
            print("Skipping file: {}".format(filename))


if __name__ == "__main__":
    start()
