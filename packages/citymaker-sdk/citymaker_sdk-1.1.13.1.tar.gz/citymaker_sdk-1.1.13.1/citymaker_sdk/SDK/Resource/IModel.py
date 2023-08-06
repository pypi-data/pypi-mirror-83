#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"Envelope":{"t":"IEnvelope","v":None,
"F":"g"},"GroupCount":{"t":"int","v":0,
"F":"g"},"IsEmpty":{"t":"bool","v":False,
"F":"g"},"IsEncrypted":{"t":"bool","v":False,
"F":"g"},"ModelType":{"t":"gviModelType","v":1,
"F":"g"},"Radius":{"t":"double","v":0,
"F":"g"},"Singleton":{"t":"bool","v":True,
"F":"gs"},"SwitchSize":{"t":"int","v":0,
"F":"gs"},"TotalTriangleCount":{"t":"number","v":False,
"F":"g"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IModel","F":"g"}}
class IModel:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._Envelope=args.get("Envelope")
		self._GroupCount=args.get("GroupCount")
		self._IsEmpty=args.get("IsEmpty")
		self._IsEncrypted=args.get("IsEncrypted")
		self._ModelType=args.get("ModelType")
		self._Radius=args.get("Radius")
		self._Singleton=args.get("Singleton")
		self._SwitchSize=args.get("SwitchSize")
		self._TotalTriangleCount=args.get("TotalTriangleCount")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def addGroup(self,arg0):  # 先定义函数 
		args = {
				"drawGroup":{"t": "IDrawGroup","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'AddGroup', 1, state)


	def asBinary(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'AsBinary', 1, state)


	def checkAndRebuild(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'checkAndRebuild', 0, state)


	def checkUp(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'CheckUp', 1, state)


	def checkUpFast(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'CheckUpFast', 1, state)


	def clear(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'clear', 0, state)


	def cloneAndTransform(self,arg0):  # 先定义函数 
		args = {
				"m":{"t": "IMatrix","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'CloneAndTransform', 1, state)


	def encrypt(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'encrypt', 0, state)


	def getGroup(self,arg0):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'GetGroup', 1, state)


	def getImageNames(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'GetImageNames', 1, state)


	def insertGroup(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"drawGroup":{"t": "IDrawGroup","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'InsertGroup', 1, state)


	def multiplyMatrix(self,arg0):  # 先定义函数 
		args = {
				"m":{"t": "IMatrix","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'multiplyMatrix', 0, state)


	def removeGroup(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"count":{"t": "N","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'RemoveGroup', 1, state)


	def setGroup(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"drawGroup":{"t": "IDrawGroup","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'SetGroup', 1, state)


	def valid(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Valid', 1, state)


	def writeFile(self,arg0,arg1):  # 先定义函数 
		args = {
				"filePath":{"t": "S","v": arg0},
				"images":{"t": "IPropertySet","v": arg1}
		}
		state = ""
		CM.AddPrototype(self,args, 'writeFile', 0, state)


	def writeFileWithMatrix(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"filePath":{"t": "S","v": arg0},
				"m":{"t": "IMatrix","v": arg1},
				"images":{"t": "IPropertySet","v": arg2}
		}
		state = ""
		CM.AddPrototype(self,args, 'writeFileWithMatrix', 0, state)

	@property
	def Envelope(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Envelope",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Envelope",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Envelope", res)
		return PropsValueData["Envelope"]

	@property
	def GroupCount(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["GroupCount"]

	@property
	def IsEmpty(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["IsEmpty"]

	@property
	def IsEncrypted(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["IsEncrypted"]

	@property
	def ModelType(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["ModelType"]

	@property
	def Radius(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Radius"]

	@property
	def Singleton(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["Singleton"]

	@Singleton.setter
	def Singleton(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Singleton", val)
		args = {}
		args["Singleton"] = PropsTypeData.get("Singleton")
		args["Singleton"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Singleton", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Singleton",JsonData)

	@property
	def SwitchSize(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["SwitchSize"]

	@SwitchSize.setter
	def SwitchSize(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "SwitchSize", val)
		args = {}
		args["SwitchSize"] = PropsTypeData.get("SwitchSize")
		args["SwitchSize"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"SwitchSize", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"SwitchSize",JsonData)

	@property
	def TotalTriangleCount(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["TotalTriangleCount"]

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
