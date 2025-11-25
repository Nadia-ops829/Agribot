import requests

def get_temperature_ouagadougou():

    lat = 12.3714  # Latitude de Ouagadougou
    lon = -1.5197  # Longitude de Ouagadougou
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m&timezone=Africa/Accra"
    response = requests.get(url)
    data = response.json()
    
    temperature = data['current']['temperature_2m']
    time = data['current']['time']
    
    return temperature, time

# Obtenir la température
temp, time = get_temperature_ouagadougou()
print(f"Température à Ouagadougou: {temp}°C à {time}")