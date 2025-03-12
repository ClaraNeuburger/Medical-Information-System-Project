# Project MIS

The aim of this project was to simulate a hospital pharmacy using concepts covered in the Medical Information Systems course.

By managing pharmacy stock through a database, orders can be placed via HL7 messages. These orders are received, processed, and the medication is dispensed accordingly.

The interface is accessible to both doctors and pharmacists. Physicians can place orders and track their status, while pharmacists can manage inventory, place restocking orders, and prepare medications requested by physicians.


When you first open the project: 
1) Execute load_db.py to load the database
2) Execute Import_db.py to add data in the tables (see detail in the file)
3) Execute add_medicaments.py to add medicine in the tables (see detail in the file)
4) Execute add_rde_table.py to store HL7 messages 
5) Execute stock_database_insert.py to manage the stock of medicines
6) Execute stock_status_database_insert.py to know the delivery status in the tables
7) Execute Choose_doctor.py which allows you to choose the physician's profile
8) Execute Pharma.py which allows you to manage the orders
