''' This file is used to convert annotations from .txt file to tenforflow csv formate
    Command : python txt_to_csv.py -i data\txts -img data\images -o data\data.csv
    Output format will be 
        filename ,height ,width ,class ,xmin ,ymin ,xmax ,ymax '''

import os
import os.path
import argparse
import pandas as pd
from PIL import Image
from xml.dom.minidom import Document


def write_to_csv(ann_path ,img_path ,dict):
    annos = []
    # Read txts  
    for files in os.walk(ann_path):
        for file in files[2]:
            print (file + "-->start!")

            # Read image and get its size attributes
            img_name = os.path.splitext(file)[0] + '.jpg'
            fileimgpath = os.path.join(img_path ,img_name)
            im = Image.open(fileimgpath)
            w = int(im.size[0])
            h = int(im.size[1])

            # Read txt file 
            filelabel = open(os.path.join(ann_path , file), "r")
            lines = filelabel.read().split('\n')
            obj = lines[:len(lines)-1]  
            # name = dict[obj[0]]
            for i in range(0, int(len(obj))):
                objbud=obj[i].split(' ')                
                name = dict[objbud[0]]
                # print(name)
                x1 = float(objbud[1])
                y1 = float(objbud[2])
                w1 = float(objbud[3])
                h1 = float(objbud[4])

                xmin = int((x1*w) - (w1*w)/2.0)
                ymin = int((y1*h) - (h1*h)/2.0)
                xmax = int((x1*w) + (w1*w)/2.0)
                ymax = int((y1*h) + (h1*h)/2.0)

                annos.append([img_name ,w ,h ,name ,xmin ,ymin ,xmax ,ymax])
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax' ]
    df = pd.DataFrame(annos, columns=column_name)        
    print(annos[:10])
    return df

if __name__ == "__main__" :

    # Argument Parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="txt path")
    ap.add_argument("-img", "--image", required=True, help="images path")
    ap.add_argument("-o", "--output", required=True, help="output csv path ")
    args = vars(ap.parse_args()) 

    # Define class number according to the  classes in the .txt file
    dict = {'0' : 'autorickshaw',
            '1': "bus",
            '2': "car",
            '3': "motorcycle",
            '4': "truck",
            '5': "vehicle fallback",
            }      
    # Assign paths        
    ann_path = args["input"]
    img_path = args["image"]
    csv_path = args["output"]  

    data=write_to_csv(ann_path ,img_path  ,dict)      
    # print()
    data.to_csv(csv_path, index=None)
    print('Successfully converted xml to csv. And your output file is {}'.format(args["output"]))         
