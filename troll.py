from trollclass import *
def main():

    felkoll = Brade() #För att kunna felhantera val av bräde behövs classen aktiveras innan, gör koden mer kompakt
    for instruktiontext in felkoll.instruktioner("cmd"):
        print(instruktiontext)
    felkoll.hamta_highscore()
    text1 = ["Hur många rader? (minst 4 och max 8): ",maxgräns,"Mellan 4 och 8 rader!","Skriv ett tal!", minimigräns]
    brdstrlk = felkoll.felhantering(text1) #Felhanterar brädstorlek-inmatning
    while True: #meny för att välja om man vill lösa själv eller låta algoritm lösa
        val = input("1. Lös själv\n2. Algoritm\n")
        try:
            val = int(val)
        except:
            continue
        if val == 1:
            manorrobot = Manniska #sätter variabeln manorrobot till människa klassen
            break
        elif val == 2:
            manorrobot = Algoritm #ätter variabeln manorrobot till algoritm klassen
            break
    brdtyp = manorrobot(brdstrlk) # Classen aktiveras med brädstorleket som variabel
    brade = brdtyp.spelplan()
    brdtyp.matris(brade)
    if val == 1:
        brdtyp.placera_Troll(brade)
    elif val == 2:
        brdtyp.losnings_algoritm(brade)

main()
