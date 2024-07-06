import requests

def get_rundom_duck():
    url = 'https://random-d.uk/api/random'
    response = requests.get(url)
    data = response.json()
    return data['url']

def get_rundom_dog():
    url = 'https://random.dog/woof.json'
    response = requests.get(url)
    data = response.json()
    return data['url']

def get_rundom_fox():
    url = 'https://randomfox.ca'
    response = requests.get(url)
    data = response.json()
    return data['url']
