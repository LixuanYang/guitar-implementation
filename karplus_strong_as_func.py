def updatef0(keys,f0,octave):
    from math import sin, cos, pi
    for i in range(0, 12):
        keys[i]['f_note'] = f0*(2**(i/12))
        keys[i]['y']    = karplus(keys[i]['f_note'])

def update_upoct():
    import tkinter as Tk
    global octave,f0,listbox
    octave += 1
    if octave > 8:
        octave = 8
        print("at highest octave")
    else:
        f0*=2
        updatef0(keys,f0,octave)
    listbox.delete(0)
    listbox.insert(Tk.END,"Current octave is at " + str(octave)+"\nwith fundamental frequency of "+ str(f0))
    listbox.pack()
    
def update_downoct():
    import tkinter as Tk
    global octave,f0,listbox
    octave -= 1
    if octave < 1:
        octave = 1
        print("at lowest octave")
    else:
        f0/=2
        updatef0(keys,f0,octave)
    listbox.delete(0)
    listbox.insert(Tk.END,"Current octave is at " + str(octave)+"\nwith fundamental frequency of "+ str(f0))
    listbox.pack()

    
def clear_cache(l):
    delete_list = []
    for i in range(len(l)):
        if l[i]['state'] > 498:
            delete_list.append(i)
    for i in range(len(delete_list)):
        l.pop(0)

def my_function(event):
    import numpy as np
    global CONTINUE,KEYPRESS,key,keys,octave,f0,pressed_keys,BLOCKLEN,RATE,r

    print('You pressed ' + event.char)
    if event.char == '`':
      print('Good bye')
      CONTINUE = False
    if event.char == 'q':
        key = 0
    if event.char == 'w':
        key = 1
    if event.char == 'e':
        key = 2
    if event.char == 'r':
        key = 3
    if event.char == 't':
        key = 4
    if event.char == 'y':
        key = 5
    if event.char == 'u':
        key = 6
    if event.char == 'i':
        key = 7
    if event.char == 'o':
        key = 8
    if event.char == 'p':
        key = 9
    if event.char == '[':
        key = 10
    if event.char == ']':
        key = 11
        
    if key < 12:
        pressed_keys.append({'key':key,'x':karplus(keys[key]['f_note'])})
        
    KEYPRESS = True

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return(x)

def karplus(f):
    import numpy as np
    from matplotlib import pyplot
    from math import sin, cos, pi
    
    # Read wave file properties
    T           = 2
    RATE        = 8000     # Frame rate (frames/second)
    WIDTH       = 2     # Number of bytes per sample
    LEN         = RATE * T      # Signal length
    CHANNELS    = 1     # Number of channels


    # Delay parameters

    b0 = 1.0            # direct-path gain
    G = 0.98             # feed-forward gain
    N = int(2*pi*RATE/f)   # delay in samples

    # Buffer to store past signal values. Initialize to zero.
    BUFFER_LEN =  2048          # Set buffer length.  Must be more than N!
    buffer = BUFFER_LEN * [0]   # list of zeros


    kr = 1  # read index  # (equivalent to BUFFER_LEN evaluated circularly)
    kr_1 = 0
    kw = N + 1  # write index


    x_amp = 32768
    x = []
    for i in range(0,60):
        x.append(np.random.randint(-x_amp,x_amp))
    x = x + [0] * (LEN - len(x))
    y = [0] * len(x)
    y = np.array(y)
    for i in range(0, len(x)):

        # Compute output value
        # y(n) = 0.5x(n) + 0.5x(n-1)  (LPF)
        # y = x + x*gain(delay)*H_lpf
        # y(n) = x(n) + K/2 y(n-N) + K/2 y(n-N-1)

        y[i] = x[i] + G*buffer[kr]/2 + G*buffer[kr_1]/2

        # Update buffer (pure delay)
        buffer[kw] = y[i]
        # Increment read index
        kr = kr + 1
        if kr == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kr = 0
        
        kr_1 += 1
        if kr_1 == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kr_1 = 0

        # Increment write index    
        kw = kw + 1
        if kw == BUFFER_LEN:
            # End of buffer. Circle back to front.
            kw = 0
            
    y = y.reshape((500,32))
    return(y)
    
def guitar_mod():
    import pyaudio, struct
    import numpy as np
    from scipy import signal
    from math import sin, cos, pi
    import tkinter as Tk
    
    global CONTINUE,KEYPRESS,key,keys,octave,f0,pressed_keys,BLOCKLEN,RATE,r,listbox

    BLOCKLEN   = 32       # Number of frames per block
    WIDTH       = 2         # Bytes per sample
    CHANNELS    = 1         # Mono
    RATE        = 8000      # Frames per second

    MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)



    # Open the audio output stream
    p = pyaudio.PyAudio()
    PA_FORMAT = pyaudio.paInt16
    stream = p.open(
            format      = PA_FORMAT,
            channels    = CHANNELS,
            rate        = RATE,
            input       = False,
            output      = True,
            frames_per_buffer = 128)
    # specify low frames_per_buffer to reduce latency

    CONTINUE = True
    KEYPRESS = False
    f0 = 440
    octave = 4

    key = -1
    pressed_keys = []

        
      
    root = Tk.Tk()
    root.bind("<Key>", my_function)

    s1 =   "This is a Guitar simulation program\n"
    s1 +=   "You can use 12 keys to produce guitar string sound\n"
    s1 +=   "q w e r t y u i o p [ ]\n"
    s1 +=  "From lowest frequency to highest\n"
    s1 +=   "You also can use buttons below to change the octave"

    Label = Tk.Label(root, text = s1,anchor = 'nw')
    Label.pack()

    Up_oct = Tk.Button(root,text = 'Increase Octave', command = update_upoct)
    Down_oct = Tk.Button(root,text = 'Decrease Octave', command = update_downoct)
    listbox=Tk.Listbox(root,width = 60, height = 1)
    listbox.insert(Tk.END,"Current octave is at " + str(octave)+"\nwith fundamental frequency of "+ str(f0))
    
    Up_oct.pack()
    Down_oct.pack()
    listbox.pack()
    
    print('Press keys for sound.')
    print('Press "`" to quit')

    keys = []
    for i in range(0, 12):
        keys.append({'key': i})
        keys[i]['f_note'] = f0*(2**(i/12))
        
    while CONTINUE:
        root.update()
                    
        for i in range(len(pressed_keys)):
            if 'state' not in pressed_keys[i]:
                pressed_keys[i]['state'] = -1
                pressed_keys[i]['y_filt'] = np.zeros(BLOCKLEN)
            
            pressed_keys[i]['state'] += 1
            pressed_keys[i]['y_filt'] = pressed_keys[i]['x'][pressed_keys[i]['state']]                
            
        y = np.zeros(BLOCKLEN)

        for i in range(len(pressed_keys)):
            for j in range(len(y)):
                y[j] += pressed_keys[i]['y_filt'][j]
        

        
        y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
        
        KEYPRESS = False
        
        binary_data = struct.pack('h' * BLOCKLEN, *y)    # Convert to binary binary data
        stream.write(binary_data,BLOCKLEN)               # Write binary binary data to audio output
        key = 100
        clear_cache(pressed_keys)
        
    print('* Done.')

    # Close audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()
