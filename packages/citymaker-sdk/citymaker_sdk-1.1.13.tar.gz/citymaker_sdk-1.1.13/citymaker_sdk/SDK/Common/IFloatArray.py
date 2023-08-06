#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"Array":{"t":"A","v":None,
"F":"gs"},"IsEmpty":{"t":"bool","v":None,
"F":"g"},"Length":{"t":"int","v":0,
"F":"g"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IFloatArray","F":"g"}}
class IFloatArray:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._Array=args.get("Array")
		self._IsEmpty=args.get("IsEmpty")
		self._Length=args.get("Length")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def append(self,arg0):  # 先定义函数 
		args = {
				"value":{"t": "N","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'append', 0, state)


	def clear(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'clear', 0, state)


	def get(self,arg0):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Get', 1, state)


	def set(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"newVal":{"t": "N","v": arg1}
		}
		state = ""
		CM.AddPrototype(self,args, 'set', 0, state)

	@property
	def Array(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Array"]

	@Array.setter
	def Array(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Array", val)
		args = {}
		args["Array"] = PropsTypeData.get("Array")
		args["Array"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Array", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Array",JsonData)

	@property
	def IsEmpty(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["IsEmpty"]

	@property
	def Length(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Length"]

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
