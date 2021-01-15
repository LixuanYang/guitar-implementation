def updatef0(keys,f0,octave):
    from math import sin, cos, pi
    for i in range(0, 12):
        keys[i]['f_note'] = f0*(2**(i/12))
        keys[i]['om1']    = 2.0 * pi * float(keys[i]['f_note'])/RATE
        keys[i]['a']      = [1, -2*r*cos(keys[i]['om1']), r**2]
        keys[i]['b']      = [r*sin(keys[i]['om1'])]

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
        if l[i]['if_processed']:
            if (abs(l[i]['state'][0]) + abs(l[i]['state'][1])) < 100:
                delete_list.append(i)
    for i in range(len(delete_list)):
        l.pop(0)

def my_function(event):
    import numpy as np
    global CONTINUE,KEYPRESS,key,keys,octave,f0,pressed_keys,BLOCKLEN,RATE,r, listbox

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
        pressed_keys.append({'key':key,'if_processed':False,'x':np.zeros(BLOCKLEN)})
        
    KEYPRESS = True
    
def pinano_mod():
    import pyaudio, struct
    import numpy as np
    from scipy import signal
    from math import sin, cos, pi
    import tkinter as Tk
    
    global CONTINUE,KEYPRESS,key,keys,octave,f0,pressed_keys,BLOCKLEN,RATE,r,listbox

    BLOCKLEN   = 32        # Number of frames per block
    WIDTH       = 2         # Bytes per sample
    CHANNELS    = 1         # Mono
    RATE        = 8000      # Frames per second

    MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

    # Parameters
    Ta = 2      # Decay time (seconds)

    # Pole radius and angle
    r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude

    # Filter coefficients (second-order IIR)
    ORDER = 2   # filter order

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

    
    s1 =   "This is a Piano program\n"
    s1 +=   "You can use 12 keys to produce piano sound\n"
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

    keys = []
    for i in range(0, 12):
        keys.append({'key': i})
        keys[i]['f_note'] = f0*(2**(i/12))
        keys[i]['om1']    = 2.0 * pi * float(keys[i]['f_note'])/RATE
        keys[i]['a']      = [1, -2*r*cos(keys[i]['om1']), r**2]
        keys[i]['b']      = [r*sin(keys[i]['om1'])]
        
    while CONTINUE:
        root.update()
       
        if KEYPRESS and CONTINUE:
            # Some key (not 'q') was pressed
            for i in range(len(pressed_keys)):
                if not pressed_keys[i]['if_processed']:
                    pressed_keys[i]['x'][0] = 10000.0
                    pressed_keys[i]['if_processed'] = True
                    
        for i in range(len(pressed_keys)):
            if 'state' not in pressed_keys[i]:
                pressed_keys[i]['state'] = np.zeros(ORDER)
                pressed_keys[i]['y_filt'] = np.zeros(BLOCKLEN)
            
            [pressed_keys[i]['y_filt'], pressed_keys[i]['state']] = signal.lfilter(keys[pressed_keys[i]['key']]['b'], keys[pressed_keys[i]['key']]['a'], pressed_keys[i]['x'], zi = pressed_keys[i]['state'])
            if pressed_keys[i]['if_processed']:
                pressed_keys[i]['x'][0] = 0.0
            
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
    root.mainloop()
