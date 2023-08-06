# -*- coding: utf-8 -*-
# package: pypos3d.pftk
import os
import sys
import logging

from langutil import C_OK, C_FAIL, C_ERROR, Arrays_binarySearch

from pypos3d.pftk.PoserBasic import cleanName, getRealPath, index, PoserConst, PoserToken 
from pypos3d.pftk.StructuredAttribut import GenericTransform, ValueOpDelta, Deltas, ChannelMorphStatus, ChannelMorphStatusList, PoserMaterial, AddChildSA, Keys, calcMapping_KDTree, findNewDelta, filterLength
from pypos3d.pftk.GeomCustom import GeomCustom
from pypos3d.pftk.PoserMeshed import PoserProp, PoserActor, BaseProp
from pypos3d.pftk.ChannelImportAnalysis import ChannelImportAnalysis

# 
class Figure(PoserConst):
  ''' This class represents a Poser Figure.  '''

  # 
  #    
  def __init__(self, pf, idx=0, frf=None):
    ''' Create an empty Figure.
    Suppose that the BODY:Idx exists.
    Parameters
    ----------
    pf : PoserFile
      Parent PoserFile
    idx : int, optional, default 0
      Figure index in the PoserFile (>0)
    frf : FigureResFile
      Create a new empty figure when "figureResFile" line is read.
    '''
    super(Figure, self).__init__()

    self._pf = pf
    self._bodyIdx = idx

    #  figureResFile of the figure (single and shared with the PoserFile 
    self._bodyIdx = PoserConst.C_BAD_INDEX
    self._lstActor = [ ]
    self._lstProp = [ ]
    self._printName = ''
    self._figDesc = None
    self._lstCS = None
    self._lstMat = None
    self._figureResFile = frf

  def getBodyIndex(self):
    return self._bodyIdx

  def setBodyIndex(self, idx):
    self._bodyIdx = idx

  def getActors(self):
    return self._lstActor

  def getProps(self):
    return self._lstProp

  # 
  #    
  def findActor(self, actorName, withIndex=True):
    ''' Return the actor of the given name (full name with :index) 
    Parameters
    ----------
    actorName : str
      Actor name with index (by default)
    withIndex : bool, optional, default True
      Indicates if name shall be searched with index (:1) or not
    Returns
    -------
    PoserActor
      The PoserActor, else None
    '''
    if withIndex:
      for a in self.getActors():
        if actorName == a.getName():
          return a
    else:
      for a in self.getActors():
        if actorName == a.getName()[:-2]:
          return a
      
    return None

  def findProp(self, propName):
    ''' Return the property of the given name (full name with :index) 
    Parameters
    ----------
    actorName : str
      Prop's name with index (by default)
    Returns
    -------
    PoserProp
      The PoserProp, else None
    '''
    for a in self.getProps():
      if propName == a.getName():
        return a
    return None

  def setName(self, n):
    self._figDesc.setName(n)

  def getName(self):
    return self._figDesc.getName()

  # 
  # Return the name of the figure used by channel references
  #    
  def getRefName(self):
    return "Figure " + str(self._bodyIdx)

  # 
  # @return the printName
  #    
  def getPrintName(self):
    return self._printName

  # 
  # @param printName the printName to set
  #    
  def setPrintName(self, printName):
    self._printName = printName

  def changeReference(self, oldPartName, newPartName, changeRefToBODY=True):
    ''' Change the name of a referenced part (actor, prop, hairProp, controlProp)  
    Parameters
    ----------
    oldPartName : str
      Previously Referenced part
    newPartName : str
      New reference part
    changeRefToBODY : bool, optional, default True
      Indicates if references to 'BODY:n' in Channels' operations shall be changed.
      Needed when an actor (that references BODY's channels) is reparented
    '''
    for actor in self.getActors():
      actor.changeReference(oldPartName, newPartName, changeRefToBODY=changeRefToBODY)
      
    #  Change at figure definition level
    self._figDesc.changeReference(oldPartName, newPartName)

  # 
  def rename(self, actor, nInternalName, nPrintName):
    ''' Change the names of an Actor in a Figure.
    Propagates the changes.

    Parameters
    ----------
    actor : PoserActor
      Actor to rename
    nInternalName : str
      new internal name without leading ":n"
    nPrintName : str
      new print name
  
    Returns
    -------
    int
      Ret Code
    '''
    oldIntName = actor.getName()
    if nInternalName != cleanName(oldIntName):
      posc = oldIntName.find(':')
      if posc > 0:
        nInternalName = nInternalName + oldIntName[posc:]

    #  Change the name in both definition and Data parts of the actor
    actor.setName(nInternalName)
    pf = self.getPoserFile()
    pf.changeReference(oldIntName, nInternalName)

    actor.setPrintName(nPrintName)
    return C_OK

  def addReadActor(self, pa):
    if self._figureResFile:
      pa.setFigureResFile(self._figureResFile)

    pa.setFigure(self)
    for lpa in self._lstActor:
      if pa.getName() == lpa.getName():
        return lpa

    self._lstActor.append(pa)
    return pa

  def addReadProp(self, pp):
    pp.setFigure(self)
    for lpp in self._lstProp:
      if pp.getName() == lpp.getName():
        return lpp

    self._lstProp.append(pp)
    return pp

  #
  # 
  # @param parent
  # @param pa
  #    
  def addActor(self, parent, pa, changeRefToBODY=True):
    ''' Add actor pa as child of actor parent.
    if changeRetFoBODY is true, all reference including references to 'BODY'
    are replaced by the new parent.
    else only reference to other actors are changed

    Parameters
    ----------
    parent : PoserMeshedObject
      parent PoserMeshedObject (Prop or Actor)
    pa : PoserActor or PoserProp
      Actor to attach
    '''
    ldesc = pa.getFigure().getDescendant(pa)
    ldesc.insert(0, pa)
    idxSuffix = ":{0:d}".format(self.getBodyIndex())

    #  Figure indexes shall be changed in all moved actors    
    for act in ldesc:
      on = act.getName()
      nn = cleanName(on) + idxSuffix
      act.setName(nn)
      pa.getFigure().changeReference(on, nn)

    #  Other references like BODY:n shall be renamed too!
    ms = { vod.getGroupName() for act in ldesc for po in act.getChannels().getLstAttr() for vod in po.getVOD() }

    for otherRefName in ms:
      nn = cleanName(otherRefName) + idxSuffix
      pa.getFigure().changeReference(otherRefName, nn)

    self._lstActor += ldesc

    #  Update child and weld trees
    pa.getFigure().changeReference(pa.getParent(), parent.getName(), changeRefToBODY=changeRefToBODY)
    self._figDesc.addActor(parent, ldesc)

    #  Set the new parent figure
    pa.setFigure(self)
    if self._figureResFile:
      pa.setFigureResFile(self._figureResFile)


  #
  #
  def addMagnet(self, baseProp, deformerProp, sphereZone, masterChannelName=None, ctrlRatio=1.0, keys:'list of Tuple (key,value)'=None):
    ''' Add a Magnet to a Figure.
    Create the deformer channels in the pointed actors and optionaly bind them to a master Value Param.
    The controling channel is created either with a valueOpDeltaAdd or a valueOpKey.

    Parameters
    ----------
    baseProp : BaseProp
      Base Prop of the Magnet
    deformerProp : DeformerProp
      Deformer Prop of the Magnet
    sphereZone : SphereZoneProp
      Spheric Zone Prop of the Magnet
    masterChannelName : str, optional, default None
      Optional Master channel to control the magnet usage from the BODY

    ctrlRatio : float, optional, default 1.0
      Control Ratio of the valueOpDeltaAdd

    keys : list of Tuple (key,value), optional, default None
      List of tuples to use when a valueopKey is created. if None, a valueOpDeltaAdd is created.
    '''
    ret = C_OK
    
    smartParent = baseProp.getAttribut(PoserToken.E_smarParent).getValue()

    actorDest = self.findActor(smartParent)

    # Remove SmartParent attributs
    baseProp.deleteAttribut(PoserToken.E_smarParent.token)
    deformerProp.deleteAttribut(PoserToken.E_smarParent.token)
    sphereZone.deleteAttribut(PoserToken.E_smarParent.token)

    baseProp.setParent(actorDest.getName())
    deformerProp.setParent(baseProp.getName())
    sphereZone.setParent(actorDest.getName())

    ldesc = [baseProp, deformerProp, sphereZone]
    self._lstActor += ldesc
    self.getFigureDesc().addActor(actorDest, ldesc, weldActors=False)

    # Create Deformer Channels
    bodyName = PoserConst.C_BODY + ":" + str(self._bodyIdx)
    for targetName in [ po.getValue() for po in deformerProp.getLstAttr() if po.getPoserType()==PoserToken.E_deformTarget ]:
      targetActor = self.findActor(targetName)

      if targetActor: 
        dparm = targetActor.CreateDeformerP(deformerProp.getName(), sphereZone.getName(), deformerProp.getName(), isHidden=True)

        if masterChannelName:
          if keys:
            vop = ValueOpDelta(PoserToken.E_valueOpKey, self.getRefName(), bodyName, masterChannelName, keys=keys)
          else:
            vop = ValueOpDelta(PoserToken.E_valueOpDeltaAdd, self.getRefName(), bodyName, masterChannelName, ctrlRatio)
          
          dparm.addVOD(vop)
      else:
        logging.warning("Figure[%s] has no Actor[%s] for Magnet[%s]", self.getName(), targetName, deformerProp.getName())
        ret = min(ret, C_FAIL)

    return ret

  def setFigureDescr(self, figd):
    self._figDesc = figd

  def getFigureDesc(self):
    return self._figDesc

  # 
  # Set the figureResFile.
  #    
  def setFigResFile(self, sa):
    self._figureResFile = sa

  # 
  # Get the figureResFile.
  #    
  def getFigResFile(self):
    return self._figureResFile

  def setFigResFileGeom(self, objFileName:str):
    '''
    Set the path to the OBJ file in the figureResFile.
    '''
    fn = objFileName.replace(os.sep, ':')
    self._figureResFile.setValue(fn)

  def getPoserFile(self):
    return self._pf

  def createPropagation(self, upperActor:str or PoserActor, parmName:str, destChannelType:PoserToken, ctrlRatio:float):
    ''' Create a valueParm in upperActor and propage it to all descendants at destChannelType level.
    Parameters
    ----------
    upperActor : str or PoserActor
      Actor or upper actor's name (without :index)

    parmName : str
      Name of new channel

    destChannelType : PoserToken
      Type of channel to control

    ctrlRatio : float
      Control Ratio of the valueOpDelatAdd created operation

    Returns
    -------
    int
      C_OK : Success
      C_FAIL : Actor not found
    '''
    vparm = GenericTransform(PoserToken.E_valueParm, parmName)
    vparm.setPrintName(parmName)
    upAct = self.findActor(upperActor, withIndex=False) if isinstance(upperActor, str) else upperActor
    if not upAct:
      logging.warning("Upper Actor[" + str(upperActor) + "] not found ")
      return C_FAIL
    
    res = upAct.getChannels().addChannel(vparm)
    ldesc = self.getDescendant(upAct)
    for pa in ldesc:
      gt = pa.getChannels().findAttribut(destChannelType)
      if gt:
        vop = ValueOpDelta(PoserToken.E_valueOpDeltaAdd, self.getRefName(), upperActor.getName(), parmName, ctrlRatio)
        gt.addVOD(vop)
      else:
        logging.warning("Actor[" + pa.getName() + "] has no channel " + destChannelType.token)
        res = C_FAIL

    return res

  #TODO: Cleaning required
  def createChannelMorphList(self, InitSetTargetMorph):
    pa = self.getActors()[0]

    lstCS = ChannelMorphStatusList()
    if pa.getName().startswith("BODY"):
      # bodyIdx = pa.getIndex()

      lstdesc = self.getDescendant()

      #  Calculate the list of channels with regards to the known one
      pareel = self._pf.findActor(pa.getName())
      channelsAttr = pareel.getChannels()

      for attr in channelsAttr.getLstAttr():
        if attr.getPoserType() == PoserToken.E_valueParm:
          cs = ChannelMorphStatus(attr, InitSetTargetMorph)

          #  Channels where not found when Figure index was higher than 9 (2 digits)
          # idxRelPos = 3 if (bodyIdx > 9) else 2
          #  Since we are at "BODY" level, we should check if descendants have non null factors for this channel.
          # for groupName in lstdesc:
          #  searchName = groupName if (groupName.rfind(':')==len(groupName)-idxRelPos) else groupName + ":" + str(bodyIdx)

          #  po = self._pf.findActor(searchName)

          #  if po:
          for po in lstdesc:
              channelsAttrDesc = po.getChannels()
              for attrDesc in channelsAttrDesc.getLstAttr():
                if attrDesc.getPoserType() == PoserToken.E_targetGeom and attrDesc.getName() == attr.getName():
                  finalFactor = attrDesc.getKeysFactor(0)
                  cs.hasNonNullDesc = (finalFactor != 0.0)
                  cs.updateDelta(attrDesc)
                  break

          lstCS.append(cs)

      #  FIX 20100704 : Channels where not found when Figure index was higher than 9 (2 digits)
      #idxRelPos = 3 if (bodyIdx > 9) else 2
      #  Now check for channels unknown at BODY level (head morph for example)
#       for groupName in lstdesc:
#         searchName = groupName if (groupName.rfind(':')==len(groupName)-idxRelPos) else groupName + ":" + str(bodyIdx)
#         po = self._pf.findActor(searchName)
# 
#         if po:
      for po in lstdesc:
          for attrDesc in po.getChannels().getLstAttr():
            if attrDesc.getPoserType() == PoserToken.E_targetGeom:
              cs = lstCS.find(attrDesc.getName())
              if cs == None:
                cs = ChannelMorphStatus(attrDesc, InitSetTargetMorph)
                lstCS.append(cs)
              else:
                cs.updateDelta(attrDesc)

    self._lstCS = lstCS
    return lstCS

  def getChannelMorphList(self):
    return self._lstCS

  def getLstMaterial(self):
    if self._lstMat==None:
      self._lstMat = [ po for po in self.getFigureDesc().getLstAttr() if isinstance(po, PoserMaterial) ] if self.getFigureDesc() else [ ]

    return self._lstMat

  #
  # Return a PoserMaterial by name
  #
  def getMaterial(self, materialName):
    for mat in self.getLstMaterial():
      if mat.getName()==materialName:
        return mat
    return None


  def addMaterial(self, mat:'PoserMaterial'):
    # Check if it does not already exists and find the last material position
    found = False
        
    for i,po in enumerate(self.getFigureDesc().getLstAttr()):
      if isinstance(po, PoserMaterial):
        lastMatIdx = i 
        if po.getName()==mat.getName():
          found = True
    
    if found:
      return C_FAIL
    
    self.getFigureDesc().getLstAttr().insert(lastMatIdx+1, mat)
    
    self._lstMat = None
    return C_OK
  
  #
  # Options of the report algorithm
  # class ReportOption(object): Named Tuple from PoserMeshed
  #   translation     Translation between original MeshedObject and its localisation in this.
  #   maxDist         Maximal distance to take a point into account.
  #   enhance         Enhancement algorithm in C_NO_ENHANCEMENT, C_AVG_ENHANCEMENT, C_MLS_ENHANCEMENT.
  #   boundingType    Type of bounding in C_NO_BOUNDING, C_BOX_BOUNDING, C_SPHERE_BOUNDING
  #                   A vertex will get a calculated delta if it intersects the bounds.
  #   useVicinityLoop Use a viciniy determination algorithm to find the neighboor vertex of a face
  #                   with missing deltas. The average deplacement will be calculated on neighboor vertex list.
  #   alpha           Influence of distant point (less that one). alpha = 0.6 is usually a good value.
  #   minVectLen       Minimal value for displamcent vectors. Vectors with a norm smaller that minVecttLen will ne ignored
  #   PoserConst.C_OK when result is correct. PoserConst.C_ERROR when parameters are not correct.
  #    
  # @createDeltas.register(object, str, Figure, List, Set, ReportOption)
  # @createDeltas.register(object, str, PoserMeshedObject, Set, ReportOption)
  def createDeltas(self, poserRootDir, refFigObj, lstRefGeom, setTargetMorph, ropt):
    ''' Create in the current Figure the best deltas for the list of morph targets.
    This implementation starts with an extracted refFigure for optimisation purpose.

    Parameters
    ----------
    poserRootDir : str
      Root Dir of the installation (to find the .OBJ files)

    refFigure : str
       name of the figure that contains initial deltas

    setTargetMorph : set or list of str
      Morphs' names to create

    Returns
    -------
    int
      C_OK : Success
      C_ERROR : Error in parameters
    '''
    ret = C_OK

    if isinstance(refFigObj, Figure):

      if not lstRefGeom:
        refPoserObject = refFigObj.getPoserFile()
        lstRefGeom = refPoserObject.extractAll(poserRootDir, refFigObj.getBodyIndex(), None)
  
      #  Extract and Sort GeomCustom to get single numbered groups
      curPoserObject = self.getPoserFile()
      lstCurGeom = curPoserObject.extractAll(poserRootDir, self._bodyIdx, None)
      if (lstCurGeom == None) or (lstRefGeom == None) or (setTargetMorph == None):
          return C_ERROR
  
      for srcGC in lstCurGeom:
        srcWG = srcGC.getWaveGeom()
  
        tabMapping = calcMapping_KDTree(srcWG, lstRefGeom, ropt.translation, ropt.maxDist)
  
        #  Find the actor
        srcActor = curPoserObject.findActor(srcGC.getName())
        channelsAttr = srcActor.getChannels()
  
        #  Foreach morph target ==> Exploit tabMapping for srcGC
        for channelName in setTargetMorph:
          setFoundDeltas = findNewDelta(tabMapping, refFigObj, channelName)
          setNewDeltas = { }
  
          #  Local Enhancement
          Deltas.enhancement(srcWG, setFoundDeltas, setNewDeltas, ropt.enhance, ropt.boundingType, ropt.useVicinityLoop, ropt.alpha)
          if len(setNewDeltas) > 0:
            #  Filter the result list to remove too short vectors
            setFinalDeltas = filterLength(setNewDeltas, ropt.minVectLen)
  
            #  Create or update the channel list
            channelsAttr.updateOrCreate(channelName, self.getRefName(), srcWG, setFinalDeltas, self._bodyIdx)
            #  Check at BODY level, if valueParm exists
            self.updateOrCreateValueParm(channelName)
            logging.info("Deltas created for %s.%s : %d", srcGC.getName(), channelName, len(setFinalDeltas))

    else: # refFigObj should be a PoserMeshedObject
      refMeshedObj = refFigObj

      curPoserObject = self.getPoserFile()
      #  Extract and Sort GeomCustom to get single numbered groups
      lstCurGeom = curPoserObject.extractAll(poserRootDir, self._bodyIdx, None)
      lstRefGeom = [ refMeshedObj.getBaseGeomCustom(poserRootDir), ]

      if (lstCurGeom == None) or (lstRefGeom == None) or (setTargetMorph == None):
        return C_ERROR

      for srcGC in lstCurGeom:
        srcWG = srcGC.getWaveGeom()

        tabMapping = calcMapping_KDTree(srcWG, lstRefGeom, ropt.translation, ropt.maxDist)

        #  Find the actor
        #       List<PoserActor> lsta = curPoserObject.findAllActor(srcGC.getName());
        srcActor = curPoserObject.findActor(srcGC.getName())
        channelsAttr = srcActor.getChannels()

        #  Foreach morph target ==> Exploit tabMapping for srcGC
        for channelName in setTargetMorph:
          logging.info("Creating deltas for " + srcGC.getName() + "." + channelName)
          setFoundDeltas = findNewDelta(tabMapping, refMeshedObj, channelName)
          setNewDeltas = [ ] # new ArrayList<DeltaPoint>(lstFoundDeltas.size());

          #  Local Enhancement
          Deltas.enhancement(srcWG, setFoundDeltas, setNewDeltas, ropt.enhance, ropt.boundingType, ropt.useVicinityLoop, ropt.alpha)
          if len(setNewDeltas) > 0:
            #  Filter the result list to remove too short vectors
            setFinalDeltas = filterLength(setNewDeltas, ropt.minVectLen)

            #  Create or update the channel list
            channelsAttr.updateOrCreate(channelName, self.getRefName(), srcWG, setFinalDeltas, self._bodyIdx)
            #  Check at BODY level, if valueParm exists
            self.updateOrCreateValueParm(channelName)
            logging.info("Deltas created for %s.%s : %d", srcGC.getName(), channelName, len(setFinalDeltas))
      
    return ret

  def updateOrCreateValueParm(self, channelName):
    ''' Create or Update a valueParm channel.
    Make it visible (not Hidden)

    Parameters
    ----------
    channelName : str
      Name of the channel to create or modify.

    refFigure : str
       name of the figure that contains initial deltas

    setTargetMorph : set or list of str
      Morphs' names to create

    Returns
    -------
    GenericTransform
      The found or created channel
    '''

    #  Check at BODY level, if valueParm exists
    bodyAct = self.getPoserFile().findActor("BODY:" + str(self._bodyIdx))
    for rt in bodyAct.getChannels().getLstAttr():
      if (rt.getPoserType()==PoserToken.E_valueParm) and (rt.getName()==channelName):
        #  Ensure that it is a visible attribute
        rt.setHidden(False)
        return rt
      
    rt = GenericTransform(PoserToken.E_valueParm, channelName, None, None, None)
    bodyAct.getChannels().getLstAttr().insert(0, rt)
    return rt


  # 
  def hideAfter(self, pa, hm):
    ''' Hide descendant actors of the given one.
    Parameters
    ----------
    pa : PoserActor
      Start Actor
    hm : bool
      Indicates to Hide the descendant actors in the Poser Menu    
    '''
    lstdesc = self.getDescendant(pa)
    for act in lstdesc:
      act.setHidden(True, hm)

  # 
  def delete(self, pa):
    ''' Delete an actor and its descendant actors or 
    Delete the given PoserProp from the list of props.
    OR
    Delete a material from the figure

    Parameters
    ----------
    pa : PoserActor or PoserProp or PoserMaterial
      object to delete

    Returns
    -------
    int
      C_OK : Success
      C_FAIL : Actor not found
    '''
    res = C_OK

    if isinstance(pa, PoserActor):
      lstdesc = self.getDescendant(pa)
      lstdesc.insert(0, pa)

      for act in lstdesc:
        actorName = act.getName()
        self._lstActor.remove(act)

        #  Clean Figure Attributs : addChild and weld
        self._figDesc._lstAttr[:] = [ po for po in self._figDesc._lstAttr if not ( isinstance(po, (AddChildSA, )) and ((po.l0 == actorName) or (po.l1 == actorName))) ]

    elif isinstance(pa, PoserProp): # pa should be a PoserProp
      try:
        propName = pa.getName()
        self._lstProp.remove(pa)

        #  Clean Figure Attributs : addChild and weld
        self._figDesc._lstAttr[:] = [ po for po in self._figDesc._lstAttr if not ( isinstance(po, (AddChildSA, )) and ((po.l0 == propName) or (po.l1 == propName))) ]

      except:
        res = C_FAIL
    else: # pa should be a material
      try:
        self.getFigureDesc().getLstAttr().remove(pa)
      except:
        res = C_FAIL

    return res

  # 
  def getDescendant(self, paOrFirstName:str or PoserActor=None):
    ''' Return the list of actors which depends on given actor's name or actor object (PoserActor).

    Parameters
    ----------
    paOrFirstName : str or PoserActor, optional, default None
      Actor or actor's name (without :index)
      if None getDescendant returns the descendant of the root actor (usually BODY)

    Returns
    -------
    list of str or list of PoserActor
      A list of actors represented PoserActor or names (according to the call)
    '''
    if paOrFirstName:
      if isinstance(paOrFirstName, PoserActor):
        fn = paOrFirstName.getName()[0:paOrFirstName.getName().find(':')]
        lst = [ act for act in [ self.findActor(aname) for aname in self.getDescendant(fn) ] if act ]
      else:
        lst = [ paOrFirstName + ":" + str(self._bodyIdx) , ]
  
        for po in self._figDesc.getLstAttr():
          if (isinstance(po, (AddChildSA, ))) and (po.getName() == "addChild"):
            parentName = po.l1.strip()
            if parentName in lst:
              lst.append(po.l0)
  
        del lst[0]
    else:
      root = self.findActor(self._figDesc.getRoot(), withIndex=True)
      lst = [ a for a in self._lstActor if a!=root ]
      
    return lst


  # 
  #    * @param pa
  #    * @param objFileName
  #    * @param adaptJCM
  #    * @param hideAfter
  #    * @param hideMenuAfter
  #    * @return
  def stump(self, pa, poserRootDir, objFileName, adaptJCM, hideAfter, hideMenuAfter):
    ''' Stump an actor of the figure with the given OBJ file.
    No more deleteAfter, because it gives bad results.

    '''
    if not pa in self._lstActor:
      return PoserConst.C_ACTOR_NOTFOUND

    #  Geometry of the limb in the original OBJ file
    bodyg = pa.getBaseGeomCustom(poserRootDir)
    
    #  Change Geometry definition
    pa.setBaseMesh(poserRootDir, objFileName)

    if hideAfter:
      self.hideAfter(pa, hideMenuAfter)

    #  2008AVR14 - AdaptJCM Tested ok
    if adaptJCM:
      #  Get Custom Geometry
      curg = pa.getBaseGeomCustom(poserRootDir)

      tabCur = curg.getWaveGeom().coordList

      for attr in pa.getChannels().getLstAttr():
        if attr.getPoserType() == PoserToken.E_targetGeom and attr.getName().startswith("JCM"):
          dlt = attr.getDeltas()
          logging.info("Updating[%s] in %s : %d", attr.getName(), pa.getName(), len(dlt.deltaSet))

          nbIdx = 0
          for dp in dlt.deltaSet.values():
            pcur = bodyg.getWaveGeom().coordList[dp.noPt]

            dmin = sys.float_info.max
            res = -1
            for j,otherPt in enumerate(tabCur):
              d = pcur.distanceL1(otherPt)
              if d < dmin:
                dmin = d
                res = j
                
            if dmin < 1e-3:
              # log.info("Point[" + dp.getPointNo() + "] Found at (" + res + ") : " + dmin);
              dp.setPointNo(res)
              nbIdx += 1
            else:
              # log.info("Point[" + dp.getPointNo() + "] not exactly found " + dmin);
              dp.setPointNo(-1000)
               
          nt = { dp.noPt:dp for dp in dlt.deltaSet.values() if dp.getPointNo()>=0 }
          attr.setDeltaTab(nt)
          attr.setNumbDeltas(curg.getWaveGeom().getCoordListLength())
          logging.info("AdaptJCM[%s] : %d reported", attr.getName(), nbIdx)

    return C_OK

  # 
  def addAlternateGeom(self, pa, poserRootDir, objFileName, altChannelInternalName, altChannelName, pos):
    ''' Add an alternate geometry file to an actor of the figure.

    TODO: NOT IMPLEMENTED

    Parameters
    ----------
    pa : PoserActor
      Actor that receive the alternate geometry
    poserRootDir : str
      Root Dir of the installation (to find the .OBJ files)
   
    objFileName : str
      Path or relative path to the geometry file (.OBJ)

    pos : int
      Position of the geometry in the list of alternate geometries

    Returns
    -------
    int
    '''
    _res = C_OK
    if pa in self._lstActor:
      logging.warning("Not Implemented yet")
    else:
      _res = PoserConst.C_ACTOR_NOTFOUND
    return _res

  #
  def extractGeometry(self, poserRootDir, lstpa=None, lstch=None):
    ''' Extract the geometries of the Figure.

    Parameters
    ----------
    lstpa : list of PoserActor, optional, default None
      List of PoserActor to extract, if none all actors are considered

    lst : ChannelMorphStatusList or set/list of channel names
      List of valueParm or targetGeom names to be used for Apply delta

    Returns
    -------
    list of GeomCustom
      List of Poser representation of a geometry (contains the WaveGeom object)
    '''
    lstgeom = [ ]
    basegc = None
    resgc = None
    globalgc = None
    stm = lstch.getChannelSet() if isinstance(lstch, ChannelMorphStatusList) else lstch

    if not lstpa:
      lstpa = self.getActors() 

    for pa in lstpa:
      if pa.getGeomType()==PoserConst.GT_GLOBAL_OBJFILE:
        if not globalgc:
          basegc = pa.getFigureResFile().getGeomCustom(poserRootDir)
          if basegc and basegc.isValid():
            globalgc = GeomCustom(basegc)
            globalgc.findApplyDelta(self._bodyIdx, self._pf, stm)
          else:
            #  Probably due to a bad path
            return None

        resgc = globalgc.extractSortGeom(pa.getName(), pa.getGeomType())

      elif (pa.getGeomType()==PoserConst.GT_LOCAL_OBJFILE) or \
           (pa.getGeomType()==PoserConst.GT_INTERNAL):

        basegc = pa.getBaseGeomCustom(poserRootDir)
        localgc =  GeomCustom(basegc)
        localgc.findApplyDelta(self._bodyIdx, self._pf, stm)
        resgc = localgc.extractSortGeom(pa.getName(), pa.getGeomType())

      # elif pa.getGeomType()==PoserMeshedObject.GT_NONE:
      else:
        logging.warning("Unknown GeomType in (%s.%s):%d", self.getName(), pa.getName(), pa.getGeomType())
        resgc = None

      lstgeom.append(resgc)

    return lstgeom

  #
  def getMorphedMesh(self, poserRootDir, lstch):
    ''' Return a morphed GeomCustom of the base geometry of the figure.

    Parameters
    ----------
    poserRootDir : str
      Root Dir of the installation (to find the .OBJ files)

    lst : ChannelMorphStatusList or set/list of channel names
      List of valueParm or targetGeom names to be used for Apply delta

    Returns
    -------
    GeomCustom
      The Poser representation of a geometry (contains the WaveGeom object)
    '''
    localgc = None
    stm = lstch.getChannelSet() if isinstance(lstch, ChannelMorphStatusList) else lstch
    basegc = self.getActors()[0].getFigureResFile().getGeomCustom(poserRootDir)
    if basegc and basegc.isValid():
      localgc = GeomCustom(basegc)
      localgc.findApplyDelta(self._bodyIdx, self._pf, stm)
    return localgc

  # 
  # @param poserRootDir
  # @param pf              the poser file
  # @param lstUsedActor    
  def getActiveGeometry(self, poserRootDir, lstUsedActor):
    ''' Find and load all geometries used by the figure. (including internal and replaced ones)
    Does not extract groups of each Geom, Does not applay any morph
    Main geometry (from figureResFile is stored first).

    Parameters
    ----------
    poserRootDir : str
      Root Dir of the installation (to find the .OBJ files)

    lstUsedActor : list
      Output parameters of actors concerned by a special geometry

    Returns
    -------
    list of GeomCustom
      List of Poser representation of a geometry (contains the WaveGeom object)
    '''
    lstActor = self.getDescendant()
    lstFusion = [ ]
    if not lstUsedActor:
      lstUsedActor = [ ]

    # for gn in lstActor:
    for actor in lstActor:
#      if gn!=lstActor[0]:
      if actor!=lstActor[0]:
        lstDesc = self.getWelded(actor.getName())
        #if lstDesc:
        for descGn in lstDesc:
          pa = self.findActor(descGn)
          if (pa.getGeomType()==PoserConst.GT_LOCAL_OBJFILE) or (pa.getGeomType()==PoserConst.GT_INTERNAL):
            locGeom = pa.getBaseGeomCustom(poserRootDir)

            lstUsedActor.append(pa)
            lstFusion.append(locGeom)

            # Modify the storage class of the Actor
            pa.setGeomType(PoserConst.GT_GLOBAL_OBJFILE)
            pa.setGeomGroupName(locGeom.getGroupName())

    return lstFusion

  # 
  def getWelded(self, firstName):
    ''' Return the list of actors which are connected or welded to given actor's name.
    Parameters
    ----------
    firstName : str
      Name of the actor

    Returns
    -------
    list of str
      List of unique names
    '''
    figObj = self.getFigureDesc()

    if not figObj:
      return None

    setres = [ ]
    for po in figObj.getLstAttr():
      if po.getPoserType()==PoserToken.E_weld:

        childName = po.l0
        parentName = po.l1.strip()

        if childName==firstName:
          if not parentName in setres:
            setres.append(parentName)
        else:
          if (parentName==firstName) and (not childName in setres):
            setres.append(childName)

    return setres

  # 
  def hasMultipleGeom(self):
    ''' Return a binary maps that indicates if the figure is composed of several geometries.
    
    Returns
    -------
    int
      PoserConst.C_OK : a single geometry is used and defined by FigureResFile attribut
      Bitmask of : C_HAS_INTERNAL, C_HAS_LOCAL_OBJFILE, C_HAS_ALT_GEOM
    '''
    retmask = 0
    lstActor = self.getDescendant()
    for actor in lstActor:
      if actor!=lstActor[0]:
        lstDesc = self.getWelded(actor.getName())
        #if lstDesc:
        for descGn in lstDesc:
          pa = self.findActor(descGn)
          if pa.getGeomType()==PoserConst.GT_LOCAL_OBJFILE:
            retmask |= PoserConst.C_HAS_LOCAL_OBJFILE
          else:
            if pa.getGeomType()==PoserConst.GT_INTERNAL:
              retmask |= PoserConst.C_HAS_INTERNAL
          if pa.getAltGeomList():
            gtalt = pa.getAltGeomChannel()
            valFrame0 = int(gtalt.getKeysFactor(0))

            if valFrame0 != 0:
              retmask |= PoserConst.C_HAS_ALT_GEOM

    return retmask

  # Remap morphs' deltas of actors' channels according to a list of index map.
  # Index map contains the new index of vertex for each geom group.
  # 
  # @param poserRootDir    Should not be used. Main geom supposed to be already loaded
  # @param lstUsedActor    list of actor to remap
  # @param outMapLst       list of index map tables
  #
  # TODO: Remap weightmap(s) also
  #
  def remapMorph(self, poserRootDir, lstUsedActor, outMapLst):
    ret = C_OK
    mainGeom = self.getFigResFile().getGeomCustom(poserRootDir).getWaveGeom()
    i = 0
    for i,pa in enumerate(lstUsedActor):
      tmpmap = outMapLst[i]

      grp = mainGeom.getGroup(pa.getGeomGroupName())

      nVertIdx = mainGeom.calcGroupVertIndex(grp)

      for gt in pa.getChannels().getLstAttr():
        if gt.ishasDeltas():
          dlt = gt.getDeltas()
          for dp in dlt.getDeltaTab():
            wholeMapIdx = tmpmap[dp.getPointNo()]
            pos = Arrays_binarySearch(nVertIdx, wholeMapIdx)
            if pos < 0:
              logging.warning("Morphs remapping error for " + pa.getGeomGroupName() + "." + gt.getName())
              ret = C_ERROR
            dp.setPointNo(pos)

    return ret

  # Imported table analysis 
  # @param  tabChan
  # @param  baseDir Location of geometries
  # @return a status table, null if check is impossible 
  def checkImportedChannels(self, tabChan, baseDir):
    baseDir = baseDir if baseDir.rfind(os.sep) == len(baseDir)-1 else baseDir + os.sep
    nblgn = len(tabChan)

    if nblgn < 9:
      logging.info("Too few lines in file [%d]",  nblgn)
      return None

    cia = ChannelImportAnalysis(self, baseDir, tabChan)
    cia.checkVocab()
    cia.checkColumns()
    return cia

  # Import channel according to specifications contained by the ChannelImport Analysis.
  #
  #@param  cia          Result of file analysis
  #@param  poserRootDir Location of Poser files
  #
  def importChannels(self, cia, poserRootDir):
    ret = C_OK
    for ccd in cia.lstChan:
      if cia.ts[0][ccd.nocol] == C_OK:
        logging.info("Upgrading : " + ccd.act.getName())
        gt = ccd.gt
        if gt:
          logging.info("Overriding Channel[" + gt.getName() + "]")
        else:
          gt = GenericTransform(ccd.chanType, cia.tabChan[1][ccd.nocol])
          gt.setPrintName(gt.getName())
          ccd.act.getChannels().addChannel(gt)
          logging.info("Creating Channel[" + gt.getName() + "]")

        # Set standard values
        gt.setInitValue(ccd.initValue)
        gt.setMin(ccd.min)
        gt.setTrackingScale(ccd.trackingScale)
        gt.setForceLimits(1)
        gt.setInterpStyleLocked(1)
        gt.addKeyFrame(0, ccd.initValue)

        # Create the list of Alternate Geometries
        if ccd.chanType == PoserToken.E_geomChan:
          for fic in ccd.lstAltFiles:
            ccd.act.addAltGeom(altGeomFile=fic, poserRootDir=poserRootDir)
          ccd.max = len(ccd.act.getAltGeomList())

        # The number of alternate geom, could have changed
        gt.setMax(ccd.max)
        for vod in ccd.lstOps:
          logging.info("  Adding Op to Channel[" + gt.getName() + "] : " + vod.getPoserType().token + "(" + vod.l1 + "." + vod.l2 + ")")
          gt.addVOD(vod)

      else:
        logging.info("Bypassing column : " + str(ccd.nocol))
    return ret

  def getChannel(self, pa, expr):
    ''' Find the channel that matches the given expression.

    QualifiedChannelName = [ActorName [':' bodyIndex] '.' ]ChannelName
   
    NB :if the optional body index is different form the body index of the figure, 
    the returned channel could belong to another figure or prop.
    Parameters
    ----------
    expr : str
      Expression to find
       
    Returns null if not found
    '''

    channelName = expr
    ptind = expr.find('.')
    if ptind >= 0:
      # Extract the real channel name
      channelName = expr[ptind + 1:]
      actorName = expr[0:ptind]

      # Find the target actor
      actind = index(actorName)
      if actind <= 0:
        # No ':' the actor should belong to the current figure
        actorName = actorName + ':' + str(self._bodyIdx)

      pa = self.findActor(actorName)

    return pa.getChannel(channelName) if pa else None

  # Create a valueParam at Body level to drive the visibility of each Actor
  # @return PoserConst.C_OK
  def addDrivenVisibility(self):
    ret = C_OK
    lstAct = self.getActors()
    bodyName = PoserConst.C_BODY + ":" + str(self._bodyIdx)
    body = self._pf.findActor(bodyName)
    for pa in lstAct:
      if pa != body:
        driverVPName = "HideShow_" + cleanName(pa.getName())

        visChan = pa.getGenericTransform("visibility")

        # Create the visibility channel, if it does not exist
        if visChan == None:
          visChan = GenericTransform(PoserToken.E_visibility, 'visibility')
          visChan.setInitValue(1.0)
          visChan.setMin(0.0)
          visChan.setMax(1.0)
          visChan.setTrackingScale(1.0)

          keys = Keys() # Default keys are static=0
          keys.addKey(0, 0.0)
          visChan.addAttribut(keys)

          vod = ValueOpDelta(PoserToken.E_valueOpDeltaAdd, self.getRefName(), bodyName, driverVPName, 1.0)
          visChan.addVOD(vod)
          logging.info("Adding Channel[visibility] to " + self.getName() + "." + pa.getName())
          pa.getChannels().addChannel(visChan)

        # Check driver channel
        driverChan = body.getGenericTransform(driverVPName)
        if driverChan == None:
          driverChan = GenericTransform(PoserToken.E_valueParm, driverVPName)
          driverChan.setPrintName(driverVPName)
          driverChan.setInitValue(1.0)
          driverChan.setMin(0.0)
          driverChan.setMax(1.0)
          driverChan.setTrackingScale(1.0)

          keys = Keys() # Default keys are static=0
          keys.addKey(0, 1.0)
          driverChan.addAttribut(keys)
          logging.info("Adding Driver Channel[" + driverVPName + "] to " + self.getName())
          body.getChannels().addChannel(driverChan)

        # Remove the object from menu
        pa.setAddToMenu(False)
        pa.setHidden(True)
    return ret

  def appendCheckMat(self, pa, gc, pm, lstUse):
    wg = gc.getWaveGeom()
    lstMat = wg.getMaterialList()
    if pm.getName() in lstMat:
      lstUse.append([ pa.getName(), PoserConst.GEOMTYPE[pa.getGeomType()], pa.getDisplayName() ] )

  #  Checkif the material is used in any geometry of the figure.
  #  @param pm
  #  @param lstUse
  #  @return    PoserConst.C_OK means used, PoserConst.C_FAIL means not used
  def checkMaterialUsage(self, pm, poserRootDir, lstUse):
    cpt = 0
    for pa in self.getActors():
      if pa.getGeomType() != PoserConst.GT_NONE:
        self.appendCheckMat(pa, pa.getBaseGeomCustom(poserRootDir), pm, lstUse)

      lstAlt = pa.getAltGeomList()
      if lstAlt:
        for ag in lstAlt:
          fn = getRealPath(poserRootDir, ag.getGeomFileName())
          gc = GeomCustom(fn)
          if gc.isValid():
            self.appendCheckMat(pa, gc, pm, lstUse)

    for pp in self.getProps():
      if pp.getGeomType() != PoserConst.GT_NONE:
        self.appendCheckMat(pp, pp.getBaseGeomCustom(poserRootDir), pm, lstUse)

    return C_OK if cpt > 0 else C_FAIL


  #
  #  Return the list of actors and deformers that match the pattern
  #
  def findDeformer(self, pattern):
    lstRes = [ (act.getName(), gt.getName()) for act in self.getActors() for gt in act.getChannels().getLstAttr() if (gt.getPoserType()==PoserToken.E_deformerPropChan) and gt.getName().startswith(pattern) ]
    return lstRes

  #
  #  Add a master control channel
  #  @param pattern
  #
  def addMasterChannel(self, channelName, pattern):
    res = C_OK
    bodyName = "BODY:" + str(self.getBodyIndex())
    body = self.findActor(bodyName)
    masterGT = GenericTransform(PoserToken.E_valueParm, channelName)
    masterGT.setMin(-1.0)
    masterGT.setMax(1.0)
    masterGT.setInterpStyleLocked(0)
    masterGT.setPrintName(channelName)
    body.getChannels().addChannel(masterGT)

    for act in self.getActors():
      for gt in act.getChannels().getLstAttr():
        if (gt.getPoserType()==PoserToken.E_deformerPropChan) and gt.getName().startswith(pattern):
          vop = ValueOpDelta(PoserToken.E_valueOpDeltaAdd, self.getPrintName(), bodyName, channelName, 1.0)
          gt.addVOD(vop)

    return res

  def filterChannelList(self, outLst, inpLstChan, tk, pattern):
    outLst += [ gt for gt in inpLstChan \
               if (gt.getPoserType()==tk) and (not gt.ishasDeltas()) and gt.getName().startswith(pattern) ]

  # Etrange! (et private en Java)
  def cleanProposedList(self, lstgt):
    fin = False
    while not fin:
      fin = True
      for gt in lstgt:
        limp = self.getPoserFile().deleteChannelImpact(gt)
        if len(limp) == 1:
          logging.info("Channel " + gt.getName() + " can be deleted in " + gt.getPoserMeshedObject().getName())
          lstgt.remove(gt)
          gt.getPoserMeshedObject().deleteChannel(gt)
          fin = False


  # 
  def cleanAllChannel(self, pattern):
    ''' Clean (delete) all channels with a name that starts with the pattern and without any descendant. '''
    # Build the map of all targetGeom with empty deltas
    lstgt = [ ]
    for pa in self.getActors():
      self.filterChannelList(lstgt, pa.getChannels().getLstAttr(), PoserToken.E_targetGeom, pattern)

    for pp in self.getProps():
      self.filterChannelList(lstgt, pp.getChannels().getLstAttr(), PoserToken.E_targetGeom, pattern)

    logging.info("TargetGeoms :%d", len(lstgt))
    self.cleanProposedList(lstgt)

    # Do the same with valueParm
    # Build the map of all Value Parms (with empty deltas)
    lstvp = [ ]
    for pa in self.getActors():
      self.filterChannelList(lstvp, pa.getChannels().getLstAttr(), PoserToken.E_valueParm, pattern)
    for pp in self.getProps():
      self.filterChannelList(lstvp, pp.getChannels().getLstAttr(), PoserToken.E_valueParm, pattern)
    logging.info("ValueParm :%d", len(lstvp))
    self.cleanProposedList(lstvp)
    return C_OK

  # 
  # @param pattern
  def cleanMagnetMaterial(self):
    ''' Clean (delete) all custom materials attached to the magnets of the figure.
    Set Custom Material to False (0)
    '''
    for pp in self.getProps():
      # Check if the Prop is a : BaseProp, SphereZoneProp, MagnetDeformerProp, CurveProp
      if (pp.getCustomMaterial() == 1) and ((isinstance(pp, (BaseProp, ))) or (isinstance(pp, (BaseProp, ))) or (isinstance(pp, (BaseProp, ))) or (isinstance(pp, (BaseProp, )))):
        pp.getLstAttr()[:] = [ m for m in pp.getLstAttr() if pp.getPoserType()!=PoserToken.E_material ]
        # logging.info("Cleaning Material " + pp.getName() + " mat=" + po.getName())
    return C_OK

  # Usage not confirmed anymore
  #   def adaptMagnet(self, poserRootDir, initialGeomFile):
  #     raise(Exception, "not Implemented yet")


  def attachActor(self, parent:'new Parent Actor', srcAct:'Actor to attach from another figure', changeRefToBODY=True):
    ''' Attach an actor from a figure as child of another actor of another figure. (More or less a cut and paste).
    Relink all internal relationships of srcActor.
    Create in the destination figure the root valueParm to satisfy srcActor links
    
    Parameters
    ----------
    parent : PoserActor
      Parent actor to attach a new child
    srcAct : PoserActor
      Actor to attach from another figure
    changeRefToBODY : bool, optional, default True
      Indicates if references to BODY channels (in srcAct) shall be changed
    Returns
    -------
    int :
      Ret Code
    ''' 
    ret = C_OK

    # Retrieve all srcAct Desc and attached chanels
    srcFig = srcAct.getFigure()
    ldesc = srcFig.getDescendant(srcAct)
    ldesc.insert(0, srcAct)
    idxSuffix = ":{0:d}".format(self.getBodyIndex())

    ldescNames = [ act.getName() for act in ldesc ]

    setExternChannels =  \
     { vod for act in ldesc for po in act.getChannels().getLstAttr() for vod in po.getVOD()\
          if vod.getGroupName() not in ldescNames }

    # Recreate chanels in the destination figure (may not be only at BODY level)
    for vod in setExternChannels:
      targetActorName = cleanName(vod.getGroupName()) + idxSuffix
      act = self.findActor(targetActorName)
      if act:
        refChan = act.updateOrCreateVP(vod.getChannelName())

        srcChannel = srcFig.findActor(vod.getGroupName()).getChannel(vod.getChannelName())

        refChan.copy(srcChannel)
      else:
        logging.warning('Target Name(%s) pointed by Operator:%s not found', targetActorName, vod.__class__.__name__)

    # Attache (all) Materials of the srcAct actor figure
    for mat in srcFig.getLstMaterial():
      ret = self.addMaterial(mat)
      logging.info('Figure[%s]: Material[%s] from Actor[%s] %s', self.getName(), mat.getName(), srcAct.getName(), \
                   'added' if ret==C_OK else 'NOT added') 

    # Attach srcAct to parent + Update AddChild + Copy Weld Parts
    self.addActor(parent, srcAct, changeRefToBODY=changeRefToBODY)

    return ret


  # Write the definition part of the meshed object.
  def writeDef(self, fw, pfx):
    self._figureResFile.write(fw, "")

    for pa in self._lstActor:
      pa.writeDef(fw, "")

    for pp in self._lstProp:
      pp.writeDef(fw, "")

  # Write the Data part of the meshed object.
  def writeData(self, fw, pfx):
    self._figureResFile.write(fw, "")

    for pa in self._lstActor:
      pa.writeData(fw, "")

    for pp in self._lstProp:
      pp.writeData(fw, "")

    self._figDesc.write(fw, "")


