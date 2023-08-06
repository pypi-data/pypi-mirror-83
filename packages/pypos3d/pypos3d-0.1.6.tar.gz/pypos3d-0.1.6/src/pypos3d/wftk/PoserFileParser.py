# -*- coding: utf-8 -*-
#package pypos3d.wftk
import sys
import os
from .WFBasic import Point3d, Vector3d, TexCoord2f

class ParsingErrorException(RuntimeError):
  def __init__(self, s=''):
    super(ParsingErrorException, self).__init__(s)


# File types
OBJ_FNAT, PZ3_FNAT, CR2_FNAT = 0,1,2

class PoserFileParser(object):
  ''' Generic OBJ and Poser file parser.
  Derivated from the Java StreamTokenizer
  '''
  TRACER = False

  CT_WHITESPACE = 1
  CT_DIGIT = 2
  CT_ALPHA = 4
  CT_QUOTE = 8
  CT_COMMENT = 16

  NEED_CHAR = sys.maxsize
  SKIP_LF = sys.maxsize - 1

  #  A constant indicating that the end of the stream has been read.
  TT_EOF = -1

  #  A constant indicating that the end of the line has been read.
  TT_EOL = ord('\n')
  TT_CR  = ord('\r')
  TT_QUOTE = '"'

  #  A constant indicating that a number token has been read.
  TT_NUMBER = -2

  #  A constant indicating that a word token has been read.
  TT_WORD = -3

  #  A constant indicating that no token has been read, used for
  #  initializing ttype.  
  TT_NOTHING = -4

  # If the current token is a word token, this field contains a
  # string giving the characters of the word token. When the current
  # token is a quoted string token, this field contains the body of
  # the string.
  # The current token is a word when the value of the
  # <code>ttype</code> field is <code>PoserFileParser.TT_WORD</code>. The current token is
  # a quoted string token when the value of the <code>ttype</code> field is
  # a quote character.
  #  The initial value of this field is null.
  BACKSLASH = ord('\\')
  ZERO = ord('0')
  ONE = ord('1')
  NINE = ord('9')
  QUOTE = ord('"')
  SPACE = ord(' ')
  MINUS = ord('-')
  DOT = ord('.')


  '''
   * Specifies that all characters <i>c</i> in the range
   * <code>low&nbsp;&lt;=&nbsp;<i>c</i>&nbsp;&lt;=&nbsp;high</code>
   * are white space characters. White space characters serve only to
   * separate tokens in the input stream.
   *
   * <p>Any other attribute settings for the characters in the specified
   * range are cleared.
   *
   * @param   low   the low end of the range.
   * @param   hi    the high end of the range.
   public void whitespaceChars(int low, int hi)
  '''
  def whitespaceChars(self, low, hi):
    low = ord(low)
    hi = ord(hi)
    if (low < 0):
      low = 0
    if hi >= len(self.ctype):
      hi = len(self.ctype) - 1
    while (low <= hi):
      self.ctype[low] = PoserFileParser.CT_WHITESPACE
      low+= 1

  '''
   * Specifies that all characters <i>c</i> in the range
   * <code>low&nbsp;&lt;=&nbsp;<i>c</i>&nbsp;&lt;=&nbsp;high</code>
   * are "ordinary" in this tokenizer. See the
   * <code>ordinaryChar</code> method for more information on a
   * character being ordinary.
   *
   * @param   low   the low end of the range.
   * @param   hi    the high end of the range.
   * @see     java.io.StreamTokenizer#ordinaryChar(int)
  public void ordinaryChars(int low, int hi)
  '''
  def ordinaryChars(self, low, hi):
    low = ord(low)
    hi = ord(hi)
    if (low < 0):
      low = 0
    if hi >= len(self.ctype):
      hi = len(self.ctype) - 1
    while (low <= hi):
      self.ctype[low] = 0
      low+= 1

  '''
   * Specifies that the character argument is "ordinary"
   * in this tokenizer. It removes any special significance the
   * character has as a comment character, word component, string
   * delimiter, white space, or number character. When such a character
   * is encountered by the parser, the parser treates it as a
   * single-character token and sets <code>ttype</code> field to the
   * character value.
   *
   * @param   ch   the character.
   * @see     java.io.StreamTokenizer#ttype
  public void ordinaryChar(int ch)
  '''
  def ordinaryChar(self, ch):
    ch = ord(ch)
    if (ch >= 0 and ch < len(self.ctype)):
      self.ctype[ch] = 0

  '''
   * Specifies that all characters <i>c</i> in the range
   * <code>low&nbsp;&lt;=&nbsp;<i>c</i>&nbsp;&lt;=&nbsp;high</code>
   * are word constituents. A word token consists of a word constituent
   * followed by zero or more word constituents or number constituents.
   *
   * @param   low   the low end of the range.
   * @param   hi    the high end of the range.
  public void wordChars(int low, int hi)
  '''
  def wordChars(self, low, hi):
    low = ord(low)
    hi = ord(hi)
    if (low < 0):
      low = 0
    if hi >= len(self.ctype):
      hi = len(self.ctype) - 1
    while (low <= hi):
      self.ctype[low] |= PoserFileParser.CT_ALPHA
      low+= 1


  '''
   * Specified that the character argument starts a single-line
   * comment. All characters from the comment character to the end of
   * the line are ignored by this stream tokenizer.
   *
   * <p>Any other attribute settings for the specified character are cleared.
   *
   * @param   ch   the character.
  def commentChar(self, ch):
  '''
  def commentChar(self, ch):
    ch = ord(ch)
    if (ch >= 0 and ch < len(self.ctype)):
      self.ctype[ch] = PoserFileParser.CT_COMMENT

  '''
   * Specifies that matching pairs of this character delimit string
   * constants in this tokenizer.
   * <p>
   * When the <code>self.nextToken</code> method encounters a string
   * constant, the <code>ttype</code> field is set to the string
   * delimiter and the <code>sval</code> field is set to the body of
   * the string.
   * <p>
   * If a string quote character is encountered, then a string is
   * recognized, consisting of all characters after (but not including)
   * the string quote character, up to (but not including) the next
   * occurrence of that same string quote character, or a line
   * terminator, or end of file. The usual escape sequences such as
   * <code>"&#92;n"</code> and <code>"&#92;t"</code> are recognized and
   * converted to single characters as the string is parsed.
   *
   * <p>Any other attribute settings for the specified character are cleared.
   *
  public void quoteChar(int ch)
  '''
  def quoteChar(self, ch):
    ch = ord(ch)
    if (ch >= 0 and ch < len(self.ctype)):
      self.ctype[ch] = PoserFileParser.CT_QUOTE

  '''
  Sets up StreamTokenizer for reading ViewPoint .obj file format.
  void setup()
  '''
  def setup(self):
    # for (int i = ctype.length; --i >= 0;)
    # ctype[i] = 0

    # All printable ascii characters
    self.wordChars('!', '~')

    # Comment from ! to end of line
    # For Poser file : Avoid that        commentChar('!')
    self.commentChar('#')

    self.whitespaceChars(' ', ' ')
    self.whitespaceChars('\n', '\n')
    self.whitespaceChars('\r', '\r')
    self.whitespaceChars('\t', '\t')

    # These characters returned as tokens
    self.ordinaryChar('/')
    # ordinaryChar(BACKSLASH)

    self.quoteChar('"')
    # End of setup

  def __init__(self, reader, ftype = PZ3_FNAT):
    ''' PoserFileParser constructor
    Parameters
    ----------
    r : input file reader
    ftype : int
      Real File Nature [PZ3, CR2, OBJ]
    '''
    if not reader:
      raise Exception()
    
    # Use a hugh buffer to avoid any resize
    self.buf = [chr(0)] * 4096
    self.pushedBack = False

    # The line number of the last token read
    self.LINENO = 1

    # The next character to be considered by the self.nextToken method.  May also
    # be NEED_CHAR to indicate that a new character should be read, or SKIP_LF
    # to indicate that a new character should be read and, if it is a '\n'
    # character, it should be discarded and a second new character should be
    # read.
    self.peekc = PoserFileParser.NEED_CHAR
    self.ctype = [0] * 256

    # If the current token is a number, this field contains the value
    # of that number. The current token is a number when the value of
    # the <code>ttype</code> field is <code>PoserFileParser.TT_NUMBER</code>.
    # The initial value of this field is 0.0.
    self.nval = 0.0
    self.sval = None
    self.ttype = PoserFileParser.TT_NOTHING
    self.reader = reader

    self._FileNature = ftype
    # Just to store customer version
    self._FileVersion = None

    self.setup()


  def getToken(self):   # throws ParsingErrorException
    ''' Gets the next token from the stream.
    Puts one of the four constants (PoserFileParser.TT_WORD, PoserFileParser.TT_NUMBER, 
    PoserFileParser.TT_EOL, or PoserFileParser.TT_EOF) or the token value
    for single character tokens into ttype.  Handles backslash continuation of lines.
    '''
    t = 0
    try:
      t = self.nextToken()
      if (t == PoserFileParser.BACKSLASH):
        self.sval = PoserFileParser.BACKSLASH
      elif (t == PoserFileParser.QUOTE):
          self.sval = "\"" + self.sval + "\""
    except IOError as e:
      raise ParsingErrorException("IO error on line " + str(self.lineno()) + ": " + e.strerror)

  def isLeftBracket(self):
    return (self.ttype == PoserFileParser.TT_WORD) and (self.sval=="{")

  def isRightBracket(self):
    return ((self.ttype == PoserFileParser.TT_WORD) and (self.sval=="}"))

  # Skips all tokens on the rest of this line.  Doesn't do anything if
  # We're already at the end of a line
  def skipToNextLine(self): # throws ParsingErrorException
    if PoserFileParser.TRACER: print("skipToNextLine:"  + str(self.LINENO))
    while ((self.ttype != PoserFileParser.TT_EOL) and (self.ttype != PoserFileParser.TT_EOF)):
      self.getToken()

  # Get all tokens on the rest of this line.  Doesn't do anything if
  # We're already at the end of a line
  def getToNextLine(self): # throws ParsingErrorException
    if PoserFileParser.TRACER: print("getToNextLine:"  + str(self.LINENO))
    try:
      s=b''

      if self.pushedBack:
        self.pushedBack = False
        return self.sval
      
      ct = self.ctype
      self.sval = None

      c = self.peekc
      if c < 0:
        c = PoserFileParser.NEED_CHAR
      elif (c == PoserFileParser.SKIP_LF):
        # c = self.read()
        s = self.reader.read(1)
        if s:
          c = s[0]
        else: # (c < 0):
          self.ttype = PoserFileParser.TT_EOF
          return self.sval

        if (c == PoserFileParser.TT_EOL):
          c = PoserFileParser.NEED_CHAR

      if (c == PoserFileParser.NEED_CHAR):
        #c = self.read()
        s = self.reader.read(1)
        if s:
          c = s[0]
        else: # (c < 0):
          self.ttype = PoserFileParser.TT_EOF
          return self.sval
        
      self.ttype = c # // Just to be safe 

      self.peekc = PoserFileParser.NEED_CHAR

      nctype = ct[c] if c < 256 else PoserFileParser.CT_ALPHA
      while nctype & PoserFileParser.CT_WHITESPACE:
        if c == PoserFileParser.TT_CR:
          self.LINENO+=1
          self.peekc = PoserFileParser.SKIP_LF
          self.ttype = PoserFileParser.TT_EOL
          return self.sval
        else:
          if c == PoserFileParser.TT_EOL:
            self.LINENO+=1
            self.ttype = PoserFileParser.TT_EOL
            return self.sval
            
          # c = self.read()
          s = self.reader.read(1)
          c = s[0] if s else PoserFileParser.TT_EOF
          
        if (c < 0):
          self.ttype = PoserFileParser.TT_EOF
          return self.sval
          
        nctype = ct[c] if c < 256 else PoserFileParser.CT_ALPHA

      if c >= PoserFileParser.SPACE:
        # i = 0
        locs = ''
        while (c >= 0) and (c!=PoserFileParser.TT_EOL) and (c!=PoserFileParser.TT_CR):
          locs += chr(s[0])
          # i+=1
          s = self.reader.read(1)
          if s:
            c = s[0]
          else:
            c = PoserFileParser.TT_EOF
            break

        self.peekc = c
        self.sval = locs # ''.join(self.buf[0:i])

        self.ttype = PoserFileParser.TT_EOL if ((self.sval=="") or (self.sval=="null")) else PoserFileParser.TT_WORD

        if (self.ttype == PoserFileParser.TT_WORD):
          self.peekc = PoserFileParser.SKIP_LF

    except IOError as ioex:
      print( 'IOError:' + ioex.strerror )

    return self.sval

  #    get all tokens on the rest of this line.  Doesn't do anything if
  #    We're already at the end of a line.
  #    Return True if the first printable char is "1"
  # public boolean getBoolToNextLine() throws ParsingErrorException
  def getBoolToNextLine(self): # throws ParsingErrorException
    if PoserFileParser.TRACER: print("getBoolToNextLine:"  + str(self.LINENO))
    res = False

    try:
      if (self.pushedBack):
        self.pushedBack = False
        return self.sval[0] == "1"
        
      ct = self.ctype
      self.sval = None

      c = self.peekc
      nctype = ct[c] if c < 256 else PoserFileParser.CT_ALPHA
      while nctype & PoserFileParser.CT_WHITESPACE:
        s = self.reader.read(1)
        if s:
          c = s[0]
          nctype = ct[c] if c < 256 else PoserFileParser.CT_ALPHA
        else: # (c < 0):
          self.ttype = PoserFileParser.TT_EOF
          raise ParsingErrorException("Unexpected (EOF) Boolean on line " + str(self.lineno()))

      res = (c == PoserFileParser.ONE)
      if (c != PoserFileParser.ZERO) and (not res):
        raise ParsingErrorException("UnExpected (chars) Boolean on line " + str(self.lineno()))

    except IOError as ioex:
      #ioex.printStackTrace()
      print ('IOError:' + ioex.strerror)

    return res
    #} // end of getToNextLine


  #	Gets a number from the stream.  Note that we don't recognize
  #	numbers in the tokenizer automatically because numbers might be in
  #	scientific notation, which isn't processed correctly by 
  #	StreamTokenizer.  The number is returned in self.nval.
  def getNumber(self):
    try:
      self.getToken()
      if (self.ttype != PoserFileParser.TT_WORD):
        raise ParsingErrorException("Expected number on line " + str(self.lineno()))

      self.nval = float(self.sval)
      return self.nval
    
    except ValueError as e:  
      raise ParsingErrorException(e.msg)


  def nextToken(self):
    ''' Parses the next token from the input stream of this tokenizer.
    The type of the next token is returned in the <code>self.ttype</code>
    field. Additional information about the token may be in the
    self.nval field or the self.sval field of this tokenizer.

    Typical clients of this class first set up the syntax tables and then sit in a loop
    calling self.nextToken to parse successive tokens until PoserFileParser.TT_EOF
    is returned.
    
    Returns
    int
      the value of the self.ttype field.
    '''
    if self.pushedBack:
      self.pushedBack = False
      return self.ttype
      
    ct = self.ctype
    self.sval = None
    s = ''

    c = self.peekc
    if (c < 0):
      c = PoserFileParser.NEED_CHAR
    elif (c == PoserFileParser.SKIP_LF):
      s = self.reader.read(1)
      if s:
        c = s[0]
      else: # (c < 0):
        self.ttype = PoserFileParser.TT_EOF
        return self.ttype 

      if (c == PoserFileParser.TT_EOL):
        c = PoserFileParser.NEED_CHAR
     
    if c == PoserFileParser.NEED_CHAR:
      #c = self.read()
      s = self.reader.read(1)
      if s:
        c = s[0]
      else: # (c < 0):
        self.ttype = PoserFileParser.TT_EOF
        return self.ttype 
      
    self.ttype = c # /* Just to be safe */

    # Set self.peekc so that the next invocation of self.nextToken will read
    #  another character unless self.peekc is reset in this invocation
    self.peekc = PoserFileParser.NEED_CHAR

    nctype = ct[c] if c < 256 else PoserFileParser.CT_ALPHA
    while nctype & PoserFileParser.CT_WHITESPACE:
      if (c == PoserFileParser.TT_CR):
        self.LINENO+=1
        self.peekc = PoserFileParser.SKIP_LF
        self.ttype = PoserFileParser.TT_EOL
        return self.ttype 
      elif (c == PoserFileParser.TT_EOL):
        self.LINENO+=1
        self.ttype = PoserFileParser.TT_EOL
        return self.ttype 
          
      s = self.reader.read(1)
      if s:
        c = s[0]
        nctype = ct[c] if c < 256 else PoserFileParser.CT_ALPHA
      else: # (c < 0):
        self.ttype = PoserFileParser.TT_EOF
        return self.ttype 

    if nctype & PoserFileParser.CT_DIGIT:
      neg = False
      if c == PoserFileParser.MINUS:
        s = self.reader.read(1)
        if s and not s.isdecimal():
          self.peekc = s[0] if s else 0
          self.ttype = PoserFileParser.MINUS
          return self.ttype 
        else:
          c = s[0]
          
        neg = True
        
      v = 0.0
      decexp = 0
      seendot = 0

      while s.isdecimal():
        if s[0]=='.' and (seendot==0):
          seendot = False
        else:
          v = v * 10 + int(s[0]) - PoserFileParser.ZERO
          decexp += seendot
        s = self.reader.read(1)
        
      self.peekc = s[0]
      if decexp != 0:
        denom = 10.0
        decexp-=1
        while (decexp > 0):
          denom *= 10.0
          decexp-=1
          
        # Do one division of a likely-to-be-more-accurate number */
        v = v / denom
        
      self.nval = -v if neg else v
      self.ttype = PoserFileParser.TT_NUMBER
      return self.ttype 
      

    if nctype & PoserFileParser.CT_ALPHA:
      #c = s[0]
      #nctype = PoserFileParser.CT_WHITESPACE if (c < 0) else (ct[c] if c < 256 else PoserFileParser.CT_ALPHA)
      locs=''
      while nctype & (PoserFileParser.CT_ALPHA | PoserFileParser.CT_DIGIT):
        locs+=chr(s[0])
        s = self.reader.read(1)
        if s:
          c = s[0]
          nctype = PoserFileParser.CT_WHITESPACE if (c < 0) else (ct[c] if c < 256 else PoserFileParser.CT_ALPHA)
        else:
          c = PoserFileParser.TT_EOF
          break

      self.peekc = c
      self.sval = locs
      self.ttype = PoserFileParser.TT_WORD
      return self.ttype 

    if nctype & PoserFileParser.CT_QUOTE:
      self.ttype = c
      # Invariants (because \Octal needs a lookahead):
      #    (i)  c contains char value
      #    (ii) d contains the lookahead
      #d = self.read()
      locs=''
      s = self.reader.read(1)
      while s and s[0]!=PoserFileParser.TT_QUOTE and s[0]!=PoserFileParser.TT_EOL and s[0]!=PoserFileParser.TT_CR:
        c = s[0]
        s = self.reader.read(1)
        locs += c

      # If we broke out of the loop because we found a matching quote
      #  character then arrange to read a new character next time
      #  around; otherwise, save the character.
      self.peekc = PoserFileParser.NEED_CHAR if (s[0]==PoserFileParser.TT_QUOTE) else s[0]
      self.sval = locs
      return self.ttype

    if nctype & PoserFileParser.CT_COMMENT:
      s = self.reader.read(1)
      while s and (s[0] != PoserFileParser.TT_EOL and s[0] != PoserFileParser.TT_CR):
        s = self.reader.read(1)
        
      self.peekc = s[0] if s else PoserFileParser.TT_EOF
      return self.nextToken()

    self.ttype = c
    return self.ttype 

  def pushBack(self):
    ''' Causes the next call to the self.nextToken method of this
    tokenizer to return the current value in the self.ttype
    field, and not to modify the value in the self.nval or self.sval field.
    '''
    if (self.ttype != PoserFileParser.TT_NOTHING): # /* No-op if self.nextToken() not called */
      self.pushedBack = True

  def lineno(self):
    '''  Return the current line number. '''
    return self.LINENO

  def readVertex(self): # throws ParsingErrorException
    ''' Read a Vertex : three consecutive floats '''
    try:
      p = Point3d( self.getNumber(), self.getNumber(), self.getNumber())

    except ParsingErrorException as pex:
      # Raise added on 20201013 (TBC)
      raise(Exception("Parsing Error in line:"+str(self.LINENO)))

    self.skipToNextLine()
    return p

  def readTexture(self): # throws ParsingErrorException
    ''' Read a Texture : two consecutive float'''
    try:
      p = TexCoord2f(self.getNumber(), self.getNumber())

    except ParsingErrorException as pex:
      raise(Exception("Parsing Error in line:"+str(self.LINENO)))

    self.skipToNextLine()
    return p

  def readNormal(self): # throws ParsingErrorException
    ''' Read a Normal : three consecutive floats '''
    try:
      p = Vector3d(self.getNumber(), self.getNumber(), self.getNumber())

    except ParsingErrorException as pex:
      raise(Exception("Parsing Error in line:"+str(self.LINENO)))

    self.skipToNextLine()
    return p

  def getFileNature(self):
    return self._FileNature

  def getFileVersion(self):
    return self._FileVersion

  def setFileVersion(self, v):
    self._FileVersion = o


