#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ITopologicalOperator2D","F":"g"}}
class ITopologicalOperator2D:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def buffer2D(self,arg0,arg1):  # 先定义函数 
		args = {
				"dis":{"t": "N","v": arg0},
				"style":{"t": "gviBufferStyle","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Buffer2D', 1, state)


	def convexHull2D(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'ConvexHull2D', 1, state)


	def difference2D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IGeometry","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Difference2D', 1, state)


	def intersection2D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IGeometry","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Intersection2D', 1, state)


	def isSimple2D(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'IsSimple2D', 1, state)


	def simplify2D(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Simplify2D', 1, state)


	def symmetricDifference2D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IGeometry","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'SymmetricDifference2D', 1, state)


	def union2D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IGeometry","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Union2D', 1, state)

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
