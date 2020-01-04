# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ExifTags
from PIL import ImageFont, ImageDraw, ImageEnhance

import csv
import os
import re


def create_plate_dict(images_d):
	plates_d = {}
	for image in images_d:
		plates = images_d[image]['PlatesList']
		for plate in plates:
			if plate in plates_d:
				plates_d[plate]['ImageList'].append(image) 
				plates_d[plate]['TimeStamp'].append(images_d[image]['TimeStamp'])
				plates_d[plate]['GPS'].append(images_d[image]['GPS']) 
				plates_d[plate]['Infraction'].append('000')
			else:
				plates_d[plate] = {
				'ImageList': [image],
				'TimeStamp': [images_d[image]['TimeStamp']],
				'GPS': [images_d[image]['GPS']],
				'Infraction': ['000']
				}
	return plates_d

def write_csv(dictionary, filename):
	with open(filename, 'w') as fd:
		items = dictionary.keys()
		keys = dictionary[items[0]].keys()
		if keys[1] == 'PlatesList':
			dict_name = 'ImageName'
			keys.insert(0,dict_name)
		else:
			if keys[1] == 'ImageList':
				dict_name = 'PlateValue'
				keys.insert(0,dict_name)
		for item in keys:
			fd.write("%s;"%(item))
		fd.write("\n")
		for key in dictionary.keys():
			fd.write("%s;"%(key))
			for item in keys[1:]:
				fd.write("%s;"%(dictionary[key][item]))
			fd.write("\n")

def read_csv(csvfile, images_d):
	with open(csvfile) as fd:
		image_details = {}
		for line in fd:
			detail = line.split(',')
			img = detail[0].split('\n')
			img = img[0]
			img = img + ".JPG"

			plates = []
			if len(detail) > 1:
				plates = detail[1:]
				plates[-1] = plates[-1][:-1]

			for plate in plates:
				pattern_black1 = re.compile(r'^(B|AB|AR|AG|BC|BH|BN|BT|BV|BR|BZ|CS|CL|CJ|CT|CV|DB|DJ|GL|GR|GJ|HR|HD|IL|IS|IF|MM|MH|MS|NT|OT|PH|SM|SJ|SB|SV|TR|TM|TL|VS|VL|VN)[0-9]{2,3}[A-Z]{3}$')
				pattern_black2 = re.compile(r'^(B|AB|AR|AG|BC|BH|BN|BT|BV|BR|BZ|CS|CL|CJ|CT|CV|DB|DJ|GL|GR|GJ|HR|HD|IL|IS|IF|MM|MH|MS|NT|OT|PH|SM|SJ|SB|SV|TR|TM|TL|VS|VL|VN)[0-9]{2,3}0[A-Z]{2}$')
				pattern_black3 = re.compile(r'^(B|AB|AR|AG|BC|BH|BN|BT|BV|BR|BZ|CS|CL|CJ|CT|CV|DB|DJ|GL|GR|GJ|HR|HD|IL|IS|IF|MM|MH|MS|NT|OT|PH|SM|SJ|SB|SV|TR|TM|TL|VS|VL|VN)[0-9]{2,3}[A-Z]{1}0[A-Z]{1}$')
				pattern_black4 = re.compile(r'^(B|AB|AR|AG|BC|BH|BN|BT|BV|BR|BZ|CS|CL|CJ|CT|CV|DB|DJ|GL|GR|GJ|HR|HD|IL|IS|IF|MM|MH|MS|NT|OT|PH|SM|SJ|SB|SV|TR|TM|TL|VS|VL|VN)[0-9]{2,3}[A-Z]{2}0$')
				pattern_red = re.compile(r'^(B|AB|AR|AG|BC|BH|BN|BT|BV|BR|BZ|CS|CL|CJ|CT|CV|DB|DJ|GL|GR|GJ|HR|HD|IL|IS|IF|MM|MH|MS|NT|OT|PH|SM|SJ|SB|SV|TR|TM|TL|VS|VL|VN)[0-9]{3,7}$')

				#pattern_black1 = re.compile(r'^[A-Z]{1,2}[0-9]{2,3}[A-Z]{3}$')
				#pattern_black2 = re.compile(r'^[A-Z]{1,2}[0-9]{2,3}0[A-Z]{2}$')
				#pattern_black3 = re.compile(r'^[A-Z]{1,2}[0-9]{2,3}[A-Z]{1}0[A-Z]{1}$')
				#pattern_black4 = re.compile(r'^[A-Z]{1,2}[0-9]{2,3}[A-Z]{2}0$')
				#pattern_red = re.compile(r'^[A-Z]{1,2}[0-9]{3,6}$') 
				match_black1 = pattern_black1.search(plate)
				match_black2 = pattern_black2.search(plate)
				match_black3 = pattern_black3.search(plate)
				match_black4 = pattern_black4.search(plate)
				match_red = pattern_red.search(plate)
				if  match_black1 or match_black2 or match_black3 or match_black4 or match_red:
					continue
				else:
					plates = filter(lambda a: a != plate, plates)
			plates = list(dict.fromkeys(plates))
			images_d[img]['PlatesList'] = plates
	return images_d

def read_mycsv(filename):
	dictionary = {}
	header = []
	with open(filename) as fd:
		for line in fd:
			detail = line.replace('\n','')
			detail = detail.split(';')

			if 'PlateValue' in line or 'ImageName' in line:
				header = detail[1:]
				if not header[-1]:
					header = header[:-1]
			else:
#				print detail
				details = {}
				dictionary[detail[0]] = {}
				for i in range(len(header)):
					newlist = detail[i+1]
					newlist = newlist[1:-1]	
					newlist = newlist.split(',')
					mylist = []
					mygps = []
					for item in newlist:
						if not item:
							continue
						else:
							item = item.strip()
							if item[0] == "'":
								mylist.append(item[1:-1])
							else:
								if item[0] == '[':
									item = item[1:]
									mygps.append(float(item))
								else:
									if item[-1] == ']':
										item = item[:-1]
										mygps.append(float(item))
										mylist.append(mygps)
										mygps = []
									else:
										mylist.append(item)

					details[header[i]] = mylist
#					print header[i]
#					print details[header[i]]
				dictionary[detail[0]] = details
			
	return dictionary

def get_files(directory, images_d):
	for filename in os.listdir(directory):
		image_details = {}
		if filename.endswith(".JPG") or filename.endswith(".jpg"): 
			file_path = os.path.join(directory, filename)

			exif = get_info(file_path)

			image_details['TimeStamp'] = exif['DateTime']
			image_details['GPS'] = get_decimal_coordinates(exif['GPSInfo'])
			images_d[os.path.join(filename)] = image_details
	return images_d




def get_info(imagename):
	img = Image.open(imagename)

	exif = {
		ExifTags.TAGS[k]: v
		for k, v in img._getexif().items()
			if k in ExifTags.TAGS
	}
		
	if 'GPSInfo' in exif:
		for key in exif['GPSInfo'].keys():
			name = ExifTags.GPSTAGS.get(key,key)
			exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)
	return exif		

def get_coordinates(info):
	for key in ['Latitude', 'Longitude']:
		if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
			e = info['GPS'+key]
			ref = info['GPS'+key+'Ref']
			info[key] = ( str(e[0][0]/e[0][1]) + ' ' +
                          str(e[1][0]/e[1][1]) + ' ' +
                          str(e[2][0]/e[2][1]) + ' ' +
                          ref )

	if 'Latitude' in info and 'Longitude' in info:
		return [info['Latitude'], info['Longitude']]


def get_decimal_coordinates(info):
	for key in ['Latitude', 'Longitude']:
		if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
			e = info['GPS'+key]

			ref = info['GPS'+key+'Ref']
			info[key] = ( e[0][0]/float(e[0][1]) +
                          e[1][0]/float(e[1][1]) / 60 +
                          e[2][0]/float(e[2][1]) / 3600
                        ) * (-1 if ref in ['S','W'] else 1)

	if 'Latitude' in info and 'Longitude' in info:
		return [info['Latitude'], info['Longitude']]

def listToString(mylist):     
    return (' '.join([str(elem) for elem in mylist])) 

def working_folder(images_d, plates_d):
	for image in images_d:
		create_image(images_d, plates_d, image)
	return

def create_image(images_d, plates_d, image_name):
	if not os.path.exists("files"):
		os.makedirs("files")
	img_name = '../images/'+image_name
	source_img = Image.open(img_name).convert("RGB")
	width, height = source_img.size
	newsize = (width/3, height/3) 
	source_img = source_img.resize(newsize)
	# create image with size (1000,1000) and black background
	rectangle_img = Image.new('RGB', (3000,1200), "black")

	# put text on image
	rectangle_draw = ImageDraw.Draw(rectangle_img)
	rectangle_draw.text((1550, 70), image_name, font=ImageFont.truetype("arial", 50))
	coordinates = images_d[image_name]['GPS']
	strcoordinates = listToString(coordinates)
	rectangle_draw.text((1550, 120), strcoordinates, font=ImageFont.truetype("arial", 50))
	plates = images_d[image_name]['PlatesList']
	strplates = listToString(plates)
	xcoord = 1550
	ycoord = 170
	for plate in plates:
		imagelist = plates_d[plate]['ImageList']
		index = imagelist.index(image_name)
		infraction = plates_d[plate]['Infraction'][index]
		if '000' in infraction:
			color = 'white'
		else:
			if '002' in infraction:
				color = 'green'
			else:
				if '003' in infraction:
					color = 'blue'
				else:
					color = 'red'
		rectangle_draw.text((xcoord, ycoord), plate, font=ImageFont.truetype("arial", 50), fill=color)
		rectangle_draw.text((xcoord, ycoord + 50), infraction, font=ImageFont.truetype("arial", 50), fill=color)
		ycoord = ycoord + 100

	# put button on source image in position (100, 100)
	rectangle_img.paste(source_img, (100,100))
	
	# save in new file
	new_name = 'files/' + image_name
	rectangle_img.save(new_name, "JPEG")
	return


if __name__ == '__main__':
#	images_d = {}
#	images_d = get_files('../images', images_d)
#	images_d = read_csv('results.csv', images_d)
#	write_csv(images_d, 'image_dictionary.csv')
#	plates_d = create_plate_dict(images_d)
#	write_csv(plates_d, 'plates_dictionary.csv')
	plates_d = read_mycsv('plates_dictionary.csv')
	images_d = read_mycsv('image_dictionary.csv')
	working_folder(images_d, plates_d)
