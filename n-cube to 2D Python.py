
'''



Required modules:
    - numpy
    - pygame


Details:
    Author: SMOLDERS Daniel
    Date: 01.06.2018
    More: At home in about 2 days :)

    Description:
        A program that projects higher dimension
        cubes, also called hypercubes or n-cubes, 
        to the 2D screen.
        
        Vertices are projected as red dots and
        edges as thin black lines.
        Other n-faces are not projected (faces,
        cells, ...).
        Everything is projected to the XY plane;
        it is possible to change it by adjusting
        variables 'coord1' and 'coord2'.

        Enjoy!



'''




import math, numpy as np
import pygame, os, sys

n = 4
# !!! 'coord1' and 'coord2' must be < 'n' at all times
# !!! in order to change them, change 'n' accordingly
# !!! and don't go to dimensions <= max(coord1, coord2)
coord1 = 0
coord2 = 1

zoom = 200
maxRot = 0.05
fps = 80
otherM = -0.005

keys = [-0.005]*26

# calculate coordinates of points:
def calcp():
    points = []
    for i in range(2**n):
        b = bin(i)[2:].zfill(n)
        points.append(tuple(int(int(x)*zoom-zoom/2) for x in b))
    return points

# calculate rotation matrices:
def matrix():
    matrices, k = [], 0
    for i in range(0, n-1):
        for j in range(i+1, n):
            try:
                theta = keys[k]
            except:
                theta = otherM
            m = np.identity(n)
            m[i][i] = math.cos(theta)
            m[j][j] = math.cos(theta)
            m[i][j] = math.sin(theta)
            m[j][i] = -math.sin(theta)
            matrices.append(m)
            k += 1
    return matrices

points = calcp()
matrices = matrix()

print(points)
print(matrices)

# center window:
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# window setup:
l = 650
ext = 300
c = l//2
screen = pygame.display.set_mode((l+ext, l))
pygame.display.set_caption('N-Cube Projection To 2D')
clock = pygame.time.Clock()

# text setup:
titleFont = pygame.font.SysFont('pygame', 50)
textFont = pygame.font.SysFont('pygame', 20)
descFont = pygame.font.SysFont('pygame', 22)
desc = [['UP arrow:', 0],
        ['Increase dimension', 1],
        ['DOWN arrow:', 0],
        ['Decrease dimension', 1],
        ['Keyboard letters:', 0],
        ['(a, b, c, ..., z)', 1],
        ['Increase rotation', 1],
        ['SHIFT + keyboard letters:', 0],
        ['Decrease rotation', 1],
        ['RETURN button:', 0],
        ['Reset rotation to 0', 1],
        ['BACKSPACE button:', 0],
        ['Reset rotation to -0.005', 1]]
descText = []
for i in range(len(desc)):
    descText.append(descFont.render(desc[i][0], True, (0, 0, 0)))

while True:

    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # key events:
            hold = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                evt = event.key
                if evt == pygame.K_RETURN:
                    keys = [0.0]*26
                    otherM = 0.0
                    matrices = matrix()
                if evt == pygame.K_BACKSPACE:
                    keys = [-0.005]*26
                    otherM = -0.005
                    matrices = matrix()
                if evt == pygame.K_UP:
                    n += 1
                    points = calcp()
                    matrices = matrix()
                if evt == pygame.K_DOWN:
                    if n > 2:
                        n -= 1
                        points = calcp()
                        matrices = matrix()
                for i in range(27):
                    k = i + 97
                    if hold[pygame.K_LSHIFT] and evt == k and keys[i] > -maxRot:
                        keys[i] -= 0.005
                        keys[i] = round(keys[i], 3) 
                        matrices = matrix()
                    elif evt == k and keys[i] < maxRot:
                        keys[i] += 0.005
                        keys[i] = round(keys[i], 3) 
                        matrices = matrix()

        screen.fill((200, 200, 200))
        pygame.draw.rect(screen, (220, 220, 220), (l, 0, l+ext-80, l))
        pygame.draw.rect(screen, (245, 245, 245), (l+ext-80, 0, l+ext, l))

        # render title and description:
        title = titleFont.render('Projection of ' + str(n) + 'D Hypercube', True, (0, 0, 0))
        screen.blit(title, ((l-title.get_width())//2, 20))
        for i in range(len(desc)):
            if desc[i][1] == 0:
                screen.blit(descText[i], (l+15, 25*i+70))
            else:
                screen.blit(descText[i], (l+ext-descText[i].get_width()-95, 25*i+70))

        # dot vertices with rotation matrices:
        for i in range(len(matrices)):
            points = np.dot(points, matrices[i])
            # and render some more text:
            try:
                text = textFont.render(str(keys[i]), True, (0, 0, 0))
                screen.blit(text, (l+ext-60, 20*i+70))
            except:
                pass

        # to project to 2D, just take 2 coordinates:
        pcrds = [(int(points[x][coord1]+c), int(points[x][coord2]+c)) for x in range(len(points))]

        # drawing the edges:
        # couldn't find a more efficient way...
        for i in range(n):
            arr = 2**n*[None]
            for j in range(2**n):
                k = j+2**i
                try:
                    if arr[j] == None and arr[k] == None:
                        crds = (pcrds[j], pcrds[k])
                        pygame.draw.line(screen, (60, 60, 60), *crds, 1)
                        arr[j], arr[k] = 0, 0
                except:
                    pass

        # drawing the vertices:
        for i in range(len(points)):
            pygame.draw.circle(screen, (0, 0, 0), pcrds[i], 6)
            pygame.draw.circle(screen, (255, 0, 0), pcrds[i], 4)


        pygame.display.flip()
        clock.tick(fps)
        
    except Exception as e:
        print(e)
        pygame.quit()
        sys.exit()


