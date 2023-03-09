# from sympy import Symbol, Add, Eq
# from sympy.abc import *
from scipy.optimize import linprog
import json
import sys
from collections import defaultdict

from mongo_db_queries import rec_foods, rec_nutrient_intake, summed_nutrient_amounts

# test

# with open('OptimizationModel/Nutrient Limits.json', 'r') as json_file:
#     nutrient_limits = json.load(json_file)
#     # print("Nutrient Limits Info: ", nutrient_limits)

# with open('OptimizationModel/Nutrients Consumed.json', 'r') as json_file:
#     nutrient_consumed_dict = json.load(json_file)
#     # print("Nutrient Consumed Info: ", nutrient_consumed)

# with open('OptimizationModel/foods.json', 'r') as json_file:
#     food_info = json.load(json_file)
#     # print("Food Info: ", food_info)

nutrient_limits = rec_nutrient_intake
nutrient_consumed_dict = summed_nutrient_amounts
food_info = rec_foods

right_ineq = []
missing_nutrients = [] # for testing purposes
for nutrient in nutrient_limits:
    upper_nutrient_value = nutrient_limits[nutrient]["UL"] 
    upper_nutrient = 10000000 if isinstance(upper_nutrient_value, str) else upper_nutrient_value
    lower_nutrient = nutrient_limits[nutrient]["RDA"]
    nutrient_consumed = nutrient_consumed_dict[nutrient]
    nutrient_right_ineq_upper = upper_nutrient - nutrient_consumed
    if (lower_nutrient - nutrient_consumed) < 0:
        nutrient_right_ineq_lower = 0
    else:
        missing_nutrients.append(nutrient)  # testing purposes
        nutrient_right_ineq_lower = (lower_nutrient - nutrient_consumed) * -1
    right_ineq.append(nutrient_right_ineq_upper)
    right_ineq.append(nutrient_right_ineq_lower)

# print("right ineq", right_ineq)

# print("Right side of inequality: ", right_ineq)

# Creating objective function: apple + orange + pear, coefficients go into objective function list (i.e. all ones)
# numof1s = len(list(food_info))
numof1s = len(food_info)

# print(list(food_info))
# print("test number of ones: ", numof1s)

ObjFun = [1] * numof1s  # Obj
# print("Objective Function Coefficients: ", ObjFun)


# Create lists of nutrient coefficients to use for the inequalities (ie. to use when there is a >= inequality). The
# coefficients are the amount of the nutrient in the food ex. 10mg <= 2mg*apple + 4mg*orange + 3mg*pear <= 20mg  -->
# needs to be broken up into two inequalities (one lower & one upper). For 10 <= 2mg*apple + 4mg*orange + 3mg*pear
# inequality (lower ineq), needs to be multiplied by -1 to switch it to >=
# Note: the 10mg and 20mg have been handled in the right ineq

left_ineq = []
for nutrient in nutrient_limits:
    pos_tmp = []
    neg_tmp = []
    for food in food_info:
        nutrient_found = False
        rec_nutrients = food["nutrients"]
        for rec_nutrient in rec_nutrients:
            rec_nutrient_name = rec_nutrient["nutrient_name"]
            rec_nutrient_value = rec_nutrient["value_100g"]
            if rec_nutrient_name == nutrient:
                nutrient_found = True
                pos_tmp.append(rec_nutrient_value)
                neg_tmp.append(-1 * rec_nutrient_value)
                break
        if not nutrient_found:
            pos_tmp.append(0)
            neg_tmp.append(0)
    left_ineq.append(pos_tmp)
    left_ineq.append(neg_tmp)

# print("left side of ineq", left_ineq)
# validation check
# print(len(food_info), len(food_info) == len(left_ineq[0]))

# Eqaulity Constraints --> None in our scenario but is a required input for linprog
tmp = []
for i in range(len(food_info)):
    tmp.append(0)
lhs_eq = []
lhs_eq.append(tmp)  
# print("blah", len(food_info), len(food_info) == len(lhs_eq[0]))
rhs_eq = [0]

# Bounds for foods (any # of servings can be suggested from 0 to positive infinity)
bnd = []
bound = (0, float("inf"))
for i in range(len(food_info)):
    bnd.append(bound)
# bnd = [(0, float("inf")),  # Bounds of Apple
#        (0, float("inf")),  # Bounds of Orange
#        (0, float("inf"))]  # Bounds of Pear

# Optimizing objective function with all the constraints (inequalities)
# result = linprog(c=ObjFun, A_ub=left_ineq, b_ub=right_ineq, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
#                  method='highs-ipm')

# print(result.fun)

# print(result.success)

# print(result.x.tolist())

ListofFoods = [x["food_name"] for x in food_info]
# print(ListofFoods)