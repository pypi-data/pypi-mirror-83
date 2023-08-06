#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
from SDK.FdeGeometry.ICurve import ICurve
Props={"PointCount":{"t":"int","v":0,
"F":"g"},"SegmentCount":{"t":"int","v":0,
"F":"g"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ICompoundLine","F":"g"}}
class ICompoundLine(ICurve):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._PointCount=args.get("PointCount")
		self._SegmentCount=args.get("SegmentCount")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def addPointAfter(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"pointValue":{"t": "IPoint","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'AddPointAfter', 1, state)


	def addPointBefore(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"pointValue":{"t": "IPoint","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'AddPointBefore', 1, state)


	def addSegmentAfter(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"segment":{"t": "ISegment","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'AddSegmentAfter', 1, state)


	def addSegmentBefore(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"segment":{"t": "ISegment","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'AddSegmentBefore', 1, state)


	def appendPoint(self,arg0):  # 先定义函数 
		args = {
				"pointValue":{"t": "IPoint","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'appendPoint', 0, state)


	def appendSegment(self,arg0):  # 先定义函数 
		args = {
				"segment":{"t": "ISegment","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'AppendSegment', 1, state)


	def generalize(self,arg0):  # 先定义函数 
		args = {
				"maxAllowOffset":{"t": "N","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'generalize', 0, state)


	def getPoint(self,arg0):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'GetPoint', 1, state)


	def getSegment(self,arg0):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'GetSegment', 1, state)


	def removePoints(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"count":{"t": "N","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'RemovePoints', 1, state)


	def removeSegments(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"count":{"t": "N","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'RemoveSegments', 1, state)


	def segmentsChanged(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'segmentsChanged', 0, state)


	def smooth(self,arg0):  # 先定义函数 
		args = {
				"maxAllowOffset":{"t": "N","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'smooth', 0, state)


	def smoothLocal(self,arg0):  # 先定义函数 
		args = {
				"vertexIndex":{"t": "N","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'smoothLocal', 0, state)


	def updatePoint(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"pointValue":{"t": "IPoint","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'UpdatePoint', 1, state)


	def updateSegment(self,arg0,arg1):  # 先定义函数 
		args = {
				"index":{"t": "N","v": arg0},
				"segment":{"t": "ISegment","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'UpdateSegment', 1, state)

	@property
	def PointCount(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["PointCount"]

	@property
	def SegmentCount(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["SegmentCount"]

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
