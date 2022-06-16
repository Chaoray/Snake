import time
import os
import win32api
import random

mapHeight = 20
mapWidth = 20

texture = ('X', '#', '@')
buffer = [' ' for i in range(mapWidth * mapHeight)]

def renderEdge():
    for x in range(mapWidth):
        buffer[x] = texture[0]
        buffer[len(buffer) - x - 1] = texture[0]
    for y in range(mapHeight):
        buffer[y * mapWidth] = texture[0]
        buffer[(y + 1) * mapWidth - 1] = texture[0]

def renderBuffer():
    for y in range(mapHeight):
        for x in range(mapWidth):
            print(buffer[y * mapWidth + x], end='')
        print()

def toBufferPoint(point):
    return mapWidth * point[1] + point[0]

def playSound():
    print('\a', end="") # this sounds weird

def getRandomPoint():
    p = (random.randint(1, mapWidth - 2), random.randint(1, mapHeight - 2))
    try:
        snake.index(p)
        return getRandomPoint()
    except ValueError:
        return p

renderEdge()

# configs
snake = [(3, 3), (3, 4)]
getLonger = False
speed = 1
direction = (random.randint(-1, 1), 0)
direction = (direction[0], int(not direction[0]))

nextAppleTime = 0
apple = getRandomPoint()
isAte = True
score = 0

while True:
    time.sleep(0.7 / speed)

    if win32api.GetAsyncKeyState(ord('W')):
        if direction != (0, 1):
            direction = (0, -1)
    elif win32api.GetAsyncKeyState(ord('S')):
        if direction != (0, -1):
            direction = (0, 1)
    elif win32api.GetAsyncKeyState(ord('A')):
        if direction != (1, 0):
            direction = (-1, 0)
    elif win32api.GetAsyncKeyState(ord('D')):
        if direction != (-1, 0):
            direction = (1, 0)

    if nextAppleTime <= 0:
        if isAte:
            buffer[toBufferPoint(apple)] = texture[2]
            apple = getRandomPoint()
            nextAppleTime = random.randint(3, 10)
            isAte = False
    else:
        nextAppleTime -= 1

    snake.insert(0, (snake[0][0] + direction[0], snake[0][1] + direction[1]))
    if not getLonger:
        tail = snake.pop(len(snake) - 1)
    getLonger = False

    if buffer[toBufferPoint(snake[0])] == texture[0]:
        break
    
    if buffer[toBufferPoint(snake[0])] == texture[1]:
        break

    if buffer[toBufferPoint(snake[0])] == texture[2]:
        getLonger = True
        isAte = True
        score += 1
        speed += 0.05
        playSound()

    for i in range(len(snake)):
        buffer[toBufferPoint(snake[i])] = texture[1]
        buffer[toBufferPoint(tail)] = ' '

    os.system('cls')
    renderBuffer()
    print('Score:', score)

print('YOU LOSE')