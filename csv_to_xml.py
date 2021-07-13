#  Your csv format should have these columns
#       filename,width,height,class,xmin,ymin,xmax,ymax
#  Command : py csv_to_xml.py -i tractor\tractor.csv -o tractor\xmls


import os
import csv
import argparse
from collections import defaultdict
from lxml.etree import Element, SubElement, ElementTree


def write_xml(folder, filename, bbox_list):

    root = Element('annotation')
    SubElement(root, 'folder').text = folder
    SubElement(root, 'filename').text = filename
    # SubElement(root, 'path').text = './images' +  filename

    source = SubElement(root, 'source')
    SubElement(source, 'database').text = 'coco'

    # Details from first entry
    e_filename,  e_height, e_width,e_class_name, e_xmin, e_ymin, e_xmax, e_ymax = bbox_list[0]   
    size = SubElement(root, 'size')
    SubElement(size, 'width').text = e_width
    SubElement(size, 'height').text = e_height
    SubElement(size, 'depth').text = '3'
    SubElement(root, 'segmented').text = '0'

    for entry in bbox_list:
        e_filename,  e_height, e_width, e_class_name, e_xmin, e_ymin, e_xmax, e_ymax = entry  

        obj = SubElement(root, 'object')
        SubElement(obj, 'name').text = e_class_name
        SubElement(obj, 'pose').text = 'Unspecified'
        SubElement(obj, 'truncated').text = '0'
        SubElement(obj, 'difficult').text = '0'

        bbox = SubElement(obj, 'bndbox')
        SubElement(bbox, 'xmin').text = e_xmin
        SubElement(bbox, 'ymin').text = e_ymin
        SubElement(bbox, 'xmax').text = e_xmax
        SubElement(bbox, 'ymax').text = e_ymax

    tree = ElementTree(root)  
    xml_filename = os.path.join('.', folder, os.path.splitext(filename)[0] + '.xml')
    tree.write(xml_filename, pretty_print=True)

def main(input ,output):
    # Initialize a list 
    entries_by_filename = defaultdict(list)

    # Read csv file
    with open( input, 'r', encoding='utf-8') as f_input_csv:
        csv_input = csv.reader(f_input_csv)
        header = next(csv_input)
        for row in csv_input:
            filename, width, height, class_name, xmin, ymin, xmax, ymax = row
            entries_by_filename[filename].append(row) 

    # Write to xml file
    for filename, entries in entries_by_filename.items():
        write_xml( output , filename, entries)    

    print(" Successfully Converted annotations from CSV to XML format .🎉🥳")    

if __name__ == "__main__" :
    # Argument Parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="csv path")
    ap.add_argument("-o", "--output", required=True, help="output directory ")
    args = vars(ap.parse_args())   

    # Create output directory if not already there
    if not os.path.exists(args["output"]):
        os.mkdir( args["output"])  

    # Start Writing
    main(args["input"], args["output"] )
