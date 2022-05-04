import sys
import pygame
import cairosvg
import io

def load_svg(filename):
    new_bites = cairosvg.svg2png(url = filename)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io)


pygame.init()
size = width, height = 480, 320
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
currentWeatherIcon = load_svg("svg/wi-cloudy.svg")
font_18 = pygame.font.Font('jbm.ttf', 18)
font_12 = pygame.font.Font('jbm.ttf', 12)
font_10 = pygame.font.Font('jbm.ttf', 10)

currentTempC = font_18.render('30.0°C', True, (255, 255, 255), (0, 0, 0))
currentTempF = font_12.render('86.0°F', True, (255, 255, 255), (0, 0, 0))
currentWeatherDescription = font_10.render('Partially Cloudy', True, (255, 255, 255), (0, 0, 0))
currentWeatherFeelLike = font_10.render('Feels like: 34.0°C', True, (255, 255, 255), (0, 0, 0))
currentWeatherWind = font_10.render('Wind: SSW @ 19.1 km/h', True, (255, 255, 255), (0, 0, 0))
currentWeatherHumidity = font_10.render('Humidity: 75%', True, (255, 255, 255), (0, 0, 0))
currentTime = font_10.render('Sun, May 4 03:58:05 PM', True, (255, 255, 255), (0, 0, 0))
currentZone = font_10.render('Asia/Singapore', True, (255, 255, 255), (0, 0, 0))

currentWeatherDescriptionRect = currentWeatherDescription.get_rect(center = (80, 64))
currentTimeRect = currentTime.get_rect(center = (320+80, 32))
currentZoneRect = currentZone.get_rect(center = (320+80, 48))

while 1:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(currentWeatherIcon, (20, 8))
    screen.blit(currentTempC, (70, 10))
    screen.blit(currentTempF, (70, 32))
    screen.blit(currentWeatherDescription, currentWeatherDescriptionRect)
    screen.blit(currentWeatherFeelLike, (180, 18))
    screen.blit(currentWeatherWind, (180, 34))
    screen.blit(currentWeatherHumidity, (180, 50))
    screen.blit(currentTime, currentTimeRect)
    screen.blit(currentZone, currentZoneRect)

    pygame.draw.line(screen, (255, 255, 255), (0, 80), (480, 80), 1)
    pygame.draw.line(screen, (255, 255, 255), (160, 0), (160, 80), 1)
    pygame.draw.line(screen, (255, 255, 255), (320, 0), (320, 80), 1)

    pygame.display.flip()