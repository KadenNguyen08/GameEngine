import pygame as pg
#create a loop that loops through the list over and over 

frames = ['frame1', 'frame2', 'frame3', 'frame4']
x = 0
print(frames[x])
x+=1
print(frames[x])
x+=1
print(frames[x])
x+=1
print(frames[x])
x+=1
 #x is now 4
#print(frames[x])
firstFrame = x%len(frames)
print(frames[firstFrame])

last_update = 0
while True:
    now = pg.time.get_ticks()
    if now - then > 350:
        print("time for a new frame")
        then = now
    clock.tick(FPS)

    
    