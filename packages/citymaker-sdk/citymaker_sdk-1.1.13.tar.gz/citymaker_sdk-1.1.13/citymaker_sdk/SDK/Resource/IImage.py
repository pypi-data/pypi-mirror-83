#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"FrameInterval":{"t":"int","v":1000,
"F":"gs"},"FrameNumber":{"t":"int","v":0,
"F":"g"},"HasAlpha":{"t":"bool","v":False,
"F":"g"},"Height":{"t":"int","v":0,
"F":"g"},"ImageFormat":{"t":"gviImageFormat","v":0,
"F":"g"},"ImageType":{"t":"gviImageType","v":0,
"F":"g"},"IsEncrypted":{"t":"bool","v":False,
"F":"g"},"width":{"t":"int","v":0,
"F":"g"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IImage","F":"g"}}
class IImage:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._FrameInterval=args.get("FrameInterval")
		self._FrameNumber=args.get("FrameNumber")
		self._HasAlpha=args.get("HasAlpha")
		self._Height=args.get("Height")
		self._ImageFormat=args.get("ImageFormat")
		self._ImageType=args.get("ImageType")
		self._IsEncrypted=args.get("IsEncrypted")
		self._width=args.get("width")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def asBinary(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'AsBinary', 1, state)


	def compare(self,arg0):  # 先定义函数 
		args = {
				"otherImage":{"t": "IImage","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'compare', 1, state)


	def convertFormat(self,arg0):  # 先定义函数 
		args = {
				"newVal":{"t": "gviImageFormat","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'convertFormat', 0, state)


	def downSize(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'downSize', 0, state)


	def embedWatermark(self,arg0):  # 先定义函数 
		args = {
				"watermark":{"t": "IImage","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'embedWatermark', 0, state)


	def encrypt(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'encrypt', 0, state)


	def flip(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'flip', 0, state)


	def writeFile(self,arg0):  # 先定义函数 
		args = {
				"imageFile":{"t": "S","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'WriteFile', 1, state)

	@property
	def FrameInterval(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["FrameInterval"]

	@FrameInterval.setter
	def FrameInterval(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "FrameInterval", val)
		args = {}
		args["FrameInterval"] = PropsTypeData.get("FrameInterval")
		args["FrameInterval"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"FrameInterval", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"FrameInterval",JsonData)

	@property
	def FrameNumber(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["FrameNumber"]

	@property
	def HasAlpha(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["HasAlpha"]

	@property
	def Height(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Height"]

	@property
	def ImageFormat(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["ImageFormat"]

	@property
	def ImageType(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["ImageType"]

	@property
	def IsEncrypted(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["IsEncrypted"]

	@property
	def width(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["width"]

	@property
	def propertyType(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["propertyType"]

	def to_json(self):
		result={}
		for k, v in self.__dict__.items():
			if k=="_HashCode":
				result[k] = v
			else:
				result[k.strip("_")] = v
		return result
