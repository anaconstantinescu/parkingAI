# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ExifTags

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
			else:
				plates_d[plate] = {
				'ImageList': [image],
				'TimeStamp': [images_d[image]['TimeStamp']],
				'GPS': [images_d[image]['GPS']]
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
			fd.write("%s\t"%(item))
		fd.write("\n")
		for key in dictionary.keys():
			fd.write("%s\t"%(key))
			for item in keys[1:]:
				fd.write("%s\t"%(dictionary[key][item]))
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
#				pattern_black1 = re.compile(r'^(B|AB|AR|AG|BC|BH|BN|BT|BV|BR|BZ|CS|CL|CJ|CT|CV|DB|DJ|GL|GR|GJ|HR|HD|IL|IS|IF|MM|MH|MS|NT|OT|PH|SM|SJ|SB|SV|TR|TM|TL|VS|VL|VN)[0-9]{2,3}[a-z]{3}$')
#				pattern_red1 = re.compile(r'^(B|AB|AR|AG|BC|BH|BN|BT|BV|BR|BZ|CS|CL|CJ|CT|CV|DB|DJ|GL|GR|GJ|HR|HD|IL|IS|IF|MM|MH|MS|NT|OT|PH|SM|SJ|SB|SV|TR|TM|TL|VS|VL|VN)[0-9]{3,7}$')
				pattern_black = re.compile(r'^[A-Z]{1,2}[0-9]{2,3}[A-Z]{3}$')
				pattern_red = re.compile(r'^[A-Z]{1,2}[0-9]{3,6}$') 
				match_black = pattern_black.search(plate)
				match_red = pattern_red.search(plate)
				if !match_black or !match_red:
					plates = filter(lambda a: a != plate, plates)
			images_d[img]['PlatesList'] = plates
	return images_d

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


if __name__ == '__main__':
	images_d = {}
	images_d = get_files('../images', images_d)
	images_d = read_csv('results.csv', images_d)
	write_csv(images_d, 'image_dictionary.csv')
	plates_d = create_plate_dict(images_d)
	write_csv(plates_d, 'plates_dictionary.csv')
