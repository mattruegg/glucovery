import sys
import time
import requests
import json

if __name__ == '__main__':

    start = time.time()

    code = input("Enter food code: ")
    url = 'https://food-nutrition.canada.ca/api/canadian-nutrient-file/food/?id='

    response = requests.get(url + code)
    data = response.text
    parse_json = json.loads(data)
    info = parse_json[0]
    print(info['food_description'])

    end = time.time()
    print("time", end - start)