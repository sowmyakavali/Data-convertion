# Command : py xml_csv.py -i tractor\xmls -o tractor\tractor.csv

import glob
import argparse
from numpy import split
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        image = xml_file.split("\\")[-1].split(".")[0] + '.jpg'
        for member in root.findall('object'):
            if member[0].text in ['car', 'motorcycle', 'truck', 'bus', 'autorickshaw', 'vehicle fallback']:
                value = (root.find('filename').text, # image : For IDD
                        int(root.find('size')[0].text),
                        int(root.find('size')[1].text),
                        member[0].text ,
                        int(member[4][0].text),
                        int(member[4][1].text),                       
                        int(member[4][2].text),
                        int(member[4][3].text),
                        )
                xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax' ]
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


if __name__ == "__main__" :
    # Argument Parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Xmls path")
    ap.add_argument("-o", "--output", required=True, help="output file name ")
    args = vars(ap.parse_args())                

    xmls_path = args["input"]
    xml_df = xml_to_csv(xmls_path)
    xml_df.to_csv(args["output"], index=None)
    print('Successfully converted xml to csv. And your output file is {}'.format(args["output"])) 