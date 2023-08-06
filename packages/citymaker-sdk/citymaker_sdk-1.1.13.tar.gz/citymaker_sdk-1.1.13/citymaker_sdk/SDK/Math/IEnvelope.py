#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"Center":{"t":"IVector3","v":None,
"F":"g"},"Depth":{"t":"double","v":0,
"F":"g"},"Height":{"t":"double","v":0,
"F":"g"},"MaxX":{"t":"double","v":0,
"F":"gs"},"MaxY":{"t":"double","v":0,
"F":"gs"},"MaxZ":{"t":"double","v":0,
"F":"gs"},"MinX":{"t":"double","v":0,
"F":"gs"},"MinY":{"t":"double","v":0,
"F":"gs"},"MinZ":{"t":"double","v":0,
"F":"gs"},"Width":{"t":"double","v":0,
"F":"g"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IEnvelope","F":"g"}}
class IEnvelope:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._Center=args.get("Center")
		self._Depth=args.get("Depth")
		self._Height=args.get("Height")
		self._MaxX=args.get("MaxX")
		self._MaxY=args.get("MaxY")
		self._MaxZ=args.get("MaxZ")
		self._MinX=args.get("MinX")
		self._MinY=args.get("MinY")
		self._MinZ=args.get("MinZ")
		self._Width=args.get("Width")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def clone(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Clone', 1, state)


	def contain(self,arg0):  # 先定义函数 
		args = {
				"val":{"t": "IVector3","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Contain', 1, state)


	def expandByEnvelope(self,arg0):  # 先定义函数 
		args = {
				"val":{"t": "IEnvelope","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'expandByEnvelope', 0, state)


	def expandByVector(self,arg0):  # 先定义函数 
		args = {
				"val":{"t": "IVector3","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'expandByVector', 0, state)


	def intersect(self,arg0):  # 先定义函数 
		args = {
				"envelope":{"t": "IEnvelope","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Intersect', 1, state)


	def isIntersect(self,arg0):  # 先定义函数 
		args = {
				"envelope":{"t": "IEnvelope","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'IsIntersect', 1, state)


	def set(self,arg0,arg1,arg2,arg3,arg4,arg5):  # 先定义函数 
		args = {
				"minX":{"t": "N","v": arg0},
				"maxX":{"t": "N","v": arg1},
				"minY":{"t": "N","v": arg2},
				"maxY":{"t": "N","v": arg3},
				"minZ":{"t": "N","v": arg4},
				"maxZ":{"t": "N","v": arg5}
		}
		state = ""
		CM.AddPrototype(self,args, 'set', 0, state)


	def setByEnvelope(self,arg0):  # 先定义函数 
		args = {
				"val":{"t": "IEnvelope","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'setByEnvelope', 0, state)


	def valid(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Valid', 1, state)

	@property
	def Center(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Center",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Center",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Center", res)
		return PropsValueData["Center"]

	@property
	def Depth(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Depth"]

	@property
	def Height(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Height"]

	@property
	def MaxX(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["MaxX"]

	@MaxX.setter
	def MaxX(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "MaxX", val)
		args = {}
		args["MaxX"] = PropsTypeData.get("MaxX")
		args["MaxX"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"MaxX", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"MaxX",JsonData)

	@property
	def MaxY(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["MaxY"]

	@MaxY.setter
	def MaxY(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "MaxY", val)
		args = {}
		args["MaxY"] = PropsTypeData.get("MaxY")
		args["MaxY"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"MaxY", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"MaxY",JsonData)

	@property
	def MaxZ(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["MaxZ"]

	@MaxZ.setter
	def MaxZ(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "MaxZ", val)
		args = {}
		args["MaxZ"] = PropsTypeData.get("MaxZ")
		args["MaxZ"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"MaxZ", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"MaxZ",JsonData)

	@property
	def MinX(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["MinX"]

	@MinX.setter
	def MinX(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "MinX", val)
		args = {}
		args["MinX"] = PropsTypeData.get("MinX")
		args["MinX"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"MinX", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"MinX",JsonData)

	@property
	def MinY(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["MinY"]

	@MinY.setter
	def MinY(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "MinY", val)
		args = {}
		args["MinY"] = PropsTypeData.get("MinY")
		args["MinY"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"MinY", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"MinY",JsonData)

	@property
	def MinZ(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["MinZ"]

	@MinZ.setter
	def MinZ(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "MinZ", val)
		args = {}
		args["MinZ"] = PropsTypeData.get("MinZ")
		args["MinZ"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"MinZ", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"MinZ",JsonData)

	@property
	def Width(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Width"]

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
