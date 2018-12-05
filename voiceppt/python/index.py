from pyaudio import PyAudio, paInt16 
import numpy as np 
from datetime import datetime 
import wave
from aip import AipSpeech
from websocket import create_connection

# added by jxc 20180912 
'''
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
'''
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
    # 2017_think    
    # key_words = ['欢迎','哲学','轴心时代','知网','跟随策略','订阅','代码大会','场景','线下','激励','搜索','双轨','优势','安全','头脑风暴','踏实','收纳','预算','手作','写作','分类','语言学习','立法','模拟','指数化','产业基金','谢谢']
    key_words = ['欢迎','预算','个人学习','开发','投资','理论','政策','策略','品牌建设','语言','写作','分类','指数化','回顾','致敬','3d','产业','职业目录','谢谢']
    # add end by jxc 

    def savewav(self,filename):
        wf = wave.open(filename, 'wb') 
        wf.setnchannels(1) 
        wf.setsampwidth(2) 
        wf.setframerate(self.SAMPLING_RATE) 
        wf.writeframes(np.array(self.Voice_String).tostring()) 
        # wf.writeframes(self.Voice_String.decode())
        wf.close() 

    def recoder(self):
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
            # print('又回来了')
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
                    # print(result['result'])
                    ppt_send = ''
                    # 需要判断是否为空！
                    # ppt 区域，专门设置ppt需要的内容
                    if(result.get('result') == None ):
                        print(' get none ')
                        break
                    for item in self.key_words :
                        if item in result.get('result')[0]:
                            ppt_send = item
                            '''
                            if(item == '手作'):
                                ppt_send = 'diy'
                            elif(item == '订阅'):
                                ppt_send = 'RSS'
                            '''    
                            ws = create_connection("ws://127.0.0.1:9001")
                            ws.send(ppt_send)
                            ws.close()
                    
                        '''
                        # server.send_message_to_all('北京欢迎你')
                        ws = create_connection("ws://127.0.0.1:9001")
                        ws.send("Hello, PeKing! ")
                        ws.close()
                        '''
                    # modified end by jxc 
                    print("Recode a piece of  voice successfully! 1 ")
                    time_count = self.TIME_COUNT
                    return True   # modified by jxc 20180912 for loop again and again 
                    # return True
            if time_count==0: 
                if len(save_buffer)>0:
                    self.Voice_String = save_buffer
                    save_buffer = [] 
                    # added by jxc 20180913
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
                    # print(result['result'])
                    ppt_send = ''
                    # 需要判断是否为空！
                    # ppt 区域，专门设置ppt需要的内容
                    if(result.get('result') == None ):
                        print(' get none ')
                        break
                    for item in self.key_words :
                        if item in result.get('result')[0]:
                            ppt_send = item
                            '''
                            if(item == '手作'):
                                ppt_send = 'diy'
                            elif(item == '订阅'):
                                ppt_send = 'RSS'
                            '''    
                            ws = create_connection("ws://127.0.0.1:9001")
                            ws.send(ppt_send)
                            ws.close()
                    
                        '''
                        # server.send_message_to_all('北京欢迎你')
                        ws = create_connection("ws://127.0.0.1:9001")
                        ws.send("Hello, PeKing! ")
                        ws.close()
                        '''
                    
                    time_count = self.TIME_COUNT
                    # add end by jxc 
                    print("Recode a piece of  voice successfully! 2 ")
                    time_count = self.TIME_COUNT
                    return True
                else:
                    return True

if __name__ == "__main__":
    r = recoder()
    while True:
        r.recoder()
    # r.savewav("test.wav")  