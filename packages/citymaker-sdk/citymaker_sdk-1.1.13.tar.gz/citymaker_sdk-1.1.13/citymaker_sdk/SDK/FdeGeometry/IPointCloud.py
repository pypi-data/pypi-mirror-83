#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
from SDK.FdeGeometry.IGeometry import IGeometry
Props={"Colors":{"t":"nt32 []","v":"",
"F":"gs"},"Ids":{"t":"nt32 []","v":"",
"F":"gs"},"Measurements":{"t":"IDoubleArray","v":"",
"F":"gs"},"Positions":{"t":"IDoubleArray","v":"",
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IPointCloud","F":"g"}}
class IPointCloud(IGeometry):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._Colors=args.get("Colors")
		self._Ids=args.get("Ids")
		self._Measurements=args.get("Measurements")
		self._Positions=args.get("Positions")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")
	@property
	def Colors(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Colors"]

	@Colors.setter
	def Colors(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Colors", val)
		args = {}
		args["Colors"] = PropsTypeData.get("Colors")
		args["Colors"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Colors", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Colors",JsonData)

	@property
	def Ids(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Ids"]

	@Ids.setter
	def Ids(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Ids", val)
		args = {}
		args["Ids"] = PropsTypeData.get("Ids")
		args["Ids"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Ids", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Ids",JsonData)

	@property
	def Measurements(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Measurements",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Measurements",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Measurements", res)
		return PropsValueData["Measurements"]

	@Measurements.setter
	def Measurements(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Measurements", val)
		args = {}
		args["Measurements"] = PropsTypeData.get("Measurements")
		args["Measurements"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Measurements", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Measurements",JsonData)

	@property
	def Positions(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Positions",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Positions",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Positions", res)
		return PropsValueData["Positions"]

	@Positions.setter
	def Positions(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Positions", val)
		args = {}
		args["Positions"] = PropsTypeData.get("Positions")
		args["Positions"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Positions", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Positions",JsonData)

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
