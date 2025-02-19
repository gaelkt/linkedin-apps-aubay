
from sqlalchemy import create_engine, text

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()
import logging

host=os.environ['DB_HOST'] 
port=os.environ.get("DB_PORT")
user=os.environ['DB_USER']
password=os.environ['DB_PASSWORD'] 
database_name=os.environ['DB_NAME']  
table_jobs = os.environ['DB_TABLE_JOB']  
table_applications = os.environ['DB_TABLE_APPLICATIONS'] 
table_scores = os.environ['DB_TABLE_SCORES']
table_tasks = os.environ['DB_TABLE_TASKS'] 
celery_table = os.environ['CELERY_TABLE_TASKS'] 

database_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"

def generate_engine():
    engine = create_engine(database_url)
    return engine

engine = generate_engine()

def createDB():

    '''
    Create a database database_name

    '''    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(host=host,port=port,user=user, password=password)
        if connection.is_connected():
            cursor = connection.cursor()
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            logging.info(f"Database '{database_name}' created successfully!")
        else:
            logging.error(f"Unable to connect to MySQL with host {host} and user {user}")
    except Error as e:
        print(f"Error: '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()






def refreshDB():

    '''
    Check if the JOBS table exist. If not create a new one

    Inputs:
        - host: database host
        - user: database user
        - password: database password
        - database_name: database name
        - table_job: JOBS table to be created

    Output:
        None

    '''

    try:

        # We check if the database exist
        db_exists = checkDB()

        if not db_exists:
            createDB()
            
        # Checking JOBS table
        if not checkTable(table_name=table_jobs):
        
            # JOBS table does not exist. We Create a new one
            createJobsTable(table_jobs=table_jobs)
            logging.info(f"Job table {table_jobs} has been created successfully !") 
        else:
            logging.info(f"The Job table {table_jobs} already exists ")

        
        # Checking APPLICATIONS table
        if not checkTable(table_name=table_applications):
            # APPLICATIONS table does not exist. We Create a new one
            createApplicationTable(table_applications=table_applications)
            logging.info(f"Application table {table_applications} has been created successfully !") 
        else:
            logging.info(f"The Application table {table_jobs} already exists ")


        # Checking Task tablecelery_table
        if not checkTable(table_name=table_tasks):
            # APPLICATIONS table does not exist. We Create a new one
            createTaskTable(table_tasks=table_tasks)
            logging.info(f"Task table {table_tasks} has been created successfully !") 
        else:
            logging.info(f"The Task table {table_tasks} already exists ")
            
        # Checking Task table celery_table
        # Checking Task table celery_table
        if not checkTable(table_name=celery_table):
            # APPLICATIONS table does not exist. We Create a new one
            createTaskTable(table_tasks=celery_table)
            logging.info(f"Task table {celery_table} has been created successfully !") 
        else:
            logging.info(f"The Task table {celery_table} already exists ")


        # Checking SCORES table
        if not checkTable(table_name=table_scores):
            # APPLICATIONS table does not exist. We Create a new one
            createScoreTable(table_scores=table_scores)
            logging.info(f"Score table {table_scores} has been created successfully !") 
        else:
            logging.info(f"The scores table {table_scores} already exists ")   

    except Error as e:
        logging.critical(f"Error: {e}")
    finally:
        logging.info("Finish with function refreshDB ")
    return 0


def checkTable(table_name):
    '''
    Check if a particular table exists

    Inputs:

        - table_name: table to check

    Output:
        None

    '''
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect( host=host,port=port,user=user,password=password)

        if connection.is_connected():
            cursor = connection.cursor()
            # Query to check if the table exists
            query = f"""SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{database_name}' AND table_name = '{table_name}';
            """
            cursor.execute(query)
            result = cursor.fetchone()
            # Check if table exists
            if result[0] > 0:
                logging.info(f"Table '{table_name}' already exists in the database '{database_name}'.")
                return True
            else:
                logging.info(f"Table '{table_name}' does not exist in the database '{database_name}'.")
                return False
        
        else:
            logging.error(f"Unable to connect to MySQL with host {host} and user {user}")

    except Error as e:
        logging.error(f"Error in the function check_table_exists: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




def checkDB():

    '''
    Check if MySQL is properly set up and if database exists

    '''


    try:
        # Connect to MySQL server
        try:
            logging.info(f"host={host} user={user} database={database_name}, jobs={table_jobs} and password={password}")
            connection = mysql.connector.connect(host=host,port=port, user=user, password=password)
            logging.info("Connected to MySQL Server")
        except Exception as e:
            logging.error(f"Unable to connect to MySQL with host {host} user={user} database={database_name} and password={password}")
            logging.error("Check MySQL Server or credentials and try again")
            logging.error(e)
            print(e)
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            if database_name in databases:
                logging.info(f"Database {database_name} already exist ")
                return True
            else:
                logging.info(f"Database {database_name} does not exist ")
                return False
        else:
            logging.error(f"Unable to connect to MySQL database for user {user} and host {host}")
    except Error as e:
        logging.error(f"Error in the function check_database_exists: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




def createScoreTable(table_scores):
    logging.info(f"......Creating Scores table {table_scores}")
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(host=host,port=port, user=user, password=password, database=database_name)

        if connection.is_connected():
            cursor = connection.cursor()
            
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_scores} (
                Id VARCHAR(255) PRIMARY KEY,
                roleId VARCHAR(255),
                score INT,
                experience INT,
                diplome INT,
                certifications INT,
                hard_skills INT,
                soft_skills INT,
                langues INT
            )
            """
            # Execute the SQL command
            cursor.execute(create_table_query)
            connection.commit()  # Save changes
            logging.info(f"Table {table_scores} created successfully.")

    except Error as e:
        logging.error(f"Error in the function createScoreTable: {e}")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()
 


            
def createJobsTable(table_jobs):
    logging.info(f"......Creating Job table {table_jobs}") 
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(host=host,port=port, user=user, password=password, database=database_name)

        if connection.is_connected():
            cursor = connection.cursor()
            # SQL command to create the jobs table


            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_jobs} (
                roleId VARCHAR(255) PRIMARY KEY,
                role VARCHAR(255) NOT NULL,
                isActive BOOLEAN DEFAULT TRUE,
                date DATE,
                path VARCHAR(255) NOT NULL,
                diplome VARCHAR(255),
                experience INT,
                certifications TEXT,
                hard_skills TEXT,
                langues TEXT,
                soft_skills TEXT
            )
            """
            # Execute the SQL command
            cursor.execute(create_table_query)
            connection.commit()  # Save changes
            logging.info(f"Table {table_jobs} created successfully !.")

    except Error as e:
        logging.error(f"Unable to create job table {table_jobs} in the function createJobsTable: Error {e} \n")

        raise Exception(e)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()




def get_inactive_role_ids(host, user, password, database_name, table_name):
    try:
        # Connect to the MySQL database
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=host,   # e.g., 'localhost'
            port=port,    
            user=user,   # e.g., 'root'
            password=password,
            database=database_name # e.g., 'test_db'
        )

        cursor = connection.cursor()

        # Query to get RoleID of jobs where is_active = 0
        query = f"SELECT RoleID FROM {table_name} WHERE is_active = 1"
        cursor.execute(query)

        # Fetch all results
        result = cursor.fetchall()

        # Extract RoleID values into a list
        role_ids = [row[0] for row in result]

        return role_ids

    except mysql.connector.Error as err:
        logging.error(f"Error in the function get_inactive_role_ids. Error {err}")
        raise Exception(err)

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection is not None:
            connection.close()


def getRole(roleId):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(host=host,port=port, user=user, password=password)

        cursor = connection.cursor()

        # Query to get Role for a specific RoleID
        query = f"SELECT role FROM {table_jobs} WHERE roleId = %s"
        cursor.execute(query, (roleId,))

        # Fetch the result
        result = cursor.fetchone()

        # Check if a result was found
        if result:
            return result[0]  # Return the Role value
        else:
            return None  # Return None if no matching RoleID is found

    except mysql.connector.Error as err:
        logging.error(f"Error in the function getRole: {err}")
        return None

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection is not None:
            connection.close()




def createApplicationTable(table_applications):

    logging.info(f"Creating table: {table_applications}")

    '''
    Create table for applications

    Inputs:
        - table_name: application table to be created

    Output:
        None


    '''
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(host=host, port=port,user=user, password=password, database=database_name)
        if connection.is_connected():
            cursor = connection.cursor()
            # SQL command to create the jobs table
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_applications} (
                Id VARCHAR(255) PRIMARY KEY,
                roleId VARCHAR(255),
                name VARCHAR(255),
                role VARCHAR(255) NOT NULL,
                date DATE,
                score FLOAT,
                alternative_role VARCHAR(255) NOT NULL,
                alternative_score FLOAT,
                diplome VARCHAR(255),
                annee_diplome INT,
                experience FLOAT,
                certifications TEXT,
                hard_skills TEXT,
                langues TEXT,
                soft_skills TEXT,
                path TEXT
            )
            """
            # Execute the SQL command
            cursor.execute(create_table_query)
            connection.commit()  # Save changes
            logging.info(f"Applciation table {table_applications} created successfully.")

    except Error as e:
        logging.error(f"Error in the function createApplicationTable: {e}")
        raise Exception(e)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()



def getRoleId(role):
    try:
        if role == None:
            logging.error(f"role can not be None. Error in function getRoleId")
            raise Exception("role can not be None. Error in function getRoleId")

        
        # Connect to the MySQL database
        connection = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database_name)

        cursor = connection.cursor()

        # Define the query
        query = f"""
        SELECT roleId FROM {table_jobs}
        WHERE role = %s
        LIMIT 1;
        """

        # Execute the query with parameters
        cursor.execute(query, (role,))

        # Fetch the result
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        # Return RoleID if found, otherwise None
        return result[0] if result else None

    except mysql.connector.Error as e:
        logging.error(f"Error in the function getRoleId for the role={role}. Error = {e}")
        raise Exception(e)

    # finally:
    #     # Close the connection
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()




def getJobData(roleId):

    if roleId == None:
        logging.error("roleId can't be None. Error in getJobData(roleId) function")
        raise Exception("roleId can't be None. Error in getJobData(roleId) function")
    
    engine = create_engine(database_url)
    
    index_parameters ={"experience":0, "diplome":1, "certifications":2, "hard_skills":3, "soft_skills":4, "langues":5, "role":6, "path":7, "date":8}
    query = text(f"SELECT experience, diplome, certifications, hard_skills, soft_skills, langues, role, path, date FROM {table_jobs} WHERE roleId = :value")
    
    try:
        
        with engine.connect() as connection:
            
            with connection.begin():
                
                result = connection.execute(query, {"value": roleId})
                rows = result.fetchall()

                job_data = {}
                job_data["experience"] = rows[0][0]
                job_data["diplome"] = rows[0][1]
                job_data["certifications"] = rows[0][2]
                job_data["hard_skills"] = rows[0][3]
                job_data["soft_skills"] = rows[0][4]
                job_data["langues"] = rows[0][5]
                job_data["role"] = rows[0][6]
                job_data["path"] = rows[0][7]
                job_data["date"] = rows[0][8]
                
                return index_parameters, job_data
            
    except Exception as e:
        logging.error(f"Error in getJobData with roleId = {roleId}. Error = {e}")
        raise Exception(e)
            
            
        
def createTaskTable(table_tasks):

    logging.info(f"Creating table: {table_tasks}")

    '''
    Create table for task

    Inputs:
        - table_tasks: Task table to be created

    Output:
        None


    '''
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(host=host, port=port,user=user, password=password, database=database_name)
        if connection.is_connected():
            cursor = connection.cursor()
            # SQL command to create the jobs table
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_tasks} (
            Id VARCHAR(255) NOT NULL PRIMARY KEY,
            user VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            date DATETIME NOT NULL,
            status VARCHAR(255) NOT NULL,
            message VARCHAR(255) NOT NULL
        );
        """
            
            # Execute the SQL command
            cursor.execute(create_table_query)
            connection.commit()  # Save changes
            logging.info(f"Task table {table_tasks} created successfully.")

    except Error as e:
        logging.error(f"Error in the function createTaskTable: {e}")
        raise Exception(e)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()


def createTaskCeleryTable(celery_table):

    logging.info(f"Creating table: {celery_table}")

    '''
    Create table for task

    Inputs:
        - celery_table: Task table to be created

    Output:
        None


    '''
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(host=host, port=port,user=user, password=password, database=database_name)
        if connection.is_connected():
            cursor = connection.cursor()
            # SQL command to create the jobs table
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {celery_table} (
            Id VARCHAR(255) NOT NULL PRIMARY KEY,
            user VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL,
            date DATETIME NOT NULL,
            status VARCHAR(255) NOT NULL,
            message VARCHAR(255) NOT NULL
        );
        """
            
            # Execute the SQL command
            cursor.execute(create_table_query)
            connection.commit()  # Save changes
            logging.info(f"Task table {celery_table} created successfully.")

    except Error as e:
        logging.error(f"Error in the function createTaskTable: {e}")
        raise Exception(e)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()



def check_application_exists(name, role):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
        host=os.environ['DB_HOST'],       # Replace with your database host
        port=os.environ['DB_PORT'],
        user=os.environ['DB_USER'],       # Replace with your database user
        password=os.environ['DB_PASSWORD'],  # Replace with your database password
        database=os.environ['DB_NAME']   # Replace with your database name
        )

        table_applications = os.environ['DB_TABLE_APPLICATIONS']

        cursor = connection.cursor()

        # Define the query
        query = f"""
        SELECT 1 FROM {table_applications}
        WHERE name = %s AND Role = %s
        LIMIT 1;
        """

        # Execute the query with parameters
        cursor.execute(query, (name, role))

        # Fetch the result
        result = cursor.fetchone()

        # Return True if there is a match, otherwise False
        return result is not None

    except mysql.connector.Error as e:
        logging.error(f"Error in the function check_applicantion_exists with applicant={name} and role={role}")
        logging.error(f"Error: {e}")
        return False

    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()


import mysql.connector

def getApplication(role, begin_date, end_date):
    """
    Fetches application details for a specific role from the applications table in the MySQL database.

    Args:
        role_value (str): The role value to filter by.

    Returns:
        list: A list of dictionaries containing the application details.
    """
    # Database connection details
    connection = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database_name)

    cursor = connection.cursor()


    try:
        # Query to fetch applications for a specific role
        query = f"""
        SELECT Id, roleId, name, role, date, score, experience, experience, 
               diplome, annee_diplome, alternative_score, alternative_role, certifications,
               hard_skills, soft_skills, langues, path
        FROM {table_applications}
        WHERE role = %s AND date BETWEEN %s AND %s
        ORDER BY score DESC;;
        """
        # Execute the query with the role value
        cursor.execute(query, (role, begin_date, end_date))

        # Fetch all matching rows
        rows = cursor.fetchall()

        # Get column names from the cursor description
        columns = [desc[0] for desc in cursor.description]

        # Convert rows into a list of dictionaries
        results = [dict(zip(columns, row)) for row in rows]

        return results
    finally:
        # Close the connection
        cursor.close()
        connection.close()



def getJobs():

    from sqlalchemy import create_engine, MetaData, Table
    import json

    # Create an engine
    engine = create_engine(database_url)

    # Connect to the database
    connection = engine.connect()

    # Reflect the Jobs table
    metadata = MetaData()
    jobs = Table(table_jobs, metadata, autoload_with=engine)

    # Query all rows from the Jobs table
    result = connection.execute(jobs.select())
    
    # print(result)

    logging.info(result)

    # Convert the result into the desired JSON structure
    jobs = {
    row[0]: {
        "role": row[1],
        "isActive": row[2],
        "date": str(row[3]),
        "path": row[4],
        "diplome": row[5],
        "experience": row[6],
        "certifications": row[7],
        "hard_skills": row[8],
        "langues": row[9],
        "soft_skills": row[10],
        }
    for row in result
    }

    # Close the connection
    connection.close()


    return jobs












# Example usage
if __name__ == "__main__":
    result = getJobs()
    content = {roleId: result[roleId] for roleId in result}
    # print(result)result
    # role_to_query = "Consultant Data Management"  # Replace with the role you want to query
    # applications = fetch_applications_by_role(role_to_query)

    # # Print the results
    # for app in applications:
    #     print(app)


