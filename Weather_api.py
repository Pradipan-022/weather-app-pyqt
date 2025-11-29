import sys, requests
from PyQt5 import QtCore, QtWidgets

weather_emojis = {
    # Thunderstorm
    200: "⛈️", 201: "⛈️", 202: "⛈️",
    210: "🌩️", 211: "🌩️", 212: "🌩️", 221: "🌩️",
    230: "🌦️⚡", 231: "🌦️⚡", 232: "🌦️⚡",

    # Drizzle
    300: "🌦️", 301: "🌦️", 302: "🌦️",
    310: "🌧️", 311: "🌧️", 312: "🌧️",
    313: "🌧️", 314: "🌧️", 321: "🌧️",

    # Rain
    500: "🌦️", 501: "🌧️", 502: "🌧️", 503: "🌧️", 504: "🌧️",
    511: "🧊🌧️",
    520: "🌦️", 521: "🌦️", 522: "🌧️", 531: "🌧️",

    # Snow
    600: "🌨️", 601: "🌨️", 602: "❄️",
    611: "🌧️❄️", 612: "🌧️❄️", 613: "🌧️❄️",
    615: "🌧️❄️", 616: "🌧️❄️",
    620: "🌨️☃️", 621: "🌨️☃️", 622: "🌨️☃️",

    # Atmosphere
    701: "🌫️", 711: "💨🔥", 721: "🌫️",
    731: "🌪️", 741: "🌁", 751: "🏜️",
    761: "🌪️", 762: "🌋", 771: "💨🌊", 781: "🌪️",

    # Clear
    800: "☀️",

    # Clouds
    801: "🌤️", 802: "⛅", 803: "🌥️", 804: "☁️",
}

class WeatherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QtWidgets.QLabel("Enter city name:", self)
        self.city_input = QtWidgets.QLineEdit(self)
        self.weather_get_button = QtWidgets.QPushButton("Get Weather", self)
        self.temperature_label = QtWidgets.QLabel(self)
        self.emoji_label = QtWidgets.QLabel(self)
        self.description_label = QtWidgets.QLabel(self)
        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.weather_get_button.setObjectName("weather_get_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle("Weather App")
        
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()
        width = int(screen_width * 0.35)
        height = int(screen_height * 0.7)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.setGeometry(x, y, width, height)
        
        vbox = QtWidgets.QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.weather_get_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)

        self.city_label.setAlignment(QtCore.Qt.AlignCenter)
        self.city_input.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature_label.setAlignment(QtCore.Qt.AlignCenter)
        self.emoji_label.setAlignment(QtCore.Qt.AlignCenter)
        self.description_label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #263238; /* charcoal gray */
                font-family: Segoe UI, Arial, sans-serif;
                color: #ECEFF1; /* light gray text */
            }

            #city_label {
                font-size: 30px;
                font-weight: bold;
                color: #ECEFF1;
            }

            #city_input {
                background-color: #37474F; /* dark slate */
                border: 2px solid #546E7A; /* muted blue-gray */
                border-radius: 8px;
                padding: 6px;
                font-size: 18px;
                color: #ECEFF1;
            }
            #city_input:focus {
                border: 2px solid #29B6F6; /* bright cyan accent */
                outline: none;
            }

            #weather_get_button {
                background-color: #29B6F6; /* cyan accent */
                color: #263238; /* dark text on cyan */
                font-size: 18px;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 8px;
            }
            #weather_get_button:hover {
                background-color: #0288D1; /* darker cyan on hover */
                color: white;
            }
            #weather_get_button:pressed {
                background-color: #01579B; /* even darker blue when clicked */
                color: white;
            }

            #temperature_label {
                font-size: 28px;
                font-weight: bold;
                color: #FF7043; /* warm orange for contrast */
                margin-top: 10px;
            }

            #emoji_label {
                font-size: 90px;  /* bigger, main focus */
                margin: 5px;
            }

            #description_label {
                font-size: 24px;  /* smaller than emoji, supportive */
                color: #B0BEC5;   /* soft gray-blue */
                font-style: italic;
            }
            """)
        
        self.weather_get_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "83be25485127acdcc32f6a8418adf061"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:    
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
        
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("401 Unauthorized\nInvalid API key or authentication required")
                case 403:
                    self.display_error("403 Forbidden\nYou don't have permission to access this resource")
                case 404:
                    self.display_error("404 Not Found\nThe requested resource could not be found")
                case 408:
                    self.display_error("408 Request Timeout\nThe server took too long to respond")
                case 429:
                    self.display_error("429 Too Many Requests\nYou have exceeded the API rate limit")
                case 500:
                    self.display_error("500 Internal Server Error\nSomething went wrong on the server")
                case 502:
                    self.display_error("502 Bad Gateway\nReceived an invalid response from upstream server")
                case 503:
                    self.display_error("503 Service Unavailable\nThe server is temporarily overloaded or down")
                case 504:
                    self.display_error("504 Gateway Timeout\nThe server did not respond in time")
                case _:
                    self.display_error(f"Unexpected HTTP error: {response.status_code}")
                    
        except requests.exceptions.ConnectionError:
            self.display_error("Network error: Could not connect to the server")

        except requests.exceptions.Timeout:
            self.display_error("Request timed out: The server is taking too long to respond")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects: Check the URL or server configuration")

        except requests.exceptions.RequestException as e:
            self.display_error(f"An unexpected error occurred: {e}")
            
    
    def display_error(self, message):
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        temperature_k = data['main']['temp']
        temperature_c = temperature_k - 273.15
        weather_id = data['weather'][0]['id']        
        weather_description = data['weather'][0]['description']
        
        emoji = weather_emojis.get(weather_id, "❓")
        
        self.temperature_label.setText(f"{temperature_c:.2f}°C")
        self.description_label.setText(f"{weather_description}")
        self.emoji_label.setText(emoji)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
