from distutils.command import check
from os import times
import requests
import json
import time


URL = "http://0.0.0.0:22222"

# gibt alle user in einem json zurück
def getusers():
    payload={}
    headers = {}
    
    response = requests.request("GET", URL+"/v1/users", headers=headers, data=payload)
    
    return response.json()

# gibt den spieler im json zurück, gesucht wird dabei anhand der id
def getUserByID(id):
    payload={}
    headers = {}
    
    response = requests.request("GET", URL+"/v1/users/"+ str(id), headers=headers, data=payload)
    
    return response.json()

# gibt den spieler im json zurück, gesucht wird dabei anhand des namens
def getUserByName(name):
    payload={}
    headers = {}
    
    payload={}
    headers = {}

    response = requests.request("GET", URL +"/v1/users/name/" +str(name), headers=headers, data=payload)

    return response.json()

# gibt eine gewählte anzahl an fragen in einem json zurück
def getQuestions(anzahl):
    payload={}
    headers = {}
    
    response = requests.request("GET", URL+"/v1/questions/amount/"+str(anzahl), headers=headers, data=payload)
    
    return response.json()

# fügt eine neue frage hinzu 
def addQuestion(question, answer1, answer2, answer3, correctanswer):
    payload = json.dumps({
      "question": question,
      "answer1": answer1,
      "answer2": answer2,
      "answer3": answer3,
      "correctanswer": correctanswer
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", URL+"/v1/questions", headers=headers, data=payload)
    print(response.json())
    return response.json()

# gibt alle fragen im json zurück       
def getallQuestions():
    payload={}
    headers = {}
    
    response = requests.request("GET", URL+"/v1/questions", headers=headers, data=payload)
    
    return response.json()

# gibt die frage im json zurück, gesucht wird dabei anhand der frageid 
def getQuestionsByID(id): 
    payload={}
    headers = {}
    
    response = requests.request("GET", URL + "/v1/questions/" +str(id), headers=headers, data=payload)
    
    return response.json()

# überprüft ob die antwort richtig ist
def checkAnswer(questionsID, answer, username):
    payload={}
    headers = {}
    
    response = requests.request("POST", URL+"/v1/answer/" + str(questionsID)+"/"+str(answer)+"/"+username, headers=headers, data=payload)
    return response.json()

# fragt den user nach seinem spielernamen und gibt diesen zurück
def askForUserName():
    name = str(input("\nWie ist dein Name?\n"))
    return name

# fragt den spieler wie viele fragen er beantworten möchte
def askAnswerAmount():
    while True:
        try:
           anzahl=int(input("\nWie viele Fragen möchtest du beantworten?:\n"))
        except ValueError:
            print("Gebe bitte eine Zahl ein!")
            continue
        else:
            return anzahl

# eigentliches spiel
def GameWithMySever():
    #fragt zuerst nach zsername, und anzahl der fragen
    username = askForUserName()
    anzahl = askAnswerAmount()
    # sendet anfrage an den server, über beliebige anzahl von fragen
    questions = getQuestions(anzahl)
    #zeigt dem spieler jede frage an
    for question in questions:
        
        print("\nFrage: " + question["Question"])
        print("(1) " + question["Answer1"])
        print("(2) " + question["Answer2"])
        print("(3) " + question["Answer3"])
        print("Bitte trage eine Lösung ein:\n")
        #startet einen timer
        timestart = time.time()
        answer = input()
        # stoppt den timer
        needed_time_answer = time.time()-timestart
        
        if answer is not None:
            #prüft ob die antwort vor ablauf der zeit eingetragen wurde
            if(needed_time_answer < 20):  
                # prüft ob die frage richtig beantwortet wurde 
                if(checkAnswer(question["ID"], answer, username) == 200):     
                    print("Du hast " + str( round(needed_time_answer, 1)) + " Sekunden zum Antworten gebraucht!\nDu erhälst einen Punkt!")
                else:
                    print("Du hast die Frage leider Falsch beantwortet!")
            else: 
                # frage wurde nach ablauf der zeit beantwortet, deswegen erhält der spieler einen minuspunkt
                checkAnswer(question["ID"], 99, username)
                print("Leider ist die Zeit abgelaufen, du bekommst einen Minuspunkt!")
                print("Benötigte Zeit: " + str(round(needed_time_answer,1)))

    # prüft ob der spieler in der datenbank zu finden ist
    output = getUserByName(username)
    if(output == 404):
        print("Leider hast du keine Frage richtig beantwortet :(")
    else:
        # gibt dem spieler seinen neuen aktuellen score zurück
        outputname=output[0]["Name"]
        outputscore=output[0]["Score"]
        print("\n\n\n\nSuper! \n"+ str(outputname) + " dein neuer Score ist: "+ str(outputscore))

 
# mein methode, welche das spiel startet
def main():
    GameWithMySever()

    
    # addQuestion("Wie hoch war der Umsatz von Apple im Jahr 2021?", "375 Mrd €", "366 Mrd €", "362 Mrd €", 2)
    # addQuestion("Wer ist der Gründer von Microsoft?", "Bill Gates", "Elon Musk", "Steve Jobs", 1)
    # addQuestion("Wo werden in Europa Autos von der Marke Tesla produziert?", "Leipzig", "Grunewald", "Gruenheide", 3)
    # addQuestion("Was ist der Break-Even-Point?", "Punkt an dem ein Rohstoff bricht (zum Beispiel: Holz, Carbon...)", "Zeitpunkt in den Konjukturphasen, an dem von einem Aufschwund in eine Rezession uebergegangen wird", "Punkt an dem Erlöse und Gesamtkosten gleich hoch sind", 3)
    # addQuestion("Was ist Bitcoin?", "Eine Kryptowaehrung", "Eine Kryptowaehrung", "Eine sehr alte Goldmuenze", 1)
    # addQuestion("Was muss am Ende eines Geschaeftsjahres getan werden?", "Eine Party veranstallten", "Eine Bilanz erstellen", "Dem besten Mitarbeiter eine Auszeichnung uebergeben", 2)
    # addQuestion("Welche Marktform gibt es?", "Polypol", "Polpol", "Palupol", 1)
    # addQuestion("Was ist mit den Begriff 'Industrie 4.0' gemeint?", "Die vierte industrielle Revolution", "Das vierte Software Update", "Die vierte jemals gebaute Industriemaschine", 1)
    # addQuestion("Für was steht die Abkuerzung 'MwSt'?", "Mach was Susi tut", "Mehrwertsteuer", "Musst Wasser still trinken", 2)
    # addQuestion("Was ist SpaceX?", "Ein Rüstungsunternehmen", "Ein andere Bezeichnung fue ein Leerzeichen", "Ein Raumfahrt und Telekommunikationsunternehmen", 3)


    
if __name__ == '__main__':
    main()
    


    