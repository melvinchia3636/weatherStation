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
# screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)

currentWeatherIcon = load_svg("svg/wi-day-cloudy.svg")
morningWeatherIcon = load_svg("svg/wi-day-hail.svg")
afternoonWeatherIcon = load_svg("svg/wi-day-cloudy.svg")
eveningWeatherIcon = load_svg("svg/wi-night-cloudy.svg")
nightWeatherIcon = load_svg("svg/wi-night-clear.svg")

morningWeatherIconRect = morningWeatherIcon.get_rect(center = (0 + 60, 136))
afternoonWeatherIconRect = afternoonWeatherIcon.get_rect(center = (120 + 60, 136))
eveningWeatherIconRect = eveningWeatherIcon.get_rect(center = (240 + 60, 136))
nightWeatherIconRect = nightWeatherIcon.get_rect(center = (360 + 60, 136))

font_18 = pygame.font.Font('jbm.ttf', 18)
font_14 = pygame.font.Font('jbm.ttf', 14)
font_12 = pygame.font.Font('jbm.ttf', 12)
font_10 = pygame.font.Font('jbm.ttf', 10)
font_8 = pygame.font.Font('jbm.ttf', 8)

currentTempC = font_18.render('30.0°C', True, (255, 255, 255), (0, 0, 0))
currentTempF = font_12.render('86.0°F', True, (255, 255, 255), (0, 0, 0))
currentWeatherDescription = font_10.render('Partially Cloudy', True, (255, 255, 255), (0, 0, 0))
currentWeatherFeelLike = font_10.render('Feels like: 34.0°C', True, (255, 255, 255), (0, 0, 0))
currentWeatherWind = font_10.render('Wind: SSW @ 19.1 km/h', True, (255, 255, 255), (0, 0, 0))
currentWeatherHumidity = font_10.render('Humidity: 75%', True, (255, 255, 255), (0, 0, 0))
currentTime = font_10.render('Sun, May 4 03:58:05 PM', True, (255, 255, 255), (0, 0, 0))
currentZone = font_10.render('Asia/Singapore', True, (255, 255, 255), (0, 0, 0))

morningLabel = font_10.render('Morning', True, (255, 255, 255), (0, 0, 0))
afternoonLabel = font_10.render('Afternoon', True, (255, 255, 255), (0, 0, 0))
eveningLabel = font_10.render('Evening', True, (255, 255, 255), (0, 0, 0))
nightLabel = font_10.render('Night', True, (255, 255, 255), (0, 0, 0))

morningTemp = font_14.render('25.9°C', True, (255, 255, 255), (0, 0, 0))
afternoonTemp = font_14.render('30.7°C', True, (255, 255, 255), (0, 0, 0))
eveningTemp = font_14.render('27.0°C', True, (255, 255, 255), (0, 0, 0))
nightTemp = font_14.render('26.8°C', True, (255, 255, 255), (0, 0, 0))

morningWind = font_8.render('SW @ 7.9 km/h', True, (255, 255, 255), (0, 0, 0))
afternoonWind = font_8.render('SW @ 13.3 km/h', True, (255, 255, 255), (0, 0, 0))
eveningWind = font_8.render('S @ 10.4 km/h', True, (255, 255, 255), (0, 0, 0))
nightWind = font_8.render('SW @ 13.3 km/h', True, (255, 255, 255), (0, 0, 0))

currentWeatherDescriptionRect = currentWeatherDescription.get_rect(center = (80, 64))
currentTimeRect = currentTime.get_rect(center = (320+80, 32))
currentZoneRect = currentZone.get_rect(center = (320+80, 48))

morningLabelRect = morningLabel.get_rect(center = (0+60, 96))
afternoonLabelRect = afternoonLabel.get_rect(center = (120+60, 96))
eveningLabelRect = eveningLabel.get_rect(center = (240+60, 96))
nightLabelRect = nightLabel.get_rect(center = (360+60, 96))

morningTempRect = morningTemp.get_rect(center = (0+60, 170))
afternoonTempRect = afternoonTemp.get_rect(center = (120+60, 170))
eveningTempRect = eveningTemp.get_rect(center = (240+60, 170))
nightTempRect = nightTemp.get_rect(center = (360+60, 170))

morningWindRect = morningWind.get_rect(center = (0+60, 186))
afternoonWindRect = afternoonWind.get_rect(center = (120+60, 186))
eveningWindRect = eveningWind.get_rect(center = (240+60, 186))
nightWindRect = nightWind.get_rect(center = (360+60, 186))

while 1:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

    screen.blit(currentWeatherIcon, (20, 8))
    screen.blit(currentTempC, (70, 10))
    screen.blit(currentTempF, (70, 32))
    screen.blit(currentWeatherDescription, currentWeatherDescriptionRect)
    screen.blit(currentWeatherFeelLike, (180, 18))
    screen.blit(currentWeatherWind, (180, 34))
    screen.blit(currentWeatherHumidity, (180, 50mion))
    screen.blit(currentTime, currentTimeRect)
    screen.blit(currentZone, currentZoneRect)

    screen.blit(morningLabel, morningLabelRect)
    screen.blit(afternoonLabel, afternoonLabelRect)
    screen.blit(eveningLabel, eveningLabelRect)
    screen.blit(nightLabel, nightLabelRect)

    screen.blit(morningWeatherIcon, morningWeatherIconRect)
    screen.blit(afternoonWeatherIcon, afternoonWeatherIconRect)
    screen.blit(eveningWeatherIcon, eveningWeatherIconRect)
    screen.blit(nightWeatherIcon, nightWeatherIconRect)

    screen.blit(morningTemp, morningTempRect)
    screen.blit(afternoonTemp, afternoonTempRect)
    screen.blit(eveningTemp, eveningTempRect)
    screen.blit(nightTemp, nightTempRect)

    screen.blit(morningWind, morningWindRect)
    screen.blit(afternoonWind, afternoonWindRect)
    screen.blit(eveningWind, eveningWindRect)
    screen.blit(nightWind, nightWindRect)

    pygame.draw.line(screen, (255, 255, 255), (0, 80), (480, 80), 1)
    pygame.draw.line(screen, (255, 255, 255), (160, 0), (160, 80), 1)
    pygame.draw.line(screen, (255, 255, 255), (320, 0), (320, 80), 1)
    pygame.draw.line(screen, (255, 255, 255), (0, 202), (480, 202), 1)

    pygame.display.flip()