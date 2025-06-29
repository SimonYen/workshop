import requests
import os


# 当前天气
class WeatherNow:
    def __init__(self, location: str):
        self.location = location
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "pa2tudhgtj.re.qweatherapi.com"

        # 天气的各项属性
        self.temperature = None  # 当前温度
        self.humidity = None  # 湿度
        self.wind_speed = None  # 风速
        self.wind_direction = None  # 风向
        self.icon_code = None  # 天气图标代码
        self.description = None  # 天气描述
        self.body_temperature = None  # 体感温度
        self.visibility = None  # 能见度
        self.pressure = None  # 气压
        self.update_time = None  # 更新时间

        # 预警的各项属性
        self.warning_sender = None  # 预警发布者
        self.warning_publish_time = None  # 预警发布时间
        self.warning_title = None  # 预警标题
        self.warning_text = None  # 预警内容

    def fetch_weather(self):
        """
        获取当前天气信息
        """
        url = f"https://{self.base_url}/v7/weather/now?location={self.location}&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "now" in data:
                now = data["now"]
                self.temperature = now.get("temp")
                self.humidity = now.get("humidity")
                self.wind_speed = now.get("windSpeed")
                self.wind_direction = now.get("windDir")
                self.icon_code = now.get("icon")
                self.description = now.get("text")
                self.body_temperature = now.get("feelsLike")
                self.visibility = now.get("vis")
                self.pressure = now.get("pressure")
                self.update_time = now.get("obsTime")
            else:
                raise ValueError("Invalid response format: 'now' key not found.")
        else:
            raise ValueError(f"Failed to fetch weather data: {response.status_code}")

    def fetch_warning(self):
        """
        获取天气预警信息
        """
        url = f"https://{self.base_url}/v7/warning/now?location={self.location}&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "warning" in data:
                if data["warning"] is None or len(data["warning"]) == 0:
                    raise ValueError("No warning data available.")
                # 解析预警信息
                warning = data["warning"][0]
                self.warning_sender = warning.get("sender")
                self.warning_publish_time = warning.get("pubTime")
                self.warning_title = warning.get("title")
                self.warning_text = warning.get("text")
            else:
                raise ValueError("Invalid response format: 'warning' key not found.")
        else:
            raise ValueError(f"Failed to fetch warning data: {response.status_code}")

    def __str__(self):
        """
        返回天气信息的字符串表示
        """
        return (
            f"Location: {self.location}\n"
            f"Temperature: {self.temperature}°C\n"
            f"Humidity: {self.humidity}%\n"
            f"Wind Speed: {self.wind_speed} km/h\n"
            f"Wind Direction: {self.wind_direction}\n"
            f"Icon Code: {self.icon_code}\n"
            f"Description: {self.description}\n"
            f"Body Temperature: {self.body_temperature}°C\n"
            f"Visibility: {self.visibility} km\n"
            f"Pressure: {self.pressure} hPa"
        )


if __name__ == "__main__":
    # 示例用法
    location = "101010100"  # 北京的行政区划代码
    weather = WeatherNow(location)
    try:
        weather.fetch_weather()
        print(weather)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
