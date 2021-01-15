def guitar_chord():
    import pyaudio
    import struct
    import math
    from matplotlib import pyplot as plt
    import numpy as np
    import tkinter as Tk
    plt.ion()           # Turn on interactive mode so plot gets updated

    WIDTH     = 2         # bytes per sample
    CHANNELS  = 1         # mono
    RATE      = 8000     # Sampling rate (samples/second)
    BLOCKSIZE = 1024      # length of block (samples)
    DURATION  = 5        # Duration (seconds)

    NumBlocks = int( DURATION * RATE / BLOCKSIZE )

    # Open audio device:
    def call():
        print('Running for ', DURATION, 'seconds...')
        p = pyaudio.PyAudio()
        PA_FORMAT = p.get_format_from_width(WIDTH)

        stream = p.open(
            format    = PA_FORMAT,
            channels  = CHANNELS,
            rate      = RATE,
            input     = True,
            output    = True)

      
        frequencylist = []
        printlist = []

        for i in range(0, NumBlocks):
            count = 0
            input_bytes = stream.read(BLOCKSIZE)                     # Read audio input stream
            input_tuple = struct.unpack('h' * BLOCKSIZE, input_bytes)# Convert
            
            X = np.fft.fft(input_tuple)
            freqs = np.fft.fftfreq(len(X))
            
            for i in np.abs(X):
                if i>380000:
                    count+=1
            sorted_array = np.argsort(np.abs(X))
            indices = sorted_array[-1:-1*count-1:-1]
            values= np.abs(X)[indices]
            for i in range(len(values)):
                freq = abs(freqs[indices[i]]*RATE)
                if freq not in frequencylist and freq<1000:
                    frequencylist.append(abs(freqs[indices[i]]*RATE))
            list(filter(lambda num: num != 0, frequencylist))
            for i in range (len(frequencylist)-1):
              
                if abs (frequencylist[i]-frequencylist[i+1])<10 :
                    frequencylist[i] = (frequencylist[i]+frequencylist[i+1])/2
                    frequencylist[i+1] = 0
                    i+=1
                elif abs(frequencylist[i]-2*frequencylist[i+1])<10:
                    frequencylist[i] = frequencylist[i+1]
                    frequencylist[i+1] = 0
                    i+=1
                elif abs(frequencylist[i+1]-2*frequencylist[i])<10:
                    frequencylist[i+1] = 0
                    i+=1
         
            chordlist = []
            #print(frequencylist)
            for i in frequencylist:
                if abs(i-440)<5:
                    chordlist.append("A4")
                elif abs(i-659)<5 or abs(i-328)<5:
                    chordlist.append("E4")
                
                elif abs(i-246.94)<5:
                    chordlist.append("B3")
                elif abs(i-191)<2:
                    chordlist.append("G3")
                elif abs(i-146.83)<5:
                    chordlist.append("D3")
                elif abs(i-113)<2:
                    chordlist.append("A2")#Am,A,D,Dm
                elif abs(i-164)<2:
                    chordlist.append("E2")#(32)Em, E, Am,C,A
                    
                elif abs(i-97)<5:
                    chordlist.append("13")#G    
                elif abs(i-121)<5: 
                    chordlist.append("22")#Em,E,G
                elif abs(i-136)<8:
                    chordlist.append("23")#C
                elif abs(i-207)<5:
                    chordlist.append("41")#E
                elif abs(i-218)<5:
                    chordlist.append("42")#Am,A,D,Dm
                elif abs(i-265.6)<7:
                    chordlist.append("51")#Am,C
                
                elif abs(i-281)<4:
                    chordlist.append("52")#A
                elif abs(i-296)<5:
                    chordlist.append("53")#D,Dm
                elif abs(i-351)<2 or abs(i-703)<2:
                    chordlist.append("61")#Dm
                elif abs(i-375)<9:
                    chordlist.append("62")#D
                elif abs(i-394)<5:
                    chordlist.append("63")#G
                #elif abs(i-392)<5:
                    #chordlist.append("G4")
            Elist = ["22","E2","41"]
            Emlist = ["22","E2","E4","B3"]
            Amlist = ["42","E2","51"]
            Clist = ["23","E2","51","E4"]
            Alist = ["E2","42","52"]
            Glist = ["13","22","63"]
            Dlist = ["42","53","62"]
            Dmlist = ["42","53","61"]
          
            
            #print(chordlist)
            if len(chordlist)<=9:
                if all (elem in chordlist[0:4] for elem in Alist):
                    chord = "A"
                    if not chord in printlist:
                        printlist.append(chord)
                elif all (elem in chordlist for elem in Clist) and "41" not in chordlist and "62" not in chordlist and "42" not in chordlist:
                    chord = "C"
                    if not chord in printlist:
                        printlist.append(chord)
                elif all (elem in chordlist for elem in Glist):
                    chord = "G"
                    if not chord in printlist:
                        printlist.append(chord)
                elif all (elem in chordlist for elem in Amlist) and "D3" not in chordlist:
                    chord = "Am"
                    if not chord in printlist:
                        printlist.append(chord)  
                elif all (elem in chordlist for elem in Elist):
                    chord = "E"
                    if not chord in printlist:
                        printlist.append(chord)
                elif all (elem in chordlist for elem in Emlist):
                    chord = "Em"
                    if not chord in printlist:
                        printlist.append(chord)
                
                

                elif all (elem in chordlist for elem in Dlist):
                    chord = "D"
                    if not chord in printlist:
                        printlist.append(chord)
                elif all (elem in chordlist for elem in Dmlist) and "62" not in chordlist:
                    chord = "Dm"
                    if not chord in printlist:
                        printlist.append(chord)
                
            
            #print(printlist)
            
            if(len(printlist)==1):
                string = "The chord is: "+printlist[0]
            else:
                string = "Try again" 
            frequencylist.clear()
            
            #chordlist.clear()
          
        listbox.insert(Tk.END,string)   
        stream.stop_stream()
        stream.close()
        p.terminate()
        print('* Finished')


    root = Tk.Tk()
    listbox = Tk.Listbox(root)
    L1 = Tk.Label(root, text = 'Play a chord(A,Am,C,D,Dm,E,Em,G):')
    B1 = Tk.Button(root, text = 'Start', command = call, anchor = 'center')
    B3 = Tk.Button(root, text = 'Quit', command = root.quit)
    L1.pack(side = Tk.TOP)
    B1.pack()
    listbox.pack()
    B3.pack(side = Tk.BOTTOM)
    root.mainloop()

