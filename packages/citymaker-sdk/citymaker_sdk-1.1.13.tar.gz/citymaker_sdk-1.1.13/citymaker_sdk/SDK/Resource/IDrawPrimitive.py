#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"BakedTexcoordArray":{"t":"IFloatArray","v":"",
"F":"gs"},"ColorArray":{"t":"IUInt32Array","v":"",
"F":"gs"},"ElementCount":{"t":"int","v":0,
"F":"g"},"IndexArray":{"t":"IUInt16Array","v":"",
"F":"gs"},"IsEncrypted":{"t":"bool","v":False,
"F":"g"},"Material":{"t":"IDrawMaterial","v":None,
"F":"gs"},"NormalArray":{"t":"IFloatArray","v":"",
"F":"gs"},"PrimitiveMode":{"t":"gviPrimitiveMode","v":0,
"F":"gs"},"PrimitiveType":{"t":"gviPrimitiveType","v":0,
"F":"gs"},"TexcoordArray":{"t":"IFloatArray","v":"",
"F":"gs"},"VertexArray":{"t":"IFloatArray","v":"",
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IDrawPrimitive","F":"g"}}
class IDrawPrimitive:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._BakedTexcoordArray=args.get("BakedTexcoordArray")
		self._ColorArray=args.get("ColorArray")
		self._ElementCount=args.get("ElementCount")
		self._IndexArray=args.get("IndexArray")
		self._IsEncrypted=args.get("IsEncrypted")
		self._Material=args.get("Material")
		self._NormalArray=args.get("NormalArray")
		self._PrimitiveMode=args.get("PrimitiveMode")
		self._PrimitiveType=args.get("PrimitiveType")
		self._TexcoordArray=args.get("TexcoordArray")
		self._VertexArray=args.get("VertexArray")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def encrypt(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'encrypt', 0, state)

	@property
	def BakedTexcoordArray(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"BakedTexcoordArray",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"BakedTexcoordArray",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "BakedTexcoordArray", res)
		return PropsValueData["BakedTexcoordArray"]

	@BakedTexcoordArray.setter
	def BakedTexcoordArray(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "BakedTexcoordArray", val)
		args = {}
		args["BakedTexcoordArray"] = PropsTypeData.get("BakedTexcoordArray")
		args["BakedTexcoordArray"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"BakedTexcoordArray", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"BakedTexcoordArray",JsonData)

	@property
	def ColorArray(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"ColorArray",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"ColorArray",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "ColorArray", res)
		return PropsValueData["ColorArray"]

	@ColorArray.setter
	def ColorArray(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "ColorArray", val)
		args = {}
		args["ColorArray"] = PropsTypeData.get("ColorArray")
		args["ColorArray"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"ColorArray", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"ColorArray",JsonData)

	@property
	def ElementCount(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["ElementCount"]

	@property
	def IndexArray(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"IndexArray",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"IndexArray",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "IndexArray", res)
		return PropsValueData["IndexArray"]

	@IndexArray.setter
	def IndexArray(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "IndexArray", val)
		args = {}
		args["IndexArray"] = PropsTypeData.get("IndexArray")
		args["IndexArray"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"IndexArray", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"IndexArray",JsonData)

	@property
	def IsEncrypted(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["IsEncrypted"]

	@property
	def Material(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"Material",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Material",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "Material", res)
		return PropsValueData["Material"]

	@Material.setter
	def Material(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "Material", val)
		args = {}
		args["Material"] = PropsTypeData.get("Material")
		args["Material"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"Material", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"Material",JsonData)

	@property
	def NormalArray(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"NormalArray",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"NormalArray",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "NormalArray", res)
		return PropsValueData["NormalArray"]

	@NormalArray.setter
	def NormalArray(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "NormalArray", val)
		args = {}
		args["NormalArray"] = PropsTypeData.get("NormalArray")
		args["NormalArray"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"NormalArray", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"NormalArray",JsonData)

	@property
	def PrimitiveMode(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["PrimitiveMode"]

	@PrimitiveMode.setter
	def PrimitiveMode(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "PrimitiveMode", val)
		args = {}
		args["PrimitiveMode"] = PropsTypeData.get("PrimitiveMode")
		args["PrimitiveMode"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"PrimitiveMode", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"PrimitiveMode",JsonData)

	@property
	def PrimitiveType(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["PrimitiveType"]

	@PrimitiveType.setter
	def PrimitiveType(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "PrimitiveType", val)
		args = {}
		args["PrimitiveType"] = PropsTypeData.get("PrimitiveType")
		args["PrimitiveType"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"PrimitiveType", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"PrimitiveType",JsonData)

	@property
	def TexcoordArray(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"TexcoordArray",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"TexcoordArray",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "TexcoordArray", res)
		return PropsValueData["TexcoordArray"]

	@TexcoordArray.setter
	def TexcoordArray(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "TexcoordArray", val)
		args = {}
		args["TexcoordArray"] = PropsTypeData.get("TexcoordArray")
		args["TexcoordArray"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"TexcoordArray", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"TexcoordArray",JsonData)

	@property
	def VertexArray(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"VertexArray",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"VertexArray",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "VertexArray", res)
		return PropsValueData["VertexArray"]

	@VertexArray.setter
	def VertexArray(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "VertexArray", val)
		args = {}
		args["VertexArray"] = PropsTypeData.get("VertexArray")
		args["VertexArray"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"VertexArray", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"VertexArray",JsonData)

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
