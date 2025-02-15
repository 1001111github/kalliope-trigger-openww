# djm 2025/02
# 90% of this code is from Kalliope
# all can use

import time
import logging
import pyaudio
from threading import Thread, Event

from kalliope import Utils
from openww_runner import OpenWWRunner

logging.basicConfig()
logger = logging.getLogger("kalliope")

class HotwordDetector(Thread):
    """
    OpenWakeWord decoder to detect whether a keyword specified by `decoder_model`
    exists in a microphone input stream.

    :param keyword	: decoder model file path, a string or a list of strings
    """
    def __init__(self, keywords, detected_callback, inf_engine):                
        super(HotwordDetector, self).__init__()
        self.detected_callback = detected_callback
        self.keywords = keywords
        self.found_keyword = False
        self.paused_loop = False

        self.runner = OpenWWRunner( keywords=self.keywords,
                                    on_activation=self.activation,
                                    inf_engine=inf_engine
                                    )
        
        self.runner.start()

# sleep is to handle microphone locks
# edit /etc/pulse/default.pa to remove suspend on idle module

    def run(self):
        logger.debug("detecting...")
        while True:
            if not self.paused_loop:
                if self.found_keyword:
                    self.pause()                          # We start pausing it here, to avoid double activations
                    message = "[OpenWW] Keyword detected"
                    Utils.print_info(message)
                    logger.debug(message)
                    self.detected_callback()

            time.sleep(0.01)
        logger.debug("finished")


    def activation(self):
        self.found_keyword = True

    def pause(self):
        self.runner.pause()
        self.paused_loop = True

    def unpause(self):
        self.runner.play()
        self.paused_loop = False
        self.found_keyword = False
