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

def isFreelance(resume: str) -> bool:
    keywords = ["freelance", "ceo", "indépendant"]
    resume_lower = resume.lower()
    
    for keyword in keywords:
        if keyword in resume_lower:
            return True
    return False

def extractEmail(resume: str) -> list:
    """
    Extracts all email addresses from the resume string.

    :param resume: The candidate's resume as a string.
    :return: A list of all email addresses found in the resume.
    """
    # Basic email matching pattern:
    # Explanation:
    # [a-zA-Z0-9._%+-]+    -> user part can contain alphanumeric and certain special characters
    # @                    -> '@' character
    # [a-zA-Z0-9.-]+       -> domain can contain alphanumeric and dots/hyphens
    # \.[a-zA-Z]{2,}       -> TLD at least 2 characters (e.g. .com, .io, etc.)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    emails = re.findall(email_pattern, resume)
    return emails




def anonymizeResume(fullname: str, resume: str) -> str:
    """
    Removes all words from 'resume' that appear in 'fullname' 
    (case-insensitive, matches whole words).
    
    :param fullname: The candidate's full name (e.g. "John Doe", 
                     "John Michael Doe", "John, Adam Doe", 
                     "John Doe Smith", etc.)
    :param resume: The resume text.
    :return: A version of the resume with those name components removed.
    """
    # 1. Split the full name by any character that is NOT a word character 
    #    (letters, digits, underscore). 
    #    This will handle commas, spaces, hyphens, etc.
    tokens = re.split(r'[^\w]+', fullname.strip())
    
    # Remove empty strings that can occur if the split finds extra punctuation/spaces
    tokens = [token for token in tokens if token.strip()]
    
    # Convert list to a set to avoid duplicate tokens
    tokens_set = set(tokens)
    
    # 2. Remove each token from the resume (case-insensitive, whole word match)
    #    \b ensures we match whole words only.
    #    re.IGNORECASE ensures case-insensitive matching.
    #    We replace each match with an empty string.
    for token in tokens_set:
        pattern = re.compile(r'\b' + re.escape(token) + r'\b', re.IGNORECASE)
        resume = pattern.sub('', resume)

    # 3. Clean up extra spaces, line breaks, etc. that might result from removals
    resume = re.sub(r'\s+', ' ', resume).strip()
    
    return resume



