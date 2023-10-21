# COMP3019J_Web-Project

## Product Ranking Website
The website allows registered sellers to upload a catalogue of products, complete with descriptions, images, and prices. It also permits registered buyers to view products, leave both positive and negative feedback, rate the products via a visual indicator such as stars, and provide textual comments. Furthermore, unregistered users can view top-rated products and observe feedback from the top-5 positive comments as well as the lowest-5 negative comments.

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

   
