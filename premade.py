from google.appengine.ext import ndb
import models

Ing = models.Ing
Rec = models.Recipe

#      ING LIST      #
# ------------------ #
# IDEA: have the option to permanently save ingredients to premade.py. XML? JSON?
# Other / Liquids
# ------------------
water = Ing(ingName="Water", ingType="other",
            imgPath="../img/water.png", calories=0)
if len(Ing.query(Ing.ingName == "Water").fetch(1)) == 0:
    water.put()

# Fruits
# ------------------
apple = Ing(ingName="Apple", ingType="fruit", imgPath="../img/apple.png", calories=95,
            vitA=1, vitB6=5, vitC=14, potassium=195, totalFat=0.3, calcium=1, iron=1, magnesium=2, protein=0.5, sugars=19)
if len(Ing.query(Ing.ingName == "Apple").fetch(1)) == 0:
    apple.put()

orange = Ing(ingName="Orange", ingType="fruit", imgPath="../img/orange.png", calories=45,
             vitA=4, vitB6=5, vitC=85, potassium=174, totalFat=0.1, calcium=1, iron=1, magnesium=2, protein=0.5, sugars=19)
if len(Ing.query(Ing.ingName == "Orange").fetch(1)) == 0:
    orange.put()

pear = Ing(ingName="Pear", ingType="fruit", imgPath="../img/pear.png", calories=102,
           vitB6=5, vitC=12, potassium=206, totalFat=0.2, calcium=1, iron=1, magnesium=3, protein=0.6, sugars=17)
if len(Ing.query(Ing.ingName == "Pear").fetch(1)) == 0:
    pear.put()

banana = Ing(ingName="Banana", ingType="fruit", imgPath="../img/banana.png", calories=105,
             vitA=1, vitB6=20, vitC=17, potassium=422, totalFat=0.4, iron=1, magnesium=8, protein=1.3, sugars=17)
if len(Ing.query(Ing.ingName == "Banana").fetch(1)) == 0:
    banana.put()

grapefruit = Ing(ingName="Grapefruit", ingType="fruit", imgPath="../img/grapefruit.png", calories=52,
                 vitA=28, vitB6=5, vitC=64, potassium=166, totalFat=0.2, magnesium=2, protein=0.9, sugars=8)
if len(Ing.query(Ing.ingName == "Grapefruit").fetch(1)) == 0:
    grapefruit.put()

grape = Ing(ingName="Grape", ingType="fruit", imgPath="../img/grape.png", calories=62,
            vitA=1, vitB6=5, vitC=6, potassium=176, totalFat=0.3, calcium=1, iron=1, magnesium=1, protein=0.6, sugars=15)
if len(Ing.query(Ing.ingName == "Grape").fetch(1)) == 0:
    grape.put()  # 1 cup

strawberry = Ing(ingName="Strawberry", ingType="fruit", imgPath="../img/strawberry.png", calories=47,
                 vitB6=5, vitC=141, potassium=220, totalFat=0.4, calcium=2, iron=3, magnesium=4, protein=1.0, sugars=7)
if len(Ing.query(Ing.ingName == "Strawberry").fetch(1)) == 0:
    strawberry.put()  # 1 cup

blueberry = Ing(ingName="Blueberry", ingType="fruit", imgPath="../img/blueberry.png", calories=85,
                vitA=1, vitB6=5, vitC=24, potassium=114, totalFat=0.5, iron=2, magnesium=2, protein=1.1, sugars=15)
if len(Ing.query(Ing.ingName == "Blueberry").fetch(1)) == 0:
    blueberry.put()  # 1 cup

# Vegetables
# ------------------
carrot = Ing(ingName="Carrot", ingType="veg", imgPath="../img/carrot.png", calories=25,
             vitA=203, vitB6=5, vitC=6, potassium=195, totalFat=0.1, calcium=2, iron=1, magnesium=1, protein=0.6, sugars=2.9)
if len(Ing.query(Ing.ingName == "Carrot").fetch(1)) == 0:
    carrot.put()

cucumber = Ing(ingName="Cucumber", ingType="veg", imgPath="../img/cucumber.png", calories=47,
               vitA=6, vitB6=5, vitC=14, potassium=442, totalFat=0.3, calcium=4, iron=4, magnesium=9, protein=2, sugars=5)
if len(Ing.query(Ing.ingName == "Cucumber").fetch(1)) == 0:
    cucumber.put()

broccoli = Ing(ingName="Broccoli", ingType="veg", imgPath="../img/broccoli.png", calories=51,
               vitA=18, vitB6=15, vitC=224, potassium=468, totalFat=0.5, calcium=7, iron=6, magnesium=8, protein=4.3, sugars=2.6)
if len(Ing.query(Ing.ingName == "Broccoli").fetch(1)) == 0:
    broccoli.put()

spinach = Ing(ingName="Spinach", ingType="veg", imgPath="../img/spinach.png", calories=7,
              vitA=56, vitB6=5, vitC=14, potassium=167, totalFat=0.1, calcium=3, iron=4, magnesium=6, protein=0.9, sugars=0.1)
if len(Ing.query(Ing.ingName == "Spinach").fetch(1)) == 0:
    spinach.put()  # 1 cup

kale = Ing(ingName="Kale", ingType="veg", imgPath="../img/kale.png", calories=33,
           vitA=133, vitB6=10, vitC=134, potassium=329, totalFat=0.6, calcium=10, iron=5, magnesium=7, protein=2.9, sugars=0)
if len(Ing.query(Ing.ingName == "Kale").fetch(1)) == 0:
    kale.put()  # 1 cup

# TODO: Recipes
# ------------------
# Rec1 = Rec(rName="", )
