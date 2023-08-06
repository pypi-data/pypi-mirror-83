# SPDX-License-Identifier: GPL-3.0-only
import logging

from multiprocessing import Process, Queue

import numpy as np
import pyaudio
import pyrubberband

# logging.basicConfig(level=logging.DEBUG)


class AudioPlayer:

    CHUNK_SIZE = 1024

    def __init__(self, device_id):
        self.cmd_queue = Queue()
        self.data_queue = Queue()
        self.status_queue = Queue()
        self.is_playing = False
        self._playback_time = 0
        self.effects_process = None
        self.play_process = None
        self.start_offset = 0
        self.playback_speed = 1.0
        self.device_id = device_id

    @ property
    def playback_time(self):
        self.drain_status_queue()
        return self._playback_time*self.playback_speed + self.start_offset

    def drain_status_queue(self):
        while not self.status_queue.empty():
            status_msg = self.status_queue.get()
            if "time" in status_msg:
                self._playback_time = status_msg["time"]

    def _recreate_queues(self):
        self.cmd_queue.close()
        self.data_queue.close()
        self.status_queue.close()
        self.cmd_queue = Queue()
        self.data_queue = Queue()
        self.status_queue = Queue()

    def play(self, signal, start_at, end_at, sampling_rate, playback_speed=1.0):
        if self.is_playing:
            # TODO raise expection
            return
        self._recreate_queues()
        self.is_playing = True
        self.start_offset = start_at
        self.playback_speed = playback_speed
        signal = signal[int(start_at*sampling_rate):int(end_at*sampling_rate)]
        self.effects_process = Process(target=effects_process_wrapper,
                                       args=(signal, self.data_queue),
                                       kwargs={
                                           "sampling_rate": sampling_rate,
                                           "playback_speed": playback_speed})

        if len(signal.shape) == 2 and signal.shape[1] == 2:
            nr_channels = 2
        else:
            nr_channels = 1
        self.play_process = Process(target=playback_process_wrapper,
                                    args=(self.cmd_queue, self.data_queue,
                                          self.status_queue, self.device_id,
                                          sampling_rate, nr_channels))
        print("Starting effects process")
        self.effects_process.start()
        self.play_process.start()

    def stop(self):
        logging.debug("Sending stop feedback message")
        self.cmd_queue.put("STOP")
        if self.effects_process is not None:
            self.effects_process.join()
            self.effects_process = None
        logging.debug("Effects process is stopped")
        if self.play_process is not None:
            self.play_process.join()
            self.play_process = None
        self.is_playing = False
        logging.info("Playback stopped")


def effects_process_wrapper(signal, data_queue, sampling_rate=44100,
                            playback_speed=1.0):
    # If signal is large, process a smaller chunk first
    if len(signal)//sampling_rate > 20:  # large means longer than 20s
        chunk = pyrubberband.time_stretch(
            signal[0:sampling_rate*20],
            rate=playback_speed, sr=sampling_rate).astype(np.float32)/2
        data_queue.put(chunk)
    whole = pyrubberband.time_stretch(signal, rate=playback_speed,
                                      sr=sampling_rate).astype(np.float32)/2
    data_queue.put(whole)


def playback_process_wrapper(cmd_queue, data_queue, status_queue,
                             device_id, sampling_rate, nr_channels):
    logging.info("playback started")
    time = 0
    pyaudio_obj = pyaudio.PyAudio()
    stream = pyaudio_obj.open(format=pyaudio.paFloat32,
                              channels=nr_channels,
                              rate=sampling_rate,
                              output_device_index=device_id,
                              output=True
                              )
    signal = []
    while True:
        while not data_queue.empty():
            signal = data_queue.get()
        if not cmd_queue.empty():
            cmd = cmd_queue.get()
            logging.debug(f"Received command: '{cmd}'")
            if cmd == "STOP":
                break
        if len(signal) > 0:
            chunk = signal[time:time+AudioPlayer.CHUNK_SIZE]
            stream.write(chunk.tobytes())
            time += AudioPlayer.CHUNK_SIZE
            status_queue.put({"time": time/sampling_rate})
            if time > len(signal):
                time = 0
    logging.debug("Closing stream")
    stream.close()
    logging.debug("Closed stream")
    pyaudio_obj.terminate()
    logging.debug("Pyaudio terminated")
