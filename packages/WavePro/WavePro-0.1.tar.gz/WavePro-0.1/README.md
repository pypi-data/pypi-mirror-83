这个程序的主要就包含了一个处理函数，即为

def WavPro(wav_data)

其中 wav_data 为语音数据

eg:
 wav_data, sr= librosa.load(wav_path, 16000)

其中的wav_data即为语音数据；wav_path是语音的路径

一些参考的参数如下：
CHUNK = 1000      # 每次处理1000帧这样的数据

FORMAT = pyaudio.paInt16   # 以16进制的方式打开音频文件

CHANNELS = 1  # 声道数

RATE = 16000  # 每秒提取16000帧的数据   采样率