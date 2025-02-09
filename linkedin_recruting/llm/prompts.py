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
    
    class Experience(BaseModel):
        experience: str = Field(description="experience")
    parser_experience = JsonOutputParser(pydantic_object=Experience) 

    json_structure_experience = {
        "experience": "<votre_réponse>"
        }
    prompt = PromptTemplate(template=prompt_template_experience_requise, input_variables=["context"], 
        json_structure=json_structure_experience,
        partial_variables={"format_instructions": parser_experience.get_format_instructions()})

    chain = prompt | llm | parser_experience

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

    from templates import prompt_template_experience_candidat_1, prompt_template_experience_candidat_2, prompt_template_diplome_annee_candidat

    start = time.time()
    #################################################
    #       Calcul du diplome et de l'annee
    #################################################
    # Json_structure and parse
    json_structure_diplome_annee = {"diplome": '<diplome>', "annee": '<annee>'}
    class DiplomeAnnee(BaseModel):
        diplome: str = Field(description="diplome")
        annee: str = Field(description="annee")
    parser_diplome_annee = JsonOutputParser(pydantic_object=DiplomeAnnee)   

    # prompt
    logging.info("Prompt")

    if llm_type == "gpt-4-turbo" or llm_type == "gpt-4" or llm_type == "openai":
        prompt_diplome_annee = ChatPromptTemplate.from_template(template=prompt_template_diplome_annee_candidat)
        logging.info("Defining chain")
        chain_diplome_annee = (prompt_diplome_annee| llm| parser_diplome_annee)
    
    else:
        prompt_diplome_annee = PromptTemplate(template=prompt_template_diplome_annee_candidat, input_variables=["context"], 
        json_structure=json_structure_diplome_annee,
        partial_variables={"format_instructions": parser_diplome_annee.get_format_instructions()})

        # chain
        logging.info("Defining chain")
        chain_diplome_annee = prompt_diplome_annee | llm | parser_diplome_annee

    # Output
    logging.info("Running chain")
    output_annee_diplome = chain_diplome_annee.invoke({"context": context})

    logging.info("")
    logging.info(f"output_annee_diplome={output_annee_diplome}")

    diplome = output_annee_diplome['diplome']
    annee = output_annee_diplome['annee']

        
    if annee == "":
        logging.info("")
        logging.info("Impossible de trouver l'annee du dernier diplome ...")
        annee = "2016"
        

    #################################################
    #       Calcul de l'experience professionnelle
    #################################################

    # Json_structure and parse
    class Experience(BaseModel):
        experience: str = Field(description="experience requise du candidat")
    parser_experience = JsonOutputParser(pydantic_object=Experience) 

    json_structure_experience = {"experience": "<votre_réponse>"}

    # prompt
    prompt_1 = PromptTemplate(template=prompt_template_experience_candidat_1, input_variables=["context"], 
        json_structure=json_structure_experience,
        partial_variables={"format_instructions": parser_experience.get_format_instructions()})

    prompt_2 = PromptTemplate(template=prompt_template_experience_candidat_2, input_variables=["context"], 
        json_structure=json_structure_experience,
        partial_variables={"format_instructions": parser_experience.get_format_instructions()})

    # chains
    chain_1 = prompt_1 | llm | parser_experience
    chain_2 = prompt_2 | llm | parser_experience

    # Outputs
    output_experience_1 = chain_1.invoke({"context": context, "annee":annee})
    logging.info("")
    logging.info(f"output_experience_1={output_experience_1}")
    # output_experience_2 = chain_2.invoke({"context": context, "annee":annee})
    logging.info("")
    # logging.info(f"output_experience_2={output_experience_2}")
   

    # Experience
    experience_1 = int(output_experience_1["experience"])/12.0
    # experience_2 = int(output_experience_2["experience"])/12.0
    logging.info("")
    # logging.info(f"experience_1={experience_1} and experience_1={experience_1}")

    # experience = np.round(np.mean([experience_2, experience_1]), 1)
    experience = np.round(experience_1, 1)


    end = time.time()
    execution_time = end - start
    logging.info(f"experience={experience} ans and time={round(execution_time/60)} seconds")

    return diplome, int(annee), experience

def extractHardSkillsCandidat(context, llm):

    logging.info("Calculating Candidate Certifications")

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

    output_hard_skills = chain.invoke({"context": context})

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


