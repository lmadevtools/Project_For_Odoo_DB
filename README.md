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
|------ data_customers.json  : (NOT_USED_ANYMORE) file containing the customers in JSON format  
|------ data_orders.json     : (NOT_USED_ANYMORE) file containing the orders in JSON format  
|------ data_products.json   : (NOT_USED_ANYMORE) file containing the products in JSON format  
|------ stock_moves.csv      : file containing the stock_moves export in CSV format  
|------ stock_moves.json     : (NOT_USED_ANYMORE) file containing the stock_moves in JSON format  
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
|------ mail_sender          : (NOT_USED) manage the mail sending part. (Should be used to automatically send mail to order low stock products)  
|------ queries.py           : list of queries used in the project.  
|------ validator.py         : class containing validating functions used by others class as is_mail_valid to check if the format of a mail is correct   
config.py                    : config file (containing path, etc)  
main.py                      : first main file to test function  
main_menu.py                 : main file with menu for users  (CLI)   
main_test_DB.py              : main file with DB tests   
run_tests.py                 : execute the tests  

-----------------

updates:

27/05/2026 :

  -  Writing of the classes customer, product and order

28/05/2026 :

  -  Writing of the class inventory
  -  Management of the classes customer, product, order in JSON
  -  Structure of the projects (folders Classes, Data, ...)
  -  Added Utils ( helper, validator) and a config file
  -  Management of a log
  -  Management of the stock_moves, save in json and export in CSV
  -  Update of the auto generated ID for order ( CMD/YEAR/XXXX ) based on param located in config.py
  -  Writing of the README

29/05/2026 :

  -  Writing of the tests cases + save of the result in a file run_tests.txt
  -  Writing of the main_menu.py (Command Line Interface (CLI))
  -  Added Utils/mail_sender.py to manage mail. Not used for the moment. But should be interesting to manage auto order per mail to the supplier for low stock
  -  Added the necessary Getter/Setter in the differents classes.
  -  Wrote the personnal note for the explanation of different of my coding choices.

01/06/2026 :  
  - Creation of the file init_db.sql and drop_db.sql
  - Writing class db_connector and queries
  - Put in comment JSON code and udpating it by DB
  - Writing the unit test for DB
  - Writing the main_test_DB to try the DB access
  - Writing the db_faker to complete DB with fake data

---------

Personnal note:

1)   The class mail_sender is not used. I just put it in case we would like to implement an automatic order for low stock products.

2)  Using to_dict instad of __dict__ ?
        to manage what I want to display if I need to get only some infos, and leaving __dict__ at his normal use if I need to display everything (including eventuals intern var)
        denormalisation (exemple : in order, I want to get the product.name)

3)   classmethod from_dict ?
    if I call
    p=product then product(???) #I don't have the informations here.
    then
    p.from_dict(data) #a little late : p already exists.
    I should have done a p_load_from_dict(data) but I lose all the goal of the checks done at the creation, and I will get ValueError (and no way to disable checks)
    Also, it avoid an eventual error occuring between the creation and the p_load_from_dict...

4) __str__ is used as display for user, while __repr__ is used as a display for dev, with more technical information.

5)  !r in repr add a ' : this permit to see, by exemple ID = 'P1', instead of ID = P1, and to be sure it is a string

6)  In Order, I used a property for the subtotal. As it is based on unitprice*quantity, it is a way to always have an up-to-date value, even if we change the quantity.

7)   Getter/Setter :

    order.py :
    °status change only by confirm/cancel/mark_done
    °total already in @property.
    °lines should not be modified directly.
    stock_move.py :
    ° read only. stock move should not be modified after creation.

8) Using @patch to works with mock (fake object to avoir connecting to the true DB)  

------------------
Other informations :  
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

for faker :
pip install faker
------------
venv.zip contains all the file installed in the folder venv.  
