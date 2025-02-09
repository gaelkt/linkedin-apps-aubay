import random
import string
from datetime import datetime, timedelta
import re


def generate_random_id():
    
    # Generate a random string of 10 characters
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    return random_string

def generate_random_date(start_date="2024-08-01", end_date="2024-11-08"):
    # Convert the start and end dates to datetime objects if they are in string format
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Calculate the difference between the start and end dates
    delta = end_date - start_date
    # Generate a random number of days to add to the start_date
    random_days = random.randint(0, delta.days)
    
    jobDate = start_date + timedelta(days=random_days)
    
    jobDate = jobDate.strftime("%Y-%m-%d")
    
    # Return the random date
    return jobDate


def convert_to_date(input_date_str):
    # Parse the input string into a datetime object
    dt = datetime.fromisoformat(input_date_str)
    # Format the datetime object to the desired format
    return dt.strftime('%Y-%m-%d')


def generate_random_string(length=10) -> str:
    characters = string.ascii_letters + string.digits  # Letters and digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string



def extract_applicant_name_from_subjet(subject):
    # Use regular expression to match "from <name>"
    match = re.search(r"from (.+)$", subject)
    if match:
        return match.group(1).strip()
    return None


def extract_role_name_from_subject(email_subject: str) -> str:
    """
    Extracts the role name from the input email subject string.

    Args:
        email_subject (str): The subject of the email containing job application details.

    Returns:
        str: The extracted role name.
    """

    pattern = r"New application(?:_|\:)\s*(.+?)\s*(?:\(F[\/_]?H\)|from)"
    

    match = re.search(pattern, email_subject, re.IGNORECASE)
    
    if match:

        A =  match.group(1).strip()
    
        if A.endswith(" F/H"):
            return A[:-4].strip()  
        else:
            return A


