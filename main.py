import sys
from datetime import datetime
import pygame
import cairosvg
import io
import numpy as np
import requests
import json

WEATHER_DATA = json.load(open('weathers.json'))

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

class WeatherStation:
    def __init__(self):
        pygame.init()

        size = 480, 320
        self.screen = self.display.set_mode(size, self.FULLSCREEN)
        # self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Weather Station")

        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.tick = 0

        self.fetchWeather()
        self.initFonts()
        self.initLabel()
        
        self.updateTime()

        self.updateWeather()
        self.updateIcons()

        self.updateNews()
        self.updateCurrencyConvertion()
        self.updateLunarDate()

        self.updateRect()

    def fetchWeather(self):
        self.weatherData = requests.get("http://api.weatherapi.com/v1/forecast.json?key=3226026245ad4bd4a0d75052220405&q=Johor&days=1&aqi=yes&alerts=no").json()

    def updateIcons(self):
        if self.weatherData['current']['is_day']:
            self.currentWeatherIcon = load_svg('svg/'+[i for i in WEATHER_DATA if i['day'] == self.weatherData['current']['condition']['text']][0]['dayIcon']+".svg")
        else:
            self.currentWeatherIcon = load_svg('svg/'+[i for i in WEATHER_DATA if i['night'] == self.weatherData['current']['condition']['text']][0]['nightIcon']+".svg")
        self.morningWeatherIcon = load_svg('svg/'+[i for i in WEATHER_DATA if i['day'] == self.weatherData['forecast']['forecastday'][0]['hour'][6]['condition']['text']][0]['dayIcon']+".svg")
        self.afternoonWeatherIcon = load_svg('svg/'+[i for i in WEATHER_DATA if i['day'] == self.weatherData['forecast']['forecastday'][0]['hour'][12]['condition']['text']][0]['dayIcon']+".svg")

        self.eveningWeatherIcon = load_svg('svg/'+[i for i in WEATHER_DATA if i['night'] == self.weatherData['forecast']['forecastday'][0]['hour'][19]['condition']['text']][0]['nightIcon']+".svg")
        self.nightWeatherIcon = load_svg('svg/'+[i for i in WEATHER_DATA if i['night'] == self.weatherData['forecast']['forecastday'][0]['hour'][0]['condition']['text']][0]['nightIcon']+".svg")

        sunriseIcon = load_svg("svg/wi-sunrise.svg")
        sunsetIcon = load_svg("svg/wi-sunset.svg")
        moonriseIcon = load_svg("svg/wi-moonrise.svg")
        moonsetIcon = load_svg("svg/wi-moonset.svg")

        self.sunriseIcon = pygame.transform.scale(sunriseIcon, (30, 30))
        self.sunsetIcon = pygame.transform.scale(sunsetIcon, (30, 30))
        self.moonriseIcon = pygame.transform.scale(moonriseIcon, (30, 30))
        self.moonsetIcon = pygame.transform.scale(moonsetIcon, (30, 30))
        
        self.moonStateIcon = load_svg("svg/wi-moon-waxing-crescent-3.svg")

        self.morningWeatherIconRect = self.morningWeatherIcon.get_rect(center = (0 + 60, 136))
        self.afternoonWeatherIconRect = self.afternoonWeatherIcon.get_rect(center = (120 + 60, 136))
        self.eveningWeatherIconRect = self.eveningWeatherIcon.get_rect(center = (240 + 60, 136))
        self.nightWeatherIconRect = self.nightWeatherIcon.get_rect(center = (360 + 60, 136))
        self.moonStateIconRect = self.moonStateIcon.get_rect(center = (215 + 50, 236))

    def initFonts(self):
        self.font_18 = pygame.font.Font('jbm.ttf', 18)
        self.font_14 = pygame.font.Font('jbm.ttf', 14)
        self.font_12 = pygame.font.Font('jbm.ttf', 12)
        self.font_10 = pygame.font.Font('jbm.ttf', 10)
        self.font_8 = pygame.font.Font('jbm.ttf', 8)
        self.font_ch = pygame.font.Font("ht.otf", 10)

    def initLabel(self):
        self.morningLabel = self.font_10.render('Morning', True, (255, 255, 255), (0, 0, 0))
        self.afternoonLabel = self.font_10.render('Afternoon', True, (255, 255, 255), (0, 0, 0))
        self.eveningLabel = self.font_10.render('Evening', True, (255, 255, 255), (0, 0, 0))
        self.nightLabel = self.font_10.render('Night', True, (255, 255, 255), (0, 0, 0))

        self.sunriseLabel = self.font_8.render('Sunrise', True, (255, 255, 255), (0, 0, 0))
        self.sunsetLabel = self.font_8.render('Sunset', True, (255, 255, 255), (0, 0, 0))
        self.moonriseLabel = self.font_8.render('Moonrise', True, (255, 255, 255), (0, 0, 0))
        self.moonsetLabel = self.font_8.render('Moonset', True, (255, 255, 255), (0, 0, 0))

        self.techNewsLabel = self.font_8.render('Random Tech News', True, (255, 255, 255), (0, 0, 0))

        self.colabel = self.font_8.render('CO', True, (255, 255, 255), (0, 0, 0))
        self.no2label = self.font_8.render('NO2', True, (255, 255, 255), (0, 0, 0))
        self.o3label = self.font_8.render('O3', True, (255, 255, 255), (0, 0, 0))
        self.so2 = self.font_8.render('SO2', True, (255, 255, 255), (0, 0, 0))
        self.pm25label = self.font_8.render('PM2.5', True, (255, 255, 255), (0, 0, 0))
        self.pm10label = self.font_8.render('PM10', True, (255, 255, 255), (0, 0, 0))

    def updateTime(self):
        self.currentTime = self.font_10.render(datetime.strftime(datetime.now(), '%a, %b %d %I:%M:%S %p'), True, (255, 255, 255), (0, 0, 0))

    def updateWeather(self):
        weather = self.weatherData['current']

        self.currentTempC = self.font_18.render(str(weather['temp_c'])+"°C", True, (255, 255, 255), (0, 0, 0))
        self.currentTempF = self.font_12.render(str(weather['temp_f'])+'°F', True, (255, 255, 255), (0, 0, 0))
        self.currentWeatherDescription = self.font_10.render(weather['condition']['text'], True, (255, 255, 255), (0, 0, 0))
        self.currentWeatherFeelLike = self.font_10.render('Feels like: {}°C'.format(weather['feelslike_c']), True, (255, 255, 255), (0, 0, 0))
        self.currentWeatherWind = self.font_10.render('Wind: {} @ {} km/h'.format(weather['wind_dir'], self.weatherData['current']['wind_kph']), True, (255, 255, 255), (0, 0, 0))
        self.currentWeatherHumidity = self.font_10.render('Humidity: {}%'.format(weather['humidity']), True, (255, 255, 255), (0, 0, 0))
        
        self.currentZone = self.font_10.render(self.weatherData['location']['tz_id'], True, (255, 255, 255), (0, 0, 0))

        self.covalue = self.font_10.render(str(round(weather['air_quality']['co']))+'µm', True, (255, 255, 255), (0, 0, 0))
        self.no2value = self.font_10.render(str(round(weather['air_quality']['no2']))+'µm', True, (255, 255, 255), (0, 0, 0))
        self.o3value = self.font_10.render(str(round(weather['air_quality']['o3']))+'µm', True, (255, 255, 255), (0, 0, 0))
        self.so2value = self.font_10.render(str(round(weather['air_quality']['so2']))+'µm', True, (255, 255, 255), (0, 0, 0))
        self.pm25value = self.font_10.render(str(round(weather['air_quality']['pm2_5']))+'µm', True, (255, 255, 255), (0, 0, 0))
        self.pm10value = self.font_10.render(str(round(weather['air_quality']['pm10']))+'µm', True, (255, 255, 255), (0, 0, 0))

        weather = self.weatherData['forecast']['forecastday'][0]

        self.morningTemp = self.font_14.render(str(weather['hour'][6]['temp_c'])+"°C", True, (255, 255, 255), (0, 0, 0))
        self.afternoonTemp = self.font_14.render(str(weather['hour'][12]['temp_c'])+"°C", True, (255, 255, 255), (0, 0, 0))
        self.eveningTemp = self.font_14.render(str(weather['hour'][19]['temp_c'])+"°C", True, (255, 255, 255), (0, 0, 0))
        self.nightTemp = self.font_14.render(str(weather['hour'][0]['temp_c'])+"°C", True, (255, 255, 255), (0, 0, 0))

        self.morningWind = self.font_8.render('{} @ {} km/h'.format(weather['hour'][6]['wind_dir'], weather['hour'][6]['wind_kph']), True, (255, 255, 255), (0, 0, 0))
        self.afternoonWind = self.font_8.render('{} @ {} km/h'.format(weather['hour'][12]['wind_dir'], weather['hour'][12]['wind_kph']), True, (255, 255, 255), (0, 0, 0))
        self.eveningWind = self.font_8.render('{} @ {} km/h'.format(weather['hour'][19]['wind_dir'], weather['hour'][19]['wind_kph']), True, (255, 255, 255), (0, 0, 0))
        self.nightWind = self.font_8.render('{} @ {} km/h'.format(weather['hour'][0]['wind_dir'], weather['hour'][0]['wind_kph']), True, (255, 255, 255), (0, 0, 0))

        self.sunsetTime = self.font_10.render(weather['astro']['sunrise'], True, (255, 255, 255), (0, 0, 0))
        self.sunriseTime = self.font_10.render(weather['astro']['sunset'], True, (255, 255, 255), (0, 0, 0))
        self.moonriseTime = self.font_10.render(weather['astro']['moonrise'], True, (255, 255, 255), (0, 0, 0))
        self.moonsetTime = self.font_10.render(weather['astro']['moonset'], True, (255, 255, 255), (0, 0, 0))

        self.moonState = self.font_10.render(weather['astro']['moon_phase'], True, (255, 255, 255), (0, 0, 0))

    def updateNews(self):
        self.techNewsTitle = create_text(
            text="Amazon Union Loses Vote at Second Staten Island Warehouse",
            font=self.font_10,
            color=(255, 255, 255),  # White
            pos=(325, 230),  # Center of the self.screen
            max_width=140,
        )

    def updateCurrencyConvertion(self):
        self.currencyConvertion = self.font_10.render('1 USD = 4.35 MYR', True, (255, 255, 255), (0, 0, 0))

    def updateLunarDate(self):
        self.lunarDate = self.font_ch.render('立夏 农历三月廿九', True, (255, 255, 255), (0, 0, 0))

    def updateRect(self):
        self.currentTimeRect = self.currentTime.get_rect(center = (320+80, 32))

        self.currentWeatherDescriptionRect = self.currentWeatherDescription.get_rect(center = (80, 64))
        self.currentZoneRect = self.currentZone.get_rect(center = (320+80, 48))

        self.morningLabelRect = self.morningLabel.get_rect(center = (0+60, 96))
        self.afternoonLabelRect = self.afternoonLabel.get_rect(center = (120+60, 96))
        self.eveningLabelRect = self.eveningLabel.get_rect(center = (240+60, 96))
        self.nightLabelRect = self.nightLabel.get_rect(center = (360+60, 96))

        self.morningTempRect = self.morningTemp.get_rect(center = (0+60, 170))
        self.afternoonTempRect = self.afternoonTemp.get_rect(center = (120+60, 170))
        self.eveningTempRect = self.eveningTemp.get_rect(center = (240+60, 170))
        self.nightTempRect = self.nightTemp.get_rect(center = (360+60, 170))

        self.morningWindRect = self.morningWind.get_rect(center = (0+60, 186))
        self.afternoonWindRect = self.afternoonWind.get_rect(center = (120+60, 186))
        self.eveningWindRect = self.eveningWind.get_rect(center = (240+60, 186))
        self.nightWindRect = self.nightWind.get_rect(center = (360+60, 186))

        self.moonStateRect = self.moonState.get_rect(center = (215+50, 274))

        self.currencyConvertionRect = self.currencyConvertion.get_rect(center = (0+67.5, 288+16))

        self.lunarDateRect = self.lunarDate.get_rect(center = (368+56, 288+16))

    def draw(self):
        self.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

        self.screen.blit(self.currentWeatherIcon, (20, 8))
        self.screen.blit(self.currentTempC, (70, 10))
        self.screen.blit(self.currentTempF, (70, 32))
        self.screen.blit(self.currentWeatherDescription, self.currentWeatherDescriptionRect)
        self.screen.blit(self.currentWeatherFeelLike, (180, 18))
        self.screen.blit(self.currentWeatherWind, (180, 34))
        self.screen.blit(self.currentWeatherHumidity, (180, 50))
        self.screen.blit(self.currentTime, self.currentTimeRect)
        self.screen.blit(self.currentZone, self.currentZoneRect)

        self.screen.blit(self.morningLabel, self.morningLabelRect)
        self.screen.blit(self.afternoonLabel, self.afternoonLabelRect)
        self.screen.blit(self.eveningLabel, self.eveningLabelRect)
        self.screen.blit(self.nightLabel, self.nightLabelRect)

        self.screen.blit(self.morningWeatherIcon, self.morningWeatherIconRect)
        self.screen.blit(self.afternoonWeatherIcon, self.afternoonWeatherIconRect)
        self.screen.blit(self.eveningWeatherIcon, self.eveningWeatherIconRect)
        self.screen.blit(self.nightWeatherIcon, self.nightWeatherIconRect)

        self.screen.blit(self.morningTemp, self.morningTempRect)
        self.screen.blit(self.afternoonTemp, self.afternoonTempRect)
        self.screen.blit(self.eveningTemp, self.eveningTempRect)
        self.screen.blit(self.nightTemp, self.nightTempRect)

        self.screen.blit(self.morningWind, self.morningWindRect)
        self.screen.blit(self.afternoonWind, self.afternoonWindRect)
        self.screen.blit(self.eveningWind, self.eveningWindRect)
        self.screen.blit(self.nightWind, self.nightWindRect)

        self.screen.blit(self.sunriseIcon, (20, 216))
        self.screen.blit(self.sunsetIcon, (20, 246))
        self.screen.blit(self.moonriseIcon, (110, 216))
        self.screen.blit(self.moonsetIcon, (110, 246))

        self.screen.blit(self.sunriseLabel, (54, 218))
        self.screen.blit(self.sunsetLabel, (54, 248))
        self.screen.blit(self.moonriseLabel, (140, 218))
        self.screen.blit(self.moonsetLabel, (140, 248))

        self.screen.blit(self.sunriseTime, (54, 230))
        self.screen.blit(self.sunsetTime, (54, 260))
        self.screen.blit(self.moonriseTime, (140, 230))
        self.screen.blit(self.moonsetTime, (140, 260))

        self.screen.blit(self.moonStateIcon, self.moonStateIconRect)
        self.screen.blit(self.moonState, self.moonStateRect)

        self.screen.blit(self.techNewsLabel, (325, 214))
        for text_object in self.techNewsTitle[:3]:
            self.screen.blit(*text_object)

        self.screen.blit(self.currencyConvertion, self.currencyConvertionRect)

        self.screen.blit(self.colabel, (140, 292))
        self.screen.blit(self.no2label, (180, 292))
        self.screen.blit(self.o3label, (220, 292))
        self.screen.blit(self.so2, (260, 292))
        self.screen.blit(self.pm25label, (300, 292))
        self.screen.blit(self.pm10label, (340, 292))

        self.screen.blit(self.covalue, (140, 302))
        self.screen.blit(self.no2value, (180, 302))
        self.screen.blit(self.o3value, (220, 302))
        self.screen.blit(self.so2value, (260, 302))
        self.screen.blit(self.pm25value, (300, 302))
        self.screen.blit(self.pm10value, (340, 302))

        self.screen.blit(self.lunarDate, self.lunarDateRect)

        pygame.draw.line(self.screen, (255, 255, 255), (0, 80), (480, 80), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (160, 0), (160, 80), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (320, 0), (320, 80), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (0, 202), (480, 202), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (0, 288), (480, 288), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (215, 202), (215, 288), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (315, 202), (315, 288), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (135, 288), (135, 320), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (368, 288), (368, 320), 1)

        pygame.display.flip()
        self.tick += 1
        self.clock.tick(1)

    def run(self):
        while True:
            self.draw()
            self.updateTime()

            if self.tick % 600 == 0:
                self.fetchWeather()
                self.updateWeather()
                self.updateIcons()

            self.updateRect()

if __name__ == "__main__":
    station = WeatherStation()
    station.run()