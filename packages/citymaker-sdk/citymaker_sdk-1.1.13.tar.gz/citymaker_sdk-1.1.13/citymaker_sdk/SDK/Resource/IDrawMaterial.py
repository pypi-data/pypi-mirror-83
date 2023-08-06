#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"CullMode":{"t":"gviCullFaceMode","v":1,
"F":"gs"},"DepthBias":{"t":"double","v":0,
"F":"gs"},"DiffuseColor":{"t":"Color","v":"",
"F":"gs"},"EnableBlend":{"t":"bool","v":False,
"F":"gs"},"EnableLight":{"t":"bool","v":False,
"F":"gs"},"SpecularColor":{"t":"Color","v":"",
"F":"gs"},"WrapModeS":{"t":"gviTextureWrapMode","v":1,
"F":"gs"},"WrapModeT":{"t":"gviTextureWrapMode","v":1,
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IDrawMaterial","F":"g"}}
#Events = {TextureName:{fn:null}}
class IDrawMaterial:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._CullMode=args.get("CullMode")
		self._DepthBias=args.get("DepthBias")
		self._DiffuseColor=args.get("DiffuseColor")
		self._EnableBlend=args.get("EnableBlend")
		self._EnableLight=args.get("EnableLight")
		self._SpecularColor=args.get("SpecularColor")
		self._WrapModeS=args.get("WrapModeS")
		self._WrapModeT=args.get("WrapModeT")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")
	@property
	def CullMode(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["CullMode"]

	@CullMode.setter
	def CullMode(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "CullMode", val)
		args = {}
		args["CullMode"] = PropsTypeData.get("CullMode")
		args["CullMode"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"CullMode", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"CullMode",JsonData)

	@property
	def DepthBias(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["DepthBias"]

	@DepthBias.setter
	def DepthBias(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "DepthBias", val)
		args = {}
		args["DepthBias"] = PropsTypeData.get("DepthBias")
		args["DepthBias"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"DepthBias", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"DepthBias",JsonData)

	@property
	def DiffuseColor(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["DiffuseColor"]

	@DiffuseColor.setter
	def DiffuseColor(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "DiffuseColor", val)
		args = {}
		args["DiffuseColor"] = PropsTypeData.get("DiffuseColor")
		args["DiffuseColor"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"DiffuseColor", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"DiffuseColor",JsonData)

	@property
	def EnableBlend(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["EnableBlend"]

	@EnableBlend.setter
	def EnableBlend(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "EnableBlend", val)
		args = {}
		args["EnableBlend"] = PropsTypeData.get("EnableBlend")
		args["EnableBlend"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"EnableBlend", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"EnableBlend",JsonData)

	@property
	def EnableLight(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["EnableLight"]

	@EnableLight.setter
	def EnableLight(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "EnableLight", val)
		args = {}
		args["EnableLight"] = PropsTypeData.get("EnableLight")
		args["EnableLight"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"EnableLight", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"EnableLight",JsonData)

	@property
	def SpecularColor(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["SpecularColor"]

	@SpecularColor.setter
	def SpecularColor(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "SpecularColor", val)
		args = {}
		args["SpecularColor"] = PropsTypeData.get("SpecularColor")
		args["SpecularColor"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"SpecularColor", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"SpecularColor",JsonData)

	@property
	def WrapModeS(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["WrapModeS"]

	@WrapModeS.setter
	def WrapModeS(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "WrapModeS", val)
		args = {}
		args["WrapModeS"] = PropsTypeData.get("WrapModeS")
		args["WrapModeS"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"WrapModeS", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"WrapModeS",JsonData)

	@property
	def WrapModeT(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["WrapModeT"]

	@WrapModeT.setter
	def WrapModeT(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "WrapModeT", val)
		args = {}
		args["WrapModeT"] = PropsTypeData.get("WrapModeT")
		args["WrapModeT"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"WrapModeT", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"WrapModeT",JsonData)

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
