#  Run file as py csv_to_json.py -i data\src\src_annotations.csv -o coco.json
import os
import json
import argparse
import pandas as pd

def image(row):
    print(row , type(row))
    image = {}
    image["height"] = row.height
    image["width"] = row.width
    image["id"] = row.fileid
    image["file_name"] = row.filename
    return image

def category(row):
    category = {}
    category["supercategory"] = 'None'
    category["id"] = row.categoryid
    category["name"] = row._4
    return category

def annotation(row):
    annotation = {}
    area = (row.xmax -row.xmin)*(row.ymax - row.ymin)
    annotation["segmentation"] = []
    annotation["iscrowd"] = 0
    annotation["area"] = area
    annotation["image_id"] = row.fileid

    annotation["bbox"] = [row.xmin, row.ymin, row.xmax -row.xmin,row.ymax-row.ymin ]

    annotation["category_id"] = row.categoryid
    annotation["id"] = row.annid
    annotation["class"]=row._4
    return annotation

def csv_to_json():
    data = pd.read_csv(args["input"])

    images = []
    categories = []
    annotations = []

    category_ = {}
    category_["supercategory"] = 'none'
    category_["id"] = 0
    category_["name"] = 'None'
    categories.append(category_)

    data['fileid'] = data['filename'].astype('category').cat.codes
    data['categoryid']= pd.Categorical(data['class'],ordered= True).codes
    data['categoryid'] = data['categoryid']+1
    data['annid'] = data.index    

    for row in data.itertuples():

        annotations.append(annotation(row))

    imagedf = data.drop_duplicates(subset=['fileid']).sort_values(by='fileid')
    for row in imagedf.itertuples():
        images.append(image(row))

    catdf = data.drop_duplicates(subset=['categoryid']).sort_values(by='categoryid')
    for row in catdf.itertuples():
        categories.append(category(row))   

    data_coco = {}
    data_coco["images"] = images
    data_coco["categories"] = categories
    data_coco["annotations"] = annotations  

    # Convert into json format
    json.dump(data_coco, open(args["output"], "w"), indent=4)
    print("Successfully generated json file \nSaved to {} ".format(os.path.join(os.curdir,args["output"])))   

    return True   

if __name__ == "__main__":
    
    # Argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input",
                    required=True,
                    help="path to csv file")
    ap.add_argument("-o","--output",
                    required=True,
                    help="path to output json file")
    args = vars(ap.parse_args()) 

    csv_to_json()