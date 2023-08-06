import threading
import wave
import pyaudio
from moocxing.package.MXThread import MXThread
print("*** 初始化录音播放模块")


class MXMedia():
    def __init__(self):
        self._stop = False  
        self._pause = False  
        self._isPlay = False  
        self.thread = MXThread()

        
    def record(self, fname="back.wav",rs=4):
        """录音"""
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = rs
        p1 = pyaudio.PyAudio()
        stream1 = p1.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        stream1.start_stream()
        print("* 开始录音<<<<<<")

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream1.read(CHUNK)
            frames.append(data)

        stream1.stop_stream()
        stream1.close()
        p1.terminate()

        wf1 = wave.open(fname, 'wb')
        wf1.setnchannels(CHANNELS)
        wf1.setsampwidth(p1.get_sample_size(FORMAT))
        wf1.setframerate(RATE)
        wf1.writeframes(b''.join(frames))
        wf1.close()
        print("* 结束录音<<<<<<")

    def play(self,fname="back.wav"):
        self._stop = False  
        self._pause = False  
        CHUNK = 1024
        wf = wave.open(fname,'rb')
        p = pyaudio.PyAudio()
        stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                input=False,
                output=True)

        stream.start_stream()
        data = wf.readframes(CHUNK)
        print("* 开始播放>>>>>>")
        
        self._isPlay = True 
        while data != b'' and not self._stop:
            if not self._pause:
                stream.write(data)
                data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()
        self._isPlay = False 

        print("* 结束播放>>>>>>")
    
    def playThread(self,fname="back.wav"):
        if not self.isPlay():
            self.thread._start(target=self.play, args=(fname,))

  
    def stop(self):
        self._stop = True
        print("退出")

    def pause(self):
        self._pause = True
        print("暂停")

    def go(self):
        self._pause = False
        print("继续")

    def isPlay(self):
        return self._isPlay 

   
    
