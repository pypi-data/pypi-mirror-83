#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
from SDK.FdeGeometry.IGeometry import IGeometry
Props={"Centroid":{"t":"IPoint","v":None,
"F":"g"},"IsClosed":{"t":"bool","v":False,
"F":"g"},"PointOnSurface":{"t":"IPoint","v":None,
"F":"g"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ISurface","F":"g"}}
class ISurface(IGeometry):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._Centroid=args.get("Centroid")
		self._IsClosed=args.get("IsClosed")
		self._PointOnSurface=args.get("PointOnSurface")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def area(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Area', 1, state)


	def getBoundary(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'GetBoundary', 1, state)


	def isPointOnSurface(self,arg0):  # 先定义函数 
		args = {
				"pointValue":{"t": "IPoint","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'IsPointOnSurface', 1, state)

	@property
	def Centroid(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Centroid",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Centroid",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Centroid", res)
		return PropsValueData["Centroid"]

	@property
	def IsClosed(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["IsClosed"]

	@property
	def PointOnSurface(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"PointOnSurface",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"PointOnSurface",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "PointOnSurface", res)
		return PropsValueData["PointOnSurface"]

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
