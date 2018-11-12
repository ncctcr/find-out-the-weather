# https://openweathermap.org/api
#
# дать возможность выбрать погоду(в Херсоне) за
# - текущий день
# - неделю
# - две недели
#
# использовать консоль  для ввода и вывода данных

import requests

API_URL_REALTIME = 'http://api.openweathermap.org/data/2.5/find?q='
API_URL_MORE_DAYS = 'http://api.openweathermap.org/data/2.5/forecast?q='
API_CITY = input('Введите город: ')
API_PREFIX = '&type=like&APPID='
API_KEY = '4b7deb1c712335c4c4f17fcc98a84c27'

API_ADDRESS_REALTIME = API_URL_REALTIME + API_CITY + API_PREFIX + API_KEY
API_ADDRESS_MORE_DAYS = API_URL_MORE_DAYS + API_CITY + API_PREFIX + API_KEY


class Weather:

    def get_json_data(self):
        if self.answear == '1':
            json_data = requests.get(API_ADDRESS_REALTIME).json()
        elif self.answear == '2':
            json_data = requests.get(API_ADDRESS_MORE_DAYS).json()
        return json_data

    def main_menu(self):
        self.answear = input("\nНа какой день вы хотите узнать погоду в городе " + API_CITY + '?'
                                                                                              '\n[1] - текущий день'
                                                                                              '\n[2] - 5 дней вперёд'
                                                                                              '\n\nВвод: ')
        json_data = self.get_json_data()

        if self.answear == '1':
            self.now_data(json_data)
        elif self.answear == '2':
            self.five_day_data(json_data)
        else:
            print("Error. Not find a suitable answear")

    def now_data(self, json_data):
        weather_data = json_data['list'][0]['weather'][0]['description']
        temp_data = json_data['list'][0]['main']['temp']
        print('\n-----News weather-----')
        print('\n[REALTIME] Currently in ' + API_CITY + ': ' + weather_data)
        print('[REALTIME] Temperature in ' + API_CITY + ': ', self.far_to_cel(temp_data), 'C')

    def five_day_data(self, json_data):
        self.current_date = ''
        for item in json_data['list']:
            time = item['dt_txt']
            self.next_date, self.hour = time.split(' ')
            print(self.get_data())
            print(self.get_AM_PM())
            temperature = item['main']['temp']
            description = item['weather'][0]['description']
            print('Weather condition: %s' % description)
            print('Celcius: {:.2f}'.format(temperature - 273.15))

    def get_data(self):
        if self.current_date != self.next_date:
            self.current_date = self.next_date
            year, month, day = self.current_date.split('-')
            date = {'y': year, 'm': month, 'd': day}
            return '\n{m}/{d}/{y}'.format(**date)

    def get_AM_PM(self):
        self.hour = int(self.hour[:2])
        if self.hour < 12:
            if self.hour == 0:
                self.hour = 12
            meridiem = 'AM'
        else:
            if self.hour > 12:
                self.hour -= 12
            meridiem = 'PM'
        return '\n%i:00 %s' % (self.hour, meridiem)

    def far_to_cel(self, x):
        return round(x - 273.15, 2)


obj_weather = Weather()
obj_weather.main_menu()
