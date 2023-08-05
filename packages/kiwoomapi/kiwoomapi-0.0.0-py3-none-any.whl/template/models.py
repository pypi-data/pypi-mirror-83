# -*- coding: utf-8 -*-
"""
"""
# print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import inspect
# ============================================================ External-Library.
# from bson.objectid import ObjectId
# ============================================================ My-Library.
import idebug as dbg
import ipandas as ipd
import ipymongo as mongo
# ============================================================ Project.
from pjtname import PJT_NAME
# ============================================================ Constant.





# ============================================================
"""BaseModels."""
# ============================================================
class GenBaseModel:
    """
    General Base Model.
    PyMongoDB 연결없이 일반적인 클래스에서 자주 사용하는 기능들을 Model 을 통해 제공.
    (Thread 생성 수를 최소화 시키기 위함.)
    """
    def attributize(self, dic):
        try:
            for k, v in dic.items():
                # setattr(self, k, v)
                self.__setattr__(k, v)
        except Exception as e:
            dbg.exception(locals(), f"{__name__}.{inspect.stack()[0][3]}")
        finally:
            return self
    def attributize_flocals(self, frame):
        dic = {k:v for k,v in frame.f_locals.items() if k not in ['self','__class__']}


class NonIOModel(GenBaseModel, ipd.DfBaseModel):
    def __init__(self):
        pass

class __IOModel__(mongo.Model, GenBaseModel, ipd.DfBaseModel):
    def __init__(self):
        super().__init__(PJT_NAME)
# ============================================================
"""DerivedModels."""
# ============================================================
class DerivedModel(__IOModel__):
    def __init__(self):
        super().__init__()
        self.modeling(__class__)
