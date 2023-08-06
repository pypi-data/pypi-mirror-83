#!/usr/bin/env Python
# coding=utf-8#
#作者： tony1
import os, sys,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import Utils.classmake as CM
import Utils.SocketApiServe as socketApi 
Props={"HasMirror":{"t":"bool","v":False,
"F":"g"},"HasShear":{"t":"bool","v":False,
"F":"g"},"IsIdentity":{"t":"bool","v":False,
"F":"g"},"M11":{"t":"double","v":0,
"F":"gs"},"M12":{"t":"double","v":0,
"F":"gs"},"M13":{"t":"double","v":0,
"F":"gs"},"M14":{"t":"double","v":0,
"F":"gs"},"M21":{"t":"double","v":0,
"F":"gs"},"M22":{"t":"double","v":0,
"F":"gs"},"M23":{"t":"double","v":0,
"F":"gs"},"M24":{"t":"double","v":0,
"F":"gs"},"M31":{"t":"double","v":0,
"F":"gs"},"M32":{"t":"double","v":0,
"F":"gs"},"M33":{"t":"double","v":0,
"F":"gs"},"M34":{"t":"double","v":0,
"F":"gs"},"M41":{"t":"double","v":0,
"F":"gs"},"M42":{"t":"double","v":0,
"F":"gs"},"M43":{"t":"double","v":0,
"F":"gs"},"M44":{"t":"double","v":0,
"F":"gs"},"_HashCode":{"t":"S","v":"","F":"g"},
"propertyType":{"t":"S","v":"IMatrix","F":"g"}}
class IMatrix:
	def __init__(self,args):
		CM.AddProps(self, Props, args)
		#CM.AddDefineProperty(self, Props)

	def initParam(self,args):
		self._HasMirror=args.get("HasMirror")
		self._HasShear=args.get("HasShear")
		self._IsIdentity=args.get("IsIdentity")
		self._M11=args.get("M11")
		self._M12=args.get("M12")
		self._M13=args.get("M13")
		self._M14=args.get("M14")
		self._M21=args.get("M21")
		self._M22=args.get("M22")
		self._M23=args.get("M23")
		self._M24=args.get("M24")
		self._M31=args.get("M31")
		self._M32=args.get("M32")
		self._M33=args.get("M33")
		self._M34=args.get("M34")
		self._M41=args.get("M41")
		self._M42=args.get("M42")
		self._M43=args.get("M43")
		self._M44=args.get("M44")
		self._HashCode=args.get("_HashCode")
		self._propertyType=args.get("propertyType")

	def clone(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Clone', 1, state)


	def compose(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"trans":{"t": "IVector3","v": arg0},
				"scale":{"t": "IVector3","v": arg1},
				"euler":{"t": "IEulerAngle","v": arg2}
		}
		state = ""
		CM.AddPrototype(self,args, 'compose', 0, state)


	def compose2(self,arg0,arg1,arg2,arg3,arg4,arg5):  # 先定义函数 
		args = {
				"trans":{"t": "IVector3","v": arg0},
				"scale":{"t": "IVector3","v": arg1},
				"rotationAngle":{"t": "N","v": arg2},
				"rotationDir":{"t": "IVector3","v": arg3},
				"shearAngle":{"t": "N","v": arg4},
				"shearDir":{"t": "IVector3","v": arg5}
		}
		state = ""
		CM.AddPrototype(self,args, 'compose2', 0, state)


	def decompose(self,arg0,arg1,arg2):  # 先定义函数 
		args = {
				"trans":{"t": "IVector3","v": arg0},
				"scale":{"t": "IVector3","v": arg1},
				"euler":{"t": "IEulerAngle","v": arg2}
		}
		state = ""
		return CM.AddPrototype(self,args, 'Decompose', 1, state)


	def decompose2(self,arg0,arg1,arg2,arg3):  # 先定义函数 
		args = {
				"trans":{"t": "IVector3","v": arg0},
				"scale":{"t": "IVector3","v": arg1},
				"rotationAngle":{"t": "N","v": arg2},
				"rotationDir":{"t": "IVector3","v": arg3}
		}
		state = ""
		CM.AddPrototype(self,args, 'decompose2', 0, state)


	def getRotation(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'GetRotation', 1, state)


	def getScale(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'GetScale', 1, state)


	def getTranslate(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'GetTranslate', 1, state)


	def interpolatePosition(self,arg0,arg1,arg2,arg3,arg4,arg5,arg6):  # 先定义函数 
		args = {
				"mat1":{"t": "IMatrix","v": arg0},
				"velocity1":{"t": "N","v": arg1},
				"time1":{"t": "N","v": arg2},
				"mat2":{"t": "IMatrix","v": arg3},
				"velocity2":{"t": "N","v": arg4},
				"time2":{"t": "N","v": arg5},
				"time":{"t": "N","v": arg6}
		}
		state = ""
		CM.AddPrototype(self,args, 'interpolatePosition', 0, state)


	def inverse(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'inverse', 0, state)


	def makeIdentity(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'makeIdentity', 0, state)


	def multiplyVector(self,arg0,arg1):  # 先定义函数 
		args = {
				"src":{"t": "IVector3","v": arg0},
				"pVal":{"t": "IVector3","v": arg1}
		}
		state = ""
		CM.AddPrototype(self,args, 'multiplyVector', 0, state)


	def set(self,arg0,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11,arg12,arg13,arg14,arg15):  # 先定义函数 
		args = {
				"a00":{"t": "N","v": arg0},
				"a01":{"t": "N","v": arg1},
				"a02":{"t": "N","v": arg2},
				"a03":{"t": "N","v": arg3},
				"a10":{"t": "N","v": arg4},
				"a11":{"t": "N","v": arg5},
				"a12":{"t": "N","v": arg6},
				"a13":{"t": "N","v": arg7},
				"a20":{"t": "N","v": arg8},
				"a21":{"t": "N","v": arg9},
				"a22":{"t": "N","v": arg10},
				"a23":{"t": "N","v": arg11},
				"a30":{"t": "N","v": arg12},
				"a31":{"t": "N","v": arg13},
				"a32":{"t": "N","v": arg14},
				"a33":{"t": "N","v": arg15}
		}
		state = ""
		CM.AddPrototype(self,args, 'set', 0, state)


	def setByMatrix(self,arg0):  # 先定义函数 
		args = {
				"val":{"t": "IMatrix","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'setByMatrix', 0, state)


	def setRotation(self,arg0):  # 先定义函数 
		args = {
				"newVal":{"t": "IEulerAngle","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'setRotation', 0, state)


	def setScale(self,arg0):  # 先定义函数 
		args = {
				"newVal":{"t": "IVector3","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'setScale', 0, state)


	def setTranslate(self,arg0):  # 先定义函数 
		args = {
				"newVal":{"t": "IVector3","v": arg0}
		}
		state = ""
		CM.AddPrototype(self,args, 'setTranslate', 0, state)


	def transpose(self,):  # 先定义函数 
		args = {}
		state = ""
		CM.AddPrototype(self,args, 'transpose', 0, state)


	def valid(self,):  # 先定义函数 
		args = {}
		state = ""
		return CM.AddPrototype(self,args, 'Valid', 1, state)

	@property
	def HasMirror(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["HasMirror"]

	@property
	def HasShear(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["HasShear"]

	@property
	def IsIdentity(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["IsIdentity"]

	@property
	def M11(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M11"]

	@M11.setter
	def M11(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M11", val)
		args = {}
		args["M11"] = PropsTypeData.get("M11")
		args["M11"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M11", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M11",JsonData)

	@property
	def M12(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M12"]

	@M12.setter
	def M12(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M12", val)
		args = {}
		args["M12"] = PropsTypeData.get("M12")
		args["M12"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M12", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M12",JsonData)

	@property
	def M13(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M13"]

	@M13.setter
	def M13(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M13", val)
		args = {}
		args["M13"] = PropsTypeData.get("M13")
		args["M13"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M13", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M13",JsonData)

	@property
	def M14(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M14"]

	@M14.setter
	def M14(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M14", val)
		args = {}
		args["M14"] = PropsTypeData.get("M14")
		args["M14"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M14", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M14",JsonData)

	@property
	def M21(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M21"]

	@M21.setter
	def M21(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M21", val)
		args = {}
		args["M21"] = PropsTypeData.get("M21")
		args["M21"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M21", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M21",JsonData)

	@property
	def M22(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M22"]

	@M22.setter
	def M22(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M22", val)
		args = {}
		args["M22"] = PropsTypeData.get("M22")
		args["M22"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M22", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M22",JsonData)

	@property
	def M23(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M23"]

	@M23.setter
	def M23(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M23", val)
		args = {}
		args["M23"] = PropsTypeData.get("M23")
		args["M23"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M23", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M23",JsonData)

	@property
	def M24(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M24"]

	@M24.setter
	def M24(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M24", val)
		args = {}
		args["M24"] = PropsTypeData.get("M24")
		args["M24"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M24", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M24",JsonData)

	@property
	def M31(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M31"]

	@M31.setter
	def M31(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M31", val)
		args = {}
		args["M31"] = PropsTypeData.get("M31")
		args["M31"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M31", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M31",JsonData)

	@property
	def M32(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M32"]

	@M32.setter
	def M32(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M32", val)
		args = {}
		args["M32"] = PropsTypeData.get("M32")
		args["M32"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M32", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M32",JsonData)

	@property
	def M33(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M33"]

	@M33.setter
	def M33(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M33", val)
		args = {}
		args["M33"] = PropsTypeData.get("M33")
		args["M33"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M33", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M33",JsonData)

	@property
	def M34(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M34"]

	@M34.setter
	def M34(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M34", val)
		args = {}
		args["M34"] = PropsTypeData.get("M34")
		args["M34"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M34", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M34",JsonData)

	@property
	def M41(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M41"]

	@M41.setter
	def M41(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M41", val)
		args = {}
		args["M41"] = PropsTypeData.get("M41")
		args["M41"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M41", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M41",JsonData)

	@property
	def M42(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M42"]

	@M42.setter
	def M42(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M42", val)
		args = {}
		args["M42"] = PropsTypeData.get("M42")
		args["M42"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M42", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M42",JsonData)

	@property
	def M43(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M43"]

	@M43.setter
	def M43(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M43", val)
		args = {}
		args["M43"] = PropsTypeData.get("M43")
		args["M43"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M43", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M43",JsonData)

	@property
	def M44(self):
		if hasattr(self,"_HashCode") is False:
			return
		PropsValueData = CM.getPropsValueData(self._HashCode)
		return PropsValueData["M44"]

	@M44.setter
	def M44(self,val):
		PropsTypeData = CM.getPropsTypeData(self._HashCode)
		PropsValueData = CM.getPropsValueData(self._HashCode)
		CM.addPropsValue(PropsValueData.get("_HashCode"), "M44", val)
		args = {}
		args["M44"] = PropsTypeData.get("M44")
		args["M44"]["v"] = val
		JsonData = CM.setJsonData("set_",PropsValueData.get("_HashCode"),"M44", args)
		socketApi.postMessage({"propertyType": PropsTypeData["propertyType"]["v"],"_HashCode": PropsValueData["_HashCode"]},"M44",JsonData)

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
