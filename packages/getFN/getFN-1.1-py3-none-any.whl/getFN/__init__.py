### IMPORTS     ###
import ntpath
### IMPORTS     ###
### GETFN FUNC  ###
def get_filename(path: str) -> str:
    """
    Returns the file name at the end of a path.
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
def get_file_ext(fn: str=None, path: str=None) -> str:
    """
    Returns the file extension from a path or filename
    """
    ## Constants    ##
    EXT_DELIMITER   = '.'
    NONE            = "None"
    ## Constants    ##
    ext = fn.split(
        EXT_DELIMITER   # ext delimiter i.e. what we split on
    ) if fn != None else get_filename(path) if path != None else FileNotFoundError(
        "fn and path arguments cannot both be None"     # error msg in the __init__ dunder
    )
        # fnne error        #
    if isinstance(ext, FileNotFoundError): raise ext
        # fnne error        #
        # check for no ext  #
    if (type(ext) == list) and (len(ext)) <= 1: return NONE
        # check for no ext  #
    return ext[-1]
### GETFN FUNC  ###