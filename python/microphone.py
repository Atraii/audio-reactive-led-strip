import queue
import numpy as np
import sounddevice as sd
import config
import time
q = queue.Queue()


def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(np.squeeze(indata))


def start_stream(callback):
    temp_fps = 0
    temp_fps_time = time.time()
    frames_per_buffer = int(config.MIC_RATE / config.FPS)

    stream = sd.InputStream(channels=1,
                            samplerate=config.MIC_RATE,
                            blocksize=frames_per_buffer,
                            dtype=np.float32,
                            callback=audio_callback,
                            device=12)

    with stream:
        while True:
            while True:
                try:
                    data = q.get_nowait()
                except queue.Empty:
                    break
                callback(data)
                temp_fps += 1
                if time.time() - temp_fps_time > 1:
                    temp_fps_time = time.time()
                    print('COOL FPS {:.0f} / {:.0f}'.format(temp_fps, config.FPS))
                    temp_fps = 0
