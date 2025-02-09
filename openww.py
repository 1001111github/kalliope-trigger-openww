# djm 2025
# 90% of this code is from Kalliope
# All can use

import logging
import os
import sys
from threading import Thread, Event

from kalliope import Utils 

from cffi import FFI as _FFI

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from openwwdecoder import HotwordDetector

class OpenWWModelNotFound(Exception):
    pass

class MissingParameterException(Exception):
    pass

logging.basicConfig()
logger = logging.getLogger("kalliope")

"""
High Level Wrapper class around a reader and hot word detector
-- Model and inference engine data are headed to the runner which does the work
-- Mostly parameter checking and state handling
"""
class Openww(Thread):
 
    def __init__(self, **kwargs):
        super(Openww, self).__init__()
        self._ignore_stderr()
        # pause listening boolean
        self.interrupted = False        

        # callback function to call when hotword caught
        self.callback = kwargs.get('callback', None)
        if self.callback is None:
            raise MissingParameterException("Callback function is required with OpenWW")
        
        #onnx as default, more support
        self.inf_engine = kwargs.get('engine', 'onnx')
        if self.inf_engine is None:
            raise MissingParameterException("Inference engine is required with OpenWW")

        keyword = kwargs.get('model_file', None)
        if keyword is None:
            raise MissingParameterException("Wake word file is required with OpenWW")
	
        self.model_list = keyword.split(",")
        for mdl in self.model_list:
            try:
                os.path.isfile(Utils.get_real_file_path(mdl))
            except TypeError: 
                raise OpenWWModelNotFound("OpenWW wake word file %s does not exist" % mdl)
        
        self.detector = HotwordDetector(keywords=self.model_list,
                                        detected_callback=self.callback,
					inf_engine=self.inf_engine,
                                        )

    def run(self):
        """
        Start the OpenWW thread and wait for a Kalliope trigger word
        :return:
        """
        # start OpenWW loop forever
        self.detector.daemon = True
        self.detector.start()
        self.detector.join()

    def pause(self):
        """
        pause the OpenWW main thread
        """
        logger.debug("Pausing OpenWW process")
        self.detector.pause()

    def unpause(self):
        """
        unpause the OpenWW main thread
        """
        logger.debug("Unpausing OpenWW process")
        self.detector.unpause()

    @staticmethod
    def _ignore_stderr():
        """
        Try to forward PortAudio messages from stderr to /dev/null.
        """
        ffi = _FFI()
        ffi.cdef("""
            /* from stdio.h */
            extern FILE* fopen(const char* path, const char* mode);
            extern int fclose(FILE* fp);
            extern FILE* stderr;  /* GNU C library */
            extern FILE* __stderrp;  /* Mac OS X */
            """)
        stdio = ffi.dlopen(None)
        devnull = stdio.fopen(os.devnull.encode(), b'w')
        try:
            stdio.stderr = devnull
        except KeyError:
            try:
                stdio.__stderrp = devnull
            except KeyError:
                stdio.fclose(devnull)
