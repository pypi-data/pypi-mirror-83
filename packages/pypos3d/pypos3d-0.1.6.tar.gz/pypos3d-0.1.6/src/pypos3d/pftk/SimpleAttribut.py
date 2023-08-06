# -*- coding: utf-8 -*-
# package: pypos3d.pftk
import logging
from collections import namedtuple

from pypos3d.wftk.PoserFileParser import PoserFileParser, ParsingErrorException
from pypos3d.pftk.PoserBasic import PoserConst, PoserObject, PoserToken, Lang, TAS, index, WBoolLine 


# 
#  *
#  
class SimpleAttribut(PoserObject):
  ''' Base class for single value entry of a Poser file :  NAME VALUE '''

  def __init__(self, n=None, value=None):
    super(SimpleAttribut, self).__init__()
    if n:
      self.setName(n.token)
      self.setPoserType(n)
    else:
      self.setPoserType(PoserToken.BADTOKEN)
        
    self._value = value

  #  (non-Javadoc)
  #    * @see deyme.v3d.poser.PoserObject#read(deyme.v3d.poser.PoserFileParser)
  #    
  def read(self, st):
    st.getToNextLine()
    #  FIX: 20090520 - Avoid to keep trailing spaces
    if st.sval:
      idx = len(st.sval) - 1
      while (idx >= 0) and (st.sval[idx].isspace()):
        idx -= 1
      self._value = st.sval[0:idx+1]
    else:
      self._value = None

  def getValue(self):
    return self._value

  def setValue(self, v):
      self._value = v

  def TAS(self, oldValue, newValue):
      if oldValue == self.getValue():
          self.setValue(newValue)

  def getIntegerValue(self):
      return int(self._value)

  def getDoubleValue(self):
      return float(self._value)

  def getBooleanValue(self):
      return (self._value != "0")

  #    * @see deyme.v3d.poser.PoserObject#write(java.io.FileWriter)
  #    
  def write(self, fw, pfx):
    
    v = self.getValue()
    if (v == None) or ("" == v):
      fw.write("{0:s}{1:s}\n".format(pfx, self.getName()))
    else:
      fw.write("{0:s}{1:s} {2:s}\n".format(pfx, self.getName(), v))




# addchild and weld attributs
class AddChildSA(SimpleAttribut):
  def __init__(self, realType = None, son = None, parent = None):
    super(AddChildSA, self).__init__(realType)
    self.l0 = son
    self.l1 = parent
    if parent:
      self.setValue(son + "\n\t" + parent)
    
  #  * Change the name of referenced part (actor, prop, hairProp, controlProp)  
  #  * @param oldPartName
  #  * @param newPartName
  def changeReference(self, oldPartName, newPartName):
    self.l0 = TAS(self.l0, oldPartName, newPartName)
    self.l1 = TAS(self.l1, oldPartName, newPartName)
    self.setValue(self.l0 + "\n\t" + self.l1)
    
  def read(self, st):
    st.getToNextLine()
    self.l0 = st.sval.strip()

    st.getToNextLine();
    self.l1 = st.sval.strip()
        
    self._value = self.l0 + "\n\t" + self.l1
    
  def getChildName(self): return self.l0
    
  def getParentName(self): return self.l1


# 
#  * Attribute alone on its line : "ON", "OFF" and flipped
#  
class OffSA(SimpleAttribut):

  def __init__(self, n = None):
    if n:
      super(OffSA, self).__init__(Lang[n], "")
    else:
      super(OffSA, self).__init__()
      
    self.setName(n)

  def read(self, st):
    st.getToNextLine()
    if (self.getPoserType() == PoserToken.E_flipped) and (st.sval != None):
      self._value = st.sval
    else:
      self._value = ""



# 
#  Color attribut
#  
class ColorSA(SimpleAttribut):

  def __init__(self):
    super(ColorSA, self).__init__()
    self.v0 = None
    self.v1 = None
    self.v2 = None
    self.v3 = None

  def read(self, st):
    st.getToken()
    self.v0 = st.sval
    st.getToken()
    self.v1 = st.sval
    st.getToken()
    self.v2 = st.sval
    st.getToken()
    self.v3 = st.sval
    self._value = self.v0 + " " + self.v1 + " " + self.v2 + " " + self.v3


# 
# Orientation Attribut
#  
class OrientationSA(SimpleAttribut):
  def __init__(self):
    super(OrientationSA, self).__init__()
    self.v0 = None
    self.v1 = None
    self.v2 = None

  def read(self, st):
    st.getToken()
    self.v0 = st.sval
    st.getToken()
    self.v1 = st.sval
    st.getToken()
    self.v2 = st.sval
    self._value = self.v0 + " " + self.v1 + " " + self.v2

# 
# Origin Attribut
#  
class OriginSA(SimpleAttribut):
  def __init__(self):
    super(OriginSA, self).__init__()
    self.v0 = None
    self.v1 = None
    self.v2 = None

  def read(self, st):
    st.getToken()
    self.v0 = st.sval
    st.getToken()
    self.v1 = st.sval
    st.getToken()
    self.v2 = st.sval
    self._value = self.v0 + " " + self.v1 + " " + self.v2

# 
# StorageOffseSA  Attribut
#  
class StorageOffsetSA(SimpleAttribut):
  def __init__(self):
    super(StorageOffsetSA, self).__init__()
    self.v0 = None
    self.v1 = None
    self.v2 = None
    self.setName("storageOffset")

  def read(self, st):
    st.getToken()
    self.v0 = st.sval
    st.getToken()
    self.v1 = st.sval
    st.getToken()
    self.v2 = st.sval
    self._value = self.v0 + " " + self.v1 + " " + self.v2

# 
# Just read the entire line
#  
class TextureMapSA(SimpleAttribut):
  def __init__(self):
    super(TextureMapSA, self).__init__()
    self._path = ""

  def read(self, st):
    st.getToNextLine()
    self._path = st.sval.strip()
    if self._path == PoserConst.C_NO_MAP:
      self._value = self._path
    else:
      st.getToNextLine()
      l1 = st.sval.strip() if st.sval else ''
      self._value = self._path + "\n\t" + l1

  def getPath(self): return self._path

#  
# Dimension attribut.
#  
class DimensionSA(SimpleAttribut):
  def __init__(self):
    super(DimensionSA, self).__init__()
    self.v0 = str()
    self.v1 = str()

  def read(self, st):
    st.getToken()
    self.v0 = st.sval
    st.getToken()
    self.v1 = st.sval
    self._value = self.v0 + " " + self.v1

#  
# endPoint attribut
#  
class EndPointSA(SimpleAttribut):
  def __init__(self):
    super(EndPointSA, self).__init__()
    self.v0 = str()
    self.v1 = str()
    self.v2 = str()

  def read(self, st):
    st.getToken()
    self.v0 = st.sval
    st.getToken()
    self.v1 = st.sval
    st.getToken()
    self.v2 = st.sval
    self._value = self.v0 + " " + self.v1 + " " + self.v2

# 
#  * This class represents the following attributs :
#  * widthRange       0.400000 0.700000
#  * lengthRange     0.040000 0.040000
#  * 
#  * Found in Poser 6 hair Prop.
#  
class HairRange(SimpleAttribut):
  def __init__(self):
    super(HairRange, self).__init__()
    self.v0 = str()
    self.v1 = str()

  def read(self, st):
    st.getToken()
    self.v0 = st.sval
    st.getToken()
    self.v1 = st.sval
    self._value = self.v0 + " " + self.v1


class SphereMathsRaw(SimpleAttribut):
  
  def __init__(self):
    super(SphereMathsRaw, self).__init__()
    self.m = [ '', '' ]

  # Read two 4x4 matrix of double
  def read(self, st):
    for i in range(0, 2):
      self.m[i] = ''
      for j in range(0,4):
        for k in range(0,4):
          st.getToken()
          while (st.ttype != PoserFileParser.TT_EOF) and (st.sval == None):
            st.skipToNextLine()
            st.getToken()
          self.m[i] += st.sval + ' '
           
        self.m[i] += '\n'
       
    self._value = "\n\t" + self.m[0] + "\n" + self.m[1]


# Tuple Key/Value for OpKey operation
valueKey = namedtuple('valueKey', ['key', 'val'])
#class valueKey(object):
#key = float()
#val = float()

# 
#  * This class represents a Poser Mathematical operation between channels
#  * 
#  
class ValueOpDelta(SimpleAttribut):
  #  Should not be used, because SimpleAttribut stores already the tokenID
  #  PTK deltaType = null;
  # 
  #    *  Default constructor needed by StructuredAttribut.

  # if figure and actor not null
  #   * Create an operation from a text expression
  #   * +QualifiedChannelName
  #   * -QualifiedChannelName
  #   * +VAL*QualifiedChannelName
  #   * 
  #   * QualifiedChannelName = [ActorName [':' bodyIndex] '.' ]ChannelName
  #   * 
  #   * @param fig
  #   * @param expr
  # public ValueOpDelta(PoserToken deltaType, String figureName, String actorName, String channelName, float ctrlRatio)
  # public ValueOpDelta(Figure fig, PoserActor curAct, String expr)
  def __init__(self, deltatype=None, pfigure=None, pactor=None, channelExpr=None, ctrlRatio=None, keys:'list of (key,val)'=None, src=None):
    super(ValueOpDelta, self).__init__(deltatype if deltatype else src.getPoserType() if src else None)
    self.lstValKeys = [ ]

    if pfigure and isinstance(pfigure, str) and pactor and channelExpr:
      self.l0 = pfigure
      self.l1 = pactor # As Name
      self.l2 = channelExpr # As Name
      self.controlRatio = ctrlRatio if ctrlRatio else 0.0
      
      if keys:
        # Force type to OpKey
        self.setPoserType(PoserToken.E_valueOpKey)
        for t in keys:
          self.addValueKey(t[0], t[1])


    elif pfigure and pactor and channelExpr:
      # String Cleaning
      expr = channelExpr.strip()
  
      if (expr[0]=="'") or (expr[0]=="\""):
        expr = expr[1:]
  
      if (expr[-1]=="'") or (expr[-1]=="\""):
        expr = expr[:len(expr) - 1]
  
      if (len(expr) < 2):
        logging.info("Too short string")
        return
  
      expr = expr.strip()
  
      c0 = expr[0]
      c1 = expr[1]
  
      qualifiedName = None
  
      opType = PoserToken.E_valueOpDeltaAdd if (c0.isdigit() or (c1.isdigit() and ((c0 == '+') or (c0 == '-')))) else \
               PoserToken.E_valueOpPlus  if c0=='+' else \
               PoserToken.E_valueOpMinus if c0=='-' else \
               PoserToken.E_valueOpTimes if c0=='*' else \
               PoserToken.E_valueOpDivideBy
  
      self.setPoserType(opType)
      self.setName(opType.token)
  
      if (opType==PoserToken.E_valueOpPlus) or (opType==PoserToken.E_valueOpMinus) or \
         (opType==PoserToken.E_valueOpTimes) or (opType==PoserToken.E_valueOpDivideBy):
        qualifiedName = expr[1:]
      else: # case(PoserToken.E_valueOpDeltaAdd):
        posstar = expr.find('*')
        self.controlRatio = float(expr[0:posstar])
        qualifiedName = expr[posstar + 1:]
  
      ptind = qualifiedName.find('.')
      if ptind < 0:
        self.l0 = "Figure " + str(pfigure.getBodyIndex())
        self.l1 = pactor.getName()
        self.l2 = qualifiedName
      else:
        self.l1 = qualifiedName[0:ptind]
        
        ptdp = qualifiedName.find(':')
        if (ptdp < 0):
          self.l1 += ':' + str(pfigure.getBodyIndex())
  
        self.l0 = "Figure " + str(index(self.l1))
        self.l2 = qualifiedName[ptind + 1:]
  
    elif src: # Copy Constructor
      self.setName(src.getPoserType().token)
      self.l0 = src.l0
      self.l1 = src.l1
      self.l2 = src.l2
      self.controlRatio = src.ctrlRatio
      
      if src.keys:
        for t in src.keys:
          self.addValueKey(t[0], t[1])

    else: # Default Creator called 
      self.l0 = ''
      self.l1 = ''
      self.l2 = ''
      self.controlRatio = 0.0

    self._value = self.l0 + "\n" + self.l1 + "\n" + self.l2

  # Add a pair {key value} the a OptKey operation
  # @param key
  # @param val
  def addValueKey(self, key, val):
    vk = valueKey(key, val)
    self.lstValKeys.append(vk)

  def read(self, st):
    st.skipToNextLine()
    st.getToNextLine()
    self.l0 = st.sval.strip()
    st.getToNextLine()
    self.l1 = st.sval.strip()
    st.getToNextLine()
    self.l2 = st.sval.strip()
    if self.getPoserType() == PoserToken.E_valueOpDeltaAdd:
      st.getToken()       #  Should get 'deltaAddDelta'      
      self.controlRatio = st.getNumber()
    else:
      if self.getPoserType() == PoserToken.E_valueOpKey:
        st.getToken() #  Should get 'beginValueKeys'
        #  While next token != endValueKeys : Store the keys
        fin = False
        while not fin:
          st.getToken()
          if st.ttype == PoserFileParser.TT_EOF:
            fin = True
            continue 

          if st.sval == None:
            continue 

          if st.ttype == PoserFileParser.TT_WORD:
            try:
              vc = Lang[st.sval]

              if vc==PoserToken.E_valueKey:                
                cle = st.getNumber()                
                val = st.getNumber()
                self.addValueKey(cle, val)
              elif vc==PoserToken.E_endValueKeys:
                fin = True
              else:
                logging.warning("L[" + st.lineno() + "] - Not Accepted :" + st.sval)
                continue 
            except KeyError:
              logging.warning("L[" + st.lineno() + "] - Not Accepted :" + st.sval)
              raise ParsingErrorException()


    _value = self.l0 + "\n" + self.l1 + "\n" + self.l2

  #    * @see deyme.v3d.poser.PoserObject#write(java.io.FileWriter)
  #    
  def write(self, fw, pfx):
    fw.write(pfx + self.getName() + '\n')
    #  FIX 20140329 - Use indentation to avoid some cross bug in Poser7
    #  fw.write(pfx + "\t" + getValue());
    fw.write(pfx + "\t" + self.l0 + '\n')
    fw.write(pfx + "\t" + self.l1 + '\n')
    fw.write(pfx + "\t" + self.l2 + '\n')
    #  fw.write(pfx + "\t" + getValue().replaceAll("\n", pfx+"\n"));
    if self.getPoserType()==PoserToken.E_valueOpDeltaAdd:
      fw.write(pfx + "\t" + "deltaAddDelta " + str(self.controlRatio) + '\n')
    elif self.getPoserType()==PoserToken.E_valueOpKey:
      fw.write(pfx + "\t" + "beginValueKeys" + '\n')
      for vk in self.lstValKeys:
        fw.write(pfx + "\t  valueKey " + str(vk.key) + " " + str(vk.val) + '\n')
      fw.write(pfx + "\t" + "endValueKeys" + '\n')

  def getFigureName(self): return self.l0

  def getGroupName(self): return self.l1

  def setGroupName(self, gn):
    self.l1 = gn
    self._value = self.l0 + "\n" + self.l1 + "\n" + self.l2

  def getChannelName(self): return self.l2

  def getControlRatio(self): return self.controlRatio

  def setControlRatio(self, cr):
    self.controlRatio = cr



# 
#  KS Attribut
#  
class KSA(SimpleAttribut):
  def __init__(self, frameNo = -1, f=0.0, src=None):
    self._noFrame = src._noFrame if src else frameNo
    self._factor = src._factor if src else f

    #    * 0x80 : hasFlag
    #    * 0x40 : sl
    #    * 0x20, 0x10, 0x08 : spl=0x20, lin=0x10, con=0x08
    #    * 0x00=sm 0x01=br
    self._flags = src._flags if src else 0x00

  def getFactor(self): return self._factor

  def setFactor(self, f):
    self._factor = f

  def getFrameNo(self): return self._noFrame

  def setSl(self, sl):
    if sl:
      self._flags |= 0x40
    else:
      self._flags &= 0xBF
    self._flags |= 0x80

  def isSl(self): return (self._flags & 0x40) != 0

  def getCurveType(self):
    if (self._flags & 0x20) != 0: return PoserToken.E_spl
    if (self._flags & 0x10) != 0: return PoserToken.E_lin
    if (self._flags & 0x08) != 0: return PoserToken.E_con
    return None

  def setCurveType(self, ct):
    if ct == PoserToken.E_spl:
      self._flags |= 0x20
    else:
      if ct == PoserToken.E_lin:
        self._flags |= 0x10
      else:
        self._flags |= 0x08
    self._flags |= 0x80

  def setCurveCnx(self, cc):
    if cc == PoserToken.E_br:
      self._flags |= 0x01
    else:
      self._flags &= 0xFE
    self._flags |= 0x80

  def write(self, fw, pfx):
    fw.write(pfx + "k {0:d} {1:g}\n".format(self._noFrame, self._factor))
    if (self._flags & 0x80) != 0:
      WBoolLine(fw, pfx, "sl", ((self._flags & 0x40) != 0))
      fw.write(pfx + "spl\n" if ((self._flags & 0x20) != 0) else ("lin\n" if ((self._flags & 0x10) != 0) else "con\n"))
      fw.write(pfx + ("br\n" if ((self._flags & 0x01) != 0) else "sm\n"))


#  
# linkParms attribut
#  
class LinkParmsSA(SimpleAttribut):
  def __init__(self, item='', parent=''):
    super(LinkParmsSA, self).__init__()
    self.MasterGroupName = item
    self.MasterChannelName = parent
    self.setValue(self.MasterGroupName + "\n\t" + self.MasterChannelName)
    self.SlaveGroupName = ''
    self.SlaveChannelName = ''
    
  def read(self, st):
    st.getToNextLine()
    self.MasterGroupName = st.sval.strip()
    st.getToNextLine()
    self.MasterChannelName = st.sval.strip()
    st.getToNextLine()
    self.SlaveGroupName = st.sval.strip()
    st.getToNextLine()
    self.SlaveChannelName = st.sval.strip()
    self._value = self.MasterGroupName + "\n\t" + self.MasterChannelName + "\n\t" + self.SlaveGroupName + "\n\t" + self.SlaveChannelName

  def getChildName(self): return self.MasterGroupName

  def getParentName(self): return self.MasterChannelName


#  
# LinkWeight attribut.
#  
class LinkWeightSA(SimpleAttribut):
  def __init__(self):
    super(LinkWeightSA, self).__init__()
    self.v0 = str()
    self.v1 = str()

  def read(self, st):
    st.getToken()
    self.v0 = st.sval
    st.getToken()
    self.v1 = st.sval
    self._value = self.v0 + " " + self.v1

#  
# Just read the entire line
#  
class NameSA(SimpleAttribut):
  def read(self, st):
    st.getToNextLine()
    self._value = st.sval







if __name__ == '__main__':
  print(dir(SimpleAttribut))

