"""
Created on Wed Jun 15 11:20:15 2022

@author: john-simon
"""

############################ Logik über hinzufügen von Fragen und User ############################


from tabnanny import check
from tkinter.messagebox import QUESTION
import pandas as pd
import os

# Funktion zum Speichern einer neue Frage
def save_new_question(frage, antwort1, antwort2, antwort3, loesung):
    id = 1
    data = {"ID" : str(id), "Question": [frage], "Answer1": [antwort1], "Answer2": [antwort2], "Answer3": [antwort3], "CorrectAnswer": [loesung]}
    df = pd.DataFrame(data)
    df.to_excel("questions.xlsx")
    return

# Speichere den Score mit Spielername in eine neue Excel-Datei, damit er bei einem neuen Spiel wieder aufgerufen werden kann
# Input -> Name und Score des Spielers
def save_to_new_file(name, score):
    id = 1
    data = {"ID" : str(id), "Name": [name], "Score": [score]}
    df = pd.DataFrame(data)
    df.to_excel("scores.xlsx")
    return


# Speichert den Score und Namen in eine bereits bestehende Excel-Datei
# Input -> Name und Score des Spielers
def add_player(name, score):
    # Läd die Excel-Datei aus dem Dateipfad
    df = pd.read_excel("scores.xlsx", index_col=0)
    index = (df[df['Name']== name].index.values)
    if ((df[df['Name']== name].index.values).size == 0 ):
        if(score == -1):
            return
        else:
            # Speichere den Score und Spielernamen am Ende der Excel-Datei ab -> alle anderen Spielerdaten bleiben bestehen
            id = len(df)+1
            new_row = {"ID" : str(id) ,"Name": str(name), "Score": score}
            df_marks = df.append(new_row, ignore_index=True)
            writer = pd.ExcelWriter("scores.xlsx", engine="xlsxwriter")
            df_marks.to_excel(writer, sheet_name="Score", index="False")
            writer.save()
            # Zeige den Spieler alle Highscores
        return
    else:
        # Excel Datei mit Spielerdaten wurde gefunden, deshalb wird der neue Score dem alten hinzugefügt und abgespeichert -> alle anderen Spielerdaten bleiben bestehen
        # Lese den alten Score aus 
        old_score = df.loc[index,"Score"]
        if(old_score.iloc[0] > 0):
            # Berechne den neuen Score
            new_score = int(old_score) + score
            # Speichere den neuen Score
            df.loc[index, "Score"] = new_score
            os.remove("scores.xlsx")
            df.to_excel("scores.xlsx")
            # Zeige den Spieler alle Highscores
            return
        else:
            return


# Funktion zum Speichern einer neue Frage
def add_question(frage, antwort1, antwort2, antwort3, loesung):
    # Läd die Excel-Datei aus dem Dateipfad
    df = pd.read_excel("questions.xlsx", index_col=0)
    id = len(df)+1
    # Speichere den Score und Spielernamen am Ende der Excel-Datei ab -> alle anderen Spielerdaten bleiben bestehen
    new_row = {"ID" : str(id), "Question": str(frage), "Answer1": str(antwort1), "Answer2": str(antwort2), "Answer3": str(antwort3), "CorrectAnswer": loesung}
    df_marks = df.append(new_row, ignore_index=True)
    writer = pd.ExcelWriter("questions.xlsx", engine="xlsxwriter")
    df_marks.to_excel(writer, sheet_name="questions", index="False")
    writer.save()
    return

# Funktion zum überprüfen der Lösung, ist die Lösung richtig -> gebe True zurück, ansonsten False
def check_answer(questionid, answer):
    df = pd.read_excel("questions.xlsx", index_col=0)
    index = (df[df['ID']== questionid].index.values)
    correctanswer = df.iloc[index]["CorrectAnswer"].values
    if (correctanswer == answer):
        return True
    else:
        return False

