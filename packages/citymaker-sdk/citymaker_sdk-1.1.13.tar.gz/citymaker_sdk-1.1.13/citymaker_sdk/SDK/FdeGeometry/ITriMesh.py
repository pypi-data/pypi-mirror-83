#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
from SDK.FdeGeometry.ISurface import ISurface
Props={"DirectedEdgeCount":{"t":"int","v":0,
"F":"g"},"FacetCount":{"t":"int","v":0,
"F":"g"},"VertexCount":{"t":"int","v":0,
"F":"g"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ITriMesh","F":"g"}}
class ITriMesh(ISurface):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._DirectedEdgeCount=args.get("DirectedEdgeCount")
		self._FacetCount=args.get("FacetCount")
		self._VertexCount=args.get("VertexCount")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def addPoint(self,arg0):  # 先定义函数 
		args = {
				"point":{"t": "IPoint","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'AddPoint', 1, state)


	def addTriangle(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"handlef":{"t": "ITopoNode","v": arg0},
				"handles":{"t": "ITopoNode","v": arg1},
				"handlet":{"t": "ITopoNode","v": arg2}
		}
		state = ""
		return CM.AddPrototype(self,args, 'AddTriangle', 1, state)


	def batchExport(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'BatchExport', 1, state)


	def beginEdge(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'BeginEdge', 1, state)


	def beginFacet(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'BeginFacet', 1, state)


	def beginVertex(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'BeginVertex', 1, state)


	def endEdge(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'EndEdge', 1, state)


	def endFacet(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'EndFacet', 1, state)


	def endVertex(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'EndVertex', 1, state)


	def eraseConnectedEdge(self,arg0):  # 先定义函数 
		args = {
				"handle":{"t": "ITopoDirectedEdge","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'EraseConnectedEdge', 1, state)


	def eraseConnectedFacet(self,arg0):  # 先定义函数 
		args = {
				"handle":{"t": "ITopoFacet","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'EraseConnectedFacet', 1, state)


	def eraseFacet(self,arg0):  # 先定义函数 
		args = {
				"handle":{"t": "ITopoFacet","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'EraseFacet', 1, state)


	def getPoint(self,arg0):  # 先定义函数 
		args = {
				"handle":{"t": "ITopoNode","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'GetPoint', 1, state)


	def intersectPlane(self,arg0,arg1):  # 先定义函数 
		args = {
				"normal":{"t": "IVector3","v": arg0},
				"constant":{"t": "N","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'IntersectPlane', 1, state)


	def lineSegmentIntersect(self,arg0):  # 先定义函数 
		args = {
				"line":{"t": "ILine","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'LineSegmentIntersect', 1, state)


	def locate(self,arg0):  # 先定义函数 
		args = {
				"point":{"t": "IPoint","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Locate', 1, state)


	def rayIntersect(self,arg0,arg1):  # 先定义函数 
		args = {
				"start":{"t": "IPoint","v": arg0},
				"dir":{"t": "IVector3","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'RayIntersect', 1, state)


	def removeUnconnectedVertices(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'RemoveUnconnectedVertices', 1, state)


	def setPoint(self,arg0,arg1):  # 先定义函数 
		args = {
				"handle":{"t": "ITopoNode","v": arg0},
				"point":{"t": "IPoint","v": arg1}
		}
		state = ""
		return CM.AddPrototype(self,args, 'SetPoint', 1, state)

	@property
	def DirectedEdgeCount(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["DirectedEdgeCount"]

	@property
	def FacetCount(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["FacetCount"]

	@property
	def VertexCount(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["VertexCount"]

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
