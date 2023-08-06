#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
from SDK.FdeGeometry.IGeometry import IGeometry
Props={"EndPoint":{"t":"IPoint","v":None,
"F":"gs"},"IsClosed":{"t":"bool","v":False,
"F":"g"},"Length":{"t":"double","v":0,
"F":"g"},"Midpoint":{"t":"IPoint","v":None,
"F":"g"},"StartPoint":{"t":"IPoint","v":None,
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ICurve","F":"g"}}
class ICurve(IGeometry):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._EndPoint=args.get("EndPoint")
		self._IsClosed=args.get("IsClosed")
		self._Length=args.get("Length")
		self._Midpoint=args.get("Midpoint")
		self._StartPoint=args.get("StartPoint")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def reverseOrientation(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'reverseOrientation', 0, state)

	@property
	def EndPoint(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"EndPoint",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"EndPoint",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "EndPoint", res)
		return PropsValueData["EndPoint"]

	@EndPoint.setter
	def EndPoint(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "EndPoint", val)
		args = {}
		args["EndPoint"] = PropsTypeData.get("EndPoint")
		args["EndPoint"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"EndPoint", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"EndPoint",JsonData)

	@property
	def IsClosed(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["IsClosed"]

	@property
	def Length(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Length"]

	@property
	def Midpoint(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Midpoint",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Midpoint",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Midpoint", res)
		return PropsValueData["Midpoint"]

	@property
	def StartPoint(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"StartPoint",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"StartPoint",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "StartPoint", res)
		return PropsValueData["StartPoint"]

	@StartPoint.setter
	def StartPoint(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "StartPoint", val)
		args = {}
		args["StartPoint"] = PropsTypeData.get("StartPoint")
		args["StartPoint"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"StartPoint", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"StartPoint",JsonData)

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
