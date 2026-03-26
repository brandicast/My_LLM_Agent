import os
import json
import requests
import logging

logger = logging.getLogger(__name__)

# Load config
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

API_KEY = os.environ.get("CWA_API_KEY", "")
FORECAST_URL = config.get("forecast_url")
EARTHQUAKE_URL = config.get("earthquake_url")
ALERT_URL = config.get("alert_url")

def get_weather_forecast(city: str) -> str:
    """Gets the 36-hour weather forecast for a specific city in Taiwan.
    
    Args:
        city: The name of the city in Taiwan (e.g., '臺北市', '高雄市'). Must use traditional Chinese.
              If you don't know the exact city name natively, the tool will return a list of available cities.
    """
    if not API_KEY or not FORECAST_URL:
         return "Weather API is not fully configured."
         
    try:
        response = requests.get(
            FORECAST_URL,
            headers={'Authorization': API_KEY},
            params={'format': 'JSON'}
        )
        response.raise_for_status()
        data = response.json()
        
        locations = data.get('records', {}).get('location', [])
        available_cities = [loc['locationName'] for loc in locations]
        
        if city not in available_cities:
            return f"找不到指定的城市 '{city}'。可用的城市列表：{', '.join(available_cities)}"
            
        for loc in locations:
            if loc['locationName'] == city:
                elements = loc.get('weatherElement', [])
                weather_desc = []
                for elem in elements:
                    elem_name = elem.get('elementName')
                    times = elem.get('time', [])
                    if times:
                        # Just grab the immediate forecast (first time block)
                        t = times[0]
                        start = t.get('startTime')
                        end = t.get('endTime')
                        param = t.get('parameter', {})
                        param_name = param.get('parameterName', '')
                        param_unit = param.get('parameterUnit', '')
                        
                        if elem_name == 'Wx':
                            weather_desc.append(f"天氣現象: {param_name}")
                        elif elem_name == 'PoP':
                            weather_desc.append(f"降雨機率: {param_name}%")
                        elif elem_name == 'MinT':
                            weather_desc.append(f"最低溫度: {param_name}°{param_unit}")
                        elif elem_name == 'MaxT':
                            weather_desc.append(f"最高溫度: {param_name}°{param_unit}")
                
                return f"{city}的天氣預報:\n" + "\n".join(weather_desc)
                
        return f"無法解析 {city} 的天氣資料。"
    except Exception as e:
        logger.error(f"Error fetching weather forecast: {e}")
        return f"查詢天氣時發生錯誤: {str(e)}"

def get_earthquake_info() -> str:
    """Reports the latest earthquake or tsunami API alerts from Taiwan."""
    if not API_KEY or not EARTHQUAKE_URL:
         return "Earthquake API is not fully configured."
         
    try:
        response = requests.get(
            EARTHQUAKE_URL,
            headers={'Authorization': API_KEY},
            params={'format': 'JSON'}
        )
        response.raise_for_status()
        data = response.json()
        
        earthquakes = data.get('records', {}).get('Earthquake', [])
        if not earthquakes:
            return "目前沒有最新的顯著地震報告。"
            
        latest = earthquakes[0]
        eq_info = latest.get('EarthquakeInfo', {})
        origin_time = eq_info.get('OriginTime', '未知時間')
        depth = eq_info.get('FocalDepth', '未知深度')
        magnitude = eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue', '未知規模')
        location = eq_info.get('Epicenter', {}).get('Location', '未知地點')
        
        return f"最新顯著地震報告:\n時間: {origin_time}\n地點: {location}\n深度: {depth} km\n芮氏規模: {magnitude}"
    except Exception as e:
        logger.error(f"Error fetching earthquake info: {e}")
        return f"查詢地震資料時發生錯誤: {str(e)}"

def get_weather_alerts() -> str:
    """Check for special weather alerts (e.g., heavy rain warnings) across Taiwan."""
    if not API_KEY or not ALERT_URL:
         return "Alert API is not fully configured."
         
    try:
        response = requests.get(
            ALERT_URL,
            headers={'Authorization': API_KEY},
            params={'format': 'JSON'}
        )
        response.raise_for_status()
        data = response.json()
        
        records = data.get('records', {})
        hazard_conditions = records.get('hazardConditions', {})
        validities = hazard_conditions.get('validities', [])
        
        if not validities:
             return "目前台灣沒有發布特別的天氣警特報。"
             
        # Extract warnings from the validities structure
        warnings = []
        for v in validities[:5]: # just top 5 to keep it reasonable
            desc = v.get('hazardDetails', {}).get('hazardDescription', '')
            if desc:
                warnings.append(desc)
                
        if warnings:
            return "目前的天氣警特報有：\n" + "\n".join(warnings)
        return "目前台灣沒有發布特別的天氣警特報。"
    except Exception as e:
        logger.error(f"Error fetching weather alerts: {e}")
        return f"查詢氣象警爆時發生錯誤: {str(e)}"

def get_tools():
    """Returns a list of callable tools for Gemini."""
    return [get_weather_forecast, get_earthquake_info, get_weather_alerts]
