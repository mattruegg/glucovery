# Glucovery
A project by Yonael Debebe, Matt Ruegg, Chetan Kalia, Katie Doleweerd as part of our engineering capstone project at the University of Waterloo.

## About
Our project focuses on people with Celiac Disease and the symptomatic and nutritional recovery issues they face after accidentally ingesting gluten. After ingesting gluten (colloquially known as a Gluten Flare-up, or GFU), the villi (small hair-like projections that line the inside of the small intestine) of people with Celiac disease are damaged and are not able to process and absorb nutrients as well as normal. As such, many people with Celiac Disease face some form of nutritional deficiency after a GFU. Additionally, many of them get sick after a GFU. Examples of common symptoms include headaches, nausea, brain fog, and mood swings. 

As such, our project aims to provide foods that can help reduce the symptoms Celiac patients are feeling while also promoting a strong nutritional balance to help the users recover faster.

## Designed Solution

### Wireframes
One component of our solution is a series of wireframes that demonstrate what information our application would show to the user and how the user can interact with the application. Try it out [here](https://www.figma.com/proto/ZlgOy12Jee6zj6PC6rtWtB/Wireframes?node-id=317-271&viewport=1364%2C1350%2C0.25&scaling=scale-down&starting-point-node-id=317%3A271&show-proto-sidebar=1&fbclid=IwAR3KQ3ZsqszI348nvOq44M7mknu9Igq6eosRAcCRjlV-GgpJvfVOxlb29do)

### Web Application
The second component of our solution is a Python web application that recommends gluten-free foods to users based on their current diet and symptoms during recovery from a GFU. The application uses Flutter for the frontend and MongoDB Atlas as a database and search engine. The database stores over 100 gluten-free foods and includes information such as their nutritional breakdown, serving size, allergens, and dietary restrictions. 

To use our application, users input their daily food consumption and symptoms. Our algorithm then takes this into account, as well as the user's recommended daily nutrient intake, allergies, and dietary restrictions, to generate a list of foods for the following day that help prevent the user from developing a nutrient deficiency. Finally, an optimization model minimizes the number of unique foods recommended to the user and determines the number of servings that contain the right amount of nutrients that are missing from the user's diet.

#### How to Run
- Clone this repository
- Install Python
- At the root level where `requirements.txt` is located, run the command `pip install -r requirements.txt` to install any dependencies
- In the `src` folder, execute the command `python frontend.py` in the terminal to run the flutter application or run the `frontend.py` file


