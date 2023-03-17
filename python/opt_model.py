# from sympy import Symbol, Add, Eq
# from sympy.abc import *
from scipy.optimize import linprog
import json
import sys
from collections import defaultdict

class OptModel:
    
    def __int__(this):
        pass

    def optimize_food_suggestions(this, nutrient_limits, nutrient_consumed_dict, food_info):
        """
        nutrient_limits: RDA and upper limit nutrient intake values for a given age and gender
        nutrient_consumed_dict: dictionary where key is food name and value is quantity consumed
        food_info: list of dictionaries, where each dictionary is a possible food to recommend

        returns the names and quantities of foods to be recommended to the user
        """

        right_ineq = []
        for nutrient in nutrient_limits:
            upper_nutrient_value = nutrient_limits[nutrient]["UL"] 
            upper_nutrient = 10000000 if isinstance(upper_nutrient_value, str) else upper_nutrient_value
            lower_nutrient = nutrient_limits[nutrient]["RDA"]
            if nutrient in nutrient_consumed_dict:
                nutrient_consumed = nutrient_consumed_dict[nutrient]
            else:
                nutrient_consumed = lower_nutrient
            nutrient_right_ineq_upper = upper_nutrient - nutrient_consumed
            if (lower_nutrient - nutrient_consumed) < 0:
                nutrient_right_ineq_lower = 0
            else:
                nutrient_right_ineq_lower = (lower_nutrient - nutrient_consumed) * -1
            right_ineq.append(nutrient_right_ineq_upper)
            right_ineq.append(nutrient_right_ineq_lower)

        # print("Right side of inequality: ", right_ineq)

        # Creating objective function: apple + orange + pear, coefficients go into objective function list (i.e. all ones)
        # numof1s = len(list(food_info))
        numof1s = len(food_info)
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

        # Eqaulity Constraints --> None in our scenario but is a required input for linprog
        tmp = []
        for i in range(len(food_info)):
            tmp.append(0)
        lhs_eq = []
        lhs_eq.append(tmp)  
        rhs_eq = [0]

        # Bounds for foods (any # of servings can be suggested from 0 to positive infinity)
        bnd = []
        bound = (0, float("inf"))
        for i in range(len(food_info)):
            bnd.append(bound)

        # Optimizing objective function with all the constraints (inequalities)
        result = linprog(c=ObjFun, A_ub=left_ineq, b_ub=right_ineq, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
                         method='highs-ipm')
        
        optimized_foods = {}
        if result.success:
            quantities = result.x.tolist()
            for quantity, food in zip(quantities, food_info):
                if quantity > 0:
                    food_name = food["food_name"]
                    quantity_grams = quantity * 100
                    optimized_foods[food_name] = quantity_grams
                    return optimized_foods
        else:
            print("no opt results found")


# with open('OptimizationModel/Nutrient Limits.json', 'r') as json_file:
#     nutrient_limits = json.load(json_file)
#     # print("Nutrient Limits Info: ", nutrient_limits)

# with open('OptimizationModel/Nutrients Consumed.json', 'r') as json_file:
#     nutrient_consumed_dict = json.load(json_file)
#     # print("Nutrient Consumed Info: ", nutrient_consumed)

# with open('OptimizationModel/foods.json', 'r') as json_file:
#     food_info = json.load(json_file)
#     # print("Food Info: ", food_info)