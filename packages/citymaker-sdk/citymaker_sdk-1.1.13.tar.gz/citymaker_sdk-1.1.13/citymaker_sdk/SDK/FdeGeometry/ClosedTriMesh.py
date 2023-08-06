#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
from SDK.FdeGeometry.IClosedTriMesh import IClosedTriMesh
Props={"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"ClosedTriMesh","F":"g"}}
class ClosedTriMesh(IClosedTriMesh):
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def distance2D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IGeometry","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Distance2D', 1, state)


	def distance3D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IGeometry","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Distance3D', 1, state)


	def distanceEx2D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IGeometry","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'DistanceEx2D', 1, state)


	def distanceEx3D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IGeometry","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'DistanceEx3D', 1, state)


	def nearestPoint2D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IPoint","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'NearestPoint2D', 1, state)


	def nearestPoint3D(self,arg0):  # 先定义函数 
		args = {
				"other":{"t": "IPoint","v": arg0}
		}
		state = ""
		return CM.AddPrototype(self,args, 'NearestPoint3D', 1, state)


	def moveModel(self,arg0):  # 先定义函数 
		args = {
				"deltaPos":{"t": "IVector3","v": arg0}
		}
		state = "new"
		return CM.AddPrototype(self,args, 'MoveModel', 1, state)


	def rotateModel(self,arg0,arg1):  # 先定义函数 
		args = {
				"rotateCenter":{"t": "IVector3","v": arg0},
				"angle":{"t": "IEulerAngle","v": arg1}
		}
		state = "new"
		return CM.AddPrototype(self,args, 'RotateModel', 1, state)


	def scaleModel(self,arg0):  # 先定义函数 
		args = {
				"scaleRatio":{"t": "IVector3","v": arg0}
		}
		state = "new"
		return CM.AddPrototype(self,args, 'ScaleModel', 1, state)


	def moveFeature(self,arg0,arg1):  # 先定义函数 
		args = {
				"deltaPos":{"t": "IVector3","v": arg0},
				"mode":{"t": "N","v": arg1}
		}
		state = "new"
		return CM.AddPrototype(self,args, 'MoveFeature', 1, state)


	def rotateFeature(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"rotateCenter":{"t": "IVector3","v": arg0},
				"angle":{"t": "IEulerAngle","v": arg1},
				"mode":{"t": "N","v": arg2}
		}
		state = "new"
		return CM.AddPrototype(self,args, 'RotateFeature', 1, state)


	def scaleFeature(self,arg0,arg1):  # 先定义函数 
		args = {
				"scaleRatio":{"t": "IVector3","v": arg0},
				"mode":{"t": "N","v": arg1}
		}
		state = "new"
		return CM.AddPrototype(self,args, 'ScaleFeature', 1, state)


	def move2D(self,arg0,arg1):  # 先定义函数 
		args = {
				"dX":{"t": "N","v": arg0},
				"dY":{"t": "N","v": arg1}
		}
		state = ""
		CM.AddPrototype(self,args, 'move2D', 0, state)


	def move3D(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"dX":{"t": "N","v": arg0},
				"dY":{"t": "N","v": arg1},
				"dZ":{"t": "N","v": arg2}
		}
		state = ""
		CM.AddPrototype(self,args, 'move3D', 0, state)


	def rotate2D(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"centerX":{"t": "N","v": arg0},
				"centerY":{"t": "N","v": arg1},
				"angle":{"t": "N","v": arg2}
		}
		state = ""
		CM.AddPrototype(self,args, 'rotate2D', 0, state)


	def rotate3D(self,arg0,arg1,arg2,arg3,arg4,arg5,arg6):  # 先定义函数 
		args = {
				"axisX":{"t": "N","v": arg0},
				"axisY":{"t": "N","v": arg1},
				"axisZ":{"t": "N","v": arg2},
				"centerX":{"t": "N","v": arg3},
				"centerY":{"t": "N","v": arg4},
				"centerZ":{"t": "N","v": arg5},
				"angle":{"t": "N","v": arg6}
		}
		state = ""
		CM.AddPrototype(self,args, 'rotate3D', 0, state)


	def scale2D(self,arg0,arg1,arg2,arg3):  # 先定义函数 
		args = {
				"scaleX":{"t": "N","v": arg0},
				"scaleY":{"t": "N","v": arg1},
				"centerX":{"t": "N","v": arg2},
				"centerY":{"t": "N","v": arg3}
		}
		state = ""
		CM.AddPrototype(self,args, 'scale2D', 0, state)


	def scale3D(self,arg0,arg1,arg2,arg3,arg4,arg5):  # 先定义函数 
		args = {
				"scaleX":{"t": "N","v": arg0},
				"scaleY":{"t": "N","v": arg1},
				"scaleZ":{"t": "N","v": arg2},
				"centerX":{"t": "N","v": arg3},
				"centerY":{"t": "N","v": arg4},
				"centerZ":{"t": "N","v": arg5}
		}
		state = ""
		CM.AddPrototype(self,args, 'scale3D', 0, state)

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
