class MOOCXING():
    def __init__(self):
        pass

    def initMedia(self):
        from .MXMedia import MXMedia
        return MXMedia()

    def initSpeech(self, APP_ID, API_KEY, SECRET_KEY):
        from .MXSpeech import MXSpeech
        return MXSpeech(APP_ID, API_KEY, SECRET_KEY)

    def initNLP(self, APP_ID, API_KEY, SECRET_KEY):
        from .MXNLP import MXNLP
        return MXNLP(APP_ID, API_KEY, SECRET_KEY)

    def initMinecraft(self, address="localhost", port=4711):
        from .MXMinecraft import Minecraft
        return Minecraft.create(address, port)

    def initMqtt(self, MQTTHOST="mqtt.16302.com", MQTTPORT=1883):
        from .MXMqtt import MXMqtt
        return MXMqtt(MQTTHOST, MQTTPORT)

    def initSerial(self, com=None, bps=9600):
        from .MXSerial import MXSerial
        if com == None:
            return MXSerial(MXSerial.getCom(-1), bps)
        else:
            return MXSerial(com, bps)
