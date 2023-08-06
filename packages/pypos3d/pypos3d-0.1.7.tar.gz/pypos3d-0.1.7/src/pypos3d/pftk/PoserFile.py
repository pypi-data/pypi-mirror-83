# -*- coding: utf-8 -*-
import traceback
import logging
import os, gzip

from langutil import C_OK, C_FAIL, C_ERROR
from pypos3d.wftk.PoserFileParser import PoserFileParser, PZ3_FNAT

from pypos3d.pftk.PoserBasic import getRealPath, index, PoserConst, PoserToken , isCompressed, Lang, getPoserFileType, create
from pypos3d.pftk.StructuredAttribut import GenericTransform, NodeInput, PoserMaterial
from pypos3d.pftk.GeomCustom import GeomCustom
from pypos3d.pftk.PoserMeshed import PoserProp, Camera, Light
from pypos3d.pftk.Figure import Figure
from pypos3d.wftk import WFBasic
# package: pypos3d.pftk

# 
#  Path Match between a referenced path of Poser and a real path.
#  
class PathMatch(object):

    def __init__(self, o, r):
        self._originalPath = o
        self._realPath = r
        self._exist = False

    def getOriginalPath(self):
        return self._originalPath

    def setOriginalPath(self, _originalPath):
        self._originalPath = _originalPath

    def getRealPath(self):
        return self._realPath

    def setRealPath(self, _realPath):
        self._realPath = _realPath

    def isExist(self):
        return self._exist

    def setExist(self, _exist):
        self._exist = _exist

# 
class PoserFile(object):
  ''' Poser File internal representation.
  The aim of this class is to represent all kind of Poser files.
  But it works fine with : Characters (.cr2), Scenes (.pz3) and Props (.pp2)
  '''
  # 
  def __init__(self, fn):
    ''' Create a PoserFile from a file.
    
    Parameters
    ----------
    fn : str
      Filename to read
      
    Raises
    ------
    OSError : File Not found
    
    '''
    super(PoserFile, self).__init__()

    #  File name 
    self._name = ''
  
    #  PoserFile type 
    self._fileType = PoserConst.FFT_UNKNOWN
  
    #  Poser File Version   
    self._version = None
    self._versionStr = None
  
    #  Poser File PZ3 movieinfo   
    self._movieinfo = None
  
    #  Poser File PZ3 GROUND prop   
    self._ground = None
  
    #  Poser File PZ3 FocusDistanceControl prop   
    self._focusDistanceControl = None
  
    #  First actor of a PZ3 file 
    self._universe = None
  
    #  List of "Free" props (Prop, hairProp, controlProp)  = Not Attached to any character 
    self._lstProp = [ ]
  
    #  List of managed Camera 
    self._lstCamera = [ ]
  
    #  List of managed Lights 
    self._lstLight = [ ]
  
    #  List of managed Hair growth groups 
    self._lstGrowtGroup = [ ]
  
    #  List of Figure 
    self._lstFigure = [ ]
  
    #  Poser File PZ3 doc   
    self._doc = None
    self._illustrationParms = None
    self._renderDefaults = None
    self._faceRoom = None
  
    #  Temporary Attributes 
    self._lastBodyIdx = 0
  
    #  Last read (or discovered) figure at read time 
    self._lastFigure = None
    self._lastFRF = None

    self.setName(fn)
    ft = getPoserFileType(fn)
    self._fileType = ft & PoserConst.PFT_MASK
    isZipped = isCompressed(ft)

    logging.info("File[%s] : opening", fn)
    rin =  gzip.open(fn, 'rb') if isZipped else open(fn, 'rb')
    pfr = PoserFileParser(rin, PZ3_FNAT)
    pfr.getToken()
    if pfr.isLeftBracket():
      self.read(pfr)

    rin.close()
    logging.info("File[%s] : %d lines read", fn,  pfr.lineno())
    #  if WFBasic.PYPOS3D_TRACE: print ('File({0:s} - Read Error {1:s}'.format(fn, str(e.args)))
      

  # 
  def getName(self): 
    ''' Return the name of the object, for a Poser file the name is the filename. '''
    return self._name

  # 
  # * Set the name.
  # @param string
  #    
  def setName(self, s):
    self._name = s

  # 
  # Return the Poser Language Version as an PoserObject
  #    
  def getVersion(self): return self._version

  def isVersion(self, cmpVers):
    if not self._versionStr:
      sa = self._version.findAttribut(PoserToken.E_number)
      self._versionStr = sa.getValue() if sa else ''

    return False if self._versionStr==None else (self._versionStr==cmpVers)

  # 
  # Read a structured attribute data from the file. This class name, the name
  # and the opening bracket are supposed to be consumed by the caller.
  # Because it is the mean it uses to recognize a structured attribute.
  #    
  def read(self, st):
    nextLine = True
    st.getToken()
    while st.ttype != PoserFileParser.TT_EOF:
      if st.ttype == PoserFileParser.TT_EOL:
        st.getToken()

      if st.ttype == PoserFileParser.TT_WORD:
        if st.isRightBracket():
          #  End of current structured attribute
          break

        cn = st.sval

        try:
          vc = Lang[st.sval]
          #  Known word
          if vc.isStructured:
            st.getToNextLine()
            nom = "" if st.ttype == PoserFileParser.TT_EOL else st.sval
            sta = create(vc, nom)

            #  Overload of object if definition part exists
            sta = self.addAttribut(sta)

            #  Read the opening bracket
            st.getToken()
            if st.isLeftBracket():
              sta.read(st)
            else:
              logging.error( "Line[%d]:  '{' is missing for %s", st.lineno(),  cn)
          else:
            if vc.isDirect:
              st.getToNextLine()
              logging.error("Line[%d]: setDirect() illegal at PoserFile level %s", st.lineno(), cn)
            else:
              # Read before add
              sa = create(vc, st.sval)
              sa.read(st)
              self.addAttribut(sa)

            nextLine = False
        except KeyError: # if vc == None: --> Unknow word
          logging.info("Line[%d] - Unknown word:%s", st.lineno() , cn)

      if nextLine:
        st.skipToNextLine()
      else:
        nextLine = True

      #  Get next token
      st.getToken()

  # 
  # Add an object at highest level of the Poser File.
  #    
  def addAttribut(self, po):
    pot = po.getPoserType()

    if pot==PoserToken.E_version:
      self._version = po
      return self._version

    elif pot==PoserToken.E_movieInfo:
      self._movieinfo = po
      return self._movieinfo

    elif pot==PoserToken.E_keyLayer:
      logging.error("Ignored " + po.getName() + "[" + po.getPoserType() + "]")
      return po

    elif pot==PoserToken.E_figureResFile:
      #  Beginning of a figure
      self._lastFRF = po
      fig = self.findFigure(self._lastFRF)
      if fig == None:
        fig = Figure(self, frf=self._lastFRF)
        self._lstFigure.append(fig)
        self._lastFRF = None
      #  else  keep the lastFRF, because could be used for another figure with same geometry      
      self._lastFigure = fig
      return None

    elif pot==PoserToken.E_actor:
      pa = po
      pa.setPoserFile(self)
      if pa.getName() == PoserConst.C_UNIVERSE:
        if self._universe == None:
          self._universe = pa
        return self._universe

      idx = pa.getIndex()

      if self._lastFigure == None:
        self._lastFigure = Figure(self, idx)
        self._lstFigure.append(self._lastFigure)
        if (self._fileType==PoserConst.PFT_CR2) or (self._fileType==PoserConst.PFT_PZ3):
          logging.warning("Actor " + pa.getName() + " without figure in " + self.getName())

      else:
        if self._lastFigure.getBodyIndex()==PoserConst.C_BAD_INDEX:
          #  The figure has just been discovered, so the first actor gives the body index
          self._lastFigure.setBodyIndex(idx)

        else:
          #  Check index coherence
          if self._lastFigure.getBodyIndex() != idx:
            #  Means that several figures have the same target OBJ file 
            nf = self.getFigure(idx)
            if nf:
              self._lastFigure = nf
            else:
              #  log.warning("Figure index [" + idx + "] does not exists for actor " + pa.getName());              
              self._lastFigure = Figure(self, frf=self._lastFRF)
              self._lstFigure.append(self._lastFigure)
              self._lastFigure.setBodyIndex(idx)
              self._lastFRF = None

      pa = self._lastFigure.addReadActor(pa)
      if pa.isBody():
        self._lastBodyIdx = idx
      return pa

    elif pot==PoserToken.E_prop:
      pp = po
      pp.setPoserFile(self)
      if pp.getName() == "GROUND":
        if self._ground == None:
          self._ground = pp
        return self._ground

      for epp in self._lstProp:
        if pp.getName() == epp.getName():
          return epp

      if self._lastFigure == None:
        #  We are in the declarative part of "free" props
        self._lstProp.append(pp)
      else:
        pp = self._lastFigure.addReadProp(pp)
      return pp

    elif pot==PoserToken.E_light:
      li = po
      li.setPoserFile(self)
      for ell in self._lstLight:
        if li.getName() == ell.getName():
          return ell
      self._lstLight.append(li)
      return li

    elif pot==PoserToken.E_camera:
      cam = po
      cam.setPoserFile(self)
      for ec in self._lstCamera:
        if cam.getName() == ec.getName():
          return ec
      self._lstCamera.append(cam)
      return cam

    elif pot==PoserToken.E_figure:
      fig2 = self.getFigure(self._lastBodyIdx)
      if fig2:
        fig2.setFigureDescr(po)
      else:
        #  We're not reading a CR2 or PP2 or PZ3 file, but
        #  probably a Pose file ... nothing to do
        logging.warning("Figure chapter found without figure declaration")
      return po

    # Manage other Props : hairProp, controlProp, Magnets
    elif pot==PoserToken.E_controlProp or \
         pot==PoserToken.E_baseProp or \
         pot==PoserToken.E_hairProp or \
         pot==PoserToken.E_magnetDeformerProp or \
         pot==PoserToken.E_sphereZoneProp or \
         pot==PoserToken.E_curveProp:
      pp = po
      pp.setPoserFile(self)
      if pp.getName() == "FocusDistanceControl":
        if self._focusDistanceControl == None:
          self._focusDistanceControl = pp
        return self._focusDistanceControl

      for epp in self._lstProp:
        if pp.getName() == epp.getName():
          return epp
      if self._lastFigure == None:
        #  We are in the declarative part of "free" props
        self._lstProp.append(pp)
      else:
        pp = self._lastFigure.addReadProp(pp)

      return pp

    elif pot==PoserToken.E_hairGrowthGroup:
      self._lstGrowtGroup.append(po)
      return po
    elif pot==PoserToken.E_faceRoom:
      self._faceRoom = po
      return self._faceRoom
    elif pot==PoserToken.E_illustrationParms:
      self._illustrationParms = po
      return self._illustrationParms
    elif pot==PoserToken.E_renderDefaults:
      self._renderDefaults = po
      return self._renderDefaults
    elif pot==PoserToken.E_doc:
      self._doc = po
      return self._doc
    elif pot==PoserToken.E_setGeomHandlerOffset:
      return None
    #elif pot==PoserToken.E_readScript: #  TODO : Read Other Definition Script
      #logging.error("No Management rule for %s [%s]", po.getName() , po.getPoserType().token)
    else:
      logging.error("No Management rule for %s [%s]", po.getName() , po.getPoserType().token)

    return None

  # 
  # Return the figure associated to the BODY index
  # * @param idx
  # *          The BODY index
  # * @return
  #    
  def getFigure(self, idx):
    for fig in self._lstFigure:
      if fig.getBodyIndex() == idx:
        return fig
    return None

  # 
  # Returns the list of figures contained in the Poser File
  # @return the list of Figure objects (not a copy)
  #    
  def getLstFigure(self): return self._lstFigure

  # 
  # Returns the list of Cameras contained in the Poser File
  # @return the list of Camera objects (not a copy)
  #    
  def getLstCamera(self): return self._lstCamera

  # 
  # Returns the list of Lights contained in the Poser File
  # @return the list of Light objects (not a copy)
  #    
  def getLstLight(self): return self._lstLight

  # 
  # Returns the list of Props contained in the Poser File
  # @return the list of PoserProp objects (not a copy)
  #    
  def getLstProp(self): return self._lstProp

  # 
  # Return the list of all objects names that can be referenced.
  # @return
  #    
  def getLstFigProp(self):
    return [ n for f in self.getLstFigure() for n in f.getDescendant() ] + \
           [ pp.getName() for pp in self.getLstProp() ]

  # 
  # Return the list of PoserMeshedObject (actor, prop, hairprop) 
  # Return a list of PoserMeshedObject (actor, prop, hairprop) that match the
  #  given nameif any
  # @return a list of PoserMeshedObject
  #    
  def findAllMeshedObject(self, actorPropName=None):
    if actorPropName:
      return [ pp for pp in self._lstProp + self._lstLight+self._lstCamera if actorPropName == pp.getName() ] + \
            [ part for fig in self._lstFigure for part in fig.getActors() + fig.getProps() if actorPropName == part.getName() ]
    else:
      return self._lstProp + self._lstLight + self._lstCamera + \
        [ a for fig in self._lstFigure for a in fig.getActors() ] + \
        [ p for fig in self._lstFigure for p in fig.getProps()  ] \

  # 
  def writeFile(self, fn):
    ''' Write PoserFile in text format (without compression)
    # RENAMED Java write --> Python writeFile
     
    Parameters
    ----------
    fn : str
      Full path name
      
    Returns
    -------
    int
      C_OK write without error, C_ERROR a write error has occurred
    '''
    ret = C_OK
    try:
      logging.info("File[" + fn + "] : writing")
      prn = open(fn, 'w')
      self.write(prn)
      prn.close()
      logging.info("File[" + fn + "] : " + str(os.path.getsize(fn)) + " bytes")
    except OSError:
      ret = C_ERROR
    return ret

  # 
  def writeZ(self, fn):
    ''' Write PoserFile in Zlib format (text stream compressed)
     
    Parameters
    ----------
    fn : str
      Full path name

    Returns
    -------
    int
      C_OK write without error, C_ERROR a write error has occurred
    '''
    ret = C_OK
    try:
      logging.info("File[" + fn + "] : writing/zipping")
      out = gzip.open(fn, 'wt') 
      self.write(out)
      out.close()
      logging.info("File[" + fn + "] : " + str(os.path.getsize(fn)) + " bytes")
    except OSError:
      ret = C_ERROR
    return ret

  # 
  # @see deyme.v3d.poser.PoserObject#write(java.io.FileWriter)
  #    
  def write(self, fw):
    isPZ3 = (self._fileType & PoserConst.PFT_MASK) == PoserConst.PFT_PZ3

    fw.write("{\n")
    if self._version:
      self._version.write(fw, "")

    if isPZ3 and self._movieinfo:
      self._movieinfo.write(fw, "")

    #  Write Definition of "Free" Props
    #  Write Definition of Lights
    #  Write Definition of Cameras
    #  Write Definition of Figures
    allParts = [ x for x in [ self._ground, self._universe, self._focusDistanceControl ] if isPZ3  and x ]
    allParts += self._lstProp + self._lstLight + self._lstCamera + self._lstFigure 
    for part in allParts:
      part.writeDef(fw, "")

    #  -- DATA WRITING --
    #  Write Data of "Free" Props
    #  Write Data of Lights
    #  Write Data of Cameras
    #  Write Data of Figures
    for part in allParts:
      part.writeData(fw, "")

    for hgg in self._lstGrowtGroup:
      hgg.write(fw, "")

    if self._doc:
      self._doc.write(fw, "")

    if isPZ3:
      for attr in [ self._illustrationParms, self._renderDefaults, self._faceRoom ]:
        if attr:
          attr.write(fw, "")

    if isPZ3 or (self._fileType & PoserConst.PFT_MASK) == PoserConst.PFT_CR2:
      fw.write("setGeomHandlerOffset 0 0.3487 0\n")

    fw.write("}\n")

  def getChannel(self, groupName, channelName):
    po = self.findMeshedObject(groupName)
    return po.getGenericTransform(channelName) if po else None

  # 
  # Return the k factor of the first frame of the channel given by groupName of
  # the group given by groupName.
  # 
  # * @param figureName
  # *          Unused because of well known CrossWalk problems
  # * @param groupName
  # * @param channelName
  # * @return The float factor.
  #    
  def getFactor(self, figureName, groupName, channelName):
    po = self.findActor(groupName)
    if po:
      for attr in po.getChannels().getLstAttr():
        if ((attr.getPoserType() == PoserToken.E_targetGeom) or (attr.getPoserType() == PoserToken.E_valueParm)) and (attr.getName() == channelName):
          finalFactor = attr.getKeysFactor(0)

          #  Get Recursively controling channels
          for vod in attr.getVOD():
            #  FIX: 20100906 Avoid simple deadly recursion
            if (groupName != vod.getGroupName()) or (channelName != vod.getChannelName()):
              # Get the real factor of the master
              f = self.getFactor(vod.getFigureName(), vod.getGroupName(), vod.getChannelName())
              cr = vod.getControlRatio()
              finalFactor += f * cr
                    
          return finalFactor

    logging.warning(figureName + "." + groupName + " Not Found")
    return 0.0

  def calcChannelAncestors(self, gt, lstgt, lstMissing):
    vodTab = gt.getVOD()
    for op in vodTab:
      found = False
      for gl in lstgt:
        if gl.getPoserMeshedObject().getName()==op.getGroupName() and gl.getName()==op.getChannelName():
          # Found : Already in the list
          found = True
          break

      if not found:
        newgt = self.getChannel(op.getGroupName(), op.getChannelName())
        if newgt:
          lstgt.append(newgt)
          self.calcChannelAncestors(newgt, lstgt, lstMissing)
        else:
          lstMissing.append(op.getGroupName() + '.' + op.getChannelName())

  def getChannelAncestors(self, gt, lstMissing):
    lstgt = [ ]
    self.calcChannelAncestors(gt, lstgt, lstMissing)
    return lstgt

  def getDescendant(self, bodyIdx, firstName=None):
    f = self.getFigure(bodyIdx)
    return f.getDescendant(firstName) if f else None 

  def getWelded(self, bodyIdx, firstName):
    fig = self.getFigure(bodyIdx)
    return None if (fig == None) else fig.getWelded(firstName)

  def getFigResFileGeom(self, bodyIdx, PoserRootDir):
    gc = None
    f = self.getFigure(bodyIdx)
    if f:
      frf = f.getActors()[0].getFigureResFile()
      if frf:
        # Extract File path from the Poser File
        objFn = frf.getPath(PoserRootDir)

        # Read OBJ filename of the object
        gc = GeomCustom(objFn)
      else:
        gc = GeomCustom()

    return gc

  def addToSet(self, poserRootDir, hshres, ficpath):
    if (ficpath==None) or (ficpath=="") or (ficpath=='""') or (ficpath=="NO_MAP"):
      return

    try: # pm = 
      hshres[ficpath]
    except KeyError:
      # Clean the ficpath
      # Build a full path
      realpath = getRealPath(poserRootDir, ficpath)
      logging.info("Add:" + realpath)
      hshres.update( { ficpath : PathMatch(ficpath, realpath) } )

  def refPoserMaterial(self, poserRootDir, hshres, mat):
    self.addToSet(poserRootDir, hshres, mat.getTextureMap())
    self.addToSet(poserRootDir, hshres, mat.getBumpMap())
    self.addToSet(poserRootDir, hshres, mat.getReflectionMap())
    self.addToSet(poserRootDir, hshres, mat.getTransparencyMap())
    for nd in mat.getLstNodes():
      for po in nd.getLstAttr():
        if isinstance(po, (NodeInput, )):
          self.addToSet(poserRootDir, hshres, po.getFile())

  def refPoserMesh(self, poserRootDir, hshres, po):
    if (po.getPoserType() == PoserToken.E_prop) or (po.getPoserType() == PoserToken.E_hairProp) or (po.getPoserType() == PoserToken.E_actor):
      if po.getGeomType() == PoserConst.GT_LOCAL_OBJFILE:
        self.addToSet(poserRootDir, hshres, po.getGeomFileName())

      la = po.getAltGeomList()
      if la:
        for altg in la:
          self.addToSet(poserRootDir, hshres, altg.getGeomFileName())

      if po.getCustomMaterial() == 1:
        for mo in po.getLstAttr():
          if isinstance(mo, (PoserMaterial, )):
            self.refPoserMaterial(poserRootDir, hshres, mo)

  #  Compute the list of referenced files.
  #  @return    a list of Matched files
  def getReferencedFiles(self, poserRootDir):
    lstres = { }
    for fig in self.getLstFigure():
      # Get figure main file
      frf = fig.getFigResFile()

      ficpath = frf.getPath(poserRootDir)
      self.addToSet(poserRootDir, lstres, ficpath)

      for pa in fig.getActors()+fig.getProps():
        self.refPoserMesh(poserRootDir, lstres, pa)

      for mat in fig.getLstMaterial():
        self.refPoserMaterial(poserRootDir, lstres, mat)

    # Look up in alone props
    for pp in self.getLstProp():
      self.refPoserMesh(poserRootDir, lstres, pp)

    #logging.info("List size:" + str(len(lstres)))
    return lstres

  # TODO: Ugly interface to change
  # TODO: Duplicate code to clean
  def cleanNonNullDelta(self, bodyIdx:int=-1, pp=None, setTargetMorph=None):
    ''' Remove deltas from targetGeom in a Figure or a PoserProp or a PoserActor.
    Parameters
    ----------
    bodyIdx : int, optional, default -1
      Index of the figure in the PoserFile
    pp : PoserProp or PoserActor, optional, default None
      Used when bodyIdx not set
    setTargetMorph : iterable, optional, default None
      List or Set or channel names to clean. If None targetGeom starting by 'PBM' are cleaned
    Returns
    -------
    int
      Return Code
    '''
    ret = C_OK
    if bodyIdx>=0:
      logging.info("------------------------ Cleaning Deltas ------------------------")
      # Remove unused attributes of the PoserObject
      # Get all part of the character
      lstActor = self.getDescendant(bodyIdx)
      if lstActor:
        # Channels where not found when Figure index was higher than 9 (2 digits)
        #idxRelPos = 3 if (bodyIdx > 9) else 2

        for po in lstActor:
          #searchName = groupName if(groupName.rfind(':')==len(groupName) - idxRelPos) else groupName + ":" + str(bodyIdx)

          #po = self.findActor(searchName)
          #if po:
            for attr in po.getChannels().getLstAttr():
              if attr.getPoserType()==PoserToken.E_targetGeom and GenericTransform.concerned(attr.getName(), setTargetMorph):
                finalFactor = 0.0
                for vod in attr.getVOD():
                  # Get the real factor of the master
                  f = self.getFactor(vod.getFigureName(), vod.getGroupName(), vod.getChannelName())
                  # Take into account the Control Ratio (deltaAddDelta)
                  finalFactor += f*vod.getControlRatio()

                # Deltas dltAttr = attr.getDeltas();
                finalFactor += attr.getKeysFactor(0)
                logging.info("Cleaning[%s] in %s f=%g", attr.getName(), po.getName(), finalFactor)
                attr.removeDeltas()
      else:
        ret = C_ERROR

    else: # pp should be a PoserProp
      if not pp: return C_ERROR
      
      for attr in pp.getChannels()._lstAttr:
        if attr.getPoserType()==PoserToken.E_targetGeom and GenericTransform.concerned(attr.getName(), setTargetMorph):
          finalFactor = 0.0
          for vod in attr.getVOD():
            # Get the real factor of the master
            f = self.getFactor(vod.getFigureName(), vod.getGroupName(), vod.getChannelName())
            # Take into account the Control Ratio (deltaAddDelta)
            cr = vod.getControlRatio()
            finalFactor += f * cr

          finalFactor += attr.getKeysFactor(0)

          # Remove the deltas but not the targetGeom
          logging.info("Cleaning[%s] in %s f=%g", pp.getName(), pp.getName(), finalFactor)
          attr.removeDeltas()

    return ret


  # Extract the geometries of a Figure, with or without taking into account the
  # applied morph.
  # 
  # @param poserRootDir
  #          Path to Poser install
  # @param bodyIdx
  #          Index of the figure
  # @param channelSet
  #          Channels to take into account. If null, no delta are applied.
  # @return The list of geometries that compose the figure.
  def extractAll(self, poserRootDir, bodyIdx, channelSet):
    lstgeom = None
    eg = None

    # Read OBJ filename
    body = self.getFigResFileGeom(bodyIdx, poserRootDir)
    if body and body.isValid():
      if channelSet:
        body.findApplyDelta(bodyIdx, self, channelSet)

      lstactors = self.getDescendant(bodyIdx)
      lstgeom = [ ]
      for pa in lstactors:
        # Check if the name of the actor vs the name of the meshed part
        #pa = self.findActor(pn)
        #if pa:
        if pa.getGeomType()==PoserConst.GT_GLOBAL_OBJFILE:
          # geomHandlerGeom 13 hip
          eg = body.extractSortGeom(pa.getGeomGroupName(), pa.getGeomType())

        elif pa.getGeomType()==PoserConst.GT_LOCAL_OBJFILE:
          # objFileGeom 0 0 :Runtime:Geometries:Marforno:Elaya:Lamp.obj          
          eg = GeomCustom(getRealPath(poserRootDir, pa.getGeomFileName()))

        #elif pa.getGeomType()==PoserConst.GT_NONE:
        #elif pa.getGeomType()==PoserConst.GT_INTERNAL:
        else:
          eg = None

        if eg:
          eg.setName(pa.getName())
          lstgeom.append(eg)

    return lstgeom

  # Calculate the impact of a channel deletion. (Not recursive search)
  # The first item is the concerned channel.
  # @param channel
  def deleteChannelImpact(self, channel):
    implst = [ channel, ]
    for f in self.getLstFigure():
      for pa in f.getActors():
        pa.getChannelDescendant(channel, implst)
      for pp in f.getProps():
        pp.getChannelDescendant(channel, implst)
    for pp in self.getLstProp():
      pp.getChannelDescendant(channel, implst)
    return implst

  # Calculate the list of channels that reference at any level the given channel. (recursive search)
  # @param channel
  def calcChannelDesc(self, channel):
    implst = [ ]
    l = self.deleteChannelImpact(channel)
    del l[0]
    for gt in l:
      if not gt in implst:
        implst.append(gt)
        lstsub = self.calcChannelDesc(gt)
        for gt2 in lstsub:
          if not gt2 in implst:
            implst.append(gt2)

    return implst

  # Delete a channel in a PoserMeshedObject
  # @param fig
  #          Figure where is the channel (if the meshed object is an Actor)
  # @param lstImp
  #          Prepared impact list. If null will be calculated again.
  def deleteChannel(self, channel, lstImp):
    if lstImp == None:
      lstImp = self.deleteChannelImpact(channel)
    fci = lstImp.pop(0)
    pmo = fci.getPoserMeshedObject()
    pmo.deleteChannel(fci)
    for ci in lstImp:
      ci.deleteChannelRef(channel)


  def findMeshedObject(self, actorPropName):
    for fig in self._lstFigure:
      for a in fig.getActors() + fig.getProps():
        if actorPropName == a.getName():
          return a

    for pp in self._lstProp + self._lstLight + self._lstCamera:
      if actorPropName == pp.getName():
        return pp

    return None

  def deleteFigureImpact(self, fig):
    logging.error("Not implemented yet")
    return None

  def delete(self, obj):
    '''  Delete the given PoserProp or Figure from the list of general props '''
    res = C_OK
    if isinstance(obj, PoserProp):
      try:
        self._lstProp.remove(obj)
        propName = obj.getName()

        # Clean Figure Attributs : addChild and weld
        for po in self._doc.getLstAttr():
          if (po.getPoserType() == PoserToken.E_addActor) and (po.getValue()==propName):
            self._doc.getLstAttr().remove(po)

      except:
        res = C_FAIL
    elif isinstance(obj, Camera):
      try:
        self._lstCamera.remove(obj)
        propName = obj.getName()
        for po in self._doc.getLstAttr():
          if (po.getPoserType() == PoserToken.E_addCamera) and (po.getValue()==propName):
            self._doc.getLstAttr().remove(po)

        # Relink Lights, if the parent of the deleted camera was not "UNIVERSE"
        if not obj.getParent() == PoserConst.C_UNIVERSE:
          for li in self._lstLight:
            sa = li.findAttribut(PoserToken.E_depthCamera)
            if sa and (sa.getValue() == propName):
              # What value to set?? instead : Name of the first Camera of the file
              sa.setValue(self._lstCamera[0].getName())
      except:
        res = C_FAIL

    elif isinstance(obj, Light):
      try:
        self._lstLight.remove(obj)
        propName = obj.getName()
        for po in self._doc.getLstAttr():
          if (po.getPoserType() == PoserToken.E_addLight) and (po.getValue()==propName):
            self._doc.getLstAttr().remove(po)

        # Check the 'parent' of each Camera and relikn if needed
        firstLight = self._lstLight[0]
        for cam in self._lstCamera:
          if cam.getParent() == propName:
            if firstLight == None:
              logging.warning("Camera[" + cam.getName() + "] can not be relinked (no more lights)")
            else:
              cam.setParent(firstLight.getName())
              logging.info("Camera[" + cam.getName() + "] relinked to " + firstLight.getName())
      except:
        res = C_FAIL

    elif isinstance(obj, Figure):
      try:
        self._lstFigure.remove(obj)
        fi = obj.getBodyIndex()
        lstprp = self.findAllMeshedObject()

        # Change any references in "ConformingTarget" of actors of other figures.
        # No more "conformingTarget" attributs.
        for pmo in lstprp:
          if index(pmo.getConformingTarget()) == fi:
            pmo.setConformingTarget(None)

          # Delete any references in channels of actors of other figures and Props
          for pgt in pmo.getChannels().getLstAttr():
            pgt.deleteFigureRef(obj)

      except:
        res = C_FAIL

    return res


  def findFigure(self, frf):
    for fig in self._lstFigure:
      if frf.getValue() == fig.getFigResFile().getValue():
        return fig
    return None

  def findActor(self, actorName):
    for fig in self._lstFigure:
      for act in fig.getActors():
        if act.getName() == actorName:
          return act
    return None

  # Return the ancestors channel list of the channel given by channelName in
  # groupName actor.
  # 
  # @param figureName
  #          Unused because of welknown CrossWalk problems
  # @param groupName
  # @param channelName
  # @return The list of GenericTransform
  def getChannelAncestor(self, figureName, groupName, channelName):
    lstact = self.findAllMeshedObject(groupName)
    reslst = [ ]
    if lstact and (len(lstact)==1):
      po = lstact[0]
      
      for attr in po.getChannels().getLstAttr():
        if attr.getName() == channelName:
          reslst.append(attr)
          # Get Recursively controlling channels
          for vod in attr.getVOD():
            # Get other ancestors of the master
            sublst = self.getChannelAncestor(vod.getFigureName(), vod.getGroupName(), vod.getChannelName())
            # Add new found ancestors channels
            for agt in sublst:
              if not agt in reslst:
                reslst.append(agt)

          return reslst

    logging.warning(figureName + "." + groupName + " Not Found")
    return reslst

  # Change the name of referenced part (actor, prop, hairProp, controlProp)  
  # @param oldPartName
  # @param newPartName
  def changeReference(self, oldPartName, newPartName):
    for fig in self._lstFigure + self._lstProp:
      fig.changeReference(oldPartName, newPartName)

