import datetime
import subprocess
import Testing
import tkinter as tk


#Definisanje pinova koji ce se u ovom slucaju koristiti kao input/output.
#Po ovoj definiciji pinova LOW stanje ce biti kad je prekidac pritisnut, HIGH kad je pusten.

"""
ODAVDE NA DOLE SU FUNKCIJE KOJE SE KORISTE ZA KREIRANJE NALEPNICA I STAMPANJE, KAO I PISANJE/CITANJE BACKUP-A COUNTERA

"""
def check_counter(counterr, counterr2, counterr3, operater_ID):  # provera countera ako je potrebno stampanje labele

    if counterr == 25:
        label_printing(25, operater_ID)
        Testing.counter = 0

    if counterr2 == 100:
        label_printing(100, operater_ID)
        Testing.counter2 = 0
        Testing.counter3 += 1
        counterr3 += 1

    if counterr3 == 10:
        label_printing(1000, operater_ID)
        Testing.counter3 = 0
        
def label_printing(quantity, operater_ID):  #Poziva funkcije zaduzene za kreiranje sadrzaja labele i pisanja u odredjeni file, nakon cega se ta labela stampa.
    if quantity == 25:
        label = create_label(quantity, operater_ID)
        create_file(label, quantity)
        subprocess.run(["lp", "-c", "/home/lear/Apps/txt/labela_25"])
    if quantity == 100:
        label = create_label(quantity, operater_ID)
        create_file(label, quantity)
        subprocess.run(["lp", "-c", "/home/lear/Apps/txt/labela_100"])
    if quantity == 1000:
        label = create_label(quantity, operater_ID)
        create_file(label, quantity)
        #subprocess.run(["lp", "-c", "/home/lear/Apps/txt/labela_1000"])
        
def create_label(quantity, operater_ID):  #Kreira sadrzaj labela u zavisnosti od datih argumenata.
        label = '''
N
A770,220,2,3,2,2,N,"QUANTITY: {qty}"
A340,325,2,3,1,1,N,"BOARD ID: TI01-S1014A"
A770,325,2,3,1,1,N,"OPERATER ID:{operater_id}"
B340,220,2,1B,2,2,65,N,"{qty}"
A770,100,2,3,1,1,N,"DATE:{date}"
A770,75,2,3,1,1,N,"TIME:{current_time}"
P1
    '''.format(date=datetime.datetime.now().strftime("%d/%m/%y"), operater_id = str(operater_ID), current_time = datetime.datetime.now().strftime('%H:%M:%S'), qty = quantity)
        return label
        
def create_file(created_label, quantity):  #Nakon sto je sadrzaj labele kreiran, taj sadrzaj se cuva u odgovarajuci file. Koji ce kasnije biti stampan.
    if quantity == 25:
        file = open("/home/lear/Apps/txt/labela_25", 'w')
    if quantity ==100:
        file = open("/home/lear/Apps/txt/labela_100", 'w')
    if quantity ==1000:
        file = open("/home/lear/Apps/txt/labela_1000", 'w')
    file.write(created_label)
    file.close()
    
def write_backup(quantity_to_store, counter1000=None):  #Pise backup u zavisnoti od trenutnog broja countera2 i countera3.
    file = open("/home/lear/Apps/txt/counter_backup", 'w')
    if quantity_to_store == "100":
        file.write(f'0,{counter1000}')
    else:
        file.write(f'{quantity_to_store},{counter1000}')
    file.close()
    
def read_backup(): #Cita zapisan backup od funkcije write_backup i updejtuje counter.
    file = open("/home/lear/Apps/txt/counter_backup", "r")
    content = file.read()
    content_list = content.split(",")
    Testing.counter2 = int(content_list[0])
    Testing.counter = int(content_list[0])%25
    Testing.counter3 = int(content_list[1])
    file.close()

"""
OVDE SE ZAVRSAVAJU FUNKCIJE KOJE SE KORISTE ZA KREIRANJE NALEPNICA I STAMPANJE KAO I PISANJE/CITANJE BACKUP-A COUNTERA

"""

"""
ODAVDE NA DOLE SU FUNKCIJE KOJE SE KORISTE ZA LOG FILE

"""
def update_operater_list(): #Updejtuje dictionary u kome se nalaze podaci o id-u operatera i broju zapakovanih komada za dati dan.
    file = open("/home/lear/Apps/txt/log_file", "r")
    file_content = file.readlines()
    file.close()
    global error_index
    error_index = None
    
    for count, line in enumerate(file_content):
        if count == 0:
            pass
        else:
            id_from_file = line.split(",")
            try:
                Testing.operater_list[int(id_from_file[0])] = int(id_from_file[3])
            except IndexError:
                error_index = count
      
    if error_index !=None:
        overwrite_log_file(eror_with_update_operater_list = error_index)
            
def write_in_dict(operated_ID_to_write): #U log file upisuje podatke o ID-u i vremenu kad se operater ulogovao.
    log_file() #Pogledaj komentar na mestu gde je funckija definisana.

    if operated_ID_to_write != Testing.administrator_id:

        #Slucaj kada se operater vec nalazi u log file-u
        if operated_ID_to_write in Testing.operater_list:
            overwrite_log_file(ID = operated_ID_to_write) #Pogledaj komentar na mestu gde je funckija definisana.
            log_in_time = datetime.datetime.now().strftime('%H:%M:%S')
            file = open("/home/lear/Apps/txt/log_file", 'a')
            file.write(f'{operated_ID_to_write},{log_in_time},')
            file.close()
            Testing.current_counter = read_counter_1000() #Postavlja trenutnu vrednost countera da bi se na kraju znalo koliko je operater zapakovao(razlika).
        #Slucaj kada se operater ne nalazi u log file-u
        else:
            log_in_time = datetime.datetime.now().strftime('%H:%M:%S')
            file = open("/home/lear/Apps/txt/log_file", 'a')
            file.write(f'{operated_ID_to_write},{log_in_time},')
            file.close()
            Testing.operater_list[operated_ID_to_write] = 0 #Dodaje novog operatera u operater Dictionary
            Testing.current_counter = read_counter_1000()

    else:
        pass
        
def log_file(): #Poziva funkcije read_date_log i overwrite_date_log radi provere datuma u file-u i real-time vremena. Restartuje log_file ukoluko je novi dan!
    func_result = read_date_log()
    if func_result == 1:
        pass
    else:
        overwrite_date_log()
        
def read_date_log(): #Proverava datum upisan u date file i trenutan datum ukoliko je datum razlicit vraca 0, u suprotnom vraca 1.
    file = open("/home/lear/Apps/txt/log_file", "r")
    try:
        written_date = file.readlines()[0].strip()
    except IndexError:
        Testing.operater_list.clear()
        file.close()
        return 0
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if written_date != current_date:
        Testing.operater_list.clear()
        file.close()
        return 0
    else:
        file.close()
        return 1
        
def overwrite_date_log(): #Ako se vremena u date filu-u i realnom vremenu ne poklapaju brise citav sadrzaj file-a i ostavlja samo trenutni(realtime) datum.
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    file = open("/home/lear/Apps/txt/log_file", 'w')
    file.write(f'{date}\n')
    file.close()
    
def overwrite_log_file(ID = None, eror_with_update_operater_list = None): #Poziva funkciju find_the_line nakon cega ponovo pise podatke u log file i izuzima operatera koji se vec logovao. I upisuje nove podatke o vremenu logovanja.
    if ID != None:
        line_to_delete = find_the_line(ID)
    else:
        line_to_delete = eror_with_update_operater_list
    file = open("/home/lear/Apps/txt/log_file", "r")
    file_content = file.readlines()
    file.close()
    file = open("/home/lear/Apps/txt/log_file", 'w')
    for count, line in enumerate(file_content):
        if count == line_to_delete:
            continue
        else:
            file.write(f'{line.strip()}\n')
    file.close()
    
def find_the_line(operater_ID_to_find): #Nalazi u kojoj liniji log_fila se nalazi operater koji se drugi put u toku dana loguje i taj podatak vraca funkciji overwrite_log_file.
    file = open("/home/lear/Apps/txt/log_file", "r")
    file_content = file.readlines()
    file.close()
    for count, line in enumerate(file_content):
        if count == 0:
            continue
        else:
            id_from_file = line.split(",")
            if int(id_from_file[0]) == operater_ID_to_find:
                return count
                
def write_out_dict(operated_ID_to_write): #U log file upisuje podatke o vremenu kada se operater izlogovao kao i o broju zapakovanih komada za vreme rada.
    value = Testing.operater_list.get(operated_ID_to_write)
    current_count = read_counter_1000() #Provera trenutni broj countera i uporedjuje ga sa Testing.current_counter kako bi mogao da zna pravi broj zabakovanih komada operatera.
    
    if operated_ID_to_write != Testing.administrator_id:
        #Slucaj ako je vrednost zapakovanih nula, odnosno operater se bio prvi put logovao.
        if value == 0:
            #Slucaj ako je counter na pocetku logovanja npr bio 978, a sada je 332
            if current_count < Testing.current_counter:
                Testing.operater_list[operated_ID_to_write] = (1000-Testing.current_counter) + current_count
            #Slucaj ako je counter na pocetku logovanja npr bio 332, a sada je 978
            if current_count > Testing.current_counter:
                Testing.operater_list[operated_ID_to_write] = current_count - Testing.current_counter
            
            packed_number = Testing.operater_list.get(operated_ID_to_write)
            log_out_time = datetime.datetime.now().strftime('%H:%M:%S')
            file = open("/home/lear/Apps/txt/log_file", 'a')
            file.write(f'{log_out_time},{packed_number}\n')
            file.close()
        #Slucaj ako je vrednost zapakovanih vise od nula, odnosno operater se ulogovao vise od jednom.
        else:
            # Slucaj ako je counter na pocetku logovanja npr bio 978, a sada je 332
            if current_count < Testing.current_counter:
                Testing.operater_list[operated_ID_to_write] = ((1000-Testing.current_counter) + current_count) + value
            # Slucaj ako je counter na pocetku logovanja npr bio 332, a sada je 978
            if current_count > Testing.current_counter:
                Testing.operater_list[operated_ID_to_write] = (current_count - Testing.current_counter) + value
            
            packed_number = Testing.operater_list.get(operated_ID_to_write)
            log_out_time = datetime.datetime.now().strftime('%H:%M:%S')
            file = open("/home/lear/Apps/txt/log_file", 'a')
            file.write(f'{log_out_time},{packed_number}\n')
            file.close()
    else:
        pass
        
def read_counter_1000(): #Cita do koje vrednosti je dosao broj na counter3 promenjivoj
    file = open("/home/lear/Apps/txt/counter_backup", "r")
    content = file.read()
    content_list = content.split(",")
    total_counter = int(content_list[0]) + (int(content_list[1])*100)
    file.close()
    return total_counter
    
def print_daily(): #Funkcija koja cita podatke log file-a i stampa dnevni izvestaj odnosno operatere koji su radili i ostale relevante podatke.
    #Multiline promenjiva je deo koji se uvek koristi i ne menja se.
    
    file = open("/home/lear/Apps/txt/log_file", "r")
    file_content = file.readlines()
    file.close()
    
    multiline = '''
N
A500,300,2,3,1,1,N,"DATUM:{date}"
A550,250,2,3,1,1,N,"ZAPAKOVANO:"
A750,250,2,3,1,1,N,"OPERATER ID:"
A330,250,2,3,1,1,N,"ULOGOVAN:"
A150,250,2,3,1,1,N,"IZLOGOVAN:"
'''.format(date = file_content[0].strip())

    file = open("/home/lear/Apps/txt/daily_report", 'w')
    file.write(multiline)
    for i, line in enumerate(file_content):
        if i == 0:
            continue
        else:
            content = line.split(",")
            multiline2 = '''A550,{y},2,3,1,1,N,"{packed}"
A750,{y},2,3,1,1,N,"{ID}"
A330,{y},2,3,1,1,N,"{log}"
A150,{y},2,3,1,1,N,"{logout}"
'''.format(packed=content[3].strip(), ID=content[0], log =content[1], logout=content[2], y=250-(50*i))
            file.write(multiline2)
    file.write("P1\n")
    file.close()
    subprocess.run(["lp", "-c", "/home/lear/Apps/txt/daily_report"])

"""
OVDE SE ZAVRSAVAJU FUNKCIJE KOJE SU ZADUZENE ZA LOG FILE

"""
"""
OSTALO

"""

def check_input_datatype(data):  #Proverava da li je input integer.
    try:
        int(data)
        return 1
    except ValueError:
        return 0
        
def display_error(): #Popup koji prikazuje gresku.
    error = tk.Toplevel()
    error.geometry("500x100-150+325")
    error.title("error")
    error.lift()
    error.bind('<Return>', lambda event: error.destroy())

    def close():
        error.destroy()

    label = tk.Label(error, text="Trenutni komad mora biti zapakovan", font=("Arial", 16))
    label.pack(pady=10)
    close_button = tk.Button(error, text="OK", command=close, width=20, height=2)
    close_button.pack(pady=10)
    error.after(5000, lambda: error.destroy())

def create_file_administrator(whiclabel):
    file = open("/home/lear/Apps/txt/labela_custom", 'w')
    file.write(whiclabel)
    file.close()
