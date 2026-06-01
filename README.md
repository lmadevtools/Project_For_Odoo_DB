# Project_For_Odoo_DB
Project_Odoo with PostGre DB

To use psycopg2 :  
[Link from geelsforgeeks for step by step install](https://www.geeksforgeeks.org/python/how-to-install-psycopg2-in-visual-studio-code/)

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

