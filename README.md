# Project_For_Odoo_DB
Project_Odoo with PostGre DB

Classes (contain the business class)  
|------ __init__.py          : to marks the directory Classes as a regular package  
|------ customer.py          : class to manage the customers  
|------ inventory.py         : class to centralize the actions with the others business class (customer, order, product) and manage JSON load / save files  
|------ order.py             : class to manage the orders  
|------ product.py           : class to manage the products  
|------ stock_move.py        : class to manage the stock moves (add / remove in stock)    
Data    (created at start if doesn't exist. This directory will contains the .json files)  
|------ data_customers.json  : file containing the customers in JSON format  
|------ data_orders.json     : file containing the orders in JSON format  
|------ data_products.json   : file containing the products in JSON format  
|------ stock_moves.csv      : file containing the stock_moves export in CSV format  
|------ stock_moves.json     : file containing the stock_moves in JSON format  
Logs    (created at start if doesn't exist. This directory will contains the logs of the application)  
|------ app.log              : log file  
|------ run_tests.txt        : log file for the result of the tests  
Sql
|------ drop_db.sql          : SQL script to delete tables  
|------ init_db.sql          : SQL script to init tables  
Tests  (contains the units test)  
|------ __init__.py          : to marks the directory Tests as a regular package  
|------ test_customer.py     : tests for the class customer  
|------ test_helper          : tests for the helper classes  
|------ test_inventory       : tests for the class inventory  
|------ test_order           : tests for the class order and orderline  
|------ test_product         : tests for the class product  
|------ test_stock_move      : tests for the class stock_move  
Utils   (contains Utils classes used by others classes)  
|------ __init__.py          : to marks the directory Utils as a regular package
|------ db_connector.py      : class to manage the connection and queries to the DB  
|------ helper.py            : class containing functions used by others class as TimeStamp function, Logs functions, etc  
|------ mail_sender          : (NOT_USED) should manage the mail sending part. (Should be used to automatically send mail to order low stock products) 
|------ queries.py           : list of queries used in the project.  
|------ validator.py         : class containing validating functions used by others class as is_mail_valid to check if the format of a mail is correct   
config.py                    : config file (containing path, etc)  
main.py                      : first main file to test function  
main_menu.py                 : main file with menu for users  (CLI)   
main_test_DB.py              : main file with DB tests   
run_tests.py                 : execute the tests  












------------------

To use psycopg2 :  
[Link from geeksforgeeks for step by step install](https://www.geeksforgeeks.org/python/how-to-install-psycopg2-in-visual-studio-code/)

To install psycopg2, we need to use the terminal in VS Code.  
Before that, let's create a virtual environment for our Python projects to keep dependencies isolated.  

In the terminal, navigate to the project folder using cd project_directory. Then, run the following command to create a virtual environment:  
python -m venv venv  

Activate Virtual Environment,  
.\venv\Scripts\activate  #for windows  
source venv/bin/activate #for macOS/Linux  

--------------

[in case of PSSECURITYERROR](https://www.easytutoriel.com/powershell-execution-de-scripts-est-desactivee.html)
<img width="868" height="323" alt="image" src="https://github.com/user-attachments/assets/32b5b9a8-3d6c-4a26-9eb0-bff0b9a04c64" />

In PowerShell :  
Set-ExecutionPolicy Unrestricted -Scope "CurrentUser"  

--------------

Step 3: Install psycopg2  
Now that our environment is ready, we can install psycopg2 using pip.  
pip install psycopg2  

------------
venv.zip contains all the file installed in the folder venv.  
