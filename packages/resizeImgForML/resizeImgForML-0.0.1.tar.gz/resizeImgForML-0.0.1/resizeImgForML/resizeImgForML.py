from PIL import Image, ImageOps
import glob
import os

class Resizer:
	def __init__(self):
		pass

	def detectAllJpgImg(self, path):
		path = os.path.join(path,"*.jpg")
		print(path)
		try:
			imgs = glob.glob(path)			
		except:
			imgs = None
		if imgs != None:
			imgs = glob.glob("*.jpg")
			print("Image detect Sccessfly!")
			return imgs
		else:
			print("cannot detect any Image")

	def detectOneJpgImg(self, path):
		print(path)
		imgList = []
		try:
			img = Image.open(path)			
		except:
			img = None
		if img != None:
			print("Image detect Sccessfly!")
			return img
		else:
			print("cannot detect any Image")

	def expandSquare(self, img, backGroundColor):
		wdth, hght = img.size
		if wdth == hght:
			return img
		elif wdth > hght:
			result = Image.new(img.mode, (wdth, wdth), backGroundColor)
			result.paste(img, (0, (wdth - hght) // 2))
			return result
		else:
			result = Image.new(img.mode, (hght, hght), backGroundColor)
			result.paste(img, ((hght - wdth) // 2, 0))
			return result

	def resizeBlackBackedMultipleImg(self,imgs,size):
		for i in imgs:
			openim = Image.open(i)
			im = ImageOps.invert(openim)
			im_new = self.expandSquare(im, "black").resize((size, size))
			im_new.convert("L")
			im_new.save('./_blacked{}'.format(i), quality=100)
	
	def resizeBlackBackedOneImg(self,img,size):
		openim = img
		im = ImageOps.invert(openim)
		im_new = self.expandSquare(im, "black").resize((size, size))
		im_new.convert("L")
		im_new.save('./_blacked.jpg', quality=100)