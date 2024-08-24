import tkinter as tk
from tkinter import ttk
import Testing
import tkinter.messagebox
import Functions
log_off = False
def create_second_gui(): #Funkcija koja se pokrece klikom na dugme promeni ID u main GUI-u.

    def back_to_test(): #Vraca se na Testing GUI.
        if not log_off:
            operater.destroy()
            Testing.create_second_gui(previous = None)
        else:
            tkinter.messagebox.showinfo("", "Morate se ulogovati!")
    def change_operaterid():
        global log_off
        value = entry.get()
        info = Functions.check_input_datatype(value)
        if info == 1 and int(value) > 0:
            #Stanje ako operater nije izlogovan nego se odmah menja na drugog operatera.
            if not log_off:
                Functions.write_out_dict(Testing.operater_id)
            #Stanje ako je operater izlogovan, dakle nema potrebe za write_out_dict posto je to obavljeno u log_out funkciji.
            else:
                log_off = False
            Testing.operater_id = int(value)
            entry.delete(0, tk.END) 
            if Testing.operater_id == Testing.administrator_id:
                tkinter.messagebox.showinfo("", "Uspesno ste ulogovali kao administrator!")
            else:
                tkinter.messagebox.showinfo("", "Uspesno ste promenili ID u " + str(value) + "!")
            Functions.write_in_dict(Testing.operater_id)
        else:
            tkinter.messagebox.showinfo("Greska", "ID moze biti samo pozitivan broj")
    
    def toggle_visibility(): #Funkcija koja hajduje unos u entry ako je potrebno
        if show_password_var.get() == 1:
            entry.config(show="")
        else:
            entry.config(show="$" if entry["show"] != "$" else "")
    
    def log_out():
        global log_off
        Functions.write_out_dict(Testing.operater_id)
        log_off = True
        tkinter.messagebox.showinfo("", "Uspesno ste se izlogovali!")
    
    #Operater GUI code
    operater = tk.Tk()
    operater.title("Operater ID menu")
    operater.geometry("500x500")
    operater.bind('<Return>', lambda event: change_operaterid())

    #Gadget-i Operater GUI-a
    frame = tk.Frame(operater)
    frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
    
    entry = tk.Entry(frame, show ="")
    entry.pack(side=tk.LEFT, padx=5)
    entry.focus_set()
    
    show_password_var = tk.IntVar()
    show_password_checkbutton = ttk.Checkbutton(operater, text="Sakrij ID", variable=show_password_var, command=toggle_visibility)
    show_password_checkbutton.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    button = tk.Button(frame, text = "Promeni ID", command = change_operaterid)
    button.pack(side=tk.LEFT, padx=5)

    button = tk.Button(operater, text = "Nazad na test", command = back_to_test, width=20, height=2)
    button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    
    button = tk.Button(operater, text = "Izloguj se", command = log_out, width=20, height=2)
    button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    operater.attributes('-fullscreen', True)
    operater.mainloop()
