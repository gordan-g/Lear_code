import tkinter as tk
import Functions
import Operater
import time
from gpiozero import Button, LED, OutputDevice
#Definisane promenjive

dugme = Button(17)
fikstura = Button(23)
buzzer = LED(16)
color_sensor = Button(12)
activate_color = OutputDevice(24, active_high = False)
activate_sw = OutputDevice(25, active_high = False)


administrator_id = 20792
operater_id = 0
counter = 0
counter2 = 0
counter3 = 0
stage = 1
current_counter = 0
operater_list = {}
data = None

def create_second_gui(previous=None): #Funkcija koja se pokrece klikom na dugme pokreni test u main GUI-u
    """
    Kada otvorimo sa Main GUI-a dobijamo argument za previous, dok sa Operater GUI-a ne dobijamo.
    Kada udjemo sa Main-a ostaje nam data od tog GUI-a da bi se kasnije mogili vratiti na Main.
    Jer ako sa Operater GUI-a pozovemo create_second_gui i stavimo argument za previous,
    necemo moci da izadjemo iz Testing GUI-a na Main GUI-a vec ce se iznova vracati na Operater.
    """
    
    global data
    if previous != None:
        data = previous
    #Funkcija koja zatvara Testing i vraca Main GUI.
    def close_second_gui():
        if stage != 1: #Ako smo u fazi koja nije prva necemo moci izaci iz GUI-a.
            Functions.display_error()
        else:
            testing.destroy()
            data.deiconify() #Ovo data ce nam uvek biti Main GUI.
        
    def open_operater_gui():
        if stage != 1: #Ako smo u fazi koja nije prva necemo moci izaci iz GUI-a.
            Functions.display_error()
        else:
            testing.destroy()
            Operater.create_second_gui()
        
    #Kreiranje Testing GUI-a.
    testing = tk.Tk()
    testing.title("Wire Counter")
    testing.geometry("800x450")
    testing.configure(background="#C1CDCD")
    testing.grid_rowconfigure(1, weight=1)
    testing.grid_columnconfigure(1, weight=1)
    
    def engine():
            
        def engine_func():
            global stage, counter, counter2
            
            if stage ==1:
                if fikstura.is_pressed and operater_id != administrator_id:
                    activate_color.on()
                    stage = 2
                    label.config(text = "NAKON BANDAZIRANJA PRITISNITE TASTER")
                    
            elif stage ==2:
                if fikstura.is_pressed and dugme.is_pressed:
                    if color_sensor.is_pressed:
                        activate_color.off()
                        stage = 3
                        label.config(text="EMPTY TEST")
                    else:
                        pass
                    
            elif stage ==3:
                if not dugme.is_active and not fikstura.is_active:
                    counter += 1
                    counter2 += 1
                    Functions.check_counter(counter, counter2, counter3, operater_id)  # Proverava da li je potrebno stampanje labele.
                    Functions.write_backup(str(counter2), str(counter3))  # Pise u backup trenutnu vrednost countera.
                    counter_label.config(text="Counter: " + str(counter) + "/25")  # Updejtuje label na Testing GUI-u.
                    counter_label2.config(text="Counter: " + str(counter2) + "/100")  # Updejtuje label na Testing GUI-u.
                    label.config(text="POSTAVITI TERMINAL U FIKSTURU")
                    buzzer.on()  # Pali buzzer.
                    time.sleep(0.5)  # Uvodi delay od pola sekunde zbog buzzera kako bi zujao toliko.
                    buzzer.off()  # Gasi buzzer.
                    stage = 1
                    time.sleep(2)
			
        engine_func()
        dugme.when_pressed = engine_func
        fikstura.when_pressed = engine_func
        dugme.when_released = engine_func
        fikstura.when_released = engine_func
        
    #Gadget-i Testing GUI-a
    label = tk.Label(testing, text="POSTAVITI TERMINAL U FIKSTURU", font=("Arial", 50))
    label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
    
    counter_label = tk.Label(testing, text="Counter: " + str(counter) + "/25", font=("Arial", 24))
    counter_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    counter_label2 = tk.Label(testing, text="Counter: " + str(counter2) + "/100", font=("Arial", 24))
    counter_label2.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    
    frame = tk.Frame(testing, bg = '#C1CDCD')
    frame.pack(pady = 10)
    
    button = tk.Button(frame, text = "Nazad na glavni menu", command = close_second_gui, width=30, height=3)
    button.pack(side=tk.LEFT, padx=10, pady=10)
    
    button = tk.Button(frame, text = "Promeni ID", command = open_operater_gui, width=30, height=3)
    button.pack(side=tk.LEFT, padx=10, pady=10)

    testing.after(100, engine)

    testing.attributes('-fullscreen', True)
    testing.mainloop()
