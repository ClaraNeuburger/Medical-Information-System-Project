import socket
from hl7apy.parser import parse_message
from hl7apy.exceptions import ParserError
from hl7apy.core import Message
from hl7apy import core
from threading import Thread
import datetime
import queue
import sqlite3


class HL7Server(Thread):
    def __init__(self, host, port, message_handler):
        self.running=False
        super().__init__()
        self.host = host
        self.port = port
        self.message_handler = message_handler

    def run(self):
        self.running=True
        while self.running:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024).decode()
                    conn.close()
            try: 
                self.message_handler(data)
            except Exception as e:
                print(f"Error handling message: {e}")
            self.running=False
            print('Server stopped')
                       


  
def handle_rde_message(data):
    try:
        conn = sqlite3.connect("db_MIS.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO rde (message) VALUES(?)", (data,))
        conn.commit()
        print("RDE message well received")
    except ParserError as e:
        print(f"Error parsing RDE message: {e}")



def handle_rds_message(data):
    try:
        parsed_message=parse_message(data)
        conn = sqlite3.connect("db_MIS.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO rds (message) VALUES(?)", (data,))
        conn.commit()
        MSH = parsed_message.children[0].children
        PID = parsed_message.children[1].children[0].children
        AL1 = parsed_message.children[1].children[1].children
        PV1 = parsed_message.children[1].children[2].children[0].children
        ORC = parsed_message.children[2].children[0].children
        RXO = parsed_message.children[2].children[1].children[0].children
        TQ1 = parsed_message.children[2].children[2].children[0].children
        RXD = parsed_message.children[2].children[3].children
        RXR = parsed_message.children[2].children[4].children
        print("RDS message well received")
    except ParserError as e:
        print(f"Error parsing RDS message: {e}")


def send_rde_message(rde_server,first_name, last_name,date_of_birth,sex,Phone_home, Phone_business, primary_langage, marital_status,religion,SS_number,birth_place,nationality,doctor,service, date_entry, date_out, bed, chamber,  code, minAmount, maxAmount, Units, Admin_instru, dispense_amount, dispense_unit, frequency, notes, urgent, deadline, allergie1, allergie1_name, medicament):

    # Time of the message 
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")

    first_name_upper = first_name.upper()
    last_name_upper = last_name.upper()
    dob = date_of_birth.replace("-", "")
    admit_date = date_entry.replace("-", "")

    rde_msg = core.Message("RDE_O11")


    #MSH
    rde_msg.msh.msh_4 = "Hospital"
    rde_msg.msh.msh_6 = "Pharmacy"
    rde_msg.msh.msh_7 = formatted_datetime
    rde_msg.msh.msh_9 = "RDE^O11"
    rde_msg.msh.msh_10 = "168715"
    rde_msg.msh.msh_11 = "P"
    rde_msg.msh.msh_12 = "2.5"

    # PID
    rde_msg.add_group("RDE_O11_PATIENT")
    rde_msg.RDE_O11_PATIENT.pid.pid_2 = "1"
    rde_msg.RDE_O11_PATIENT.pid.pid_3 = "A-10001"
    rde_msg.RDE_O11_PATIENT.pid.pid_5 = f"{last_name_upper}^{first_name_upper}"
    # Date of birth with year, month, date, minute, HOUR, second
    rde_msg.RDE_O11_PATIENT.pid.pid_7 = f"{dob}^{000000}" #"DateOfBirth" f"{dob}^{000000}"
    rde_msg.RDE_O11_PATIENT.pid.pid_8 = sex  #"Sex"
    rde_msg.RDE_O11_PATIENT.pid.pid_11 = "1050 Downhill Lane^Ste. 123^Ann Arbor ^MI^99999^USA^B^^WA^" #"Adress"
    rde_msg.RDE_O11_PATIENT.pid.pid_13 = Phone_home #"PhoneHome"
    rde_msg.RDE_O11_PATIENT.pid.pid_14 = Phone_business #"PhoneBusiness"
    rde_msg.RDE_O11_PATIENT.pid.pid_15 = primary_langage #"PrimaryLanguage"
    rde_msg.RDE_O11_PATIENT.pid.pid_16 = marital_status #"MaritalStatus"  
    rde_msg.RDE_O11_PATIENT.pid.pid_17 = religion   #"Religion"
    rde_msg.RDE_O11_PATIENT.pid.pid_19 = str(SS_number) #"SSN"
    rde_msg.RDE_O11_PATIENT.pid.pid_23 = birth_place  #"BirthPlace"
    rde_msg.RDE_O11_PATIENT.pid.pid_28 = nationality #"Nationality"


    #PV1 
    rde_msg.RDE_O11_PATIENT.RDE_O11_PATIENT_VISIT.pv1.pv1_1 =  medicament#"Paracetamol"
    rde_msg.RDE_O11_PATIENT.RDE_O11_PATIENT_VISIT.pv1.pv1_2 = "E" #"PatientClass" E=emergency
    rde_msg.RDE_O11_PATIENT.RDE_O11_PATIENT_VISIT.pv1.pv1_3 = f"^{chamber}^{bed}^^^^^^" # "^123^2^^^^^^" Room, bed, floor
    rde_msg.RDE_O11_PATIENT.RDE_O11_PATIENT_VISIT.pv1.pv1_7 = f"^{doctor}^^^^Dr" # doctor
    rde_msg.RDE_O11_PATIENT.RDE_O11_PATIENT_VISIT.pv1.pv1_10 =  service  #"Service"
    rde_msg.RDE_O11_PATIENT.RDE_O11_PATIENT_VISIT.pv1.pv1_14 = "7" #"Source"
    rde_msg.RDE_O11_PATIENT.RDE_O11_PATIENT_VISIT.pv1.pv1_44 = f"{admit_date}^{000000}" #"AdmitDate"
    if date_out: 
        discharge_date = date_out.replace("-","")
        rde_msg.RDE_O11_PATIENT.RDE_O11_PATIENT_VISIT.pv1.pv1_45 = f"{discharge_date}^{000000}" #"DischargeDate"

    
    #AL1
    rde_msg.RDE_O11_PATIENT.al1.al1_1 = f"{allergie1}" #"2003" #ID
    rde_msg.RDE_O11_PATIENT.al1.al1_3 = allergie1_name #  "Grass"  #"Allergen"



    # ORC
    rde_msg.add_group("RDE_O11_ORDER")
    rde_msg.RDE_O11_ORDER.orc.orc_1 = "1"

    
    #RXE
    rde_msg.RDE_O11_ORDER.rxe.rxe_2 = code #Code
    rde_msg.RDE_O11_ORDER.rxe.rxe_3 = minAmount  #"MinAmount"
    rde_msg.RDE_O11_ORDER.rxe.rxe_4 = maxAmount #"MaxAmount"
    rde_msg.RDE_O11_ORDER.rxe.rxe_5 = Units #"Units"
    rde_msg.RDE_O11_ORDER.rxe.rxe_6 = Admin_instru #"AdministrationInstruction"
    rde_msg.RDE_O11_ORDER.rxe.rxe_10 = dispense_amount #Dispense amount
    rde_msg.RDE_O11_ORDER.rxe.rxe_11 = dispense_unit #Dispense units
    rde_msg.RDE_O11_ORDER.rxe.rxe_15 = "P-15416" #Prescription number
    rde_msg.RDE_O11_ORDER.rxe.rxe_23 = frequency #"Frequency"

    #TQ1
    rde_msg.RDE_O11_ORDER.RDE_O11_TIMING_ENCODED.tq1.tq1_9 = urgent #Urgent or not
    rde_msg.RDE_O11_ORDER.RDE_O11_TIMING_ENCODED.tq1.tq1_13 = f"{deadline}^days"  #"3^days"


    #RXR
    rde_msg.RDE_O11_ORDER.rxr.rxr_1 =  "Route"


    assert rde_msg.validate() is True #check si tous les segments required sont là et que tous les types sont ok
    rde_msg_hl7 = rde_msg.to_er7(trailing_children=True) #envoie du message en format HL7 ligne 
    print (rde_msg.to_er7(trailing_children=True).replace('\r', '\n'))

    if not rde_server.is_alive():
        rde_server.start()

    doctor_host = 'localhost'
    doctor_port = 2575

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((doctor_host, doctor_port))
            s.sendall(rde_msg_hl7.encode())
            print("RDE message sent successfully.")
          
    except Exception as e:
        print(f"Error sending RDE message: {e}")

    


def send_rds_message(rds_server):

    #get patient's info
    #mettre en MAJ

    rds_msg=core.Message("RDS_O13")

    #Header
    rds_msg.msh.msh_4="Pharmacy" #optional
    rds_msg.msh.msh_6="Hospital" #optional
    rds_msg.msh.msh_7="20240430163200" #"DateOfMessage"
    rds_msg.msh.msh_9="RDS^O13"
    rds_msg.msh.msh_10="168715"
    rds_msg.msh.msh_11="P"
    rds_msg.msh.msh_12 = "2.5"


    #PID
    rds_msg.add_group("RDS_O13_PATIENT")
    rds_msg.RDS_O13_PATIENT.pid.pid_2 = "1"
    rds_msg.RDS_O13_PATIENT.pid.pid_3 = "A-10001"
    rds_msg.RDS_O13_PATIENT.pid.pid_5 = "John^Snow" #Name
    rds_msg.RDS_O13_PATIENT.pid.pid_7 = "19810725150900"  #"DateOfBirth"
    rds_msg.RDS_O13_PATIENT.pid.pid_8 = "M"  #"Sex"
    rds_msg.RDS_O13_PATIENT.pid.pid_11 = "1050 Downhill Lane^Ste. 123^Ann Arbor ^MI^99999^USA^B^^WA^" #"Adress"
    rds_msg.RDS_O13_PATIENT.pid.pid_13 =  "0123456789" #"PhoneHome"
    rds_msg.RDS_O13_PATIENT.pid.pid_14 = "9876543210" #"PhoneBusiness"
    #rds_msg.RDS_O13_PATIENT.pid.pid_15 = "English" #"PrimaryLanguage"
    rds_msg.RDS_O13_PATIENT.pid.pid_16 = "Single" #"MaritalStatus"  
    rds_msg.RDS_O13_PATIENT.pid.pid_17 = "Atheist"  #"Religion"
    rds_msg.RDS_O13_PATIENT.pid.pid_19 = "56148113579" #"SSN"
    rds_msg.RDS_O13_PATIENT.pid.pid_23 = "Paris" #"BirthPlace"
    rds_msg.RDS_O13_PATIENT.pid.pid_28 = "Canadian" #"Nationality"


    #AL1
    rds_msg.RDS_O13_PATIENT.al1.al1_1 = "2003" #"AllergyID"
    rds_msg.RDS_O13_PATIENT.al1.al1_3 = "Grass" #"Allergen"


    #PV1 
    rds_msg.RDS_O13_PATIENT.RDS_O13_PATIENT_VISIT.pv1.pv1_2 = "E" #"PatientClass" E=emergency
    rds_msg.RDS_O13_PATIENT.RDS_O13_PATIENT_VISIT.pv1.pv1_3 = "^123^2^^^^^7" #Room, bed, floor
    rds_msg.RDS_O13_PATIENT.RDS_O13_PATIENT_VISIT.pv1.pv1_7 = "^Simons^^^^Dr"  #Doctor
    rds_msg.RDS_O13_PATIENT.RDS_O13_PATIENT_VISIT.pv1.pv1_10 = "GER" #"Service"
    rds_msg.RDS_O13_PATIENT.RDS_O13_PATIENT_VISIT.pv1.pv1_14 = "7" #"Source"
    rds_msg.RDS_O13_PATIENT.RDS_O13_PATIENT_VISIT.pv1.pv1_44 = "20243004065200" #"AdmitDate"
    rds_msg.RDS_O13_PATIENT.RDS_O13_PATIENT_VISIT.pv1.pv1_45 = "20240526154100" #"DischargeDate"


    #ORC
    rds_msg.add_group("RDS_O13_ORDER")
    rds_msg.RDS_O13_ORDER.orc.orc_1 = "1"


    #RXO
    rds_msg.RDS_O13_ORDER.RDS_O13_ORDER_DETAIL.rxo.rxo_2 = "80" # "MinAmount"
    rds_msg.RDS_O13_ORDER.RDS_O13_ORDER_DETAIL.rxo.rxo_3 = "300" #"MaxAmount"
    rds_msg.RDS_O13_ORDER.RDS_O13_ORDER_DETAIL.rxo.rxo_4 = "mg" #"Units"
    rds_msg.RDS_O13_ORDER.RDS_O13_ORDER_DETAIL.rxo.rxo_7 = "Tablets" #"AdministrationInstruction"
   

    #TQ1
    rds_msg.RDS_O13_ORDER.RDS_O13_TIMING.tq1.tq1_2="100^mg"
    rds_msg.RDS_O13_ORDER.RDS_O13_TIMING.tq1.tq1_3="H1" # frequency of 100mg/h


    #RXD
    rds_msg.RDS_O13_ORDER.rxd.rxd_1="1"
    rds_msg.RDS_O13_ORDER.rxd.rxd_2 = "Paracetamol" #"Code"
    rds_msg.RDS_O13_ORDER.rxd.rxd_3 = "20240521030000" #"DateDispensed"
    rds_msg.RDS_O13_ORDER.rxd.rxd_4 = "1" #"DispensedAmount"
    rds_msg.RDS_O13_ORDER.rxd.rxd_5 = "kg" #"DispensedUnits"
    rds_msg.RDS_O13_ORDER.rxd.rxd_6 = "Tablets" #"AdministrationType"
    rds_msg.RDS_O13_ORDER.rxd.rxd_7 = "P-1516" #"PrescriptionNumber"
    rds_msg.RDS_O13_ORDER.rxd.rxd_12 = "300^mg" #"TotalDailyDose"
    rds_msg.RDS_O13_ORDER.rxd.rxd_19 = "20260101000000" #"ExpirationDate"


    #RXR
    rds_msg.RDS_O13_ORDER.rxr.rxr_1="1"
    

    assert rds_msg.validate() is True
    rds_msg_hl7 = rds_msg.to_er7(trailing_children=True)
    print (rds_msg.to_er7(trailing_children=True).replace('\r', '\n'))

    if not rds_server.is_alive():
        rds_server.start()
    
    pharmacy_host = 'localhost'
    pharmacy_port = 2575

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((pharmacy_host, pharmacy_port))
            s.sendall(rds_msg_hl7.encode())
            print("RDS message sent successfully.")
    except Exception as e:
        print(f"Error sending RDS message: {e}")


def get_rde_segments(i):
    conn = sqlite3.connect("db_MIS.db")
    cur = conn.cursor()
    query= "SELECT message FROM rde WHERE id=?"
    cur.execute(query, (i,))
    message=cur.fetchone()
    parsed_message = parse_message(message[0] if isinstance(message, tuple) else message)
    MSH = parsed_message.children[0].children
    PID = parsed_message.children[1].children[0].children
    AL1 = parsed_message.children[1].children[2].children
    PV1 = parsed_message.children[1].children[1].children[0].children
    ORC = parsed_message.children[2].children[0].children
    RXE = parsed_message.children[2].children[1].children
    TQ1 = parsed_message.children[2].children[2].children[0].children
    RXR = parsed_message.children[2].children[3].children
    cur.execute("SELECT timestamp FROM rde WHERE message=?",(message[0] if isinstance(message, tuple) else message,))
    date=cur.fetchone()[0]
    return PID,AL1,PV1,RXE,TQ1,date

def get_command_info(i):
    
    PID,AL1,PV1,RXE,TQ1,date=get_rde_segments(i)
    key=PID[0].value
    id=PID[1].value
    lastname=PID[2].children[0].value
    name=PID[2].children[1].value
    birthdate=PID[3].value
    birthdate=f"{birthdate[:4]}-{birthdate[4:6]}-{birthdate[6:]}"
    sex=PID[4].value
    adress=PID[5].value.replace('^',' ')
    phone_home=PID[6].value
    phone_business=PID[7].value
    language=PID[8].value
    marital_satus=PID[9].value
    religion=PID[10].value
    SS_number=PID[11].value
    birth_place=PID[12].value
    nationality=PID[13].value

    allergy_id=AL1[0].value
    allergy=AL1[1].value

    patient_class=PV1[1].value
    location=PV1[2].value.split('^')
    components = [component for component in location if component]
    room=components[0] if len(components) > 0 else None
    bed=components[1] if len(components) > 1 else None
    floor=components[2] if len(components) > 2 else None
    doctor=PV1[3].value.split('^')[1]
    service=PV1[4].value
    source=PV1[5].value
    admission_date=PV1[6].value
    if len(PV1)>7:
        discharge_date=PV1[7].value
    else:
        discharge_date=None

    medicine=PV1[0].value
    order_date=date
    min=RXE[1].value
    max=RXE[2].value
    units=RXE[3].value
    instruction=RXE[4].value
    dispense_amount=RXE[5].value
    dispense_unit=RXE[6].value
    frequency=RXE[8].value


    return{
        "last_name": lastname,
        "first_name": name,
        "id": id,
        "sex": sex,
        "address": adress,
        "phone_number": phone_business,
        "birthdate": birthdate,
        "ssn": SS_number,
        "religion": religion,
        "nationality": nationality,
        "status": patient_class,
        "floor": floor,
        "room": room,
        "bed": bed,
        "service": service,
        "source": source,
        "doctor_name": doctor,
        "allergy": allergy
    },{
        "medicine": medicine,
        "date": order_date,
        "minimum_amount": min,
        "maximum_amount":max,
        "units":units,
        "instruction":instruction,
        "dispense_amount":dispense_amount,
        "dispense_units":dispense_unit,
        "frequency":frequency
    }

'''

if __name__ == "__main__":
    pharmacy_host = 'localhost'
    pharmacy_port = 2575
    doctor_host = 'localhost'
    doctor_port = 2575

    #rde_server = HL7Server(pharmacy_host, pharmacy_port, handle_rde_message)
    rds_server = HL7Server(doctor_host, doctor_port, handle_rds_message)

    send_rds_message(rds_server)


'''