from fastapi import FastAPI, status, Response
import os
import pandas as pd
from models import User
from models import Questions
import logic
import uvicorn
import random


app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/docs",
    title="Demo Rest",
    version="1.0",
    openapi_url="/api/v1/openapi.json"
)

# gibt dem user alle user zurück
@app.get("/v1/users", status_code=200)
async def get_users():
    if os.path.isfile('scores.xlsx'):
        df = pd.read_excel("scores.xlsx", index_col=0).sort_values(by=['Score'], ascending=False)
        output = df.to_dict("records")
        return output
    else:
        return {"data" : "no users found"}

# gibt dem user dem spieler zurück welcher mit der gesuchten id übereinstimmt
@app.get("/v1/users/{id}", status_code=200)
async def get_users_by_id(id):
    if os.path.isfile('scores.xlsx'):
        df = pd.read_excel("scores.xlsx", index_col=0)
        index = df[df["ID"]==int(id)].index.values
        if ((df[df["ID"]==int(id)].index.values).size == 0):
           return status.HTTP_404_NOT_FOUND
        else: 
            data = df.loc[index]
            output = data.to_dict("records")
        return output
    else:
        return {"data" : "no users found"}

# gibt dem user dem spieler zurück welcher mit dem gesuchten namen übereinstimmt
@app.get("/v1/users/name/{name}", status_code=200)
async def get_users_by_id(name):
    if os.path.isfile('scores.xlsx'):
        df = pd.read_excel("scores.xlsx", index_col=0)
        index = df[df["Name"]==str(name)].index.values
        if ((df[df["Name"]==str(name)].index.values).size == 0):
           return status.HTTP_404_NOT_FOUND
        else: 
            data = df.loc[index]
            output = data.to_dict("records")
        return output
    else:
        return {"data" : "no users found"}


# fügt einen einen neuen spieler der datenbank hinzu
@app.post("/v1/users", status_code=200)
async def register_user(user : User):
    if os.path.isfile('scores.xlsx'):
        df = pd.read_excel("scores.xlsx", index_col=0)
        # Fügt Spielerdaten der besteçhenden Excel-Datei hinzu
        logic.add_player(user.name, user.score)
        return status.HTTP_201_CREATED
    else:
        # Generiert eine neue Excel-Datei mit den Spielerdaten
        logic.save_to_new_file(user.name, user.score)
        return status.HTTP_201_CREATED

# gibt dem user alle fragen zurück
@app.get("/v1/questions", status_code=200)
async def get_questions():
    if os.path.isfile('questions.xlsx'):
        df = pd.read_excel("questions.xlsx", index_col=0)
        df_new = df.iloc[:, :-1]
        output = df_new.to_dict("records")
        return output
    else:
        return {"data" : "no questions found"}

# gibt dem user eine frage mit der gewählten id zurück
@app.get("/v1/questions/{id}", status_code=200)
async def get_questions_by_id(id):    
    if os.path.isfile('questions.xlsx'):
        df = pd.read_excel("questions.xlsx", index_col=0)
        index = df[df["ID"]==int(id)].index.values
        # sucht die id in der datenbank
        if ((df[df["ID"]==int(id)].index.values).size == 0):
               return status.HTTP_406_NOT_ACCEPTABLE
        else:
            data = df.loc[index]
            df_new = data.iloc[:, :-1]
            output = df_new.to_dict("records")
        return output
    else:
        return {"data" : "no questions found"}

# gibt dem user eine gewählte anzahl von fragen zurück (die fragen sind dabei zufällig ausgewählt)
@app.get("/v1/questions/amount/{number}", status_code=200)
async def get_questions_number(number):
    if os.path.isfile('questions.xlsx'):
        n = 0
        df = pd.read_excel("questions.xlsx", index_col=0)
        df_new = df.iloc[:, :-1]
        data_you_need = pd.DataFrame()
        # wählt zufällige fragen aus und speichert sie 
        while n < int(number):
            ran = random.randint(0,(len(df_new)-1))
            question = df_new.iloc[ran]
            data_you_need=data_you_need.append(question,ignore_index=True)
            n += 1
        output = data_you_need.to_dict("records")
        print(output)
        return output
    else:
        return {"data" : "no questions found"}

# fügt eine neue frage der datenbank hinzu
@app.post("/v1/questions", status_code=200)
async def register_question(questions : Questions):
    if os.path.isfile('questions.xlsx'):
        df = pd.read_excel("questions.xlsx", index_col=0)
        # Fügt Frage der besteçhenden Excel-Datei hinzu
        logic.add_question(questions.question, questions.answer1, questions.answer2, questions.answer3, questions.correctanswer)
        return status.HTTP_201_CREATED
    else:
        # Generiert eine neue Excel-Datei mit den Fragen
        logic.save_new_question(questions.question, questions.answer1, questions.answer2, questions.answer3, questions.correctanswer)
        return status.HTTP_201_CREATED

# überprüft ob die gewählte lösung richtig ist 
# dazu müssen frageid, antwort und username übergeben werden
# bsp: 
# http://0.0.0.0:22222/v1/answer/1/2/John
# FrageID : 1
# Antwort : 2
# Username : John
@app.post("/v1/answer/{id}/{answer}/{username}", status_code=200)
async def check_answer(id, answer, username):
    if os.path.isfile('questions.xlsx'):   
        # prüft ob die antwort true ist
        if (logic.check_answer(int(id), int(answer)) == True):
            # prüft ob eine scores datei existiert
            if os.path.isfile('scores.xlsx'):
                # speichert den score mit spielernamen ab
                df = pd.read_excel("scores.xlsx", index_col=0)
                logic.add_player(str(username), 1)
                return status.HTTP_200_OK
            else:
                # speichert den score mit spielernamen in eine neue excel-datei 
                logic.save_to_new_file(str(username), 1)
                return status.HTTP_200_OK
        else:
            # antwort ist False 
            if os.path.isfile('scores.xlsx'):
                df = pd.read_excel("scores.xlsx", index_col=0)
                # speichert den score mit spielernamen ab
                logic.add_player(str(username), -1)
                return status.HTTP_400_BAD_REQUEST
    else: 
        return {"data" : "no questions found"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=22222, log_level='debug')