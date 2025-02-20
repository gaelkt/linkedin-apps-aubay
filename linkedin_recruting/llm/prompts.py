from langchain_ollama.llms import OllamaLLM
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate 
from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field 
from pydantic import BaseModel, Field
# from langchain.llms import OpenAI 

import os
from dotenv import load_dotenv
import logging
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import numpy as np
from datetime import datetime

load_dotenv()
llm_type=os.environ['LLM_TYPE']

def extractDiplomeRequired(context, llm):

    from templates import prompt_template_diplome_requis

    class Diplome(BaseModel):
        diplome: str = Field(description="diplome")
    parser_diplome = JsonOutputParser(pydantic_object=Diplome) 

    json_structure_diplome = {
        "diplome": "<votre_réponse>"
        }
    prompt = PromptTemplate(template=prompt_template_diplome_requis, input_variables=["context"], 
        json_structure=json_structure_diplome,
        partial_variables={"format_instructions": parser_diplome.get_format_instructions()})

    chain = prompt | llm | parser_diplome

    output_diplome = chain.invoke({"context": context})

    return output_diplome["diplome"]


def extractExperienceRequired(context, llm):

    from templates import prompt_template_experience_requise

    logging.info("Defining class...")
    
    class Experience(BaseModel):
        experience: str = Field(description="experience")
    parser_experience = JsonOutputParser(pydantic_object=Experience) 

    json_structure_experience = {
        "experience": "<votre_réponse>"
        }
    logging.info("Defining prompt...")
    prompt = PromptTemplate(template=prompt_template_experience_requise, input_variables=["context"], 
        json_structure=json_structure_experience,
        partial_variables={"format_instructions": parser_experience.get_format_instructions()})

    logging.info("Defining chain...")
    chain = prompt | llm | parser_experience

    logging.info("Involing chain...")
    output_experience = chain.invoke({"context": context})

    return output_experience["experience"]


def extractHardSkillsRequired(context, llm):

    from templates import prompt_template_hard_skills_requis
 
    class HardSkills(BaseModel):
        hard_skills: list = Field(description="hard_skills")
    parser_hard_skills = JsonOutputParser(pydantic_object=HardSkills) 

    json_structure_hard_skills = {
        "hard_skills": "<votre_réponse>"
        }
    prompt = PromptTemplate(template=prompt_template_hard_skills_requis, input_variables=["context"], 
        json_structure=json_structure_hard_skills,
        partial_variables={"format_instructions": parser_hard_skills.get_format_instructions()})


    chain = prompt | llm | parser_hard_skills

    output_hard_skills = chain.invoke({"context": context})

    return output_hard_skills["hard_skills"]




def extractCertificationsRequired(context, llm):

    from templates import prompt_template_certifications_requises
 
    class Certifications(BaseModel):
        certifications: list = Field(description="certifications")
    parser_certifications = JsonOutputParser(pydantic_object=Certifications) 

    json_structure_certifications = {
        "certifications": "<votre_réponse>"
        }
    prompt = PromptTemplate(template=prompt_template_certifications_requises, input_variables=["context"], 
        json_structure=json_structure_certifications,
        partial_variables={"format_instructions": parser_certifications.get_format_instructions()})

    chain = prompt | llm | parser_certifications


    output_certifications = chain.invoke({"context": context})

    return output_certifications["certifications"]







def extractDiplomeCandidat(context, llm):

    from templates import prompt_template_diplome_candidat

    start = time.time()

    class Diplome(BaseModel):
        diplome: str = Field(description="diplome du candidat")
    parser_diplome = JsonOutputParser(pydantic_object=Diplome)  

    json_structure_diplome = {
        "diplome": '<votre_réponse>'
    }

    prompt = PromptTemplate(template=prompt_template_diplome_candidat, input_variables=["context"], 
        json_structure=json_structure_diplome,
        partial_variables={"format_instructions": parser_diplome.get_format_instructions()})

    chain = prompt | llm | parser_diplome

    output_diplome = chain.invoke({"context": context})

    end = time.time()
    execution_time = end - start
    logging.info(f"output_diplome={output_diplome} and time={execution_time} seconds")

    return output_diplome["diplome"]

def extractExperienceCandidat(context, llm):
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    logging.info("Calculating Candidate Diplome, Annee et Experience")

    # from templates import prompt_template_experience_candidat_1, prompt_template_experience_candidat_2, prompt_template_diplome_annee_candidat
    from template_test2 import prompt_template_experience_candidat_1, prompt_template_experience_candidat_2, prompt_template_diplome_annee_candidat
    start = time.time()



    json_structure_annee = {"annee": "<annee>"}
    class Annee(BaseModel):
        annee: str = Field(description="annee")
    parser_annee = JsonOutputParser(pydantic_object=Annee) 

    json_structure_experience = {"experience": "<votre_réponse>"}
    class Experience(BaseModel):
        experience: str = Field(description="experience")
    parser_experience = JsonOutputParser(pydantic_object=Experience)

    # prompt
    logging.info("Prompt")

    prompt_annee_diplome = PromptTemplate(template=prompt_template_diplome_annee_candidat, input_variables=["context"], 
        json_structure=json_structure_annee,
        partial_variables={"format_instructions": parser_annee.get_format_instructions()})

    prompt_1 = PromptTemplate(template=prompt_template_experience_candidat_1, input_variables=["context", "annee"], 
        json_structure=json_structure_experience,
        partial_variables={"format_instructions": parser_experience.get_format_instructions()})

    prompt_2 = PromptTemplate(template=prompt_template_experience_candidat_2, input_variables=["context", "annee"], 
        json_structure=json_structure_experience,
        partial_variables={"format_instructions": parser_experience.get_format_instructions()})

    # Output
    logging.info("Running chain")
    chain_annee = prompt_annee_diplome | llm | parser_annee
    chain_1 = prompt_1 | llm | parser_experience
    chain_2 = prompt_2 | llm | parser_experience

    logging.info("Getting the year")
    output_annee = chain_annee.invoke({"context": context})
    annee = output_annee["annee"]

    logging.info("")
    logging.info(f"output_annee={output_annee}")

    if annee == "":
        logging.info("")
        logging.info("Impossible de trouver l'annee du dernier diplome ...")
        annee = "2016"

    logging.info("Getting the experience 1")

    exp_1_ok = False
    exp_2_ok = False
    try:
        logging.info("")
        output_1 = chain_1.invoke({"context": context, "annee": annee})
        logging.info(f"output_1={output_1}")
        exp_1 = int(output_1["experience"])/12.0
        exp_1_ok = True
        logging.info("")
        logging.info("")
    
    except Exception as e:
        logging.info("")
        logging.info("Unable to calculate the experience 1")
        logging.info("We will try another prompt")
        logging.error(e)
        logging.info("")
        logging.info("")
        logging.info("")

    try:
        logging.info("")
        logging.info("Getting the experience 2")
        output_2 = chain_2.invoke({"context": context, "annee": annee})
        logging.info(f"output_1={output_2}")
        exp_2 = int(output_2["experience"])/12.0
        exp_2_ok = True
    except Exception as e:
        logging.info("")
        logging.info("Unable to calculate the experience 2")
        logging.error(e)
        logging.info("")
        logging.info("")
        logging.info("")

    if (exp_1_ok and exp_2_ok):
        experience = 0.5*(exp_1 + exp_2)

    elif exp_1_ok:
        experience = exp_1
    
    elif exp_2_ok:
        experience = exp_2
    
    else:
        logging.info("")
        logging.info("We go by the year of degree since methods 1 and 2 failed")
        experience = datetime.now().year-annee-1
        logging.info(f"experience by degree year is ={experience}")
        logging.info("")
        logging.info("")

    # We round to 1 decimal
    experience = np.round(experience, 1)
        
    logging.info(f"Final experience={experience}")
    

    # #################################################
    # #       Calcul de l'experience professionnelle
    # #################################################

    # # Json_structure and parse
    # class Experience(BaseModel):
    #     experience: str = Field(description="experience requise du candidat")
    # parser_experience = JsonOutputParser(pydantic_object=Experience) 

    # json_structure_experience = {"experience": "<votre_réponse>"}

    # # prompt
    # prompt_1 = PromptTemplate(template=prompt_template_experience_candidat_1, input_variables=["context"], 
    #     json_structure=json_structure_experience,
    #     partial_variables={"format_instructions": parser_experience.get_format_instructions()})

    # prompt_2 = PromptTemplate(template=prompt_template_experience_candidat_2, input_variables=["context"], 
    #     json_structure=json_structure_experience,
    #     partial_variables={"format_instructions": parser_experience.get_format_instructions()})

    # # chains
    # chain_1 = prompt_1 | llm | parser_experience
    # chain_2 = prompt_2 | llm | parser_experience

    # # Outputs
    # output_experience_1 = chain_1.invoke({"context": context, "annee":annee})
    # logging.info("")
    # logging.info(f"output_experience_1={output_experience_1}")
    # # output_experience_2 = chain_2.invoke({"context": context, "annee":annee})
    # logging.info("")
    # # logging.info(f"output_experience_2={output_experience_2}")
   

    # # Experience
    # experience_1 = int(output_experience_1["experience"])/12.0
    # # experience_2 = int(output_experience_2["experience"])/12.0
    # logging.info("")
    # # logging.info(f"experience_1={experience_1} and experience_1={experience_1}")

    # # experience = np.round(np.mean([experience_2, experience_1]), 1)
    # experience = np.round(experience_1, 1)


    # end = time.time()
    # execution_time = end - start
    # logging.info(f"experience={experience} ans and time={round(execution_time/60)} seconds")

    return int(annee), experience

def extractHardSkillsCandidat(context, llm):

    logging.info("Calculating Candidate Hard Skills")

    from templates import prompt_template_hard_skills_candidat

    start = time.time()

    class Hard_Skills(BaseModel):
        hard_skills: str = Field(description="competence techniques requise du candidat")
    parser_hard_skills = JsonOutputParser(pydantic_object=Hard_Skills) 

    json_structure_hard_skills = {"hard_skills": "<votre_réponse>"}

    prompt = PromptTemplate(template=prompt_template_hard_skills_candidat, input_variables=["context"], 
        json_structure=json_structure_hard_skills,
        partial_variables={"format_instructions": parser_hard_skills.get_format_instructions()})


    chain = prompt | llm | parser_hard_skills
    logging.info("Chain ok")
    output_hard_skills = chain.invoke({"context": context})
    logging.info("Chain Invoked")

    logging.info("")
    logging.info("")
    logging.info("Here are hard skills")
    logging.info(f"{output_hard_skills}")
    logging.info("Next")


    end = time.time()
    execution_time = end - start
    logging.info(f"output_hard_skills={output_hard_skills} and time={execution_time} seconds")

    return output_hard_skills["hard_skills"]


def extractCertificationsCandidat(context, llm):

    logging.info("Calculating Candidate Certifications")

    from templates import prompt_template_certifications_candidat

    start = time.time()

    class Certifications(BaseModel):
        certifications: str = Field(description="certifications")
    parser_certifications = JsonOutputParser(pydantic_object=Certifications) 

    json_structure_certifications = {"certifications": "<votre_réponse>"}

    prompt = PromptTemplate(template=prompt_template_certifications_candidat, input_variables=["context"], 
        json_structure=json_structure_certifications,
        partial_variables={"format_instructions": parser_certifications.get_format_instructions()})


    chain = prompt | llm | parser_certifications

    output_certifications = chain.invoke({"context": context})

    end = time.time()
    execution_time = end - start
    logging.info(f"output_certifications={output_certifications} and time={execution_time} seconds")

    return output_certifications["certifications"]


