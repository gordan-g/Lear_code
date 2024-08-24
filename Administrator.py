import tkinter as tk
import Testing
import Functions
import tkinter.messagebox
import subprocess
import tkinter.font as tkFont
import math


def create_second_gui(previous):#Funkcija koja se pokrece klikom na dugme administrator u main GUI-u.

    def close_second_gui(): #Zatvara administrator GUI i vraca nazad main GUI.
        maintenance.destroy()
        previous.deiconify()

    def custom_reprint():
        def create_label(): #Funkcija koja kupi input sa entry-a kreira content labele, nakon cega stampa nalepnicu.
            qty = entry1.get()
            operater_id = entry2.get()
            date = entry3.get()
            current_time = entry4.get()
        
            label = '''
N
A770,220,2,3,2,2,N,"QUANTITY: {qty}"
A340,325,2,3,1,1,N,"BOARD ID: TI01-S1014A"
A770,325,2,3,1,1,N,"OPERATER ID:{operater_id}"
B340,220,2,1B,2,2,65,N,"{qty}"
A770,100,2,3,1,1,N,"DATE:{date}"
A770,75,2,3,1,1,N,"TIME:{current_time}"
P1
    '''.format(qty = qty, operater_id = operater_id, date = date, current_time = current_time)
            
            Functions.create_file_administrator(label)
            subprocess.run(["lp", "-c", "/home/lear/Apps/txt/labela_custom"])
            entry1.delete(0, tk.END) 
            entry2.delete(0, tk.END) 
            entry3.delete(0, tk.END) 
            entry4.delete(0, tk.END) 
            popup.destroy()

        #Gadget-i custom reprint GUI-a
        popup = tk.Toplevel(maintenance)
        popup.title("Custom label")
        popup.geometry("400x400-200+40")
        bold_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        popup.bind('<Return>', lambda event: create_label())

        label = tk.Label(popup, text="Kolicina", font = bold_font)
        label.pack(pady=10)
        frame1 = tk.Frame(popup)
        frame1.pack(pady=5)
        entry1 = tk.Entry(frame1)
        entry1.pack(side=tk.LEFT, padx=5)
        
        label = tk.Label(popup, text="Operater ID", font= bold_font)
        label.pack(pady=10)
        frame2 = tk.Frame(popup)
        frame2.pack(pady=5)
        entry2 = tk.Entry(frame2)
        entry2.pack(side=tk.LEFT, padx=5)

        label = tk.Label(popup, text="Datum  u formatu MM/DD/YY", font= bold_font)
        label.pack(pady=10)
        frame3 = tk.Frame(popup)
        frame3.pack(pady=5)
        entry3 = tk.Entry(frame3)
        entry3.pack(side=tk.LEFT, padx=5)

        label = tk.Label(popup, text="Vreme u formatu HH:MM:SS", font= bold_font)
        label.pack(pady=10)
        frame4 = tk.Frame(popup)
        frame4.pack(pady=5)
        entry4 = tk.Entry(frame4)
        entry4.pack(side=tk.LEFT, padx=5)

        button1 = tk.Button(popup, text="Print", command=create_label, width=20, height=2)
        button1.pack(pady=10)
        
    def reprint():
        def reprint_25():
            subprocess.run(["lp", "-c", "/home/lear/Apps/txt/labela_25"])

        def reprint_100():
            subprocess.run(["lp", "-c", "/home/lear/Apps/txt/labela_100"])

        def reprint_1000():
            subprocess.run(["lp", "-c", "/home/lear/Apps/txt/labela_1000"])

        popup = tk.Toplevel(maintenance)
        popup.title("Reprint")
        popup.geometry("400x100-200+125")

        #Gaget-i reprint GUI-a
        frame = tk.Frame(popup)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        button1 = tk.Button(frame, text="Reprint 25", command=reprint_25)
        button1.pack(side=tk.LEFT, padx=10, pady=10)
        button2 = tk.Button(frame, text="Reprint 100", command=reprint_100)
        button2.pack(side=tk.LEFT, padx=10, pady=10)
        button3 = tk.Button(frame, text="Reprint 1000", command=reprint_1000)
        button3.pack(side=tk.LEFT, padx=10, pady=10)

    def update_counter(): 
        def update_counter_1000():
            info = Functions.check_input_datatype(entry2.get())
            content = int(entry2.get())
            if info == 1 and 0 <= content <1000:
                Testing.counter2 = content%100
                Testing.counter = content%25
                Testing.counter3 = math.floor(content/100)
                Functions.write_backup(str(content%100), str(Testing.counter3))
                entry2.delete(0, tk.END)
                tkinter.messagebox.showinfo("", "Uspesno izmenjen counter!")
                popup.destroy()
            else:
                entry2.delete(0, tk.END)
                tkinter.messagebox.showinfo("Greska", "Moze biti unet samo broj koji je manji od 1000!")

        #Gaget-i update_counter GUI-a
        popup = tk.Toplevel(maintenance)
        popup.title("Counter update")
        popup.geometry("400x100-200+125")
        bold_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        popup.bind('<Return>', lambda event: update_counter_1000())
        
        label = tk.Label(popup, text="Unesite vrednost od 0-1000", font= bold_font)
        label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        frame2 = tk.Frame(popup)
        frame2.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        entry2 = tk.Entry(frame2)
        entry2.pack(side=tk.LEFT, padx=5)
        entry2.focus_set()
        button2 = tk.Button(frame2, text="Update", command=update_counter_1000)
        button2.pack(side=tk.LEFT, padx=10, pady=10)

    maintenance = tk.Tk()
    maintenance.title("Administrator")
    maintenance.geometry("500x500")

    #Gadget-i administrator GUI-a
    button = tk.Button(maintenance, text = "Custom label", command = custom_reprint, width=20, height=2)
    button.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    button = tk.Button(maintenance, text = "Reprint", command = reprint, width=20, height=2)
    button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

    button = tk.Button(maintenance, text = "Update counter", command = update_counter, width=20, height=2)
    button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

    button = tk.Button(maintenance, text = "Print daily", command = Functions.print_daily, width=20, height=2)
    button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

    button = tk.Button(maintenance, text = "Nazad na glavni meni", command = close_second_gui, width=20, height=2)
    button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
    
    maintenance.attributes('-fullscreen', True)
    maintenance.mainloop()
