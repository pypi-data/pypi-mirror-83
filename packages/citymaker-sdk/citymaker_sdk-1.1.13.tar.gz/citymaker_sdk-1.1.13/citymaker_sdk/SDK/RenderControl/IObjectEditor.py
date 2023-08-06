#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"isEditing":{"t":"bool","v":False,
"F":"g"},"PolygonCreateMode":{"t":"gviPolygonCreateMode","v":0,
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IObjectEditor","F":"g"}}
class IObjectEditor:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._isEditing=args.get("isEditing")
		self._PolygonCreateMode=args.get("PolygonCreateMode")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def addMovingFeatures(self,arg0,arg1):  # 先定义函数 
		args = {
				"layer":{"t": "IFeatureLayer","v": arg0},
				"rowBuffers":{"t": "IRowBufferCollection","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'addMovingFeatures', 1, state)


	def cancelEdit(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'cancelEdit', 0, state)


	def move(self,arg0):  # 先定义函数 
		args = {
				"move":{"t": "IVector3","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'move', 0, state)


	def rotate(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"axis":{"t": "IVector3","v": arg0},
				"center":{"t": "IVector3","v": arg1},
				"angle":{"t": "N","v": arg2}
		}
		state = ""
		CM.AddPrototype(self,args, 'rotate', 0, state)


	def scale(self,arg0,arg1):  # 先定义函数 
		args = {
				"scale":{"t": "IVector3","v": arg0},
				"center":{"t": "IVector3","v": arg1}
		}
		state = ""
		CM.AddPrototype(self,args, 'scale', 0, state)


	def startEditFeatureGeometry(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"rowBuffer":{"t": "IRowBuffer","v": arg0},
				"featureLayer":{"t": "IFeatureLayer","v": arg1},
				"editType":{"t": "gviGeoEditType","v": arg2}
		}
		state = ""
		return CM.AddPrototype(self,args, 'startEditFeatureGeometry', 1, state)


	def startEditPlot(self,arg0,arg1):  # 先定义函数 
		args = {
				"plot":{"t": "IPlot","v": arg0},
				"editType":{"t": "gviGeoEditType","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'StartEditPlot', 1, state)


	def startEditRenderGeometry(self,arg0,arg1):  # 先定义函数 
		args = {
				"renderGeometry":{"t": "IRenderGeometry","v": arg0},
				"editType":{"t": "gviGeoEditType","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'startEditRenderGeometry', 1, state)


	def startMoveFeatures(self,arg0):  # 先定义函数 
		args = {
				"cRS":{"t": "S","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'startMoveFeatures', 1, state)


	def finishEdit(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'finishEdit', 0, state)

	@property
	def isEditing(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["isEditing"]

	@property
	def PolygonCreateMode(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["PolygonCreateMode"]

	@PolygonCreateMode.setter
	def PolygonCreateMode(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "PolygonCreateMode", val)
		args = {}
		args["PolygonCreateMode"] = PropsTypeData.get("PolygonCreateMode")
		args["PolygonCreateMode"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"PolygonCreateMode", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"PolygonCreateMode",JsonData)

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
