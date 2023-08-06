#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"Border":{"t":"bool","v":False,
"F":"g"},"Location":{"t":"ILine","v":None,
"F":"g"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ITopoDirectedEdge","F":"g"}}
class ITopoDirectedEdge:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._Border=args.get("Border")
		self._Location=args.get("Location")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def equal(self,arg0):  # 先定义函数 
		args = {
				"x":{"t": "ITopoDirectedEdge","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Equal', 1, state)


	def getFacet(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'GetFacet', 1, state)


	def getTopoNode(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'GetTopoNode', 1, state)


	def next(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Next', 1, state)


	def notEqual(self,arg0):  # 先定义函数 
		args = {
				"x":{"t": "ITopoDirectedEdge","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'NotEqual', 1, state)


	def opposite(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Opposite', 1, state)


	def prev(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Prev', 1, state)

	@property
	def Border(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Border"]

	@property
	def Location(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Location",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Location",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Location", res)
		return PropsValueData["Location"]

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
