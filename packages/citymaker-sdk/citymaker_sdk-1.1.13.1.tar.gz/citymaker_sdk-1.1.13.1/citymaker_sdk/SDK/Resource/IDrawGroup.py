#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"CompleteMapFactor":{"t":"float","v":0.5,
"F":"gs"},"IsEmpty":{"t":"bool","v":False,
"F":"g"},"PrimitiveCount":{"t":"int","v":0,
"F":"g"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IDrawGroup","F":"g"}}
#Events = {CompleteMapTextureName:{fn:null}LightMapTextureName:{fn:null}}
class IDrawGroup:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._CompleteMapFactor=args.get("CompleteMapFactor")
		self._IsEmpty=args.get("IsEmpty")
		self._PrimitiveCount=args.get("PrimitiveCount")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def addPrimitive(self,arg0):  # 先定义函数 
		args = {
				"primitive":{"t": "IDrawPrimitive","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'AddPrimitive', 1, state)


	def clear(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'clear', 0, state)


	def computeNormal(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'computeNormal', 0, state)


	def getPrimitive(self,arg0):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'GetPrimitive', 1, state)


	def insertPrimitive(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"primitive":{"t": "IDrawPrimitive","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'InsertPrimitive', 1, state)


	def removePrimitive(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"count":{"t": "N","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'RemovePrimitive', 1, state)


	def setPrimitive(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"primitive":{"t": "IDrawPrimitive","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'SetPrimitive', 1, state)

	@property
	def CompleteMapFactor(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["CompleteMapFactor"]

	@CompleteMapFactor.setter
	def CompleteMapFactor(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "CompleteMapFactor", val)
		args = {}
		args["CompleteMapFactor"] = PropsTypeData.get("CompleteMapFactor")
		args["CompleteMapFactor"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"CompleteMapFactor", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"CompleteMapFactor",JsonData)

	@property
	def IsEmpty(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["IsEmpty"]

	@property
	def PrimitiveCount(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["PrimitiveCount"]

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
