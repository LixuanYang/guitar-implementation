
def guitar_tuning():
    import pyaudio
    import struct
    from matplotlib import pyplot as plt
    import numpy as np
    import math
    plt.ion()           # Turn on interactive mode so plot gets updated

    WIDTH     = 2         # bytes per sample
    CHANNELS  = 1         # mono
    RATE      = 8000     # Sampling rate (samples/second)
    BLOCKSIZE = 1024      # length of block (samples)
    DURATION  = 2        # Duration (seconds)

    NumBlocks = int( DURATION * RATE / BLOCKSIZE )


    DBscale = False
    # DBscale = True

    # Initialize plot window:
    plt.figure(1)
    if DBscale:
        plt.ylim(0, 150)
    else:
        plt.ylim(0, 20*RATE)

    # Frequency axis (Hz)
    plt.xlim(0, 0.5*RATE)         # set x-axis limits
    # plt.xlim(0, 2000)         # set x-axis limits
    plt.xlabel('Frequency (Hz)')
    f = RATE/BLOCKSIZE * np.arange(0, BLOCKSIZE)

    line, = plt.plot([], [], color = 'blue')  # Create empty line
    line.set_xdata(f)                         # x-data of plot (frequency)

    # Open audio device:
    p = pyaudio.PyAudio()
    PA_FORMAT = p.get_format_from_width(WIDTH)

    stream = p.open(
        format    = PA_FORMAT,
        channels  = CHANNELS,
        rate      = RATE,
        input     = True,
        output    = False)

    maxfreq=0
    for i in range(0, NumBlocks):
        input_bytes = stream.read(BLOCKSIZE)                     # Read audio input stream
        input_tuple = struct.unpack('h' * BLOCKSIZE, input_bytes)  # Convert
        X = np.fft.fft(input_tuple)
        
        #get frequency response of signal
        freqs = np.fft.fftfreq(len(X))
        #get dominant freq index
        index = np.argmax(np.abs(X))
        
        freq = freqs[index]
        #get dominant freq---key
        frequency = abs(freq*RATE)
        
        #filter out noise
        if np.max(np.abs(X))>14000 and (frequency<=330):
            
            currentfreq = frequency
        else:
            currentfreq = 0
        
        if (maxfreq<currentfreq):
            maxfreq = currentfreq

        # Update y-data of plot
        if DBscale:
            line.set_ydata(20 * np.log10(np.abs(X)))
        else:
            line.set_ydata(np.abs(X))
            
        plt.pause(0.001)
        print(maxfreq)


        

    plt.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

    print('* Finished')

    return maxfreq



