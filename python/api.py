import sys
import time
import requests
import json

def fdc_api():
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

def cnf_api():
    cnf_url = 'https://food-nutrition.canada.ca/api/canadian-nutrient-file/'
    response = requests.get(cnf_url + 'nutrientamount/?id=1701')
    data = response.text
    parse_json = json.loads(data)
    info = parse_json
    for i in info:
        if i['nutrient_value'] > 0.11:
            print("Nutrient Value:", i['nutrient_value'], "\tNutrient Name:", i['nutrient_web_name'])


if __name__ == '__main__':

    start = time.time()
    cnf_api()

    end = time.time()
    # print("time", end - start)