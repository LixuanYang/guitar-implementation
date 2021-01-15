def get_result():
    from guitar_tune import guitar_tuning
    global E1,listbox,Tk
    freq=0
    correct_entry = False
    if E1.get()=="E_low":
        freq =82.41
        correct_entry = True
    elif E1.get()=="A":
        freq=110.00
        correct_entry = True
    elif E1.get()=="D":
        freq=146.83
        correct_entry = True
    elif E1.get()=="G":
        freq=196.00
        correct_entry = True
    elif E1.get()=="B":
        freq=246.94
        correct_entry = True
    elif E1.get()=="E_high":
        freq=329.63
        correct_entry = True
    
    if correct_entry:
        sample_freq=guitar_tuning()

    if (not correct_entry):
        output = 'Invalid Entry, Please enter again.'
    elif abs(sample_freq-freq)<4 or abs(sample_freq-2*freq)<8:
        output="Just Right!"
    elif (sample_freq-freq)>4:
        output="Loosen!"
    elif (sample_freq-freq)<-4:
        output="Tighten!"

    
    listbox.insert(Tk.END,output)



def guitar_tuning_gui():

    import tkinter as Tk

    global E1,listbox,Tk

    root = Tk.Tk()
    
    #button,label,entry

    listbox=Tk.Listbox(root)


    # Define widgets
    L1 = Tk.Label(root, text = 'Enter Target Key (E_low,E_high,A,D,G,B)')
    E1 = Tk.Entry(root)

    B1 = Tk.Button(root, text = 'Result', command = get_result)

    L1.pack()
    E1.pack()
    B1.pack()
    listbox.pack()

    root.mainloop()
