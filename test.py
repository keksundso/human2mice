

def give_gui():
    import Tkinter as Tk
    import tkFileDialog

    def browse_file():
        global fname
        fname = tkFileDialog.askopenfilename()
        print "Selected File is:"
        print fname
        runBotton = Tk.Button(master = root, text = 'Run', width = 6, command=run_button)
        #runBotton.pack(side=Tk.LEFT, padx = 2, pady=2)    
        runBotton.grid(row=3, column=1)


    def run_button():
        global  var_c 
        var_c = c.get()
        global  var_k
        var_k =   k.get()
        root.quit()



    root = Tk.Tk()
    root.wm_title("mouse2human")

    T_c = Tk.Text(root, height=2, width=40)
    T_k = Tk.Text(root, height=3, width=40)
    c = Tk.Entry(root)

    k = Tk.Entry(root)


    broButton = Tk.Button(master = root, text = 'Browse', width = 6, command=browse_file)
    #broButton.pack(side=Tk.LEFT, padx = 2, pady=2)  

    #Anordnung
    c.grid(row=0, column=1)
    k.grid(row=1, column=1)
    broButton.grid(row=3, column=0)


    T_c.grid(row=0, column=0)
    T_c.insert(Tk.END, "Number sine cycles per image\n (Default is 10)")

    T_k.grid(row=1, column=0)
    T_k.insert(Tk.END, "Images will be created with the \nchoosen contrast reduction \n (Between 1-0) (e.g. 0.5) (Default is 1)")

    Tk.mainloop()

    #check validitaet
    global var_c
    global var_k
    if var_c == "":
        var_c= 10
    else:
        var_c= int(var_c)

    if var_k == "":
        var_k = 1
    else:
        var_k = float(var_k)


    return {'-c': var_c, '-k': var_k, '-o': None, 'FILE': fname}

print give_gui()