#A list of common functions used by various parts of the app

from consts import switches 
import consts.paths as paths

import datetime

def handle_err_msg(err_msg):
    globals = Globals()
    globals.handle_err_msg(err_msg)


class Globals(object):

    newline = "\n"
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Globals, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self): 
        now = datetime.datetime.now()
        self.timestamp = str(now.year) + "_" + str(now.month) + "_" + str(now.day)

    def write_err_msg_to_file(self, err_msg):
        err_msg_path = paths.ERR_MSG_PATH_DIR + paths.ERR_FILE_NAME + "_" + str(self.timestamp) + paths.ERR_FILE_EXTENSION
        with open(err_msg_path, "a") as errfile:
            errfile.write(err_msg)
            errfile.write(self.newline)

    def handle_err_msg(self, err_msg):
        if switches.WRITE_ERR_MSG_TO_FS:
            self.write_err_msg_to_file(err_msg) 

        if switches.PRINT_ERR_MSG_TO_SCREEN:
            print "Globals handle_err_msg : " + err_msg
