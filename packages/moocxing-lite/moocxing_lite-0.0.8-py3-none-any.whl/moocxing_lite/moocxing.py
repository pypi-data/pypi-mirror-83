class MOOCXING():
    def __init__(self):
        pass

    def initMedia(self):
        from .MXMedia import MXMedia
        return MXMedia()

    def initThread(self):
        from .MXThread import MXThread
        return MXThread()

    def initSpeech(self, APP_ID, API_KEY, SECRET_KEY):
        from .MXSpeech import MXSpeech
        return MXSpeech(APP_ID, API_KEY, SECRET_KEY)

    def initNLP(self, APP_ID, API_KEY, SECRET_KEY):
        from .MXNLP import MXNLP
        return MXNLP(APP_ID, API_KEY, SECRET_KEY)

    def initMinecraft(self, address="localhost", port=4711):
        from mcpi.minecraft import Minecraft
        try:
            mc = Minecraft.create(address, port)
            print("*** 初始化Minecraft模块")
            return mc
        except:
            print("xxx 未检测到Minecraft服务器")

    def initMqtt(self, MQTTHOST="mqtt.16302.com", MQTTPORT=1883):
        from .MXMqtt import MXMqtt
        return MXMqtt(MQTTHOST, MQTTPORT)

    def initSerial(self, com=None, bps=9600):
        from .MXSerial import MXSerial
        try:
            if com == None:
                return MXSerial(MXSerial.getCom(-1), bps)
            else:
                return MXSerial(com, bps)
        except:
            print("xxx 未检测到串口")
