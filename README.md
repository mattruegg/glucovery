﻿# Glucovery
A project by Yonael Debebe, Matt Ruegg, Chetan Kalia, Katie Doleweerd

## About
Our project focuses on people with Celiac Disease and the symptomatic and nutritional recovery issues they face after accidentally ingesting gluten. After ingesting gluten (colloquially known as a Gluten Flare-up, or GFU), the villi (small hair-like projections that line the inside of the small intestine) of people with Celiac disease are damaged and are not able to process and absorb nutrients as well as normal. As such, many Celiac patients face some form of nutritional deficiency after a GFU. Additionally, many Celiac patients get sick after a GFU, with symptoms ranging from headaches and nausea to brain fog and mood swings. Our project aims to provide foods that can help reduce the symptoms Celiac patients are feeling while also promoting a strong nutritional balance to help the users recover faster.

# Designed Solution

The designed solution consists of a web application and wireframes. The web application recommends gluten-free foods to users based on their current diet and recovery symptoms. The application stores a database of over 100 gluten-free foods on the cloud using MongoDB Atlas. Nutritional information, serving size, allergens, and dietary restrictions are stored for each food. Users input their daily food consumption, and the application calculates nutrient consumption by summing up the nutrients from the selected foods. The application compares the consumed nutrients to the recommended daily allowance (RDA) and upper limit (UL) based on the user's age and sex. The application then determines a list of possible foods based on the missing nutrients, dietary restrictions, allergies, and symptoms. Finally, an optimization model minimizes the number of foods recommended to the user and determines the food servings such that its constraints are met. Tests are performed to ensure the correctness of the algorithms.
