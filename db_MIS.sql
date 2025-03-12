CREATE TABLE IF NOT EXISTS person (
	id integer primary key,
	first_name TEXT NOT NULL,
	middle_name text,
	last_name TEXT NOT NULL,
	date_of_birth INT NOT NULL,
	birth_place text,  
	sex VARCHAR(1) NOT NULL,
	email TEXT,
	Phone_home INTEGER,
	Phone_business INTEGER,
	primary_langage TEXT,
	nationality text,
	national_number INTEGER NOT NULL
);
-- the type for date_of_birth is "YYYYMoMoDDHHMiMiSS"
-- for sex : "F" or "M"


CREATE TABLE IF NOT EXISTS patient (
	id_patient integer primary key,
	id_person INTEGER NOT NULL UNIQUE,
	id_doctor INTEGER NOT NULL,
	patient_class varchar(1) NOT NULL,
	chamber INTEGER,
	bed INTEGER,
	patient_source text DEFAULT "9",
	allergie1 INTEGER,
	allergie2 INTEGER,
	curent_pathologies INTEGER NOT NULL,
	past_pathologies INTEGER,
	date_entry DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
	date_out DATE,
	service INTEGER NOT NULL,
	SS_number INTEGER NOT NULL,
	marital_status TEXT,
	religion TEXT DEFAULT NULL,
FOREIGN KEY(id_person) REFERENCES person(id),
FOREIGN KEY(id_doctor) REFERENCES doctor(id_doctor),
FOREIGN KEY(curent_pathologies) REFERENCES pathologies(id_pathology),
FOREIGN KEY(past_pathologies) REFERENCES pathologies(id_pathology),
FOREIGN KEY(service) REFERENCES service(id_service),
FOREIGN KEY (allergie1) REFERENCES allergies(id),
FOREIGN KEY (allergie2) REFERENCES allergies(id)
);
-- different patient_class ; examples : 
--"B" : Obstetrics;
--"E" : Emergency 
-- "I" : Inpatient;
-- "O" : Outpatient;
-- "P" : Preadmit;
-- "R" : Recurring patient
CREATE TABLE IF NOT EXISTS allergies (
    id INTEGER PRIMARY KEY,
    name TEXT
);



CREATE TABLE IF NOT EXISTS pathologies (
	id_pathology INTEGER primary key,
	name TEXT NOT NULL,
	description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS service (
	id_service INTEGER primary key,
	name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prescription (
	id_prescription TEXT primary key,
	id_concerned_patient INTEGER not null,
	id_doctor INTEGER NOT NULL,
	medicament INTEGER NOT NULL,
	give_min_amout float NOT NULL,
	give_max_amout float,
	give_units TEXT NOT NULL,
	admin_instruction TEXT,
	dispense_amount float,
	dispense_units text,
	frequency text,
	notes TEXT,
FOREIGN KEY (id_concerned_patient) REFERENCES patient (id_patient),
FOREIGN KEY(medicament) REFERENCES medicament(id_medicament),
FOREIGN KEY(id_doctor) REFERENCES doctor(id_doctor)
);


CREATE TABLE IF NOT EXISTS MedicineDetails (
	medicament INTEGER NOT NULL,
	code float NOT NULL,
	give_min_amout float NOT NULL,
	give_max_amout float,
	give_units TEXT NOT NULL,
	admin_instruction TEXT,
	dispense_amount float,
	dispense_units text,
	frequency text,
	notes TEXT
);

CREATE TABLE IF NOT EXISTS doctor (
	id_doctor INTEGER primary key,
	id_person INTEGER NOT NULL,
	service INTEGER NOT NULL, 
	statut TEXT NOT NULL,
	login TEXT NOT NULL,
	password TEXT NOT NULL,
FOREIGN KEY(id_person) REFERENCES person(id),
FOREIGN KEY(service) REFERENCES service(id_service)
);
-- status is Intern (I), externe (E) or physician (P)

CREATE TABLE IF NOT EXISTS medicament (
	id_medicament INTEGER primary key,
	name TEXT NOT NULL,
	medicament_class INTEGER NOT NULL,
FOREIGN KEY(medicament_class) REFERENCES class_medicament(id_class)
);

CREATE TABLE IF NOT EXISTS Incompatibilities (
	id_incompatibility INTEGER primary key NOT NULL,
	description TEXT NOT NULL,
	concerned_class_medicament1 INTEGER NOT NULL,
	concerned_class_medicament2 INTEGER NOT NULL,
	concerned_class_medicament3 INTEGER
);

CREATE TABLE IF NOT EXISTS class_medicament (
	id_class int primary key,
	description_class_med text
);

/*FOREIGN KEY(id_person) REFERENCES person(id)
FOREIGN KEY(doctor) REFERENCES doctor(id_doctor)
FOREIGN KEY(allergie1) REFERENCES class_medicament(id_class)
FOREIGN KEY(curent_pathologies) REFERENCES pathologies(id_pathology)
FOREIGN KEY(past_pathologies) REFERENCES pathologies(id_pathology)
FOREIGN KEY(service) REFERENCES service(id_service)

FOREIGN KEY (id_concerned_patient) REFERENCES patient (id_patient)
FOREIGN KEY(medicament) REFERENCES medicament(id_medicament)
FOREIGN KEY(id_doctor) REFERENCES doctor(id_doctor)

FOREIGN KEY(id_person) REFERENCES person(id)
FOREIGN KEY(service) REFERENCES service(id_service)

FOREIGN KEY(medicament_class) REFERENCES class_medicament(id_class)

FOREIGN KEY(concerned_class_medicament1) REFERENCES class_medicament(id_class)
FOREIGN KEY(concerned_class_medicament2) REFERENCES class_medicament(id_class)
FOREIGN KEY(concerned_class_medicament3) REFERENCES class_medicament(id_class)*/
