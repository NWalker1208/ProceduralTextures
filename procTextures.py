import sys, pygame, math
import noise

def clamp(fl, mn, mx):
    return min(mx, max(mn, fl))


def roundToInt(fl):
    return int(round(fl))


# X and Y tile from 0 to 1
def tileNoise(u, v, mn = -1, mx = 1, u_scale = 1, v_scale = 1, octaves = 1, x = 0, y = 0, z = 0, w = 0):
    angleU = (u % 1) * 2 * math.pi
    angleV = (v % 1) * 2 * math.pi

    rU = 1 / (2 * math.pi * u_scale)
    rV = 1 / (2 * math.pi * v_scale)
    
    x += math.cos(angleU) * rU
    y += math.sin(angleU) * rU
    z += math.cos(angleV) * rV
    w += math.sin(angleV) * rV
    
    return (clamp(noise.snoise4(x, y, z, w, octaves) + 1, 0, 2) / 2) * (mx - mn) + mn


def normalColorRGB(r, g, b):
    r = clamp(r, 0, 1)
    g = clamp(g, 0, 1)
    b = clamp(b, 0, 1)
    
    return pygame.Color(roundToInt(r * 255), roundToInt(g * 255), roundToInt(b * 255), 255)


def normalColorHSV(h, s, v):
    h = clamp(h, 0, 1)
    s = clamp(s, 0, 1)
    v = clamp(v, 0, 1)
    
    clr = pygame.Color()
    clr.hsva = (roundToInt(h * 360), roundToInt(s * 100), roundToInt(v * 100), 100)
    
    return clr


def mapFloatToColorMap(colorMap, fl):
    return colorMap.get_at((roundToInt(clamp(fl, 0, 1) * colorMap.get_width()), 0))



roadColors = pygame.image.load("colormaps/road2.bmp")

def roadShader(x, y, tileWidth, tileHeight, scale = 1, offsetX = 0, offsetY = 0):
        scale *= 0.02
        c = tileNoise(*(x / tileWidth + offsetX, y / tileHeight + offsetY), *(0, 1), scale, scale, 10)

        return mapFloatToColorMap(roadColors, c) #normalColorRGB(r, g, b)


worldColors = pygame.image.load("colormaps/world.bmp")

def worldShader(x, y, tileWidth, tileHeight, scale = 1, offsetX = 0, offsetY = 0):
        scale *= 0.5
        c = tileNoise(*(x / tileWidth + offsetX, y / tileHeight + offsetY), *(0, 1), scale, scale, 10)

        return mapFloatToColorMap(worldColors, c)


woodColors = pygame.image.load("colormaps/wood.bmp")

def woodShader(x, y, tileWidth, tileHeight, scale = 1, offsetX = 0, offsetY = 0):
        scale *= 0.05
        c = tileNoise(*(x / tileWidth + offsetX, y / tileHeight + offsetY), *(0, 1), scale, scale * 4, 10)

        return mapFloatToColorMap(woodColors, c)



def drawShader(texture, shader, tileWidth, tileHeight, scale = 1, offsetX = 0, offsetY = 0):
    pxArr = pygame.PixelArray(texture)
    for x in range(0, texture.get_width()):
        for y in range(0, texture.get_height()):
            if shader == "road":
                pxArr[x, y] = roadShader(*(x, y), *(tileWidth, tileHeight), scale, *(offsetX, offsetY))
            elif shader == "world":
                pxArr[x, y] = worldShader(*(x, y), *(tileWidth, tileHeight), scale, *(offsetX, offsetY))
            elif shader == "wood":
                pxArr[x, y] = woodShader(*(x, y), *(tileWidth, tileHeight), scale, *(offsetX, offsetY))


def updateDisplay(screen, texture):
    screen.blit(texture, (0, 0))
    pygame.display.flip()


pygame.init()

size = width, height = 640, 640
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
texture = pygame.Surface(size)

keyDown = False

lastShader = ""

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    press = pygame.key.get_pressed()
    
    if not keyDown:
        if press[pygame.K_LEFT] != 0:
            print("Generating road...")
            lastShader = "road"
            drawShader(texture, lastShader, *size)
            print("done")
            keyDown = True
            
        elif press[pygame.K_RIGHT] != 0:
            print("Generating world...")
            lastShader = "world"
            drawShader(texture, lastShader, *size)
            print("done")
            keyDown = True
            
        elif press[pygame.K_UP] != 0:
            print("Generating wood...")
            lastShader = "wood"
            drawShader(texture, lastShader, *size)
            print("done")
            keyDown = True
            
        elif press[pygame.K_s] != 0:
            if lastShader != "":
                print("saving...")
                if press[pygame.K_x] != 0:
                    mult = 1
                    if press[pygame.K_2] != 0: mult = 2
                    if press[pygame.K_3] != 0: mult = 3
                    if press[pygame.K_4] != 0: mult = 4

                    largeTexture = pygame.Surface((width * mult, height * mult))
                    drawShader(largeTexture, lastShader, *(width * mult, height * mult))
                    pygame.image.save(largeTexture, lastShader + "_x" + str(mult) + ".png")
                else:
                    pygame.image.save(screen, lastShader + ".png")
                print("done")
            keyDown = True
        
    else:
        if (press[pygame.K_LEFT] == 0 and press[pygame.K_RIGHT] == 0 and
            press[pygame.K_UP] == 0 and press[pygame.K_DOWN] == 0 and
            press[pygame.K_s] == 0):
            keyDown = False

    updateDisplay(screen, texture)
