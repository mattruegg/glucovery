import sys
import time
import requests
import json

if __name__ == '__main__':

    start = time.time()

    # cnf_code = input("Enter food code (CNF): ")
    # cnf_url = 'https://food-nutrition.canada.ca/api/canadian-nutrient-file/'

    # response = requests.get(cnf_url + 'food/?id=' + cnf_code)
    # data = response.text
    # parse_json = json.loads(data)
    # info = parse_json[0]
    # print(info['food_description'])

    fdc_api_key = '?api_key=6zUVC6zgPINNy4SKljsSNKnVjwedmzcMRMh7iLkr'
    fdc_url = 'https://api.nal.usda.gov/fdc/v1/'

    # fdc_code = input("Enter food code (FDC): ")
    response2 = requests.get(fdc_url + 'food/' + "2346414" + fdc_api_key + '&nutrients=401')
    # response2 = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query=Cheddar%20Cheese')
    data2 = response2.text
    parse_json2 = json.loads(data2)
    info2 = parse_json2['foodNutrients']
    info3 = info2[0]
    print(info3)

    end = time.time()
    print("time", end - start)