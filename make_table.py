# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ExifTags
import os

def


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
	exif = get_info('images/G0587646.JPG')
	print exif['DateTime']
	print get_decimal_coordinates(exif['GPSInfo'])
