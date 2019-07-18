import numpy as np
#import pandas as pd
import cv2
#import matplotlib.pyplot as plt
#from PIL import Image
#import textract
import argparse
import os
#import pickle
import pytesseract
from PIL import Image, ImageOps



def extract_text(img):
    config = ('-l eng --oem 1 --psm 3')
    text = pytesseract.image_to_string(img, config=config)
    #print text
    return text
    
def extract_text_from_image(file, bounding_box_file):
    coor_to_text = {}
    img_file_name =  file
    img = cv2.imread(img_file_name)
    
    
    geomap_bb_path = bounding_box_file
    
    final_bb_list = []
    with open(geomap_bb_path,'r') as fp:
    	final_bb_list = fp.readlines()
    print (final_bb_list)
    
    #print (final_bb_list)
    num_bounding_boxes = len(final_bb_list)
    
    for index in range(num_bounding_boxes):
    	row = final_bb_list[index]
    	final_bb_list[index] = row.strip()
    		
    img_copy = Image.open(img_file_name)
    
    #min_x, min_y, max_x,max_y
    
    
    for index in range(num_bounding_boxes):
        
        p1,p2,p3,p4 = map(int,final_bb_list[index].split(','))
        p1-=4;p2-=4;p3+=4;p4+=4;
        print (p1,p2,p3,p4)
        #area = (p1[1],p1[0],p4[1],p4[0])
        area = (p1,p2,p3,p4)
        if 1:
            cropped_img = img_copy.crop(area)
          
            crop_img_path = "cropped_img{}".format(index)+".png"

            #######
            cropped_img.save(crop_img_path)
            #ImageOps.expand(Image.open(crop_img_path),border=20,fill='white').save(crop_img_path)

            text = extract_text(crop_img_path)
            print (text)
            
            #text = str(index)+")"+str(text)
            coor_to_text[area]=text
    print (coor_to_text)
    return coor_to_text
    

def final(coor_to_text):
	
	output = []
	
	print ("######################")
	for coord in coor_to_text.keys():
		text = coor_to_text[coord]
		print (coord, text)
		
	print ("######################")
	
	for coord in coor_to_text.keys():
		text = coor_to_text[coord]
		text = text.replace(' ','')
		if len(text) in range(8,13):
			output.append([coord,text])
			
		print (text, len(text))
	'''
	text = coor_to_text.values()
	output = []
	print (coor_to_text)
	for i in range(len(text)):
		text[i] = text[i].replace(' ','')
		if len(text[i]) in range(8,13):
			output.append(text[i])
			
		print (text[i], len(text[i]))
	'''
	return output

def main(args):
    file = args.image_path
    bounding_box_file = args.bb_coordinates_file
    
    coor_to_text = extract_text_from_image(file, bounding_box_file)
    
    output = final(coor_to_text)
    print ("Number:::", output)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('image_path',help='Img name with extension')
    parser.add_argument('bb_coordinates_file',help='Name of the file that contain bouding box coordinates')

    args = parser.parse_args()
    
    main(args)
    
