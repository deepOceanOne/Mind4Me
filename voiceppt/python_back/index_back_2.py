from pyaudio import PyAudio, paInt16 
import numpy as np 
from datetime import datetime 
import wave
from aip import AipSpeech

# added by jxc 20180912 

from websocket_server import WebsocketServer                                    
     # 当新的客户端连接时会提示                                                                        
    # Called for every client connecting (after handshake)                          
def new_client(client, server):                                                 
        print("New client connected and was given id %d" % client['id'])        
        server.send_message_to_all("Hey all, a new client has joined us")          
                                                                                                                                                 
# Called for every client disconnecting                                         
def client_left(client, server):                                                
        print("Client(%d) disconnected" % client['id'])                         
                                                                                                                                                        
# Called when a client sends a message                                          
def message_received(client, server, message):                                  
        if len(message) > 200:                                                  
                message = message[:200]+'..'                                    
        print("Client(%d) said: %s" % (client['id'], message))                  

# added end by jxc                                                                                 
                                                                                




class recoder:
    NUM_SAMPLES = 2000      #pyaudio内置缓冲大小
    SAMPLING_RATE = 16000    #取样频率
    LEVEL = 500         #声音保存的阈值
    COUNT_NUM = 20      #NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
    SAVE_LENGTH = 8         #声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
    TIME_COUNT = 60     #录音时间，单位s

    Voice_String = []
    # add by jxc 20180912 
    BAIDU_APP_ID = '11798235'
    BAIDU_API_KEY = 'aL7V21ao41uZSNdwRzSfGYUi'
    BAIDU_SECRET_KEY = 'OxN8NixEoRo3rWUj1zVY3EI8Nmlrw6xj'
    # add end by jxc 

    def savewav(self,filename):
        wf = wave.open(filename, 'wb') 
        wf.setnchannels(1) 
        wf.setsampwidth(2) 
        wf.setframerate(self.SAMPLING_RATE) 
        wf.writeframes(np.array(self.Voice_String).tostring()) 
        # wf.writeframes(self.Voice_String.decode())
        wf.close() 

    def recoder(self,server):
        pa = PyAudio() 
        stream = pa.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE, input=True, 
            frames_per_buffer=self.NUM_SAMPLES) 
        save_count = 0 
        save_buffer = [] 
        time_count = self.TIME_COUNT

        while True:
            time_count -= 1
            # print time_count
            # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES) 
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于LEVEL的取样的个数
            large_sample_count = np.sum( audio_data > self.LEVEL )
            print(np.max(audio_data))
            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH 
            else: 
                save_count -= 1

            if save_count < 0:
                save_count = 0 

            if save_count > 0 : 
            # 将要保存的数据存放到save_buffer中
                #print  save_count > 0 and time_count >0
                save_buffer.append( string_audio_data ) 
            else: 
            #print save_buffer
            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                #print "debug"
                if len(save_buffer) > 0 : 
                    self.Voice_String = save_buffer
                    save_buffer = [] 
                    # modified by jxc 20180912
                    client = AipSpeech(self.BAIDU_APP_ID,self.BAIDU_API_KEY,self.BAIDU_SECRET_KEY)
                    voice_buffer = np.array(self.Voice_String).tostring()
                    result = client.asr(voice_buffer, 'wav', 16000, {
                         'dev_pid': 1936,
                    })
                    '''
                    1536    普通话(支持简单的英文识别)  搜索模型    无标点 支持自定义词库
                    1537    普通话(纯中文识别)  输入法模型   有标点 不支持自定义词库
                    1737    英语      有标点 不支持自定义词库
                    1637    粤语      有标点 不支持自定义词库
                    1837    四川话     有标点 不支持自定义词库
                    1936    普通话远场   远场模型    有标点 不支持
                    '''
                    print("hear : ")
                    print(result)
                    if "北京" in result :
                        server.send_message_to_all('北京欢迎你')
                    # modified end by jxc 
                    print("Recode a piece of  voice successfully!")
                    return False   # modified by jxc 20180912 for loop again and again 
                    # return True
            if time_count==0: 
                if len(save_buffer)>0:
                    self.Voice_String = save_buffer
                    save_buffer = [] 
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False

if __name__ == "__main__":
    PORT=9001                                                                       
    server = WebsocketServer(PORT, "0.0.0.0")                                       
    server.set_fn_new_client(new_client)                                            
    server.set_fn_client_left(client_left)                                          
    server.set_fn_message_received(message_received)                                
    server.run_forever()
    r = recoder(server)
    r.recoder()
    # r.savewav("test.wav")  