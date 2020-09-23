import pygame, sys
from pygame.locals import *
from trollclass import *

fonsterbredd = 1200
fonsterhojd = 800
rutstrlk = 30 #storlek av rutorna
mellanrum = 2 #mellanrum mellan rutorna
XMARGIN = 500 #Hur långt brädet är från vänstra sidan av fönstret
YMARGIN = 200 #hur långt bädet är från övre sidan
pygame.font.init() #initierar fontstil för text, som input
font = pygame.font.Font(None, 32) #bestämmer font


Svart = (0,0,0)
Vit = (255,255,255)
Rod = (255,0,0)

def main():
    global fonster, brdstrlk, raknarlista #dessa är konstanter som anvönds i alla funktioner


    pygame.init() #initierar pygame
    brdstrlk = meddelande() #skapar fönster med instruktioenr som reutrnar input som brädstorlek (första skärmen)
    pygame.display.set_caption("Arga Troll")
    fonster = pygame.display.set_mode((fonsterbredd,fonsterhojd)) #skapar fönster (andra skärmen)


    rita_brade()
    brdtyp = Brade(brdstrlk) #hämtar class med brdstrlk som brädstorlek
    brade = brdtyp.spelplan()
    brdtyp.ta_tid(1)
    raknarlista = []
    while True: #håller fönstret upp
        for event in pygame.event.get(): #hämtar från knapptrycks-classen i pygame
            try:
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE): #esc, och x-knappen kan användas för att stänga fönstret
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN: #vid mustryck
                    musX, musY = event.pos #hämar position
                    (TrollX, TrollY, rutaX, rutaY) = hittaRuta(musX, musY)
                    brade[rutaY][rutaX] = "X" #rutaX och ruta
                    brade[rutaY][rutaX] = brdtyp.Kontrollera(brade, rutaY, rutaX)
                    print(brade[rutaY][rutaX])
                    if brade[rutaY][rutaX] == "X":
                        if Placera_GrafisktTroll(brade, rutaY, rutaX,TrollX,TrollY) != "O":
                            print_pa_skarm(fonster, "Snyggt!")
                    elif brade[rutaY][rutaX] == "O":
                        print_pa_skarm(fonster,"Ett troll per diagonal/kolumn!")
            except:
                continue
            if len(raknarlista) == brdstrlk:
                txtTid, txtPong = brdtyp.ta_tid(2)
                pygame.display.set_caption("Arga Troll Highscore")
                fonsterscore = pygame.display.set_mode((fonsterbredd,fonsterhojd))
                print_pa_skarm(fonsterscore,str(txtTid),300,500)
                print_pa_skarm(fonsterscore, str(txtPong),300,400)
                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                            return False
        pygame.display.update()


def rita_brade():#ritar rutorna
    for rutaX in range(brdstrlk):
        for rutaY in range(brdstrlk):
            koordinatX, koordinatY = koordinat(rutaX,rutaY)
            pygame.draw.rect(fonster, Vit, (koordinatX, koordinatY, rutstrlk, rutstrlk))

def koordinat(rutaX,rutaY): #koordinaten för rutan av knapptryck
    X = XMARGIN + rutaX*(rutstrlk+mellanrum)
    Y = YMARGIN + rutaY*(rutstrlk+mellanrum)
    return X, Y

def hittaRuta(x,y):#tar emot position av mustrycket och returnerar rutan som tryckt i både listkoordinater, och koordinater för brädet
    for rutaX in range(brdstrlk):
        for rutaY in range(brdstrlk):
            koordinatX, koordinatY = koordinat(rutaX, rutaY)
            TrycktRuta = pygame.Rect(koordinatX, koordinatY, rutstrlk, rutstrlk)
            if TrycktRuta.collidepoint(x,y):
                return (koordinatX, koordinatY, rutaX, rutaY)
    #return (None, None)

def Placera_GrafisktTroll(brade, rutaY, rutaX, TrollX,TrollY): #Tar in koordinaterna av rutan och listruan för att placera trolet på brädet ifall rutan redan har ett troll försvinner trollet
    if fonster.get_at((TrollX, TrollY)) == Vit and rutaY == len(raknarlista):
        pygame.draw.rect(fonster, Rod, (TrollX, TrollY, rutstrlk, rutstrlk))
        raknarlista.append(1)
    elif fonster.get_at((TrollX, TrollY)) == Rod and rutaY == len(raknarlista)-1:
        pygame.draw.rect(fonster, Vit, (TrollX, TrollY, rutstrlk, rutstrlk))
        brade[rutaY][rutaX] = "O"
        del raknarlista[0]
        return brade[rutaY][rutaX]
    else: #felhantering
        if rutaY < len(raknarlista):
            if fonster.get_at((TrollX, TrollY)) == Rod:
                print_pa_skarm(fonster,"Tryck bort trollen på raderna nedanför först!")
            else:
                print_pa_skarm(fonster,"Ett troll per rad!")
        else:
            print_pa_skarm(fonster,"Placera troll, rad för rad!")
        brade[rutaY][rutaX] = "O"
        return brade[rutaY][rutaX]
    pygame.display.update()


def meddelande(): #skapar fönster med instruktioenr som reutrnar input som brädstorlek (första skärmen)
    pygame.display.set_caption("Arga Troll")
    fonstermed = pygame.display.set_mode((fonsterbredd,fonsterhojd)) #skapar fönser
    loopa_instruktioner(fonstermed)
    input_box = pygame.Rect(30,500,140,32)
    pygame.display.update()
    text = ''
    done = False #håller fönstret igång

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    try:
                        brdstrlk = int(text)
                        if brdstrlk <= maxgräns and brdstrlk >= minimigräns:
                            done = True #stänger fönstret när man tryckt enter som uppfyllt kraven
                        print_pa_skarm(fonstermed,"Skriv ett nummer mellan 4 och 8!")
                    except:
                        print_pa_skarm(fonstermed,"Använd siffror!")

                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        pygame.draw.rect(fonstermed, Vit,input_box)
        skarmtxt = font.render(text,True, Svart)
        fonstermed.blit(skarmtxt,(input_box.x+5,input_box.y+5))
        pygame.display.update()
    return brdstrlk

def print_pa_skarm(window,txt,skarmstrlkX=500,skarmstrlkY=500): #gör om allt som i den ickegrafiska koden skulle printas så den printas på skärm
    pygame.draw.rect(window,Svart,(skarmstrlkX,skarmstrlkY,500,32))
    utskrift = font.render(txt,True, Vit)
    window.blit(utskrift,(skarmstrlkX,skarmstrlkY,140,32))
    pygame.display.update()

def loopa_instruktioner(window): #printar första fönstret med instruktioner och highscore
    radmsg = 0
    introduktion = Brade()
    instruktionmsg = introduktion.instruktioner()
    for msg in instruktionmsg:
        radmsg += 1
        utskrift = font.render(msg,True, Vit)
        window.blit(utskrift,(30,30*radmsg,80,80))
        pygame.display.update()
    kommandoskrift = font.render("Skriv tal här:",True,Vit)
    window.blit(kommandoskrift,(30,480,140,32))
    fa_hiscore = Brade()
    hiscore = str(fa_hiscore.hamta_highscore())
    hiscoreskrift = font.render(("Higscore: "+hiscore),True,Vit)
    window.blit(hiscoreskrift,(30,300,140,32))



main()
