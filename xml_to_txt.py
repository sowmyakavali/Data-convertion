# COMMAND : py xml_to_txt.py -i car\xmls -o car\txts
# Here you need to change the dictionary as per your classes
import os
import glob
import argparse
from xml.dom import minidom


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

def xml_to_txt( lut ,input ,output):

    # Start writing  
    for xml in glob.glob( os.path.join(input , "*.xml") ): 
        xmldoc = minidom.parse(xml)  
        # define output filename    
        fname_out = xml.split("\\")[-1] 
        fname_out = (os.path.join(output, fname_out.split(".")[0] + '.txt'))

        with open(fname_out, "w") as f:
            # Get image properties
            itemlist = xmldoc.getElementsByTagName('object')
            size = xmldoc.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)

            for item in itemlist:
                # get class label
                classid =  (item.getElementsByTagName('name')[0]).firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                else:
                    # label_str = "-1"
                    print ("warning: label '%s' not in look-up table" % classid)
                    continue
                    
                # get bbox coordinates
                xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert_coordinates((width,height), b)
                # Write out the file
                f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')

        # print ("wrote %s" % fname_out)    

if __name__ == '__main__' :
    # Argument Parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Xmls path")
    ap.add_argument("-o", "--output", required=True, help="output directory ")
    args = vars(ap.parse_args())   

    # Create output path if not already exists
    if not os.path.exists(args["output"]):
       os.makedirs(args["output"])

    #  Define your classes , you can add more 
    lut={}
    lut["bus"] = 0
    lut["car"] = 1
    lut["motorcycle"] = 2
    lut["truck"] = 3
    lut["vehicle fallback"] = 4

    # Write out to txts
    xml_to_txt( lut , args["input"], args["output"])          