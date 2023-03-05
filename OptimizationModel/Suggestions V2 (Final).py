# from sympy import Symbol, Add, Eq
# from sympy.abc import *
from scipy.optimize import linprog
import json
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
# sys.path.insert(1, r'C:\Users\ckali\github_repos\glucovery\python_work')

# test

with open('Nutrient Limits.json', 'r') as json_file:
    nutrient_limits = json.load(json_file)
    # print("Nutrient Limits Info: ", nutrient_limits)

with open('Nutrients Consumed.json', 'r') as json_file:
    nutrient_consumed_dict = json.load(json_file)
    # print("Nutrient Consumed Info: ", nutrient_consumed)

with open('foods.json', 'r') as json_file:
    food_info = json.load(json_file)
    # print("Food Info: ", food_info)


right_ineq = []
for nutrient in nutrient_limits:
    upper_nutrient = nutrient_limits[nutrient]["UL"]
    lower_nutrient = nutrient_limits[nutrient]["RDA"]
    nutrient_consumed = nutrient_consumed_dict[nutrient]
    nutrient_right_ineq_upper = upper_nutrient - int(nutrient_consumed)
    if (lower_nutrient - int(nutrient_consumed)) < 0:
        nutrient_right_ineq_lower = 0
    else:
        nutrient_right_ineq_lower = (lower_nutrient - int(nutrient_consumed)) * -1
    right_ineq.append(nutrient_right_ineq_upper)
    right_ineq.append(nutrient_right_ineq_lower)

# print("Right side of inequality: ", right_ineq)

# Creating objective function: apple + orange + pear, coefficients go into objective function list (i.e. all ones)
numof1s = len(list(food_info))
# print("test number of ones: ", numof1s)

ObjFun = [1] * numof1s  # Obj
# print("Objective Function Coefficients: ", ObjFun)


# Create lists of nutrient coefficients to use for the inequalities (ie. to use when there is a >= inequality). The
# coefficients are the amount of the nutrient in the food ex. 10mg <= 2mg*apple + 4mg*orange + 3mg*pear <= 20mg  -->
# needs to be broken up into two inequalities (one lower & one upper). For 10 <= 2mg*apple + 4mg*orange + 3mg*pear
# inequality (lower ineq), needs to be multiplied by -1 to switch it to >=
# Note: the 10mg and 20mg have been handled in the right ineq

def returnNutrientForKey(n, key):
    return n[key]["value_100g"]

left_ineq = []
for nutrient in nutrient_limits:
    nutrient_values = [returnNutrientForKey(i, nutrient) for i in food_info.values()]
    nutrient_negative = [-x for x in nutrient_values]
    left_ineq.append(nutrient_values)
    left_ineq.append(nutrient_negative)

# print("Left side of inequality: ", left_ineq)

# Eqaulity Constraints --> None in our scenario but is a required input for linprog
lhs_eq = [[0, 0, 0]]  # 0*apple +0*orange + 0*pear = 0
rhs_eq = [0]

# Bounds for foods (any # of servings can be suggested from 0 to positive infinity)
bnd = [(0, float("inf")),  # Bounds of Apple
       (0, float("inf")),  # Bounds of Orange
       (0, float("inf"))]  # Bounds of Pear

# Optimizing objective function with all the constraints (inequalities)
result = linprog(c=ObjFun, A_ub=left_ineq, b_ub=right_ineq, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
                 method='highs-ipm')

# print(result.fun)

# print(result.success)

print(result.x.tolist())

ListofFoods = [x for x in food_info]
print(ListofFoods)
