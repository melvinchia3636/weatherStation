import sys
from datetime import datetime
import pygame
import cairosvg
import io
import numpy as np
import requests
import json
import random

WEATHER_DATA = json.load(open('weathers.json'))

def load_svg(filename):
    new_bites = cairosvg.svg2png(url = filename)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io)

def wrap_text(text, font, max_width):
    texts = text.replace("\t", "    ").split("\n")
    lines = []

    for text in texts:
        text = text.rstrip(" ")

        if not text:
            lines.append("")
            continue

        a = len(text) - len(text.lstrip(" "))

        a = text.index(" ", a) if " " in text else len(text)
        line = text[:a]

        while a + 1 < len(text):
            if " " not in text[a + 1:]:
                b = len(text)
                bline = text
                
            else:
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

    text_objects = []

    for line, y_pos in zip(lines, line_ys):
        text_surface = font.render(line, True, color)
        text_objects.append((text_surface, (pos[0], y_pos)))

    return text_objects

class WeatherStation:
    airQualities = ['co', 'no2', 'o3', 'so2', 'pm2_5', 'pm10']
    lines = [
        [(0, 80), (480, 80)],
        [(160, 0), (160, 80)],
        [(320, 0), (320, 80)],
        [(0, 202), (480, 202)],
        [(0, 288), (480, 288)],
        [(215, 202), (215, 288)],
        [(315, 202), (315, 288)],
        [(135, 288), (135, 320)],
        [(368, 288), (368, 320)]
    ]
    forecast = [
        "morning",
        "afternoon",
        "evening",
        "night"
    ]
    astro = [
        'sunrise',
        'sunset',
        'moonrise',
        'moonset'
    ]
    
    
    def __init__(self):
        pygame.init()

        size = 480, 320
        # self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Weather Station")

        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.tick = 0

        self.fetchWeather()
        self.fetchNews()
        self.fetchCurrencyConvertion()
        self.fetchLunarDate()

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

    def fetchCurrencyConvertion(self):
        self.currencyConvertionRate = requests.get("https://open.er-api.com/v6/latest/USD").json()['rates']['MYR']

    def fetchNews(self):
        self.newsData = requests.get("https://api.nytimes.com/svc/topstories/v2/technology.json?api-key=53BGQxklAkbUFc7fewNlsuUABdSqzlgs").json()['results']

    def fetchLunarDate(self):
        self.lunarDate = requests.get("http://api.tianapi.com/lunar/index?key=1937befd766fa706c6169f6a2153a0f8&date={}-{}-{}".format(datetime.now().year, datetime.now().month, datetime.now().day)).json()['newslist'][0]
        
    def updateIcons(self):
        self.currentWeatherIcon = load_svg('svg/'+[i for i in WEATHER_DATA if i['day' if self.weatherData['current']['is_day'] else 'night'] == self.weatherData['current']['condition']['text']][0]['dayIcon' if self.weatherData['current']['is_day'] else 'nightIcon']+".svg")\

        weather = self.weatherData['forecast']['forecastday'][0]['hour']
        
        self.__dict__.update({
            f'{d}WeatherIcon': load_svg('svg/'+[w for w in WEATHER_DATA if w['day' if weather[[6, 12, 18, 0][i]]['is_day'] else 'night'] == weather[[6, 12, 18, 0][i]]['condition']['text']][0][('day' if weather[[6, 12, 18, 0][i]]['is_day'] else 'night')+'Icon']+".svg") for i, d in enumerate(self.forecast)
        })

        self.__dict__.update({f'{i}Icon': pygame.transform.scale(load_svg(f"svg/wi-{i}.svg"), (30, 30)) for i in self.astro})

        self.moonStateIcon = load_svg('svg/wi-moon-'+self.weatherData['forecast']['forecastday'][0]['astro']['moon_phase'].lower().replace(" ", '-')+".svg")

        self.__dict__.update({f"{i}WeatherIconRect": self.__dict__[f"{i}WeatherIcon"].get_rect(center = (index*120 + 60, 136)) for index, i in enumerate(self.forecast)})

        self.moonStateIconRect = self.moonStateIcon.get_rect(center = (215 + 50, 236))

    def initFonts(self):
        self.__dict__.update({f"font_{i}": pygame.font.Font(f"fonts/jbm.ttf", i) for i in [18, 14, 12, 10, 8]})
        self.font_ch = pygame.font.Font("fonts/ht.otf", 10)

    def initLabel(self):
        self.__dict__.update({f'{i}Label': self.font_10.render(i.title(), True, (255, 255, 255), (0, 0, 0)) for i in self.forecast+self.astro})

        self.techNewsLabel = self.font_8.render('Random Tech News', True, (255, 255, 255), (0, 0, 0))

        self.__dict__.update({
            f'{i}label': self.font_8.render(i.upper().replace("_", '.'), True, (255, 255, 255), (0, 0, 0)) for i in self.airQualities
        })

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

        self.__dict__.update({f'{i}value': self.font_10.render(str(round(weather['air_quality'][i]))+'µm' if i in weather['air_quality'] else 'N/A', True, (255, 255, 255), (0, 0, 0)) for i in self.airQualities})

        weather = self.weatherData['forecast']['forecastday'][0]

        self.__dict__.update({f'{i}Temp': self.font_14.render(str(weather['hour'][[6, 12, 18, 0][index]]['temp_c'])+"°C", True, (255, 255, 255), (0, 0, 0)) for index, i in enumerate(self.forecast)})
        self.__dict__.update({f'{i}Wind': self.font_8.render('{} @ {} km/h'.format(weather['hour'][[6, 12, 18, 0][index]]['wind_dir'], weather['hour'][[6, 12, 18, 0][index]]['wind_kph']), True, (255, 255, 255), (0, 0, 0)) for index, i in enumerate(self.forecast)})

        self.__dict__.update({f'{i}Time': self.font_10.render(weather['astro'][i], True, (255, 255, 255), (0, 0, 0)) for i in self.astro})

        self.moonState = self.font_10.render(weather['astro']['moon_phase'], True, (255, 255, 255), (0, 0, 0))

    def updateNews(self):
        self.techNewsTitle = create_text(
            text=random.choice(self.newsData)['title'],
            font=self.font_10,
            color=(255, 255, 255),  # White
            pos=(325, 230),  # Center of the self.screen
            max_width=140,
        )

    def updateCurrencyConvertion(self):
        self.currencyConvertion = self.font_10.render(f'1 USD = {self.currencyConvertionRate} MYR', True, (255, 255, 255), (0, 0, 0))

    def updateLunarDate(self):
        print(self.lunarDate['lubarmonth'], self.lunarDate['lunardate'])
        self.lunarDate = self.font_ch.render('{}年 {}{}'.format(self.lunarDate['tiangandizhiyear'], self.lunarDate['lubarmonth'], self.lunarDate['lunarday']), True, (255, 255, 255), (0, 0, 0))

    def updateRect(self):
        self.currentTimeRect = self.currentTime.get_rect(center = (320+80, 32))

        self.currentWeatherDescriptionRect = self.currentWeatherDescription.get_rect(center = (80, 64))
        self.currentZoneRect = self.currentZone.get_rect(center = (320+80, 48))

        self.__dict__.update({f'{i}LabelRect': self.__dict__[f'{i}Label'].get_rect(center = (index*120+60, 96)) for index, i in enumerate(self.forecast)})
        self.__dict__.update({f'{i}TempRect': self.__dict__[f'{i}Temp'].get_rect(center = (index*120+60, 170)) for index, i in enumerate(self.forecast)})
        self.__dict__.update({f'{i}WindRect': self.__dict__[f'{i}Wind'].get_rect(center = (index*120+60, 186)) for index, i in enumerate(self.forecast)})

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

        [self.screen.blit(self.__dict__[f'{i}{t}'], self.__dict__[f'{i}{t}Rect']) for t in ['Label', 'WeatherIcon', 'Temp', "Wind"] for i in self.forecast]

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

        [self.screen.blit(self.__dict__[f'{v}label'], (140+i*40, 292)) for i, v in enumerate(self.airQualities)]
        [self.screen.blit(self.__dict__[f'{v}value'], (140+i*40, 302)) for i, v in enumerate(self.airQualities)]

        self.screen.blit(self.lunarDate, self.lunarDateRect)

        [pygame.draw.line(self.screen, (255, 255, 255), x, y, 1) for x, y in self.lines]

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

            if self.tick % 3600 == 0:
                self.fetchCurrencyConvertion()
                self.updateCurrencyConvertion()
            
            if self.tick % 30 == 0:
                self.updateNews()

            if self.tick % 10800 == 0:
                self.fetchNews()

            if datetime.now().hour == 0 and datetime.now().minute == 1:
                self.fetchLunarDate()
                self.updateLunarDate()

            self.updateRect()

if __name__ == "__main__":
    station = WeatherStation()
    station.run()