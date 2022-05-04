import sys
import pygame
import cairosvg
import io
import numpy as np

def load_svg(filename):
    new_bites = cairosvg.svg2png(url = filename)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io)

# Adapted from https://github.com/lordmauve/pgzero/blob/master/pgzero/ptext.py#L81-L143
def wrap_text(text, font, max_width):
    texts = text.replace("\t", "    ").split("\n")
    lines = []

    for text in texts:
        text = text.rstrip(" ")

        if not text:
            lines.append("")
            continue

        # Preserve leading spaces in all cases.
        a = len(text) - len(text.lstrip(" "))

        # At any time, a is the rightmost known index you can legally split a line. I.e. it's legal
        # to add text[:a] to lines, and line is what will be added to lines if
        # text is split at a.
        a = text.index(" ", a) if " " in text else len(text)
        line = text[:a]

        while a + 1 < len(text):
            # b is the next legal place to break the line, with `bline`` the
            # corresponding line to add.
            if " " not in text[a + 1:]:
                b = len(text)
                bline = text
                
            else:
                # Lines may be split at any space character that immediately follows a non-space
                # character.
                b = text.index(" ", a + 1)
                while text[b - 1] == " ":
                    if " " in text[b + 1:]:
                        b = text.index(" ", b + 1)
                    else:
                        b = len(text)
                        break
                bline = text[:b]

            bline = text[:b]

            if font.size(bline)[0] <= max_width:
                a, line = b, bline

            else:
                lines.append(line)
                text = text[a:].lstrip(" ")
                a = text.index(" ", 1) if " " in text[1:] else len(text)
                line = text[:a]

        if text:
            lines.append(line)
    return lines

def create_text(text, font, color, pos, max_width=None):
    if max_width is not None:
        lines = wrap_text(text, font, max_width)
    else:
        lines = text.replace("\t", "    ").split("\n")

    line_ys = (
        np.arange(len(lines))
    ) * 1.05 * font.get_linesize() + pos[1]

    # Create the surface and rect that make up each line
    text_objects = []

    for line, y_pos in zip(lines, line_ys):
        text_surface = font.render(line, True, color)
        text_objects.append((text_surface, (pos[0], y_pos)))

    return text_objects

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

sunriseIcon = load_svg("svg/wi-sunrise.svg")
sunsetIcon = load_svg("svg/wi-sunset.svg")
moonriseIcon = load_svg("svg/wi-moonrise.svg")
moonsetIcon = load_svg("svg/wi-moonset.svg")

sunriseIcon = pygame.transform.scale(sunriseIcon, (30, 30))
sunsetIcon = pygame.transform.scale(sunsetIcon, (30, 30))
moonriseIcon = pygame.transform.scale(moonriseIcon, (30, 30))
moonsetIcon = pygame.transform.scale(moonsetIcon, (30, 30))

moonStateIcon = load_svg("svg/wi-moon-new.svg")

morningWeatherIconRect = morningWeatherIcon.get_rect(center = (0 + 60, 136))
afternoonWeatherIconRect = afternoonWeatherIcon.get_rect(center = (120 + 60, 136))
eveningWeatherIconRect = eveningWeatherIcon.get_rect(center = (240 + 60, 136))
nightWeatherIconRect = nightWeatherIcon.get_rect(center = (360 + 60, 136))

moonStateIconRect = moonStateIcon.get_rect(center = (215 + 50, 236))

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

sunriseLabel = font_8.render('Sunrise', True, (255, 255, 255), (0, 0, 0))
sunsetLabel = font_8.render('Sunset', True, (255, 255, 255), (0, 0, 0))
moonriseLabel = font_8.render('Moonrise', True, (255, 255, 255), (0, 0, 0))
moonsetLabel = font_8.render('Moonset', True, (255, 255, 255), (0, 0, 0))

sunsetTime = font_10.render('06:57 PM', True, (255, 255, 255), (0, 0, 0))
sunriseTime = font_10.render('07:07 AM', True, (255, 255, 255), (0, 0, 0))
moonriseTime = font_10.render('09:28 PM', True, (255, 255, 255), (0, 0, 0))
moonsetTime = font_10.render('09:57 AM', True, (255, 255, 255), (0, 0, 0))

moonStateLabel = font_10.render('New Moon', True, (255, 255, 255), (0, 0, 0))

techNewsLabel = font_8.render('Random Tech News', True, (255, 255, 255), (0, 0, 0))
techNewsTitle = create_text(
    text="Amazon Union Loses Vote at Second Staten Island Warehouse",
    font=font_10,
    color=(255, 255, 255),  # White
    pos=(325, 230),  # Center of the screen
    max_width=140,
)

currencyConvertion = font_10.render('1 USD = 4.35 MYR', True, (255, 255, 255), (0, 0, 0))

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

moonStateLabelRect = moonStateLabel.get_rect(center = (215+50, 274))

currencyConvertionRect = currencyConvertion.get_rect(center = (0+67.5, 288+16))

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
    screen.blit(currentWeatherHumidity, (180, 50))
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

    screen.blit(sunriseIcon, (20, 216))
    screen.blit(sunsetIcon, (20, 246))
    screen.blit(moonriseIcon, (110, 216))
    screen.blit(moonsetIcon, (110, 246))

    screen.blit(sunriseLabel, (54, 218))
    screen.blit(sunsetLabel, (54, 248))
    screen.blit(moonriseLabel, (140, 218))
    screen.blit(moonsetLabel, (140, 248))

    screen.blit(sunriseTime, (54, 230))
    screen.blit(sunsetTime, (54, 260))
    screen.blit(moonriseTime, (140, 230))
    screen.blit(moonsetTime, (140, 260))

    screen.blit(moonStateIcon, moonStateIconRect)
    screen.blit(moonStateLabel, moonStateLabelRect)

    screen.blit(techNewsLabel, (325, 214))
    for text_object in techNewsTitle[:3]:
        screen.blit(*text_object)

    screen.blit(currencyConvertion, currencyConvertionRect)

    pygame.draw.line(screen, (255, 255, 255), (0, 80), (480, 80), 1)
    pygame.draw.line(screen, (255, 255, 255), (160, 0), (160, 80), 1)
    pygame.draw.line(screen, (255, 255, 255), (320, 0), (320, 80), 1)
    pygame.draw.line(screen, (255, 255, 255), (0, 202), (480, 202), 1)
    pygame.draw.line(screen, (255, 255, 255), (0, 288), (480, 288), 1)
    pygame.draw.line(screen, (255, 255, 255), (215, 202), (215, 288), 1)
    pygame.draw.line(screen, (255, 255, 255), (315, 202), (315, 288), 1)
    pygame.draw.line(screen, (255, 255, 255), (135, 288), (135, 320), 1)

    pygame.display.flip()