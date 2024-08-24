import tkinter as tk
import tkinter.messagebox
import Testing
import Functions
import Administrator
from tkinter import ttk
import tkinter.font as tkFont

#Funkcije koje se koriste u main GUI-u.
def ID_popup():
    
    def potvrda():
        value = entry.get()
        info = Functions.check_input_datatype(value) #Proverama da li je input sa entry-a pozitivan integer.
        if info == 1 and int(value) > 0:
            Testing.operater_id = int(value)
            main.withdraw()  #Desio se problem sa pojavljivanjem main GUI-a kad se doda showinfo, zbog toga su dodati withdraw i deiconify.
            if Testing.operater_id == Testing.administrator_id:
                tkinter.messagebox.showinfo("", "Uspesno ste ulogovali kao administrator!")
            else:
                tkinter.messagebox.showinfo("", "Uspesno ste se ulogovali, ID:" + str(value) + "!")
            main.deiconify()
            window.destroy()
            Functions.update_operater_list() #Updejtuje dictionary u kome se nalaze podaci o id-u operatera i broju zapakovanih komada za dati dan.
            Functions.write_in_dict(Testing.operater_id) #U log file upisuje podatke o ID-u i vremenu kad se operater ulogovao.
        else:
            main.withdraw()
            tkinter.messagebox.showinfo("Greska", "ID moze biti samo pozitivan broj")
    
    def show_pass(): #Funkcija koja hajduje unos u entry ako je potrebno
        if show_password_var.get():
            entry.config(show="$")
        else:
            entry.config(show="")
    
    #POPUP GUI
    window = tk.Toplevel(main)  #posatvlja windows kao nezavisan GUI u odnosu na main.
    window.geometry("700x700")
    window.title("ID")
    window.lift(main)  #Postavlja da window GUI bude iznad main GUI-a.
    window.attributes('-fullscreen', True)  #Iskomenatrisi u slucaju testiranja GUI-a.
    window.bind('<Return>', lambda event: potvrda())

    label = tk.Label(window, text="Unesite Vas ID", font=bold_font)
    label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    frame = tk.Frame(window)
    frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    entry = tk.Entry(frame) #polje za unos inputa
    entry.pack(side=tk.LEFT, padx=5)
    entry.focus_set()
    submit_button = tk.Button(frame, text="Potvrda", command=potvrda)
    submit_button.pack(side=tk.LEFT, padx=5)
    show_password_var = tk.BooleanVar()
    show_password_var.set(False)
    show_password_checkbutton = ttk.Checkbutton(window, text="Sakrij ID", variable=show_password_var, command=show_pass)
    show_password_checkbutton.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

    
    window.grab_set() #Sprecava interakciju sa drugim GUI-em.
    window.wait_window(window) #sprecava zatvaranje prozora dok se ne dobije input, tacnije dok se windows ne unisti.

def open_test_gui():
    main.withdraw()
    Testing.create_second_gui(main)

def open_administrator_gui():
    if Testing.operater_id == Testing.administrator_id:
        main.withdraw()
        Administrator.create_second_gui(main)
    else:
        tkinter.messagebox.showinfo("Greska", "Niste ulogovani kao administrator!")

def close_program():
    if Testing.operater_id == Testing.administrator_id:
        
        main.destroy()
    else:
        tkinter.messagebox.showinfo("Greska", "Niste ulogovani kao administrator!")

#Kreiranje Main GUI-a.
main = tk.Tk()
main.title("Wire counter")
main.geometry("700x700")
bold_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

Functions.read_backup() #Prilikom pokretanja programa cita bekam i updejtuje counter na potrebnu vrednost.
ID_popup() #poziva samo prilikom inicijalnog starta programa iskakajuci prozor koji mora da se popuni da bi se nastavilo na main GUI.

#Gadget-i main GUI-a
button4 = tk.Button(main, text="Administrator", command=open_administrator_gui, width=20, height=2)
button4.pack(pady = 10)

frame = tk.Frame(main)
frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

button1 = tk.Button(frame, text="Pokreni test", command=open_test_gui, width=50, height=5, bg = 'green')
button1.pack(side=tk.LEFT, padx=10, pady=10)

button3 = tk.Button(frame, text="Zatvori program", command=close_program, width=50, height=5, bg = 'red')
button3.pack(side=tk.LEFT, padx=10, pady=10)

label = tk.Label(main, text="Created by Gordan", bg="lightblue")
label.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)

main.attributes('-fullscreen', True)
main.mainloop()

