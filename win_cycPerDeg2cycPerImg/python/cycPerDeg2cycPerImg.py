import math
import numpy as np
def give_gui():
    import Tkinter as Tk



    def run_button():
        global  var_d 
        global  var_s
        global  var_c
        var_d = d.get()
        var_s =   s.get()
        var_c =   c.get()
        print "hallo"
        T_r = Tk.Text(root, height=1, width=40)
        T_r.grid(row=10, column=0,columnspan=2)

        def calculation(d,s,c):
            def rad2deg(x):
                return x *   180. /np.pi
            wd = math.sqrt(math.pow(d,2)+math.pow(s/2,2))


            degreeOfScreen = rad2deg(np.arccos(((2*math.pow(wd,2))-(math.pow(s,2)))/(2*pow(wd,2))))
            return int(round(degreeOfScreen*c))

        T_r.insert(Tk.END, str(calculation(float(var_d),float(var_s),float(var_c)))+" Cycles are needed in image")
        #root.quit()



    root = Tk.Tk()
    root.wm_title("mouse2human")

    T_d = Tk.Text(root, height=1, width=40)
    T_s = Tk.Text(root, height=1, width=40)
    T_c = Tk.Text(root, height=1, width=40)
    #T_e = Tk.Text(root, height=1, width=40)

    d = Tk.Entry(root)
    s = Tk.Entry(root)
    c = Tk.Entry(root)


    runBotton = Tk.Button(master = root, text = 'Run', width = 6, command=run_button)
    #runBotton.pack(side=Tk.LEFT, padx = 2, pady=2)    
    runBotton.grid(row=4, column=1)
    
    #broButton.pack(side=Tk.LEFT, padx = 2, pady=2)  

    #Anordnung
    d.grid(row=1, column=1)
    s.grid(row=2, column=1)
    c.grid(row=3, column=1)


    T_d.grid(row=1, column=0)
    T_d.insert(Tk.END, "Distance to Image")
    T_s.grid(row=2, column=0)
    T_s.insert(Tk.END, "Hight of Image")

    T_c.grid(row=3, column=0)
    T_c.insert(Tk.END, "Cycles per Degree")

    #T_e.grid(row=0, column=0,columnspan=2)
    #T_e.insert(Tk.END, "Only Enter Integers!")

    
    Tk.mainloop()

    #check validitaet
    global var_s
    global var_d
    global var_c
    
    var_s = int(var_s)
    var_d = int(var_d)
    var_c = int(var_c)


    return {'-c': var_c, '-s': var_s, '-d': var_s}

print give_gui()