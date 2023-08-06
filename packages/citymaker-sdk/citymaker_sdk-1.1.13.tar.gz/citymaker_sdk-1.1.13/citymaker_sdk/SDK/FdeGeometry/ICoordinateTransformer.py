#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ICoordinateTransformer","F":"g"}}
class ICoordinateTransformer:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def inverseTransformXY(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'InverseTransformXY', 1, state)


	def inverseTransformXYArray(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'InverseTransformXYArray', 1, state)


	def inverseTransformXYZ(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'InverseTransformXYZ', 1, state)


	def inverseTransformXYZArray(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'InverseTransformXYZArray', 1, state)


	def transformXY(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'TransformXY', 1, state)


	def transformXYArray(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'TransformXYArray', 1, state)


	def transformXYZ(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'TransformXYZ', 1, state)


	def transformXYZArray(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'TransformXYZArray', 1, state)


	def coordinateTransform(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"position":{"t": "IVector3","v": arg0},
				"sourceWKT":{"t": "S","v": arg1},
				"targetWKT":{"t": "S","v": arg2}
		}
		state = "new"
		return CM.AddPrototype(self,args, 'CoordinateTransform', 1, state)

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
