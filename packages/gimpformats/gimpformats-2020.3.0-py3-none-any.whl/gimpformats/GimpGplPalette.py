#!/usr/bin/env python3
"""
Pure python implementation of the gimp gpl palette format
"""
from __future__ import annotations
import argparse

class GimpGplPalette:
	""" Pure python implementation of the gimp gpl palette format """
	def __init__(self, fileName=None):
		self.name = ''
		self.columns = 16
		self.colors = []
		self.colorNames = []
		if fileName is not None:
			self.load(fileName)

	def load(self, fileName: Union[BytesIO, str]):
		"""
		load a gimp file

		:param fileName: can be a file name or a file-like object
		"""
		if hasattr(fileName, 'read'):
			self.fileName = fileName.name
			f = fileName
		else:
			self.fileName = fileName
			f = open(fileName, 'r')
		data = f.read()
		f.close()
		self.decode(data)

	def decode(self, data):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		"""
		data = [s.strip() for s in data.split('\n')]
		if data[0] != "GIMP Palette":
			raise Exception('File format error.  Magic value mismatch.')
		self.name = data[1].split(':', 1)[-1].lstrip()
		self.columns = int(data[2].split(':', 1)[-1].lstrip())
		for line in data[3:]:
			if len(line) < 1 or line[0] == "#": # Commented Line
				continue
			line = line.split(None, 4)
			if len(line) < 3:
				continue
			self.colors.append((int(line[0]), int(line[1]), int(line[2])))
			if len(line) > 3:
				self.colorNames.append(line[3])
			else:
				self.colorNames.append(None)

	def encode(self):
		""" encode to a raw data stream """
		data = []
		data.append("GIMP Palette")
		data.append('Name: ' + str(self.name))
		data.append('Columns: ' + str(self.columns))
		data.append("#")
		for i, color in enumerate(self.colors):
			colorName = self.colorNames[i]
			line = str(color[0]).rjust(3) + ' ' + str(color[1]).rjust(3) + ' ' + str(
			color[2]).rjust(3)
			if colorName is not None:
				line = line + '\t' + colorName
			data.append(line)
		return ('\n'.join(data) + '\n').encode('utf-8')

	def save(self, tofileName=None, toExtension=None):
		""" save this gimp image to a file """
		if toExtension is None:
			if tofileName is not None:
				toExtension = tofileName.rsplit('.', 1)
				if len(toExtension) > 1:
					toExtension = toExtension[-1]
				else:
					toExtension = None
		if not hasattr(tofileName, 'write'):
			f = open(tofileName, 'wb')
		f.write(self.encode())
		f.close()

	def __repr__(self, indent=''):
		""" Get a textual representation of this object """
		ret = []
		if self.fileName is not None:
			ret.append('fileName: ' + self.fileName)
		ret.append('Name: ' + str(self.name))
		ret.append('Columns: ' + str(self.columns))
		ret.append('Colors:')
		for i, color in enumerate(self.colors):
			colorName = self.colorNames[i]
			line = '(%d,%d,%d)' % color[0], color[1], color[2]
			if colorName is not None:
				line = line + ' ' + colorName
		return '\n'.join(ret)

	def __eq__(self, other):
		""" perform a comparison """
		if other.name != self.name:
			return False
		if other.columns != self.columns:
			return False
		if len(self.colors) != len(other.colors):
			return False
		for i, c in enumerate(self.colors):
			if c != other.colors[i]:
				return False
			if self.colorNames[i] != other.colorNames[i]:
				return False
		return True

if __name__ == '__main__':
	""" CLI Entry Point """
	parser = argparse.ArgumentParser("GimpGplPalette.py")
	parser.add_argument("xcfdocument", action="store",
	help="xcf file to act on")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--dump", action="store_true",
	help="dump info about this file")
	args = parser.parse_args()

	gimpGplPalette = GimpGplPalette(args.xcfdocument)

	if args.dump:
		print(gimpGplPalette)
