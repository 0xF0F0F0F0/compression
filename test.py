import queue
import numpy as np
import pyflac
import matplotlib.pyplot as plt
from scipy.io import wavfile

idx = 0
total_bytes = 0
rate = 44100
data_queue = queue.SimpleQueue()
tmp = np.array
f = open('files/test.flac', 'wb')  

def write_callback(buf: bytes, num_bytes: int, num_samples: int, frame_num: int):
    global total_bytes
    total_bytes += num_bytes
    data_queue.put(buf)
    f.write(buf)
    print('Samples ', frame_num)
    print('\n', buf)

def read_callback(decoded_data: np.array, sample_rate: int,
                  num_channels: int, num_samples: int):
    global idx
    global tmp
    idx += num_samples
    tmp = decoded_data 

#data = np.fromfile('coeff.txt', dtype=np.int16, sep='\n')
#data = np.fromfile('coeff3.txt', dtype=np.int16, sep='\n')
samplerate, data = wavfile.read('files/djent16.wav')

encoder = pyflac.StreamEncoder(rate, write_callback, blocksize = 0, verify=True)
encoder.process(data)
encoder.finish()
f.close()

decoder = pyflac.StreamDecoder(read_callback)
while not data_queue.empty():
    decoder.process(data_queue.get())
decoder.finish()

tmp.shape = (1, tmp.size)
data.shape = (1, data.size)
if(np.array_equal(tmp, data)):
    print('Decoded value OK')

print('\nUncompressed: ' +  str(data.nbytes) + ' bytes\n')
print('Compressed: ' +  str(total_bytes) + ' bytes\n')
print('Ratio: {ratio:.2f}%'.format(ratio= (1-(total_bytes / data.nbytes) )* 100))

names = ['RAW', 'FLAC']
values = [data.nbytes, total_bytes]

plt.bar(names, values)
plt.title('Bytes Compressed Using FLAC')
plt.ylabel('Bytes')
plt.show()



