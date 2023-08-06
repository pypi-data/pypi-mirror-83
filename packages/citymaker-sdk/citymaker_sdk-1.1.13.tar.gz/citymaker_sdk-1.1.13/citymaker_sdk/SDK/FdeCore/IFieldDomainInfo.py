#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"defaultValue":{"t":"object","v":"",
"F":"gs"},"domain":{"t":"IDomain","v":None,
"F":"gs"},"inherited":{"t":"bool","v":False,
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IFieldDomainInfo","F":"g"}}
#Events = {fieldName:{fn:null}}
class IFieldDomainInfo:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._defaultValue=args.get("defaultValue")
		self._domain=args.get("domain")
		self._inherited=args.get("inherited")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")
	@property
	def defaultValue(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["defaultValue"]

	@defaultValue.setter
	def defaultValue(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "defaultValue", val)
		args = {}
		args["defaultValue"] = PropsTypeData.get("defaultValue")
		args["defaultValue"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"defaultValue", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"defaultValue",JsonData)

	@property
	def domain(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"domain",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"domain",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "domain", res)
		return PropsValueData["domain"]

	@domain.setter
	def domain(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "domain", val)
		args = {}
		args["domain"] = PropsTypeData.get("domain")
		args["domain"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"domain", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"domain",JsonData)

	@property
	def inherited(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["inherited"]

	@inherited.setter
	def inherited(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "inherited", val)
		args = {}
		args["inherited"] = PropsTypeData.get("inherited")
		args["inherited"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"inherited", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"inherited",JsonData)

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
