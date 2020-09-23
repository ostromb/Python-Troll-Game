import time
import pickle

maxgräns = 8 #maxgräns för brädstorlek, går att ändra här,
minimigräns = 4 #minimigräns för brädstorlek, går att ändra här, bräden mindre än 4 går ej att lösa

class Brade: #klass med funktioner för brädet
    def __init__(self,strlk=0): #initierar, med variabeln strlk som är brädstorlek, har ett satt värde för att kunna använda classen utan att skriva in brädstrlk, (för ex. instruktioner )
        self.rader = int(strlk)
        self.kolumner = int(strlk)

    def spelplan(self): #skapar spelplanet genom listor som har i början är utan troll "O" returnar listan
        lista = []
        for i in range(0, self.kolumner):
            inrelista = []
            for j in range(0, self.rader):
                inrelista.append("O")
            lista.append(inrelista)
        return lista

    def matris(self, matris): # printar ut brädet och skapar mellanrum mellan varje element, (snyggar till listorna)
        for rad in matris:
            for element in rad:
                print("{0:<2}".format(element), end="")
            print("")

    def Kontrollera(self, lista, n, troll): #kontrollerar att det är tillåtet att lägga troll på vald ruta
        if n > 0:
            for i in range(0,n):
                if lista[i][troll] == "X" or troll-1-i >= 0 and lista[n-i-1][troll-1-i] == "X" or troll+1+i <= self.rader-1 and lista[n-i-1][troll+1+i] == "X":
                    print("Går ej")
                    return ("O")
        else:
            return("X")
        return ("X")

    def felhantering(self, text,z=1): #kollar att inmatningen är korrekt, alltså inte ger ut Error, för icke grafiska programmet, genom att använda av textlistor för de olika alternativen, krävs endast en sådan funktion
        while True:
            skrivtext = input(text[0])
            try:
                skrivtext = int(skrivtext)
                if skrivtext <= text[1] and skrivtext >= text[4]:
                    break
                else:
                    print(text[2])
                    continue
            except:
                try:
                    if z != 0: #ser till så att det inte går att skriva undo när det finns inga troll placerade (n=0)
                        skrivtext = skrivtext.lower()
                        if skrivtext == text[5]:
                            break
                        else:
                            print(text[3])
                    else:
                        print(text[6])
                except IndexError:
                    print(text[3])
        return skrivtext

    def hamta_highscore(self): #öppnar hiscore filen, och printa.
        try:
            with open ("hiscore.dat","rb") as file:
                hiscore = pickle.load(file)
            print("\nHigscore:")
            print(hiscore)
        except:
            hiscore = []
        return hiscore  #I grafisk, returnar hiscore, där den sedan omvandlas för att dispalyas på skärm

    def ta_tid(self, nar): #startar och avslutar tiden,
        global start #måste vara global så att när funktionen anropas igenom kan en avslutas,
        if nar == 1: #nar variabeln beskriver om det är första eller andra gången funktionen anropas
            start = time.time()
        elif nar == 2:
            end = time.time()
            seconds = round(end - start,0)
            print("Du vann på",seconds,"sekunder och med",self.rader,"x",self.rader,"i brädstorlek!")
            score = float(((self.rader*self.rader*self.rader)/seconds)) #kalkylerar poäng, och sätter i varabel score
            score = round(score, 2) #printar score
            print("Poäng: ",score)
            self.highscore(score)
            return ("Du vann på",seconds,"sekunder och med",self.rader,"x",self.rader,"i brädstorlek!"), ("Poäng: ",score) #i grafiskt, returnar score, där den omvandlas och displayas på skärm


    def highscore(self, score): #kollar om du fått highscore, och isfåll lägger in den i hiscore filen
        hiscore = self.hamta_highscore()
        try:
            if score > hiscore[9]:
                hiscore[9] = score
                hiscore.sort(reverse=True)
                print("Highscore! Grattis du kom på plats",hiscore.index(score)+1)
                del hiscore[10]
                with open("hiscore.dat","wb") as file:
                    pickle.dump(hiscore,file)
        except:
            hiscore.append(score)
            hiscore.sort(reverse=True)
            with open("hiscore.dat","wb") as file:
                pickle.dump(hiscore,file)

    def instruktioner(self,instruktionstyp="gui"): #skriver ut instrutkioner
        if instruktionstyp == "cmd":
            instruktionmsg = ["Välkommern till spelet Arga Troll!","Spelet går ut på att placera troll på ett kvadratiskt spelbräde av vald storlek (mellan 4-8)","Trollen placeras rad för rad, i nedåtgående ordning, (högsta raden först)","Spelaren ska placera ut troll genom att skriva kolumnnumret", "Reglerna är: Trollen får inte vara på samma rad, kolumn eller diagonal.","För att göra om sitt drag, skriv undo","Spelaren får poäng baserat på tid och brädstorlek","Ju snabbare tid och större brädde desto mer poäng får spelaren!"]
        else:
            instruktionmsg = ["Välkommern till spelet Arga Troll!","Spelet går ut på att placera troll på ett kvadratiskt spelbräde av vald storlek (mellan 4-8)","Trollen placeras rad för rad, i nedåtgående ordning, (högsta raden först)","Spelaren ska placera ut troll genom trycka på rutor", "Reglerna är: Trollen får inte vara på samma rad, kolumn eller diagonal.","För att göra om sitt drag, tryck på den senast placerade trollet","Spelaren får poäng baserat på tid och brädstorlek","Ju snabbare tid och större brädde desto mer poäng får spelaren!"]
        return instruktionmsg

class Manniska(Brade): #class som inheritar alla funktioner från class Brade, fungerar för icke-grafisk
    def __init_(self,strlk):
        super().__init__(strlk)

    def placera_Troll(self,brade): #funktion för att placera troll
        text2 = ["Välj en kolumn på raden att placera Troll: ",self.rader,"Talet finns ej i raden!","Skriv ett tal i raden eller undo!",1,"undo","Du måste först placera ett troll!"]
        self.ta_tid(1) #startar tiden
        n = 0 #vilken rad man placerar troll på
        while n in range(0,self.rader): # loop för att placera troll
            inmatningstxt = self.felhantering(text2,n)
            if inmatningstxt == "undo": #ifall man matar in undo så placerar man troll på den tidigare raden
                n -= 1
                a =brade[n].index("X")
                brade[n][a] = "O"
            else:
                troll = int(inmatningstxt)-1
                brade[n][troll] = "X"
                brade[n][troll] = str(self.Kontrollera(brade, n, troll))
                if brade[n][troll] == "O":
                    n -=1 #ifall inmatningen inte stämmer så stannar loopen på samma rad n, genom att ta bort -1 från rad
                n += 1 # går till nästa rad n
            print("")
            self.matris(brade) #refreshar brädet
        self.ta_tid(2) #avslutar tiden och spelet


class Algoritm(Brade): #class för algoritm som löser brdäet av själv av valfri storlek, icke grafiskt. Inheritar funktioner från class Brade
    def __init__(self,strlk):
        super().__init__(strlk)

    def losnings_algoritm(self, brade): #lösningsalgoritm, testar från vänster till höger kolumner, tills alla rader går att fylla med troll, lika placera_Troll funktionen fast kräver inte input
        n = 0
        troll = 0
        while n in range(0,self.rader):
            while troll in range(0,self.rader+1):
                if troll == self.rader:
                    n -= 1
                    a =brade[n].index("X")
                    brade[n][a] = "O"
                    troll = a+1
                    break

                brade[n][troll] = "X"
                brade[n][troll] = str(self.Kontrollera(brade, n, troll))
                if brade[n][troll] == "X":
                    troll = 0
                    n += 1
                    break
                troll += 1
            print("")
            self.matris(brade)
