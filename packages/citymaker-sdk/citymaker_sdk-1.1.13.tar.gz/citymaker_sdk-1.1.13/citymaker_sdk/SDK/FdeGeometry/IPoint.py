#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
from SDK.FdeGeometry.IGeometry import IGeometry
Props={"Id":{"t":"double","v":0,
"F":"gs"},"Position":{"t":"IVector3","v":None,
"F":"gs"},"X":{"t":"double","v":0,
"F":"gs"},"Y":{"t":"double","v":0,
"F":"gs"},"Z":{"t":"double","v":0,
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IPoint","F":"g"}}
#Events = {M:{fn:null}}
class IPoint(IGeometry):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._Id=args.get("Id")
		self._Position=args.get("Position")
		self._X=args.get("X")
		self._Y=args.get("Y")
		self._Z=args.get("Z")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def setCoords(self,arg0,arg1,arg2,arg3,arg4):  # 先定义函数 
		args = {
				"x":{"t": "N","v": arg0},
				"y":{"t": "N","v": arg1},
				"z":{"t": "N","v": arg2},
				"m":{"t": "S","v": arg3},
				"id":{"t": "N","v": arg4}
		}
		state = ""
		CM.AddPrototype(self,args, 'setCoords', 0, state)

	@property
	def Id(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Id"]

	@Id.setter
	def Id(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Id", val)
		args = {}
		args["Id"] = PropsTypeData.get("Id")
		args["Id"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Id", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Id",JsonData)

	@property
	def Position(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Position",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Position",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Position", res)
		return PropsValueData["Position"]

	@Position.setter
	def Position(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Position", val)
		args = {}
		args["Position"] = PropsTypeData.get("Position")
		args["Position"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Position", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Position",JsonData)

	@property
	def X(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["X"]

	@X.setter
	def X(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "X", val)
		args = {}
		args["X"] = PropsTypeData.get("X")
		args["X"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"X", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"X",JsonData)

	@property
	def Y(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Y"]

	@Y.setter
	def Y(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Y", val)
		args = {}
		args["Y"] = PropsTypeData.get("Y")
		args["Y"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Y", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Y",JsonData)

	@property
	def Z(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Z"]

	@Z.setter
	def Z(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Z", val)
		args = {}
		args["Z"] = PropsTypeData.get("Z")
		args["Z"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Z", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Z",JsonData)

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
