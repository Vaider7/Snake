import pygame as pg
import random        
pg.init()
pg.mixer.init()
Sounds={'eat':'sounds\Eatting.ogg','die':'sounds\Dying.ogg'}
#'music\Retrowave\RetroWave.mp3',"""'music\Kda_-_Popstars.mp3','music\Savlonic-The Rider.mp3'"""
Music = []
playedMus=[]
Snake_head = [pg.image.load('sprites\Snake_head_w.png'),pg.image.load('sprites\Snake_head_d.png'),
              pg.image.load('sprites\Snake_head_s.png'),pg.image.load('sprites\Snake_head_a.png')]
Snake_body = [pg.image.load('sprites\Snake_body_v.png'),pg.image.load('sprites\Snake_body_h.png'),
              pg.image.load('sprites\Snake_body_v.png'),pg.image.load('sprites\Snake_body_h.png'),
              pg.image.load('sprites\Snake_body_t_wd.png'),pg.image.load('sprites\Snake_body_t_wa.png'),
              pg.image.load('sprites\Snake_body_t_sd.png'),pg.image.load('sprites\Snake_body_t_sa.png')]

Snake_tail = [pg.image.load('sprites\Snake_tail_w.png'),pg.image.load('sprites\Snake_tail_d.png'),
              pg.image.load('sprites\Snake_tail_s.png'),pg.image.load('sprites\Snake_tail_a.png')]

Fruits=[pg.image.load('sprites\Fruit.png'),pg.image.load('sprites\GFruit.png')]

def setlvlez():
    global lvl, presettings, play
    lvl=80
    presettings=False
    play=True

def setlvlmed():
    global lvl, presettings, play
    lvl=60
    presettings=False
    play=True

def setlvlhard():
    global lvl, presettings, play
    lvl=40
    presettings=False
    play=True

def playmusic(vol):
    #chan=pg.mixer.Channel(0)
    global playedMus,Music,TimesPlayed
    if TimesPlayed==len(Music):
        playedMus=[]
        random.shuffle(Music)
        TimesPlayed=0
        return
    name=Music[TimesPlayed]
    playedMus.append(name)
    TimesPlayed+=1
    pg.mixer.music.load(name)
    pg.mixer.music.set_volume(vol)
    pg.mixer.music.play(0)
    
def testMusic():
    if pg.mixer.music.get_busy()==0:
        playmusic(1)
    #sound=pg.mixer.Sound(name)
    #chan.set_volume(vol)
    #chan.play(sound,i)
def playsound(name,i,vol):
    chan=pg.mixer.Channel(1)
    sound=pg.mixer.Sound(name)
    chan.set_volume(vol)
    chan.play(sound,i)

def fillMusic():
    pg.mixer.music.stop()
    global songtype, Music, TimesPlayed, playmusic
    name=songtype
    way='music\%s'% name
    fileway=way+'\\'
    way+='\songs.txt'
    Songs=open(way,'r')
    Music=[]
    TimesPlayed=0
    for line in Songs:
        if '\n' in line:
            line=line[:len(line)-1:1]
        Music.append(fileway+line)
    random.shuffle(Music)
    playmusic(1)

def text_objects(text, font,i):
    global sur
    textSurface = font.render(text, True,(i,i,i))
    return textSurface, textSurface.get_rect()

def button(msg,sur,x,y,w,h,ic,ac,i,act=None):
    global mouse, click
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(sur, ac,(x,y,w,h))
        if click[0] == 1 and act != None:
            act()
    else:
        pg.draw.rect(sur, ic,(x,y,w,h))
          
    smallText = pg.font.Font("ConnectionSerif.otf",30)
    textSurf, textRect = text_objects(msg, smallText,i)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    sur.blit(textSurf, textRect)
def Textsome(msg,sur,x,y,w,h,i,Size):
    smallText = pg.font.Font("ConnectionSerif.otf",Size)
    textSurf, textRect = text_objects(msg, smallText,i)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    sur.blit(textSurf, textRect)
def polzinormalno():
    global dirmove, tailmove, Slen
    for i in range(0,Slen-2):
        if ((tailmove[i+1]==0) and (tailmove[i]==1)) or ((tailmove[i+1]==3) and (tailmove[i]==2)): 
            dirmove[i]=4
        if ((tailmove[i+1]==0) and (tailmove[i]==3)) or ((tailmove[i+1]==1) and (tailmove[i]==2)): 
            dirmove[i]=5
        if ((tailmove[i+1]==2) and (tailmove[i]==1))or((tailmove[i+1]==3)and(tailmove[i]==0)): 
            dirmove[i]=6
        if ((tailmove[i+1]==2) and (tailmove[i]==3))or((tailmove[i+1]==1)and(tailmove[i]==0)):
            dirmove[i]=7


def drawobj():
    global sur,size, Fruit, GFruit, GFExis, move, dirmove, Slen, Snakehead, Snake, Snake_head, Snake_body
    dir=0
    #Drawing Fruits
    if GFExis:
        sur.blit(Fruits[1],(GFruit[0],GFruit[1]))

    sur.blit(Fruits[0],(Fruit[0],Fruit[1]))

    #Drawing Snake
    if move=='w':
        dir=0
    if move=='d':
        dir=1
    if move=='s':
        dir=2
    if move=='a':
        dir=3
    sur.blit(Snake_head[dir],(Snakehead[0],Snakehead[1]))

    for i in range(0,Slen-2):
        sur.blit(Snake_body[dirmove[i]],(Snake[i][0],Snake[i][1]))

    sur.blit(Snake_tail[tailmove[Slen-2]],(Snake[Slen-2][0],Snake[Slen-2][1]))

def drawsur():
    global sur,W ,H, size
    pg.draw.lines(sur,(255,255,255),True,[(0,0),(0,H-1),(W-1,H-1),(W-1,0)])
    pg.draw.line(sur,(255,255,255),(0,size*10),(W-1,size*10))

    
def surupdate():
    global sur
    pg.display.update()
    sur.fill((0,0,0))

def initFruit(W,H,size,Fruit,Snake,Snakehead,Slen):
    ex=True
    while ex:
      fx=random.randint(10,((W/size)-1))*size
      fy=random.randint(11,((H/size)-1))*size
      Fruit=[fx,fy]
      if Fruit in Snake:
          ex = True
      else:
          ex=False
    return Fruit
      
def quit():
    global menu, work
    menu=False
    work=False


def choicelvl():
    global presettings, menu
    presettings=True
    menu=False

def startsettings():
    global menu, settings
    menu=False
    settings=True

    
presettings=False  
work=True
play=False
menu=True
intro=True
settings=False

TimesPlayed=0
songtype='Retrowave'
fillMusic()

event=pg.event.get()
mouse=pg.mouse.get_pos()
click=pg.mouse.get_pressed()
#random.shuffle(Music)
testMusic()
while work :
    W=800
    H=600
    pg.init()
    sur=pg.display.set_mode(size=(W,H),flags=pg.FULLSCREEN)
    while intro:
        for i in range(0,256):
            largeText = pg.font.SysFont('times new roman', 40)
            TextSurf, TextRect=text_objects('The Game by Aytomik and Vaider',largeText,i)
            TextRect.center = ((400),(300))
            sur.blit(TextSurf, TextRect)
            pg.display.update()
            sur.fill((0,0,0))
            pg.time.delay(15)
            if i == 225:
                menu=True
                intro=False
            event=pg.event.get()
            keys=pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                menu=True
                intro=False
                break
    while menu:
        for event in pg.event.get():
                keys=pg.key.get_pressed()
                mouse=pg.mouse.get_pos()
                click=pg.mouse.get_pressed()
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    play = False
                    pg.quit()
                    break
        n=255
        button('Play',sur,W/2-47,H/2-20,150,32,(0,50,0),(100,200,100),n,choicelvl)
        button('Quit',sur,W/2-47,H/2+20,150,32,(50,0,0),(200,100,100),n,quit)
        button('Settings',sur,W/2-47,H/2+60,150,32,(30,30,30),(50,50,50),n,startsettings)

        pg.display.update()
        sur.fill((0,0,0))
        testMusic()

    while settings:
        for event in pg.event.get():
            keys=pg.key.get_pressed()
            mouse=pg.mouse.get_pos()
            click=pg.mouse.get_pressed()
            if event.type == pg.QUIT or keys[pg.K_ESCAPE] :
                menu = True
                settings = False
                break
        songtype='Retrowave'
        button('Retrowave',sur,W/2-47,H/2+40,170,32,(20,20,20),(50,50,50),n,fillMusic)
        songtype='Pop'
        button('Pop',sur,W/2-47,H/2+80,170,32,(30,30,30),(60,60,60),n,fillMusic)
        pg.display.update()
        sur.fill((0,0,0))
        testMusic()
    k=100
    while presettings:
        pg.time.delay(k)
        if k == 100:
            for p in range(0,10):
                p+=1
                if p == 9:
                    k=0
        for event in pg.event.get():
            keys=pg.key.get_pressed()
            mouse=pg.mouse.get_pos()
            click=pg.mouse.get_pressed()
            if keys[pg.K_ESCAPE] :
                menu = True
                presettings = False
                break
        lvl=60
        button('Easy',sur,W-675,H/2-75,150,150,(0,70,0),(0,100,0),n,setlvlez)
        button('Medium',sur,W/2-75,H/2-75,150,150,(70,70,0),(100,100,0),n,setlvlmed)
        button('Hard',sur,W-275,H/2-75,150,150,(70,0,0),(100,0,0),n,setlvlhard)
        pg.display.update()
        sur.fill((0,0,0))


    if play==True:
        size=10
        speed=1*size
        FPS = 10
        Snakehead=[None,None]
        Snake=[]
        dirmove=[]
        tailmove=[]
        Slen=10
        mult=3
        Counter2=Slen-2
        x = random.randint(Slen,int(W/size))*size
        y = random.randint(10,int(H/size))*size
        sur=pg.display.set_mode(size=(W,H),flags = pg.FULLSCREEN)
        pg.display.set_caption('Snake')
        play=True
        xm = 0
        ym = 0
        move='d'
        if move=='w':
            ym=-speed
        if move=='s':
            ym=speed
        if move=='a':
            xm=-speed
        if move=='d':
            xm=speed

        for i in range(0,Slen-1):
            Snake.append([None]*2)
            dirmove.append(1)
            tailmove.append(1)
        for i in range(0,Slen-1):
            Snake[i]=[(x-(1+i)*size),y]
        Fruit=[None,None]
        GFruit=[None,None]
        GFExis=False
        bool=True
        counter=0
        index=0
        Fruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
        GFruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
        while play:
            pressed=False
            pg.time.delay(lvl)
            for event in pg.event.get():
                keys=pg.key.get_pressed()

                if event.type == pg.QUIT:
                    play = False
                    pg.quit()
                    break
                if keys[pg.K_ESCAPE]:
                    menu=True
                    play=False
            Snakehead=[x,y]
            
            
            if counter>=5:
                GFExis=True                                                
                if index>100:
                    counter=0
                    index=0
                    GFExis=False
                    GFruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
                index+=1
                if Snakehead==GFruit:
                    GFruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
                    mult=random.randint(1,4)
                    for i in range(0,3*mult):
                            dirmove.append(int(dirmove[Slen-2])) 
                            tailmove.append(int(tailmove[Slen-2])) 
                            Snake.append([Snake[Slen-2][0],Snake[Slen-2][1]])
                    Slen+=3*mult
                    counter=0
                    index=0
                    GFExis=False


        
            if Snakehead in Snake:
                playsound(Sounds['die'],0,0.7)
                pg.time.delay(1000)
                menu=True
                play = False
                break

            if Snakehead==Fruit:
                playsound(Sounds['eat'],0,1)
                Fruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
                mult=random.randint(1,4)
                for i in range(0,mult):
                    Snake.append([Snake[Slen-2][0],Snake[Slen-2][1]]) 
                    dirmove.append(int(dirmove[Slen-2])) 
                    tailmove.append(int(tailmove[Slen-2]))   #Snake.append([Snake[Slen-3][0],Snake[Slen-3][1]])
                Slen+=mult
                counter+=1

            if not pressed:
                if keys[pg.K_w] and (not(move == 's')):
                    move = 'w'
                    ym=-speed
                    xm=0
                    pressed=True
                elif keys[pg.K_s] and (not(move == 'w')):
                    move = 's'
                    ym=speed
                    xm=0
                    pressed=True
                elif keys[pg.K_a] and (not(move == 'd')):
                    move = 'a'
                    xm=-speed
                    ym=0
                    pressed=True
                elif keys[pg.K_d] and (not(move == 'a')):
                    move = 'd'
                    xm=speed
                    ym=0
                    pressed=True
    
            x+=xm
            y+=ym
            if x<0:
                x=W-size
            if x>(W-size):
                x=0
            if y<size*10:
                y=H-size
            if y>(H-size):
                y=size*10
            msg='Score:'+str(Slen)
            Textsome(msg,sur,20,70,130,20,255,30)
            file=open('record.txt','r')
            line=file.read()
            msg='Record:'+str(line)
            Textsome(msg,sur,500,70,130,20,255,30)
            if Slen > int(line):
                file.close()
                file=open('record.txt','w')
                file.write(str(Slen))
                file.close()


            drawobj()
            drawsur()


           
            for i in range((Slen-2),(-1),-1):
                Snake[i]=[(Snake[i-1][0]),(Snake[i-1][1])]
            Snake[0]=[Snakehead[0],Snakehead[1]]
            for i in range((Slen-2),(-1),-1):
                dirmove[i]=int(dirmove[i-1])
            if move=='w':
                dirmove[0]=0
            if move=='d':
                dirmove[0]=1
            if move=='s':
                dirmove[0]=2
            if move=='a':
                dirmove[0]=3

            for i in range((Slen-2),(-1),-1):
                tailmove[i]=int(tailmove[i-1])
            if move=='w':
                tailmove[0]=0
            if move=='d':
                tailmove[0]=1
            if move=='s':
                tailmove[0]=2
            if move=='a':
                tailmove[0]=3

            surupdate()
            polzinormalno() 
            testMusic()