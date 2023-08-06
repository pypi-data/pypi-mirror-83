### IMPORTS             ###
    ## Dependencies         ##
import getFN
    ## Dependencies         ##
import os
import sys
import re
### IMPORTS             ###
### CONSTANTS           ###
EXTS = ('nt', 'note')
TAB = '    '    # 4 spaces
EOF = 'EOF'
    ## Modes                ###
READ, WRITE, APPEND = 'r', 'w', 'a' # regs
READP, WRITEP, APPENDP = 'r+', 'w+', 'a+' # regs+
RAW_BIN = 'rb' # raw binary
    ## Modes                ###
    ## FORMATS_             ###
WITH = 'WITH'   # context management
DICT = 'DICT'   # loads/dictionary
FORMAT_ = (WITH, DICT)
    ## FORMATS_             ###
### CONSTANTS           ###
### EXCEPTIONS          ###
class FileExtensionError(Exception):
    """
    Raised when an invalid file extension is given when not expected
    """
    def __init__(self, ext): super().__init__(
        f"\n{ext} is an invalid file extension\nValid file extensions: {EXTS}"
    )
class OptionError(Exception):
    """
    Raised when an invalid option is given when not expected
    """
    def __init__(self, opt): super().__init__(
        f"\n{opt} is an invalid option\nValid options: {FORMATS_}"
    )
### EXCEPTIONS          ###
### UTILITY             ###
### UTILITY             ###
### RESULT              ###
class _Result(object):
    """
    DO NOT DISTURB AND/OR IMPORT
    """
    def __init__(self, fn: "File Name", ext: "File Extension"):
        self.fn, self.ext = (fn, ext)       # fn, ext tuple pair
    def __enter__(self):
        self.file = open(self.fn, READ)         # open file
        self.result = self.parse(self.file)   # parse the file & setattr for the parse res
        return self
    def __exit__(self, *argz: "Args to get the exception vals"):
        self.file.close()   # close file

    @staticmethod
    def omit_colon(name): return "".join(
        [char if index < (len(name) - 1) else "" for index, char in enumerate(name)]
    )
        #   list comp to get a list of chars and then checks if it is not last char
        #   if the char is the last then append an empty str instead and then join list to a str

    @staticmethod   # static for use outside of class
    def parse(file_):
        content = file_.read()     # read the contents of the file
        file_.seek(0, os.SEEK_SET)      # reset seeker/pointer
        content = content.splitlines()      # split the lines of content
        content.append(EOF)                 # add an EOF that can be hit
        keys, values = [], []   # create two seperate lists to hold keys and values
        make_note = False        # bool for making note
        current_note = []
        for ln_index, ln in enumerate(content):     # enumerate lines of the file
            
            if make_note:
                global TAB      # get access to globVar "TAB": str of val "    " == (" " * 4)
                if re.search("    ", ln): current_note.append(ln.strip()) # append ln
                else: values.append(current_note)
                continue    # skip over redundant check

            # use a regex-search to find start of note
            if re.search("\s*[A-Za-z0-9]+:", ln): # zero or more whitespace letters+digits colon
                keys.append(_Result.omit_colon(ln))
                make_note, current_note = True, []
        parsed_res = {k:v for (k, v) in zip(keys, values)}
        return parsed_res
### RESULT              ###
### MAIN FUNCS          ###
def parse(file_name: str, format_: str=WITH) -> dict:
    f"""
    Parsing file loader used to read from a Note file {EXTS}
    """
    ## Calcs                ##
    ext = getFN.get_file_ext(fn=file_name)
    ## Calcs                ##
    ## Error Check          ##
    if ext not in EXTS: raise FileExtensionError(ext)
    ## Error Check          ##
    if format_ == WITH: return _Result(file_name, ext)
    elif format_ == DICT:
        with open(file_name, READ) as f: res = _Result.parse(f)
        return res
    raise OptionError(format_)
### MAIN FUNCS          ###