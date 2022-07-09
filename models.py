"""
Created on Wed Jun 15 11:20:15 2022

@author: john-simonbachhuber
"""

############################ Logik der User und Questions ############################

from pydantic import BaseModel

# user modell
class User(BaseModel):
    id = int
    name : str
    score : int
    
# frage modell
class Questions(BaseModel):
    id = int
    question : str
    answer1: str
    answer2: str
    answer3: str
    correctanswer : int