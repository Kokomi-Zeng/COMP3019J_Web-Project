# COMP3019J_Web-Project

## Team Member

- Zhang Ziyi    21207272
- Zeng Lingyue    21207269
- Yuan Shiyang    21207285

## Product Ranking Website Description

The website is a product ranking website using Python, Flask, Mysql, Ajax, HTML, CSS, JavaScript.

- For registered sellers, the seller can change his/her personal information, view his/her own products, view product information, search for his/her own products, modify product information, view ratings of his/her own products, and upload a catalogue of products, including full descriptions, pictures and prices.

- For registered buyers, the buyer can change his/her personal information, view the products he/she has purchased, view all product information, search for all products, view all ratings for the product, rate a product (including star rating and text), purchase products, fund his/her account, and view the balance of his/her account.

- For unregistered users, he/she can login, register, view the top 10 rated products, observe feedback from the top 5 positive and bottom 5 negative reviews.

## Additional Configuration

After cloning the project to your local machine using the following command: 'git clone https://github.com/Kokomi-Zeng/COMP3019J_Web-Project.git'

Open the project in PyCharm and follow the steps below:

1. **Setting up Flask Server in PyCharm**:  

   - Navigate to `Run/Debug Configurations` in the top-right corner.  
   - Click the plus icon (`+`) on the top-left and select `Flask Server`.  
   - Within the 'Configuration' tab, set:     
     - `Target type` to `Script Path`    
     - `Target` to your project folder's path  
     - Ensure `FLASK_DEBUG` is checked.   
   - In the 'Environment' section:     
     -  Select your Python interpreter (Python 3.9 is recommended).    
     -  For `Working directory`, choose your project folder's path.   
     -  Click OK/Apply.

2. **Installing Python Packages**:

   - pip install flask 
   - pip install pymysql 
   - pip install flask-sqlalchemy
   - pip install flask-migrate

3. **Database Configuration**:

   You have two choices:

   - **Option A**: Initialize the Database
     - Create a database named `flaskdb` in MySQL.
     - Then run the commands to initialize and populate the tables: 
       - flask db init
       - flask db migrate
       - flask db upgrade
   - **Option B**: Use an Existing Database
     - Create a database named `flaskdb` in MySQL.
     - Import the SQL file provided in the project to have a database with data.

4. **Configuration File**:

   Add a `config.py` file to the project root with the following content: 

   ```python
   HOSTNAME = "127.0.0.1"
   PORT = 3306
   DATABASE = "flaskdb"
   USERNAME = "YOUR MYSQL USERNAME"
   PASSWORD = "YOUR MYSQL PASSWORD"
   DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
   SQLALCHEMY_DATABASE_URI = DB_URI
   SECRET_KEY = "123456"
   ```

   
