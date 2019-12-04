import pygame as pg
import random        
pg.init()
Sounds={'eat':'sounds\Eatting.ogg','die':'sounds\Dying.ogg'}
Music = []
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
    global playedMus,Music,TimesPlayed
    if TimesPlayed==len(Music):
        random.shuffle(Music)
        TimesPlayed=0
        return
    name=Music[TimesPlayed]
    TimesPlayed+=1
    pg.mixer.music.load(name)
    pg.mixer.music.set_volume(vol)
    pg.mixer.music.play(0)
    
def testMusic():
    if pg.mixer.music.get_busy()==0:
        playmusic(1)

def playsound(name,i,vol):
    sound=pg.mixer.Sound(name)
    sound.set_volume(vol)
    sound.play(i)

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
    file=open('songtype.txt','w')
    file.write(songtype)
    file.close()


def text_objects(text, font,i):
    global sur
    textSurface = font.render(text, True,(i,i,i))
    return textSurface, textSurface.get_rect()

def button(msg,sur,x,y,w,h,ic,ac,i,act=None):
    global mouse, click
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(sur, ac,(x,y,w,h))
        if click == 1 and act != None:
            click = 0
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

    if GFExis:
        sur.blit(Fruits[1],(GFruit[0],GFruit[1]))

    sur.blit(Fruits[0],(Fruit[0],Fruit[1]))

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
    msg='Score:'+str(Score)
    Textsome(msg,sur,20,70,130,20,255,30)
    file=open('record.txt','r')
    line=file.read()
    msg='Record:'+str(line)
    Textsome(msg,sur,620,70,130,20,255,30)
    file.close()
    if Score > int(line):
        file=open('record.txt','w')
        file.write(str(Slen))
        file.close()

    
def surupdate():
    global sur
    pg.display.update()
    sur.fill((0,0,0))

def initFruit(W,H,size,Fruit1,Snake,Snakehead,Slen):
    global GFMake, GFruit, Fruit
    ex=True
    while ex:
        fx=random.randint(10,((W/size)-1))*size
        fy=random.randint(11,((H/size)-1))*size
        Fruit1=[fx,fy]
        if GFMake:
            if Fruit1 in Snake or Fruit1==Fruit:
                ex = True
            else:
                ex=False
        else:
            if Fruit1 in Snake or Fruit1==GFruit:
                ex = True
            else:
                ex=False
    return Fruit1
      
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

def keepplaing():
    global Pause
    Pause=False

def gotomenu():
    global settings, play, menu, Pause
    settings=False
    play=False
    menu=True
    Pause=False
   
presettings=False  
work=True
play=False
menu=True
intro=True
settings=False
Pause=False
gameover=False

TimesPlayed=0
file=open('songtype.txt','r')
songtype=file.read()
file.close()
fillMusic()

mouse=pg.mouse.get_pos()
click=pg.mouse.get_pressed()
testMusic()
while work :
    W=800
    H=600
    #pg.init()
    sur=pg.display.set_mode(size=(W,H),flags=pg.FULLSCREEN)

    i=0
    while intro:
        i+=1
        largeText = pg.font.SysFont('times new roman', 40)
        TextSurf, TextRect=text_objects('The Game by Aytomik and Vaider',largeText,i)
        TextRect.center = ((400),(300))
        sur.blit(TextSurf, TextRect)
        surupdate()
        pg.time.delay(15)
        if i == 225:
            menu=True
            intro=False
        for event in pg.event.get():
            if event.type==pg.KEYUP or event.type==pg.MOUSEBUTTONDOWN:
                menu=True
                intro=False
                break

    while menu:
        for event in pg.event.get():
                keys=pg.key.get_pressed()
                if event.type == pg.MOUSEMOTION:
                         mouse=event.pos
                if event.type == pg.MOUSEBUTTONUP:
                         mouse=event.pos
                         click=event.button
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    play = False
                    pg.quit()
                    break

        n=255
        button('Play',sur,W/2-75,H/2-25,150,40,(0,50,0),(100,200,100),n,choicelvl)
        button('Quit',sur,W/2-75,H/2+20,150,40,(50,0,0),(200,100,100),n,quit)
        button('Settings',sur,W/2-75,H/2+65,150,40,(30,30,30),(50,50,50),n,startsettings)

        surupdate()
        songtype= open('songtype.txt','r')
        testMusic()
    while settings:
        for event in pg.event.get():
            keys=pg.key.get_pressed()
            if event.type == pg.MOUSEMOTION:
                         mouse=event.pos
            if event.type == pg.MOUSEBUTTONUP:
                         mouse=event.pos
                         click=event.button
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                menu = True
                settings = False
                break
        songtype='Retrowave'
        button('Retrowave',sur,W/2-47,H/2+40,170,32,(30,30,30),(60,60,60),n,fillMusic)
        songtype='Pop'
        button('Pop',sur,W/2-47,H/2+80,170,32,(30,30,30),(60,60,60),n,fillMusic)
        songtype = 'OffMusic'
        button('Off Music',sur,W/2-47,H/2+120,170,32,(30,30,30),(60,60,60),n,fillMusic)
        surupdate()
        testMusic()

    while presettings:
        for event in pg.event.get():
            keys=pg.key.get_pressed()
            if event.type == pg.MOUSEMOTION:
                         mouse=event.pos
            if event.type == pg.MOUSEBUTTONUP:
                         mouse=event.pos
                         click=event.button
            if keys[pg.K_ESCAPE] :
                menu = True
                presettings = False
                break
        
        button('Easy',sur,W-675,H/2-75,150,150,(0,70,0),(0,100,0),n,setlvlez)
        button('Medium',sur,W/2-75,H/2-75,150,150,(70,70,0),(100,100,0),n,setlvlmed)
        button('Hard',sur,W-275,H/2-75,150,150,(70,0,0),(100,0,0),n,setlvlhard)
        surupdate()
    if play==True:
        size=10
        speed=1*size
        FPS = 10
        Score=0
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
        GFMake=False
        bool=True
        counter=0
        index=0
        Fruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
        GFruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)

        while play:
            pressed = False
            pg.time.delay(lvl)
            for event in pg.event.get():
                keys=pg.key.get_pressed()
                if event.type == pg.QUIT:
                    play = False
                    pg.quit()
                    break
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        Pause = True
            Snakehead=[x,y]
            if Slen > Score:
                Score+=1
            if counter>=5:
                GFExis=True                                                
                if index>(5000/lvl):
                    counter=0
                    index=0
                    GFExis=False
                    GFMake=True
                    GFruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
                    GFMake=False
                index+=1
                if Snakehead==GFruit:
                    playsound(Sounds['eat'],0,1)
                    GFMake=True
                    GFruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
                    GFMake=False
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
                pg.time.delay(3500)
                play = False
                gameover=True

            if Snakehead==Fruit:
                playsound(Sounds['eat'],0,1)
                Fruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
                mult=random.randint(1,mult)
                for i in range(0,mult):
                    Snake.append([Snake[Slen-2][0],Snake[Slen-2][1]]) 
                    dirmove.append(int(dirmove[Slen-2])) 
                    tailmove.append(int(tailmove[Slen-2]))   
                Slen+=mult
                counter+=1

            if not pressed:
                if (keys[pg.K_w] or keys[pg.K_UP]) and (not(move == 's')):
                    move = 'w'
                    ym=-speed
                    xm=0
                    pressed=True
                elif (keys[pg.K_s] or keys[pg.K_DOWN]) and (not(move == 'w')):
                    move = 's'
                    ym=speed
                    xm=0
                    pressed=True
                elif (keys[pg.K_a] or keys[pg.K_LEFT]) and (not(move == 'd')):
                    move = 'a'
                    xm=-speed
                    ym=0
                    pressed=True
                elif (keys[pg.K_d] or keys[pg.K_RIGHT]) and (not(move == 'a')):
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
            while Pause:
                surupdate()
                for event in pg.event.get():
                     if event.type == pg.MOUSEMOTION:
                         mouse=event.pos
                     if event.type == pg.MOUSEBUTTONUP:
                         click=event.button

                button('Resume',sur,W/2-75,H/2-20,150,40,(0,70,0),(0,100,0),n,keepplaing)
                button('Menu',sur,W/2-75,H/2+25,150,40,(70,0,0),(100,0,0),n,gotomenu)
                testMusic()
    blink=0
    blink_phase=0
    while gameover:
        Textsome('Game over',sur, W/2-50, H/2-150,100,300,255,40)
        Textsome('Press any key to continue',sur, W/2-50, H/2+50,100,300,blink,22)
        Textsome('Your score:'+str(Score),sur, W/2-50, H/2-75,100,300,255,26)
        surupdate()
        if blink_phase == 0:
            blink+=1
            if blink==255:
                blink_phase=1
        else:
            blink-=1
            if blink==0:
                blink_phase=0
        
        for event in pg.event.get():
            if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONUP:
                gameover=False
                menu=True
           