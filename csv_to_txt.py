# Command : py csv_to_txt.py -i dataset_1k\balanced_data.csv -o dataset_1k\txts
import os 
import glob 
import argparse
import pandas as pd
from pandas.core.algorithms import unique

def convert_coordinates(size, box):
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def csv_to_txt(csv_path ,out_path):
    # Read Csv 
    df = pd.read_csv(csv_path)
    # Create label map
    unique_classes = pd.unique(df['class'])
    labels = {}
    for i,label in enumerate(unique_classes):
        labels[label]=i
    print(labels)
    # Group rows based on filename bcz single file may have multiple annotations
    for name, group in df.groupby('filename'):
        # Create filename
        fname_out = os.path.join( out_path, name.split(".")[0] + '.txt')
        # Open txt file to write
        with open(fname_out, "w") as f:
            # Iter through each bbox
            for row_index, row in group.iterrows():
                xmin = row['xmin']
                ymin = row['ymin']
                xmax = row['xmax']
                ymax = row['ymax']
                width = row['width']
                height = row['height']
                label = row['class']
                # Get label index
                label_str = str(labels[label])
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                # Convert bbox from pascal voc format to yolo txt format
                bb = convert_coordinates((width,height), b)
                # Write into file
                f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')

if __name__ == '__main__':
    # Argument Parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="csv path")
    ap.add_argument("-o", "--output", required=True, help="output directory ")
    args = vars(ap.parse_args())   

    # Create output path if not already exists
    if not os.path.exists(args["output"]):
       os.makedirs(args["output"])   

    # Call the function
    csv_to_txt(args["input"] , args["output"])   
