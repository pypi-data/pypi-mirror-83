# -*- coding: utf-8 -*-

import copy

def toAutoData(val):
    if type(val) == list:
        return autolist(val)
    elif type(val) == dict:
        return autodict(val)
    else: return val

class emptyitem:
    def __init__(self, parent, key):
        self.parent = parent
        self.key = key

    def __getitem__(self, key):
        return emptyitem(self, key)

    def __setitem__(self, key, val):
        if type(key) == int:
            newdata = autolist()
        else:
            newdata = autodict()
        newdata[key] = val
        self.parent[self.key] = newdata

    def __len__(self):
        return 0

    def __str__(self):
        return ""

    def __int__(self):
        return 0
    
    def __float__(self):
        return 0.0
    
    def __bool__(self):
        return False

    def __iter__(self):
        return iter([])

    def __contains__(self, item):
        return False

    def keys(self):
        return []
    
    def append(self, item):
        newdata = autolist()
        newdata.append(item)
        self.parent[self.key] = newdata

    def sort(self, *params):
        pass

    def clear(self):
        pass

    def to_same_type(self, val):
        if type(val) is str:
            return ""
        if type(val) is int:
            return 0
        if type(val) is float:
            return 0.0
        return None

    def __iadd__(self, val):
        if type(val) in (list, tuple):
            val = autolist(val)
        return copy.copy(val)

    def __ior__(self, val):
        return val
    
    def __ixor__(self, val):
        return val
    
    def __iand__(self, val):
        return self.to_same_type(val)

    def __isub__(self, val):
        return -val

    def __imul__(self, val):
        return self.to_same_type(val)
    
    def __add__(self, val):
        return val
    
    def __radd__(self, val):
        return val

    def __neg__(self):
        return 0
    
    def __sub__(self, val):
        return -val
    
    def __rsub__(self, val):
        return val
    
    def __mul__(self, val):
        return 0
    
    def __rmul__(self, val):
        return 0
    
    def __truediv__(self, val):
        return 0 / val

    def __rtruediv__(self, val):
        return val / 0.0
    
    def __floordiv__(self, val):
        return 0 // val
    
    def __rfloordiv__(self, val):
        return val // 0
    
    def __and__(self, val):
        return 0
    
    def __rand__(self, val):
        return 0
    
    def __or__(self, val):
        return val
    
    def __ror__(self, val):
        return val
    
    def __xor__(self, val):
        return val
    
    def __rxor__(self, val):
        return val

    def __lt__(self, val):
        if type(val) == emptyitem:
            return False
        return self.to_same_type(val) < val
    
    def __rlt__(self, val):
        if type(val) == emptyitem:
            return False
        return val < self.to_same_type(val)
    
    def __le__(self, val):
        if type(val) == emptyitem:
            return True
        return self.to_same_type(val) <= val
    
    def __rle__(self, val):
        if type(val) == emptyitem:
            return True
        return val <= self.to_same_type(val)

    def __gt__(self, val):
        if type(val) == emptyitem:
            return False
        return self.to_same_type(val) > val
    
    def __rgt__(self, val):
        if type(val) == emptyitem:
            return False
        return val > self.to_same_type(val)
    
    def __ge__(self, val):
        if type(val) == emptyitem:
            return True
        return self.to_same_type(val) >= val
    
    def __rge__(self, val):
        if type(val) == emptyitem:
            return True
        return val >= self.to_same_type(val)

    def __eq__(self, val):
        if type(val) == emptyitem:
            return True
        return self.to_same_type(val) == val
    
    def __req__(self, val):
        if type(val) == emptyitem:
            return True
        return val == self.to_same_type(val)
    
    def __ne__(self, val):
        if type(val) == emptyitem:
            return False
        return self.to_same_type(val) != val
    
    def __rne__(self, val):
        if type(val) == emptyitem:
            return False
        return val != self.to_same_type(val)

class autodict(dict):
    empty = object()

    def __init__(self, initData = None):
        if isinstance(initData, dict):
            for key in initData.keys():
                dict.__setitem__(self, key, toAutoData(initData[key]))
        elif initData != None:
            raise Exception("Invalid type")

    def aget(self, key, deffunc):
        item = dict.get(self, key, autodict.empty)
        if item != autodict.empty:
            return item
        if type(key) == str:
            if deffunc == None:
                return emptyitem(self, key)
            else:
                item = deffunc()
                dict.__setitem__(self, key, item)
                return item
        else:
            raise TypeError("autodict key must be str")

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return emptyitem(self, key)
        #item = dict.get(self, key, autodict.empty)
        #if item != autodict.empty:
        #    return item
        #return emptyitem(self, key)

    def __setitem__(self, key, val):
        if type(val) == emptyitem:
            if key in self:
                dict.__setitem__(self, key, None)
            return
        dict.__setitem__(self, key, val)

class autolist(list):
    def __init__(self, initData = None):
        if hasattr(initData, "__iter__"):
            for item in initData:
                self.append(toAutoData(item))
        elif initData != None:
            raise TypeError("autolist initData must be list")

    def aget(self, key, deffunc):
        t = type(key)
        if t == int:
            if key >= len(self) or list.__getitem__(self, key) == None:
                if deffunc == None:
                    return emptyitem(self, key)
                else:
                    item = deffunc()
                    self[key] = item
                    return item
            return list.__getitem__(self, key)
        elif t == slice:
            return list.__getitem__(self, key)
        else:
            raise IndexError("autolist key must be integer")

    def __getitem__(self, key):
        try:
            val = list.__getitem__(self, key)
            if val == None:
                return emptyitem(self, key)
            return val
        except :
            if type(key) == int:
                return emptyitem(self, key)
            raise IndexError()

    def __setitem__(self, key, val):
        if type(val) == emptyitem:
            if key < len(self):
                list.__setitem__(self, key, None)
            return
        if key >= len(self):
            for _ in range(0, key - len(self)): self.append(None)
            self.append(val)
        else:
            list.__setitem__(self, key, val)

    def __iadd__(self, val):
        if type(val) == emptyitem:
            return self
        elif not isinstance(val, list):
            raise TypeError("Cannot add autolist to " + str(type(val)))
        list.__iadd__(self, val)
        return self
    
    def __add__(self, val):
        return autolist(list.__add__(self, val))

    def __mul__(self, val):
        a = autolist(self)
        list.__imul__(a, val)
        return a


def defined(obj):
    if obj == None:
        return False
    elif type(obj) == emptyitem:
        return False
    else:
        return True
