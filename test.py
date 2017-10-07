import Tkinter as Tk
import tkFileDialog

import sys


root = Tk.Tk()
root.wm_title("mouse2human")

T = Tk.Text(root, height=2, width=30)
T.pack()
T.insert(Tk.END, "Just a text Widget\nin two lines\n")

def browse_file():
    global fname
    fname = tkFileDialog.askopenfilename()
    print "Selected File is:"
    print fname
    broButton = Tk.Button(master = root, text = 'Run', width = 6, command=run_button)
    broButton.pack(side=Tk.LEFT, padx = 2, pady=2)    


c = Tk.Entry(root)
c.pack()


k = Tk.Entry(root)
k.pack()

def run_button():
    global  var_c 
    var_c = c.get()
    global  var_k
    var_k =   k.get()
    root.quit()







broButton = Tk.Button(master = root, text = 'Browse', width = 6, command=browse_file)
broButton.pack(side=Tk.LEFT, padx = 2, pady=2)  



Tk.mainloop()
print fname
print var_k
print var_c