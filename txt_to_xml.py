''' This file is used to convert annotations from .txt file to .xml formate
    Command : python txt_to_xml.py -i data\txts -img data\images -o data\xmls
    Output format will be like
    <annotation>
        <filename>0004470.jpg</filename>
        <folder>BLR-2018-06-05_08-28-17_rearNear_left_6</folder>
        <size>
            <width>1920</width>
            <height>1080</height>
            <depth>3</depth>
        </size>
        <object>
            <name>bus</name>
            <bndbox>
                <xmin>844</xmin>
                <ymax>538</ymax>
                <xmax>1229</xmax>
                <ymin>126</ymin>
            </bndbox>
        </object>
    </annotation> '''

import os
import os.path
import argparse
from PIL import Image
from xml.dom.minidom import Document


def writeXml(tmp, imgname, w, h, objbud, wxml, dict):

    doc = Document()
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    # Filename
    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename_txt = doc.createTextNode(imgname)
    filename.appendChild(filename_txt)

    # owner
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder_txt = doc.createTextNode(wxml)
    folder.appendChild(folder_txt)  

    # Size tag
    size = doc.createElement('size')
    annotation.appendChild(size)

    width = doc.createElement('width')
    size.appendChild(width)
    width_txt = doc.createTextNode(str(w))
    width.appendChild(width_txt)

    height = doc.createElement('height')
    size.appendChild(height)
    height_txt = doc.createTextNode(str(h))
    height.appendChild(height_txt)

    depth = doc.createElement('depth')
    size.appendChild(depth)
    depth_txt = doc.createTextNode("3")
    depth.appendChild(depth_txt)

    # Append boxes
    for i in range(0, int(len(objbud))):
        objbuds=objbud[i].split(' ')
        # threes
        object_new = doc.createElement("object")
        annotation.appendChild(object_new)

        name = doc.createElement('name')
        object_new.appendChild(name)
        name_txt = doc.createTextNode(dict[objbuds[0]])
        name.appendChild(name_txt)

        # pose = doc.createElement('pose')
        # object_new.appendChild(pose)
        # pose_txt = doc.createTextNode("Unspecified")
        # pose.appendChild(pose_txt)

        # truncated = doc.createElement('truncated')
        # object_new.appendChild(truncated)
        # truncated_txt = doc.createTextNode("0")
        # truncated.appendChild(truncated_txt)

        # difficult = doc.createElement('difficult')
        # object_new.appendChild(difficult)
        # difficult_txt = doc.createTextNode("0")
        # difficult.appendChild(difficult_txt)

        # threes-1#
        bndbox = doc.createElement('bndbox')
        object_new.appendChild(bndbox)
        
        x1 = float(objbuds[1])
        y1 = float(objbuds[2])
        w1 = float(objbuds[3])
        h1 = float(objbuds[4])
        
        xmin = doc.createElement('xmin')
        bndbox.appendChild(xmin)
                    
        xmin_txt2 = int((x1*w) - (w1*w)/2.0)
        xmin_txt = doc.createTextNode(str(xmin_txt2))
        xmin.appendChild(xmin_txt)

        ymin = doc.createElement('ymin')
        bndbox.appendChild(ymin)
        ymin_txt2 = int((y1*h)-(h1*h)/2.0)
        ymin_txt = doc.createTextNode(str(ymin_txt2))
        ymin.appendChild(ymin_txt)

        xmax = doc.createElement('xmax')
        bndbox.appendChild(xmax) 
        xmax_txt2 = int((x1*w)+(w1*w)/2.0)
        xmax_txt = doc.createTextNode(str(xmax_txt2))
        xmax.appendChild(xmax_txt)

        ymax = doc.createElement('ymax')
        bndbox.appendChild(ymax)
        ymax_txt2 = int((y1*h)+(h1*h)/2.0)
        ymax_txt = doc.createTextNode(str(ymax_txt2))
        ymax.appendChild(ymax_txt)

    # This is to create the xml with correct indent            
    tempfile = tmp + "test.xml"
    with open(tempfile, "w") as f:
        f.write(doc.toprettyxml(indent='\t'))

    # Now rewrite the xml file with all tags
    rewrite = open(tempfile, "r")
    lines = rewrite.read().split('\n')
    newlines = lines[1:len(lines) - 1]
    fw = open(wxml, "w")
    for i in range(0, len(newlines)):
        fw.write(newlines[i] + '\n')

    # Close all opened files
    fw.close()
    rewrite.close()
    os.remove(tempfile)
    return


if __name__ == "__main__":

    # Argument Parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="txt path")
    ap.add_argument("-img", "--image", required=True, help="images path")
    ap.add_argument("-o", "--output", required=True, help="output directory ")
    args = vars(ap.parse_args()) 

    # Create output path if not exists
    if not os.path.exists(args["output"]):
        os.mkdir(args["output"])

    #Define class number according to the  classes in the .txt file
    dict = {'0': "bus",
            '1': "car",
            '2': "motorcycle",
            '3': "truck",
            '4': "vehicle fallback",
            }     

    # Assign paths        
    ann_path = args["input"]
    img_path = args["image"]
    xml_path = args["output"]

    # Start Converting
    for files in os.walk(ann_path):
        # This is for creating xml file with proper indentation
        temp = './temp/'
        if not os.path.exists(temp):
            os.mkdir(temp)

        for file in files[2]:
            print (file + "-->start!")
            # Read image and get its size attributes
            img_name = os.path.splitext(file)[0] + '.jpg'
            fileimgpath = img_path + img_name
            im = Image.open(fileimgpath)
            width = int(im.size[0])
            height = int(im.size[1])
            # Read txt file 
            filelabel = open(ann_path + file, "r")
            lines = filelabel.read().split('\n')
            obj = lines[:len(lines)-1]
            # Create output xml filename
            filename = xml_path + os.path.splitext(file)[0] + '.xml'
            # Call the function
            writeXml(temp, img_name, width, height, obj, filename, dict)
        os.rmdir(temp)