#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
from SDK.FdeGeometry.ICurve import ICurve
Props={"CenterPoint":{"t":"IPoint","v":None,
"F":"gs"},"Normal":{"t":"IVector3","v":None,
"F":"gs"},"Radius":{"t":"double","v":0,
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ICircle","F":"g"}}
class ICircle(ICurve):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._CenterPoint=args.get("CenterPoint")
		self._Normal=args.get("Normal")
		self._Radius=args.get("Radius")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def constructCenterAndRadius(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"center":{"t": "IPoint","v": arg0},
				"radius":{"t": "N","v": arg1},
				"normal":{"t": "IVector3","v": arg2}
		}
		state = ""
		return CM.AddPrototype(self,args, 'ConstructCenterAndRadius', 1, state)

	@property
	def CenterPoint(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"CenterPoint",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"CenterPoint",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "CenterPoint", res)
		return PropsValueData["CenterPoint"]

	@CenterPoint.setter
	def CenterPoint(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "CenterPoint", val)
		args = {}
		args["CenterPoint"] = PropsTypeData.get("CenterPoint")
		args["CenterPoint"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"CenterPoint", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"CenterPoint",JsonData)

	@property
	def Normal(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Normal",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Normal",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Normal", res)
		return PropsValueData["Normal"]

	@Normal.setter
	def Normal(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Normal", val)
		args = {}
		args["Normal"] = PropsTypeData.get("Normal")
		args["Normal"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Normal", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Normal",JsonData)

	@property
	def Radius(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Radius"]

	@Radius.setter
	def Radius(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Radius", val)
		args = {}
		args["Radius"] = PropsTypeData.get("Radius")
		args["Radius"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Radius", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Radius",JsonData)

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
