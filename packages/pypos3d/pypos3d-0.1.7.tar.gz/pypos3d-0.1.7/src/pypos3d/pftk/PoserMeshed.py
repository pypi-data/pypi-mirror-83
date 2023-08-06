# -*- coding: utf-8 -*-
# package: pftk.poser.kern
from collections import namedtuple
import logging

from langutil import RemoveExt, C_FAIL, C_OK, C_ERROR
from pypos3d.wftk.WFBasic import C_BAD_DELTAINDEX, C_BAD_DELTACOUNT, C_NODELTA, Vector3d
from pypos3d.pftk.PoserBasic import PoserConst, PoserToken, PToken, buildRelPath, getRealPath, index, TAS, WBoolLine, create
from pypos3d.pftk.GeomCustom import GeomCustom
from pypos3d.pftk.StructuredAttribut import StructuredAttribut, Channels, AlternateGeom, Deltas, ValueOpDelta, ChannelMorphStatus, ChannelMorphStatusList, findNewDelta, filterLength, calcMapping_KDTree


#
# Options of the report algorithm
# 
ReportOption = namedtuple('ReportOption', ['translation', \
  'maxDist', # Value changed to fit a good sphere for DAZ characters \
  'enhance',\
  'boundingType',\
  'useVicinityLoop',\
  'alpha',\
  'minVectLen'])

ReportOption.__new__.__defaults__ = ( Vector3d(), 0.025, PoserConst.C_NO_ENHANCEMENT, PoserConst.C_NO_BOUNDING, True, 0.6, 0.001)

#  
class PoserMeshedObject(StructuredAttribut):
  ''' A PoserMeshedObject represents either a Prop, an Actor, a Camera, a Light or hairs in a Poser File. '''

  def __init__(self, Name=None):
    super(PoserMeshedObject, self).__init__(Name)

    #  Figure Object (may be null) 
    self._fig = None
    self._pmName = ''
    self._hidden = False
    self._visible = True #  On
    self._bend = True #  1
  
    #  Poser V9 attribut 
    self._animatableOrigin = False
    self._dynamicsLock = True #        0
  
    #  Poser V9 attribut 
    self._collisionDetection = False
    self._addToMenu = True #     1
    self._castsShadow = True #       1
    self._includeInDepthCue = True #         1
    self._useZBuffer = True #        1
    self._parent = None
    self._conformingTarget = None
    self._creaseAngle = 80.0
  
    #  Storage class of the mesh 
    self._geomType = PoserConst.GT_NONE
  
    #  Geom Groupname when geomType is GLOBALself._OBJFILE 
    self._geomGroupName = None
  
    #  Geom filename when geomType is LOCALself._OBJFILE, formated like Poser with ':' or ""  
    self._geomFileName = None
  
    #  Base Geometry
    self._geomCustom = None
    self._geom = None
  
    #  FigureResFile with a path (relative) 
    self._FRF = None
  
    #  Channels = list of targetGeom and so on - Never null 
    self._channels = Channels()
  
    #  endPoint position 
    self._endPoint = None
  
    #  origin of the mesh 
    self._origin = None
  
    #  orientation of the mesh 
    self._orientation = None
    self._displayOrigin = False
    self._displayMode = None #  USEPARENT
    self._customMaterial = 0
    self._locked = False
    self._lstAltGeom = [ ]  # For Python, never null
    self._lstWMap = [ ] # List of Weight Maps (could be implemented with a ordered dict)
  
    #  Name + Mesh definition
    self._printName = None
    self._pf = None


  def setFigureResFile(self, frf):
    self._FRF = frf

  def getFigureResFile(self): return self._FRF

  def setPoserFile(self, pf):
    self._pf = pf

  def getPoserFile(self): return self._pf

  def getChannels(self): return self._channels

  def getGeomType(self): return self._geomType

  def setGeomType(self, gt):
    self._geomType = gt

  def getGeomGroupName(self): return self._geomGroupName

  def setGeomGroupName(self, gn):
    self._geomGroupName = gn

  def getGeomFileName(self): return self._geomFileName

  def getGeomCustom(self): return self._geomCustom

  def setGeomFileName(self, fn):
    self._geomFileName = fn

  def setFigure(self, fig):
    self._fig = fig

  def getFigure(self): return self._fig

  # Return the list of alternate geom. Null if none (never null in Python)
  def getAltGeomList(self): return self._lstAltGeom

  #    
  def addAltGeom(self, ag=None, altGeomFile=None, poserRootDir=None, pos=-1):
    ''' Add an alternate Geometry, if it does not already exists.
    Returns
    -------
    int
      C_OK, C_FAIL if the geometrie was already existing, C_ERROR in cas of file pb
    '''
    ret = C_OK
    if not ag:
      try:
        relPath = buildRelPath(poserRootDir, altGeomFile.getCanonicalPath())

        for agold in self.getAltGeomList():
          if agold.getGeomFileName()==relPath:
            return C_FAIL

        ag = AlternateGeom()
        ag.setPoserType(PoserToken.E_alternateGeom)
        n = RemoveExt(altGeomFile.getName())
        ag.setName(n)
        ag.setPrintName(n)
        ag.setGeomFileName(relPath)

      except IOError as ioex:
        ret = C_ERROR

   
    #  Add the AlternateGeom to the specified position
    if pos>=0:
      self._lstAltGeom.insert(pos, ag)
    else:
      self._lstAltGeom.append(ag)

    #  Fix internal indexes
    self.indexAltGeom()
    return ret

  def indexAltGeom(self): #  Fix internal indexes
    for i,a in enumerate(self._lstAltGeom):
      a.setNo(i)

  # 
  # Move an alternate Geometrie to an upper position
  # @return C_OK, C_FAIL if the geometrie was already existing, 
  #         PoserConst.C_ERROR in case data inconsistency
  #    
  def moveAltGeom(self, ag):
    ret = self.removeAltGeom(ag)
    if ret == C_OK:
      ret = self.addAltGeom(ag, ag.getNo())
    return ret

  # 
  # Remove an alternate Geometrie
  # @return C_OK, C_FAIL if the alt geometrie was not existing
  #    
  def removeAltGeom(self, ag):
    res = C_OK
    try:
      self.getAltGeomList().remove(ag)
      self.indexAltGeom()
    except:
      res = C_FAIL

    return res

  # 
  # Return the alternate geom channel. Null if none
  #    
  def getAltGeomChannel(self):
    for gt in self.getChannels().getLstAttr():
      if (gt.getPoserType() == PoserToken.E_geomChan):
        return gt

    return None

  def getChannel(self, channelName):
    channelName = channelName.lower()
    for gt in self.getChannels().getLstAttr():
      if gt.getName().lower() == channelName:
        return gt

    return None


  def updateOrCreateVP(self, channelName, minVal=0.0, maxVal=1.0, applyLimits=True, isHidden=False):
    return self.getChannels().updateOrCreateVP(channelName, minVal, maxVal, applyLimits, isHidden)

  def CreateShaderNodeP(self, channelName, isHidden=False):
    snp = self.getChannels().updateOrCreateVP(channelName, minVal=0.0, maxVal=1.0, applyLimits=True, isHidden=isHidden)
    snp.setPoserType(PoserToken.E_shaderNodeParm)
    return snp
  
  def CreateDeformerP(self, channelName, zoneName, deformerName, isHidden=False):
    snp = self.getChannels().updateOrCreateVP(channelName, minVal=-100.0, maxVal=100.0, applyLimits=True, isHidden=isHidden)
    snp.setPoserType(PoserToken.E_deformerPropChan)

    # Create Deformer Channel special attributs
    az = create(PoserToken.E_addZone, PoserToken.E_addZone.token)
    az.setValue('1 ' + zoneName)
    snp.addAttribut(az)

    dp = create(PoserToken.E_deformerProp, PoserToken.E_deformerProp.token)
    dp.setValue(deformerName)
    snp.addAttribut(dp)
    return snp
  

  def addAttribut(self, po):
    if po.getPoserType()==PoserToken.E_geomCustom:
      self._geomCustom = po
      self._geomType = PoserConst.GT_INTERNAL
    elif po.getPoserType()==PoserToken.E_channels:
      self._channels = po
      self._channels.setPoserMeshedObject(self)
    elif po.getPoserType()==PoserToken.E_storageOffset:
      # FIX20090607 : Storage Offset seen : shall not be kept in attribute list.
      return
    elif po.getPoserType()==PoserToken.E_alternateGeom:
      self._lstAltGeom.append(po)
      po.setNo(len(self._lstAltGeom))
    elif po.getPoserType()==PoserToken.E_weightMap:
      self._lstWMap.append(po)
    else:
      super(PoserMeshedObject, self).addAttribut(po)

  def getBaseMesh(self, poserRootDir):
    if self._geom == None:
      self._geom = self.getBaseGeomCustom(poserRootDir).getWaveGeom()
    return self._geom
 
  def printBaseGeomCustom(self):
    ''' Return a printable string representing the geometry '''
    s = PoserConst.GEOMPRINT[self._geomType]
    if self._geomType==PoserConst.GT_GLOBAL_OBJFILE:
      # geomHandlerGeom 13 hip
      s = PoserConst.GEOMPRINT[self._geomType] + '[' + self._FRF.getValue() + ', ' + self._geomGroupName + ']'
    elif self._geomType==PoserConst.GT_LOCAL_OBJFILE:
      # objFileGeom 0 0 :Runtime:Geometries:Marforno:Elaya:Lamp.obj          
      s = PoserConst.GEOMPRINT[self._geomType] + '[' + self._geomFileName + ']'
    else: # Alternate should not appear here
      s = PoserConst.GEOMPRINT[self._geomType]
    return s
  
  def getBaseGeomCustom(self, poserRootDir):
    ''' Return the Geometry definition of the object. Without applying any morph.
    Returns
    -------
    GeomCustom
      The GeomCustom object containing the WaveGeom3d
    '''
    if not self._geomCustom:
      if (self._geomType==PoserConst.GT_NONE) or (self._geomType==PoserConst.GT_INTERNAL):
        pass
      elif self._geomType==PoserConst.GT_GLOBAL_OBJFILE:
        # geomHandlerGeom 13 hip
        gc = self._FRF.getGeomCustom(poserRootDir)
        self._geomCustom = gc.extractSortGeom(self._geomGroupName, self._geomType) if gc else None

      elif self._geomType==PoserConst.GT_LOCAL_OBJFILE:
        # objFileGeom 0 0 :Runtime:Geometries:Marforno:Elaya:Lamp.obj          
        self._geomCustom = GeomCustom(getRealPath(poserRootDir, self._geomFileName))
      else:
        logging.warning("Unknown GeomType")

    return self._geomCustom

  # TODO: Take into account new installation type (Root = Runtime)
  def getMorphedMesh(self, poserRootDir, bodyIdx, lstch):
    ''' Return a mesh morphed with the selected channels.
    Parameters
    ----------
    poserRootDir : str
      Base location of Poser Installation.
    bodyIdx : int
      Index of the figure in the poser file
    lstch : List of channels.
      ChannelMorphStatusList or set of channel names
    Returns
    -------
    GeomCustom
      Return null when the object has no geometry (BODY case for example)
    '''
    resgc = None
    basegc = None
    stm = lstch.getChannelSet() if isinstance(lstch, ChannelMorphStatusList) else lstch

    # Avoid the BaseGeomCustom Extraction
    if self._geomType == PoserConst.GT_GLOBAL_OBJFILE:
      basegc = self._FRF.getGeomCustom(poserRootDir)
      copygc = GeomCustom(basegc)

      copygc.findApplyDelta(bodyIdx, self._pf, stm)
      resgc = copygc.extractSortGeom(self._geomGroupName, self._geomType)
    else:
      basegc = self.getBaseGeomCustom(poserRootDir)
      resgc = GeomCustom(basegc)
      resgc.findApplyDelta(self, self._pf, stm)
    return resgc

  def setBaseMesh(self, poserRootDir, objFileName):
    self._geomType = PoserConst.GT_LOCAL_OBJFILE
    self._geomFileName = buildRelPath(poserRootDir, objFileName)

    # 20080502 : Force Geometry reload
    self._geomCustom = None
    self._printName = None

  def getPrintName(self): return self._pmName

  def setPrintName(self, pm):
    self._pmName = pm

  def setName(self, n):
    super(PoserMeshedObject, self).setName(n)
    self._printName = None

  def getDisplayName(self):
    if self._printName == None:
      if not self._geomCustom:
        if self.getName().startswith(PoserConst.C_BODY):
          objdef = "none" if (self._FRF == None) else self._FRF.getValue()
        else:
          objdef = self._geomGroupName if self._geomType==PoserConst.GT_GLOBAL_OBJFILE else self._geomFileName
      else:
        objdef = "internal : " + str(self._geomCustom.getWaveGeom().getCoordListLength()) + " vertex"

      self._printName = self.getName() + " [" + objdef if objdef else 'None' + "]"
    return self._printName

  def isVisible(self): return self._visible

  def setVisible(self, v):
    self._visible = v

  def isHidden(self): return self._hidden

  def setHidden(self, b):
    self._hidden = b

  def isBend(self): return self._bend

  def setBend(self, b):
    self._bend = b

  def isAddToMenu(self):
    return self._addToMenu

  def setAddToMenu(self, b):
    self._addToMenu = b

  def isDisplayOrigin(self):
    return self._displayOrigin

  def setDisplayOrigin(self, b):
    self._displayOrigin = b

  def getDisplayMode(self):
    return self._displayMode

  def getCreaseAngle(self):
    return self._creaseAngle

  def setCreaseAngle(self, d):
    self._creaseAngle = d

  def getEndPoint(self):
    return self._endPoint

  def setEndPoint(self, v):
    self._endPoint = v

  def getParent(self):
    return self._parent

  def setParent(self, p):
    self._parent = p

  def getConformingTarget(self):
    return self._conformingTarget

  def setConformingTarget(self, target):
    self._conformingTarget = target

  def getCustomMaterial(self):
    return self._customMaterial

  def setCustomMaterial(self, v):
    self._customMaterial = v

  def isLocked(self):
    return self._locked

  def getOrigin(self):
    return self._origin

  def setOrigin(self, v):
    self._origin = v

  def getOrientation(self):
    return self._orientation

  def setOrientation(self, v):
    self._orientation = v

  # Create in the current MeshedObject the best deltas for the list of morph
  # targets.
  # @param poserRootDir 	To find the .OBJ files
  # @param refMeshedObj         Figure that contains initial deltas
  # @param translation          Translation between original MeshedObject and its localization in
  # this.
  # @param maxDist              Maximal distance to take a point into account. If null, no maxDist
  # are applied.
  # @param setTargetMorph       List of morphs to create
  # @param alpha                Influence of distant point (less that one). alpha = 0.6 is usually
  # a good value.
  # @return C_OK when result is correct. C_ERROR when parameters are not correct.
  def createDeltas(self, poserRootDir, refObj, setTargetMorph, ropt):
    ret = C_OK
    lstCurGeom = [ self.getBaseGeomCustom(poserRootDir) ]

    if isinstance(refObj, PoserMeshedObject):
      # Extract and Sort GeomCustom to get single numbered groups
      lstRefGeom = [ refObj.getBaseGeomCustom(poserRootDir) ]
    else: # refObj should be a Figure instance
      refPoserObject = refObj.getPoserFile()
      lstRefGeom = refPoserObject.extractAll(poserRootDir, refObj.getBodyIndex(), None)

    if (lstCurGeom == None) or (lstRefGeom == None) or (setTargetMorph == None):
      return C_ERROR

    for srcGC in lstCurGeom:
      srcWG = srcGC.getWaveGeom()

      tabMapping = calcMapping_KDTree(srcWG, lstRefGeom, ropt.translation, ropt.maxDist)
      
      channelsAttr = self.getChannels()

      # Foreach morph target ==> Exploit tabMapping for srcGC
      for channelName in setTargetMorph:
        logging.info("Creating deltas for %s.%s", srcGC.getName(), channelName)
        setFoundDeltas = findNewDelta(tabMapping, refObj, channelName)
        setNewDeltas = { }

        # Local Enhancement
        Deltas.enhancement(srcWG, setFoundDeltas, setNewDeltas, ropt.enhance, ropt.boundingType, ropt.useVicinityLoop, ropt.alpha)
        if len(setNewDeltas) > 0:
          # Filter the result list to remove too short vectors
          lstFinalDeltas = filterLength(setNewDeltas, ropt.minVectLen)

          channelsAttr.updateOrCreate(channelName, None, srcWG, lstFinalDeltas, 0)
          logging.info("Deltas created for %s.%s : %d", srcGC.getName(), channelName, len(lstFinalDeltas))
        else:
          logging.warn("No Delta created for %s.%s", srcGC.getName(), channelName )
    return ret

  # Create in the current meshed object the best deltas for the alternate geoms for the list of morph targets.
  # @param poserRootDir    To find the .OBJ files
  # @param refMeshedObj    Figure that contains initial deltas
  # @param ropt            Report options
  # @param setTargetMorph  List of morphs to create
  # @return    C_OK when result is correct. C_ERROR when parameters are not correct.
  def createAlternateDeltas(self, poserRootDir, setTargetMorph, ropt):
    ret = C_OK
    curPoserObject = self.getPoserFile()
    refMeshedObj = self

    # Find the actor      
    srcActor = curPoserObject.findActor(self.getName())
    channelsAttr = srcActor.getChannels()

    # Extract and load alternate geoms
    lstAltG = self.getAltGeomList()
    if len(lstAltG) > 0:
      lstCurGeom = [ ]
      # Table of alternate geometry usage valueParm indicators
      # GenericTransform altGeomUsageIndic[] = new GenericTransform[lstAltG.size() + 1];

      # Find the geomChan Channel (should always exists if the list of alt geom is not empty)
      geomChan = channelsAttr.findAttribut(PoserToken.E_geomChan)
      
      altno = 1
      for altg in lstAltG:
        rfn = altg.getGeomFileName()
        gc = GeomCustom(getRealPath(poserRootDir, rfn))
        lstCurGeom.append(gc)

      lstRefGeom = [ refMeshedObj.getBaseGeomCustom(poserRootDir), ]

      if (lstCurGeom == None) or (lstRefGeom == None) or (setTargetMorph == None):
        return C_ERROR

      altno = 1
      for srcGC in lstCurGeom:
        srcWG = srcGC.getWaveGeom()

        # tabMapping = PtMapping.calcMapping(srcWG, lstRefGeom, ropt.translation, ropt.maxDist)
        tabMapping = calcMapping_KDTree(srcWG, lstRefGeom, ropt.translation, ropt.maxDist)

        # Foreach morph target ==> Exploit tabMapping for srcGC
        for channelName in setTargetMorph:
          altChannelName = channelName + "_Alt" + str(altno)
          logging.info("Creating deltas for " + srcGC.getName() + "." + channelName + " into:" + altChannelName)
          setFoundDeltas = findNewDelta(tabMapping, refMeshedObj, channelName)
          setNewDeltas = { }

          # Local Enhancement
          Deltas.enhancement(srcWG, setFoundDeltas, setNewDeltas, ropt.enhance, ropt.boundingType, ropt.useVicinityLoop, ropt.alpha)
          if len(setNewDeltas) > 0:
            # Filter the result list to remove too short vectors
            setFinalDeltas = filterLength(setNewDeltas, ropt.minVectLen)

            # Create or update the channel list
            destGT = channelsAttr.updateOrCreate(altChannelName, self.getName(), srcWG, setFinalDeltas, srcActor.getFigure().getBodyIndex(), False)
            
            vod = ValueOpDelta(PoserToken.E_valueOpKey, srcActor.getFigure().getRefName(), srcActor.getName(), geomChan.getName(), 0.0)

            for ia in range(1, len(lstAltG)+1):
              vod.addValueKey(ia, 1.0 if (ia == altno) else 0.0)
                       
            destGT.addVOD(vod)

            # Multiply by the value of the copied channel
            vodMul = ValueOpDelta(PoserToken.E_valueOpTimes, srcActor.getFigure().getName(), srcActor.getName(), channelName, 0.0)
            destGT.addVOD(vodMul)

            destGT.setHidden(True)
            logging.info("Deltas created for %s.%s : %d", srcGC.getName(), channelName, len(setFinalDeltas))
        altno += 1

    return ret

  # Find the GenericTransform that represents a TargetGeom and that has the
  # given "channelName"
  # @param channelName
  #          Channel Name to look for.
  # @return Null if not found.
  def getTargetGeom(self, channelName):
    for gt in self.getChannels().getLstAttr():
      if gt.getPoserType() == PoserToken.E_targetGeom and gt.getName() == channelName:
        return gt
    return None

  # 
  # Find the GenericTransform that represents the given "channelName"
  # @param channelName
  #          Channel Name to look for.
  # @return Null if not found.
  def getGenericTransform(self, channel:'Name Or PoserToken'):
    try:
      return next(gt for gt in self.getChannels().getLstAttr() if gt.getPoserType()==channel) if isinstance(channel, PToken) \
        else next(gt for gt in self.getChannels().getLstAttr() if gt.getName()==channel)
      
    except StopIteration:
      return None
    
    
  # 
  # Return the delta for a given channel and a given vertex no.
  # @param channelName
  #          Channel Name (targetGeom name in fact)
  # @param refNo
  #          Index of the vertex in the geometry of the meshed object (Actor or
  #         Prop)
  # @return Delta Object (Aka 3D vector)
  def findDelta(self, channelName, refNo):
    gt = self.getTargetGeom(channelName)
    if gt:
      for dploc in gt.getDeltas().getDeltaTab():
        if dploc.noPt == refNo:
          return dploc
    return None

  # 
  # Delete the given channel.
  # 
  # @param gt
  def deleteChannel(self, gt):
    self._channels.deleteChannel(gt)

  # 
  # Compute the first level list of channels that point to the given channel argument.
  # @param channel Reference channel
  # @param lstIn  List to be extended and returned. Created if null. 
  #                Does not contain duplicate channel.
  def getChannelDescendant(self, channel, lstIn):
    implst = lstIn if lstIn else [ ]
    cn = channel.getName()
    gn = channel.getPoserMeshedObject().getName()
    for gt in self.getChannels().getLstAttr():
      for vop in gt.getVOD():
        if (gn==vop.getGroupName()) and (cn == vop.getChannelName()) and (not gt in implst):
          implst.append(gt)
          break

    return implst

  # Test if the deltas are consistent with the geometry.
  # @param gt
  # @return    C_OK : No problem
  #            C_NODELTA : No Deltas
  #            C_ERROR : Geometry in read error
  def checkChannelDelta(self, gt, poserRootDir):
    res = C_OK
    if gt.ishasDeltas():
      gc = self.getBaseGeomCustom(poserRootDir)
      if gc and (gc.isValid()):
        dlt = gt.getDeltas()
        dpt = dlt.getDeltaTab() if dlt else [ ]
        vertexSize = gc.getWaveGeom().getCoordListLength()
        if vertexSize == gt.getNumbDeltas():
          for dp in dpt:
            if dp.noPt >= vertexSize:
              return C_BAD_DELTAINDEX
        else:
          res = C_BAD_DELTACOUNT
      else:
            res = C_ERROR
    else:
      res = C_NODELTA
    return res

  # Change the name of referenced part (actor, prop, hairProp, controlProp)  
  # @param oldPartName
  # @param newPartName
  def changeReference(self, oldPartName, newPartName, changeRefToBODY=True):
    self._parent = TAS(self._parent, oldPartName, newPartName)
    self._conformingTarget = TAS(self._conformingTarget, oldPartName, newPartName)
    for gt in self._channels.getLstAttr():
      gt.changeReference(oldPartName, newPartName, changeRefToBODY=changeRefToBODY)

  def setDirect(self, tokenID, val):
    if tokenID==PoserToken.E_name:
      self._pmName = val
    elif tokenID==PoserToken.E_on:
      self._visible = True
    elif tokenID==PoserToken.E_off:
      self._visible = False
    elif tokenID==PoserToken.E_hidden:
      self._hidden = val.startswith("1")
    elif tokenID==PoserToken.E_bend:
      self._bend = val.startswith("1")
    elif tokenID==PoserToken.E_animatableOrigin:
      self._animatableOrigin = val.startswith("1")
    elif tokenID==PoserToken.E_dynamicsLock:
      self._dynamicsLock = val.startswith("1")
    elif tokenID==PoserToken.E_collisionDetection:
      self._collisionDetection = val.startswith("1")
    elif tokenID==PoserToken.E_addToMenu:
      self._addToMenu = val.startswith("1")
    elif tokenID==PoserToken.E_castsShadow:
      self._castsShadow = val.startswith("1")
    elif tokenID==PoserToken.E_includeInDepthCue:
      self._includeInDepthCue = val.startswith("1")
    elif tokenID==PoserToken.E_useZBuffer:
      self._useZBuffer = val.startswith("1")
    elif tokenID==PoserToken.E_parent:
      self._parent = val
    elif tokenID==PoserToken.E_conformingTarget:
      self._conformingTarget = val
    elif tokenID==PoserToken.E_creaseAngle:
      self._creaseAngle = float(val)

    elif tokenID==PoserToken.E_geomHandlerGeom:
      self._geomType = PoserConst.GT_GLOBAL_OBJFILE
      tmps = val.strip()
      bci = tmps.rfind(' ');
      self._geomGroupName = tmps[(bci + 1):]

    elif tokenID==PoserToken.E_objFileGeom:
      self._geomType = PoserConst.GT_LOCAL_OBJFILE

      tmps1 = val.strip()
      bci1 = 0

      if tmps1.startswith(PoserConst.S_LOCAL_OBJFILE_PFX):
        bci1 = len(PoserConst.S_LOCAL_OBJFILE_PFX) -1
      else:
        bci1 = tmps1.rfind(' ')

      self._geomFileName = tmps1[(bci1 + 1):]

    elif tokenID==PoserToken.E_endPoint:
      self._endPoint = Vector3d.parseVector3d(val)

    elif tokenID==PoserToken.E_origin:
      self._origin = Vector3d.parseVector3d(val)

    elif tokenID==PoserToken.E_orientation:
      self._orientation = Vector3d.parseVector3d(val)

    elif tokenID==PoserToken.E_displayOrigin:
      self._displayOrigin = val.startswith("1")

    elif tokenID==PoserToken.E_locked:
      self._locked = val.startswith("1")

    elif tokenID==PoserToken.E_customMaterial:
      self._customMaterial = int(val)

    elif tokenID==PoserToken.E_displayMode:
      self._displayMode = val

    else:
      logging.warning("Unexpected Direct: (%s) %s", tokenID.token, val)

  # Write the definition part of the meshed object.
  # @param fw
  # @param pfx
  def writeDef(self, fw, pfx):
    fw.write(pfx + self.getPoserType().token + " " + self.getName() + '\n')
    nextPfx = pfx + "\t"
    fw.write(nextPfx + "{\n")
    if self._geomType==PoserConst.GT_NONE:
      fw.write('\n')
    elif self._geomType==PoserConst.GT_GLOBAL_OBJFILE:
      fw.write(nextPfx + "storageOffset 0 0 0" + '\n')
      fw.write(nextPfx + "geomHandlerGeom 13 " + self._geomGroupName + '\n')
    elif self._geomType==PoserConst.GT_LOCAL_OBJFILE:
      fw.write(nextPfx + "storageOffset 0 0.3487 0" + '\n')
      fw.write(nextPfx + "objFileGeom 0 0 " + self._geomFileName + '\n')
    elif self._geomType==PoserConst.GT_INTERNAL:
      self._geomCustom.write(fw, nextPfx)
    else:
      logging.warning("Unknown GeomType at write")
    fw.write(nextPfx + "}\n")

  # Write the Data part of the meshed object.
  # @param fw
  # @param pfx
  def writeData(self, fw, pfx):
    fw.write(pfx + self.getPoserType().token + " " + self.getName()+'\n')
    nextPfx = pfx + "\t"
    fw.write(nextPfx + "{\n")
    fw.write(nextPfx + "name " + self._pmName+'\n')
    fw.write(nextPfx + ("on" if self._visible else "off")+'\n')
    #fw.write(nextPfx + "bend " + (1 if self._bend else 0)+'\n')
    WBoolLine(fw, nextPfx, "bend", self._bend)
    
    if self.getPoserFile().isVersion(PoserConst.POSER_V9):
        #fw.write(nextPfx + "" + (1 if self._animatableOrigin else 0)+'\n')
        WBoolLine(fw, nextPfx, "animatableOrigin", self._animatableOrigin)

    WBoolLine(fw, nextPfx, "dynamicsLock", self._dynamicsLock)

    if self.getPoserFile().isVersion(PoserConst.POSER_V9):
      WBoolLine(fw, nextPfx, "collisionDetection", self._collisionDetection )

    WBoolLine(fw, nextPfx, "hidden", self._hidden )
    WBoolLine(fw, nextPfx, "addToMenu", self._addToMenu )
    WBoolLine(fw, nextPfx, "castsShadow", self._castsShadow )
    WBoolLine(fw, nextPfx, "includeInDepthCue", self._includeInDepthCue )
    WBoolLine(fw, nextPfx, "useZBuffer", self._useZBuffer )

    if self._parent:
      fw.write(nextPfx + "parent " + self._parent+'\n')
    if self._conformingTarget:
      fw.write(nextPfx + "conformingTarget " + self._conformingTarget+'\n')
    if self._lstAltGeom:
      for ag in self._lstAltGeom:
        ag.write(fw, nextPfx)

    fw.write(nextPfx + "creaseAngle " + str(self._creaseAngle)+'\n')
    
    # Print WeightMap before channels
    for po in self._lstWMap:
      po.write(fw, nextPfx)
    
    self._channels.write(fw, nextPfx)
    if self._endPoint:
        fw.write(nextPfx + "endPoint " + self._endPoint.poserPrint()+'\n')
    if self._origin:
        fw.write(nextPfx + "origin " + self._origin.poserPrint()+'\n')
    if self._orientation:
        fw.write(nextPfx + "orientation " + self._orientation.poserPrint()+'\n')

    WBoolLine(fw, nextPfx, "displayOrigin", self._displayOrigin )

    if self._displayMode:
        fw.write(nextPfx + "displayMode " + self._displayMode+'\n')
    fw.write(nextPfx + "customMaterial " + str(self._customMaterial)+'\n')
    WBoolLine(fw, nextPfx, "locked", self._locked )
    
    # Print other found attributes
    for po in self._lstAttr:
      po.write(fw, nextPfx)
    if len(self._lstAttr) == 0:
      fw.write('\n')
    fw.write(nextPfx + "}\n")

  def write(self, fw, pfx):
    raise Exception(PoserConst.C_EX_NOTCALL)




# -----------------------------------------------------------------------------
# Descendant classes of PoserMeshedObject
# -----------------------------------------------------------------------------

# 
# Just to avoid interactions with actors or props that have geoms
#  
class Camera(PoserMeshedObject):
  def __init__(self):
    super(Camera, self).__init__()

# 
# Just to avoid interactions with actors or props that have geoms
#  
class Light(PoserMeshedObject):
  def __init__(self):
    super(Light, self).__init__()

  def getLightType(self):
    sa = self.findAttribut(PoserToken.E_lightType)
    return sa.getIntegerValue()

# 
#  Describes a Poser "actor" object.
#  
class PoserActor(PoserMeshedObject):

  def __init__(self, Name = None):
    super(PoserActor, self).__init__(Name)
    self.idx = 0

  #    * @see pftk.poser.kern.PoserObject#setName(java.lang.String)
  def setName(self, n):
    super(PoserActor, self).setName(n)
    self.idx = index(n)

  def getIndex(self): return self.idx

  def isBody(self):
    c = self.getName().rfind(':')
    return (c == 4) and self.getName().startswith("BODY")

  # Hide an actor.
  #   @param hidden
  #   @param menuHidden  Hide in Poser Menu
  def setHidden(self, hidden, menuHidden=None):
    self._hidden = hidden
    self._visible = False
    self._bend = False
    self._dynamicsLock = False
    self._addToMenu = menuHidden if menuHidden else not hidden
    self._castsShadow = False
    self._includeInDepthCue = False

  def getWeldParent(self):
    for po in self.getFigure().getFigureDesc().getLstAttr():
      if (po.getPoserType() == PoserToken.E_weld) and (po.getChildName() == self.getName()):
        return po.getParentName()
    return None

# 
# Represents a Poser "prop" object
#  
class PoserProp(PoserMeshedObject):
  def __init__(self):
    super(PoserProp, self).__init__()

  def createChannelMorphList(self, stm):
    lstCS = ChannelMorphStatusList()

    #  Calculate the list of channels with regards to the known one
    for attr in self.getChannels():
      if attr.getPoserType() == PoserToken.E_targetGeom:
        lstCS.append(ChannelMorphStatus(attr, stm))

    return lstCS


class BaseProp(PoserProp):
  def __init__(self):
    super(BaseProp, self).__init__()
    self.ambiguious = True

  #    * @see deyme.v3d.poser.PoserObject#write(java.io.FileWriter)
  def write(self, fw, pfx):
    if len(self._lstAttr) == 0:
      fw.write(pfx + self.getPoserType().token + " " + self.getName() + '\n')
    else:
      super(BaseProp, self).write(fw, pfx)

# 
# Represents the Magnet object of a Magner deformer.
# Just to avoid interactions with actors or props that have geoms
#  
class MagnetDeformerProp(PoserProp):
  def __init__(self):
    super(MagnetDeformerProp, self).__init__()

# Represents the Spehirc zone of a Magner deformer.
# Just to avoid interactions with actors or props that have geoms
class SphereZoneProp(PoserProp):
  def __init__(self):
    super(SphereZoneProp, self).__init__()

# 
# Represents a Poser "path" object
#  
class CurveProp(PoserProp):
  def __init__(self):
    super(CurveProp, self).__init__()

# 
# Just to avoid interactions with actors or props that have geoms
#  
class ControlProp(PoserProp):
  def __init__(self):
    super(ControlProp, self).__init__()



# 
# This class represents the hairProp attribut of a Poser File.
#  
class HairProp(PoserProp):
  def __init__(self):
    super(HairProp, self).__init__()
    self._isSimple = True
    self.ambiguious = True

    def __init__(self):
        super(HairProp, self).__init__()

  #    * @see deyme.v3d.poser.PoserObject#write(java.io.FileWriter)
  def write(self, fw, pfx):
    if self._isSimple:
      fw.write(pfx + self.getPoserType().token + " " + self.getName() + '\n')

  def addAttribut(self, po):
    super(HairProp, self).addAttribut(po)
    self._isSimple = False




