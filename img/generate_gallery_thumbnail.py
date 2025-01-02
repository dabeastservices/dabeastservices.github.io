from PIL import Image, ExifTags
import json
import os
import shutil

global registeredImages
registeredImages = {}



sortingOrder = [
]

# Creates a thumbnail of the input image and saves it to the output path.
def createThumbnail(inputPath, outputPath, size=(1024, 1024)):
	with Image.open(inputPath) as img:
		# Rotate the image according to its EXIF orientation
		if hasattr(img, '_getexif'): # Only present in JPEGs
			for orientation in ExifTags.TAGS.keys():
				if ExifTags.TAGS[orientation] == 'Orientation':
					break

			e = img._getexif() # Returns None if no EXIF data
			if e is not None:
				exif = dict(e.items())
				orientation = exif.get(orientation, None)
				if orientation == 3:
					img = img.rotate(180, expand=True)
				elif orientation == 6:
					img = img.rotate(270, expand=True)
				elif orientation == 8:
					img = img.rotate(90, expand=True)

		# Create thumbnail
		img.thumbnail(size)
		img.save(outputPath)

# Check if a file is an image based on its extension.
def isImageFile(filename):
	valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
	return os.path.splitext(filename)[1].lower() in valid_extensions

# Remove a directory and all its contents.
def removeDirectory(path):
	if os.path.exists(path):
		shutil.rmtree(path)

# Register the image in constructing the gallery code
def registerImage(fileName, imagePath):
	global registeredImages
	parts = imagePath.split('\\')
	# Determine if the imagePath includes a directory or is in the base directory
	if len(parts) > 1:
		# Case where there is a directory in the path
		folderName = parts[-2]
		try:
			imageNumber = int(parts[-1].split('.')[0].split('-')[0])
		except ValueError:
			imageNumber = 1000000 #parts[-1]
	else:
		# Case where the imagePath is just a filename in the base directory
		folderName = parts[0].split('.')[0]
		imageNumber = 0  # Default value for base directory images

	folderName = folderName.replace('\'', '\\\'') # For JavaScript output
	if folderName not in registeredImages:
		registeredImages[folderName] = []

	registeredImages[folderName].append((imageNumber, fileName))

# Sort the registered images by their image number
def sortRegisterImage():
	global registeredImages
	for key in registeredImages:
		registeredImages[key].sort(key=lambda x: x[0] if type(x[0]) is int else 0)
		

# Make the thumbnail directory and fill its contents with the contents from 'gallery'
def makeThumbnailDirectory(inputPath, outputPath):
	# # Remove the existing output directory first
	# removeDirectory(outputPath)

	for root, dirs, files in os.walk(inputPath):
		# Skip directories named 'raw' and 'Miscellaneous'
		for d in dirs:
			basename = os.path.basename(d)
			if basename.startswith('raw_') or basename == 'raw' or basename == 'Miscellaneous':
				dirs.remove(d)

		for fileName in files:
			if isImageFile(fileName):
				# Construct full file path
				fullFilePath = os.path.join(root, fileName)

				print('Processing', fullFilePath, '...')
				registerImage(fileName, fullFilePath)
				#continue
				
				# Construct the corresponding output file path
				relativePath = os.path.relpath(fullFilePath, inputPath)
				thumbnailFilePath = os.path.join(outputPath, relativePath)

				# Create directory if it doesn't exist
				os.makedirs(os.path.dirname(thumbnailFilePath), exist_ok=True)

				# Create thumbnail
				createThumbnail(fullFilePath, thumbnailFilePath)
	sortRegisterImage()
	# Now remove the sort index from the registeredImages
	for key in registeredImages:
		for i in range(len(registeredImages[key])):
			registeredImages[key][i] = registeredImages[key][i][1]

# Generate the JavaScript code given the dictionary of image data
def generateCode(registeredImages):
	print('let images = {')

	for key in sortingOrder:
		value = registeredImages[key]
		if type(value) is not int: value = json.dumps(value).replace('"', "'")
		print(f'\t\'{key}\': {value},')

	for key in registeredImages:
		if key in sortingOrder: continue
		value = registeredImages[key]
		if type(value) is not int: value = json.dumps(value).replace('"', "'")
		print(f'\t\'{key}\': {value},')
	print('};')


if __name__ == '__main__':
	makeThumbnailDirectory('fullres', '.')
	print('OK.')
	print()
	print()
	print()
	print()
	print()
	print()
	print()
	print()
	print()
	generateCode(registeredImages)
