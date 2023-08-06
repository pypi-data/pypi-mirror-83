#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"conflict":{"t":"IConflict","v":None,
"F":"g"},"onReplicationStatusChanged":{"t":"Dispatch","v":"",
"F":"s"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IReplication","F":"g"}}
class IReplication:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

		#CM.AddRenderEventCB(Events)
		#CM.AddRenderEvent(this, Events)

	def initParam(self,args):
		self._conflict=args.get("conflict")
		self._onReplicationStatusChanged=args.get("onReplicationStatusChanged")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def mergeFrom(self,arg0,arg1):  # 先定义函数 
		args = {
				"source":{"t": "IFeatureDataSet","v": arg0},
				"truncate":{"t": "B","v": arg1}
		}
		state = ""
		CM.AddPrototype(self,args, 'mergeFrom', 0, state)


	def mergeTo(self,arg0,arg1):  # 先定义函数 
		args = {
				"destination":{"t": "IFeatureDataSet","v": arg0},
				"truncate":{"t": "B","v": arg1}
		}
		state = ""
		CM.AddPrototype(self,args, 'mergeTo', 0, state)


	def setStepValue(self,arg0):  # 先定义函数 
		args = {
				"newVal":{"t": "N","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'setStepValue', 0, state)

	@property
	def conflict(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		jsonData = CM.setJsonData("get_",PropsValueData.get("_HashCode"),"conflict",None)
		res=socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"conflict",jsonData)
		CM.addPropsValue(PropsValueData["_HashCode"], "conflict", res)
		return PropsValueData["conflict"]

	@property
	def onReplicationStatusChanged(self):
		pass

	@onReplicationStatusChanged.setter
	def onReplicationStatusChanged(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "onReplicationStatusChanged", val)
		args = {}
		args["onReplicationStatusChanged"] = PropsTypeData.get("onReplicationStatusChanged")
		args["onReplicationStatusChanged"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"onReplicationStatusChanged", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"onReplicationStatusChanged",JsonData)

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
