from pdf2image import convert_from_path
import numpy as np
import cv2
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
    #print (final_bb_list)
    
    #print (final_bb_list)
    num_bounding_boxes = len(final_bb_list)
    
    for index in range(num_bounding_boxes):
    	row = final_bb_list[index]
    	final_bb_list[index] = row.strip()
    		
    img_copy = Image.open(img_file_name)
    
    #min_x, min_y, max_x,max_y
    
    #print (num_bounding_boxes, final_bb_list)
    
    for index in range(num_bounding_boxes):
        
        p1,p2,p3,p4 = map(int,final_bb_list[index].split(','))
        p1-=4;p2-=4;p3+=4;p4+=4;
        #print (p1,p2,p3,p4)
        #area = (p1[1],p1[0],p4[1],p4[0])
        area = (p1,p2,p3,p4)
        if 1:
            cropped_img = img_copy.crop(area)
          
            crop_img_path = "cropped_img{}".format(index)+".png"

            #######
            cropped_img.save(crop_img_path)
            #ImageOps.expand(Image.open(crop_img_path),border=20,fill='white').save(crop_img_path)

            text = extract_text(crop_img_path)
            #print (text)
            
            #text = str(index)+")"+str(text)
            coor_to_text[area]=text
    #print (coor_to_text)
    return coor_to_text
    
    

def pdf2img(pdf):
	pages = convert_from_path(pdf, 800)
	page_count = 1
	
	pdf_split = pdf.split(".")
	img_names = []
	
	for page in pages:
		img_names.append(pdf_split[0]+ "-" + str(page_count)+'.jpg')
		
		#page.save(pdf_split[0]+ "-" + str(page_count)+'.jpg', 'JPEG')
		page_count +=1

	return img_names


def final(coor_to_text):
	
	output = []
	
	print ("######################")
	for coord in coor_to_text.keys():
		text = coor_to_text[coord]
		print (coord, text)
		
	print ("######################")
	
	return output



def main(args):
    file = args.pdf_path
    
    img_names = pdf2img(file)
    
    print (img_names)
    
    for img in img_names:
    	img_split = img.split("/")
    	img_split[1] = "results"
    	img_name_txt = img_split[-1].replace('jpg', 'txt')
    	
    	img_split[-1] = img_name_txt
    	
    	print (img, '/'.join(img_split))
    	
    	bounding_box_file = '/'.join(img_split)
    	file = img
    	coor_to_text = extract_text_from_image(file, bounding_box_file)
    	output = final(coor_to_text)

    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('pdf_path',help='PDF name')
    
    args = parser.parse_args()
    
    main(args)
    
    
    
