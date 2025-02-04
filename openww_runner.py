# djm 2025 
# heavily based on Precise VOD trigger code
# Python 2 + 3
# Copyright 2019 Mycroft AI Inc.
#
# 90% is from the La;;iope Precise trigger
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

import atexit
import logging
import time
import datetime
from subprocess import PIPE, Popen
from threading import Thread, Event

from pyaudio import PyAudio, paInt16
import numpy as np

from openwakeword.model import Model

from kalliope.core.ConfigurationManager import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")

"""
class OpenWWRunner(object):
        keyword: trigger word sound file
        stream (BinaryIO): Binary audio stream to read 16000 Hz 1 channel int16
                           audio from. If not given, the microphone is used
        on_activation (Callable): callback for when the wake word is heard

Not Currently Used
        trigger_level (int): Number of chunk activations needed to trigger on_activation
                       Higher values add latency but reduce false positives
        sensitivity (float): From 0.0 to 1.0, how sensitive the network should be
        on_prediction (Callable): callback for every new prediction

Openwakeword options
            enable_speex_noise_suppression=args.noise_suppression,
            vad_threshold = args.vad_threshold,
            lots of others
Not used until v0.50 currently in python 3.11 :(
            inference_framework=inf_engine
            threshold 
"""
class OpenWWRunner(object):
    def __init__(self, keyword, inf_engine, stream=None, on_activation=lambda: None, ):
        self.keyword = keyword
        self.stream = stream
        self.on_activation = on_activation

# following load from settings ??
        self.chunk_size = 1280  # 1280 suggested as optimal for oww, 80ms  @16kHz = 16z * 80 = 1280
        self.threshold = 0.8    # high but works
        self.trigger_level = 3  # not used yet

        self.pa = None
        self.thread = None
        self.running = False
        self.is_paused = False
        self.owwModel = Model(wakeword_models=[keyword])
        logger.debug("[OpenWWRunner] Loaded wakeword model  : %s" % keyword)

        atexit.register(self.stop)

    def start(self):
        """Start listening from stream"""
        if self.stream is None:
            # audio file not set, we need to capture a sample from the microphone
            self.pa = PyAudio()
            self.stream = self.pa.open(
                16000, 1, paInt16, True, frames_per_buffer=self.chunk_size
            )
        self.running = True
        self.is_paused = False
        self.thread = Thread(target=self._handle_predictions, daemon=True)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop listening and close stream"""
        if self.thread:
            self.running = False
            self.thread.join()
            self.thread = None

        if self.pa:
            self.stream.stop_stream()
            self.stream.close()
            self.pa.terminate()
            self.stream = self.pa = None

    def pause(self):
        self.is_paused = True

    def play(self):
        self.is_paused = False

    def _handle_predictions(self):
        """Continuously check oww process output"""
        while self.running:
            chunk = self.stream.read(self.chunk_size)
            audio = np.frombuffer(chunk, dtype=np.int16)

            if self.is_paused:
                continue

            # assuption only one model
            model_name = next(iter(self.owwModel.models))
# need threshold for this
#            prediction = self.owwModel.predict(audio, patience={model_name, self.trigger_level})
            
            prediction = self.owwModel.predict(audio)
            for mdl in prediction.keys():
                if prediction[mdl] > self.threshold:
                    detect_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.debug(f'Detected activation from \"{mdl}\" model with time {detect_time}!')

                   # reset predictions, return to parent via callback
                    self.owwModel.reset()
                    self.on_activation()
