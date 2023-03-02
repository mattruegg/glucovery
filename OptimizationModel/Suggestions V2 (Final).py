from sympy import Symbol, Add, Eq
from sympy.abc import *
from scipy.optimize import linprog
import json

# test

with open('Nutrient Limits.json', 'r') as json_file:
    NutrientLimits = json.load(json_file)
    print("Nutrient Limits Info: ", NutrientLimits)

with open('Nutrients Consumed.json', 'r') as json_file:
    NutrientConsumed = json.load(json_file)
    print("Nutrient Consumed Info: ", NutrientConsumed)

with open('foods.json', 'r') as json_file:
    FoodInfo = json.load(json_file)
    print("Food Info: ", FoodInfo)

# Upper and lower nutritional limits for a healthy diet
UpperIron = NutrientLimits["Iron, Fe"]["UL"]
LowerIron = NutrientLimits["Iron, Fe"]["RDA"]
UpperVitB = NutrientLimits["Vitamin B"]["UL"]
LowerVitB = NutrientLimits["Vitamin B"]["RDA"]
UpperVitC = NutrientLimits["Vitamin C"]["UL"]
LowerVitC = NutrientLimits["Vitamin C"]["RDA"]

# Amount of nutrients the user has consumed in their current diet
IronConsumed = NutrientConsumed["Iron, Fe"]
VitBConsumed = NutrientConsumed["Vitamin B"]
VitCConsumed = NutrientConsumed["Vitamin C"]

print("Iron Consumed: ")
print(IronConsumed)
print("VitB Consumed: ")
print(VitBConsumed)
print("VitC Consumed: ")
print(VitCConsumed)

# Calculate range for how much of the nutrient is missing (and make the lower value negative for >=) If the user
# already has consumed more than the lower limit, set the lower inequality limit to 0. TO DO: Add conditions for
# upper limit (ie. if they have had more than the upper limit, flag & set upper inequality to 0)

Iron_RightIneq_Upper = UpperIron - int(IronConsumed)
if (LowerIron - int(IronConsumed)) < 0:
    Iron_RightIneq_Lower = 0
else:
    Iron_RightIneq_Lower = (LowerIron - int(IronConsumed)) * -1

VitB_RightIneq_Upper = UpperVitB - int(VitBConsumed)
if (LowerVitB - int(VitBConsumed)) < 0:
    VitB_RightIneq_Lower = 0
else:
    VitB_RightIneq_Lower = (LowerVitB - int(VitBConsumed)) * -1

VitC_RightIneq_Upper = UpperVitC - int(VitCConsumed)
if (LowerVitC - int(VitCConsumed)) < 0:
    VitC_RightIneq_Lower = 0
else:
    VitC_RightIneq_Lower = (LowerVitC - int(VitCConsumed)) * -1

print("Iron Right Upper: ", Iron_RightIneq_Upper)
print("Iron Right Lower: ", Iron_RightIneq_Lower)
print("VitB Right Upper: ", VitB_RightIneq_Upper)
print("VitB Right Lower: ", VitB_RightIneq_Lower)
print("VitC Right Upper: ", VitC_RightIneq_Upper)
print("VitC Right Lower: ", VitC_RightIneq_Lower)

# Combine upper and lower nutrient values into the right side inequality list
RightIneq = [Iron_RightIneq_Upper,
             Iron_RightIneq_Lower,
             VitB_RightIneq_Upper,
             VitB_RightIneq_Lower,
             VitC_RightIneq_Upper,
             VitC_RightIneq_Lower
             ]

print("Right side of inequality: ", RightIneq)

# Creating objective function: apple + orange + pear, coefficients go into objective function list (i.e. all ones)
numof1s = len(list(FoodInfo))
# print("test number of ones: ", numof1s)

ObjFun = [1] * numof1s  # Obj
print("Objective Function Coefficients: ", ObjFun)


# Create lists of nutrient coefficients to use for the inequalities (ie. to use when there is a >= inequality). The
# coefficients are the amount of the nutrient in the food ex. 10mg <= 2mg*apple + 4mg*orange + 3mg*pear <= 20mg  -->
# needs to be broken up into two inequalities (one lower & one upper). For 10 <= 2mg*apple + 4mg*orange + 3mg*pear
# inequality (lower ineq), needs to be multiplied by -1 to switch it to >=
# Note: the 10mg and 20mg have been handled in the right ineq

def returnNutrientForKey(n, key):
    return n[key]["value_100g"]


ironKey = "Iron, Fe"
vitaminBKey = "Vitamin B"
vitaminCKey = "Vitamin C"

ironValues = [returnNutrientForKey(i, ironKey) for i in FoodInfo.values()]
vitaminBValues = [returnNutrientForKey(i, vitaminBKey) for i in FoodInfo.values()]
vitaminCValues = [returnNutrientForKey(i, vitaminCKey) for i in FoodInfo.values()]

print("Iron Values:")
print(ironValues)
print("Vitamin B Values:")
print(vitaminBValues)
print("Vitamin C Values:")
print(vitaminCValues)

IronNegative = [-x for x in ironValues]
VitBNegative = [-x for x in vitaminBValues]
VitCNegative = [-x for x in vitaminCValues]

print("Negative Iron Coef: ", IronNegative)
print("Negative VitB Coef: ", VitBNegative)
print("Negative VitC Coef: ", VitCNegative)

# lhs_ineq
LeftIneq = [ironValues,
            IronNegative,
            vitaminBValues,
            VitBNegative,
            vitaminCValues,
            VitCNegative
            ]

print("Left side of inequality: ", LeftIneq)

# Eqaulity Constraints --> None in our scenario but is a required input for linprog
lhs_eq = [[0, 0, 0]]  # 0*apple +0*orange + 0*pear = 0
rhs_eq = [0]

# Bounds for foods (any # of servings can be suggested from 0 to positive infinity)
bnd = [(0, float("inf")),  # Bounds of Apple
       (0, float("inf")),  # Bounds of Orange
       (0, float("inf"))]  # Bounds of Pear

# Optimizing objective function with all the constraints (inequalities)
result = linprog(c=ObjFun, A_ub=LeftIneq, b_ub=RightIneq, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
                 method='highs-ipm')

print(result.fun)

print(result.success)

print(result.x)

ListofFoods = [x for x in FoodInfo]
print(ListofFoods)
