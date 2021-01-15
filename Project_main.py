import tkinter as Tk

from pinano_as_func import pinano_mod,update_upoct,update_downoct
from karplus_strong_as_func import guitar_mod
from chord import guitar_chord
from main_gui_func import guitar_tuning_gui

root = Tk.Tk()

Des = 'This is the Project Main, it contains 4 modules \n'
Des += 'Pinano with 96 notes, Guitar with 96 notes \n'
Des += 'Guitar tuning Application, and Guitar Chord Identifier.\n\n'
Des += 'Project coded by Zhiyuan Ding, Lixuan Yang, Yuanli Lu.\n'


Des_l = Tk.Label(root, text = Des)
B_p = Tk.Button(root, text = 'Piano Mod', command = pinano_mod)
B_g = Tk.Button(root, text = 'Guitar Mod', command = guitar_mod)
B_chord= Tk.Button(root, text = 'Guitar chord', command = guitar_chord)
B_tune = Tk.Button(root, text = 'Guitar tune', command = guitar_tuning_gui)

Des_l.pack(side=Tk.TOP)
B_p.pack(side=Tk.LEFT, anchor = 'e')
B_g.pack(side=Tk.LEFT, anchor = 'e')
B_chord.pack(side=Tk.RIGHT, anchor = 'e')
B_tune.pack(side=Tk.RIGHT, anchor = 'e')

root.mainloop()
