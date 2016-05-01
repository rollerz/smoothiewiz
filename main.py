#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import webapp2
import urllib
import premade  # my premade ingredients file
import models  # my ndb.models
# TODO: work on code efficiency
from google.appengine.ext import ndb

Ing = models.Ing
User = models.User
Recipe = models.Recipe

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# end of imports


class IngList(webapp2.RequestHandler):

    def get(self):
        ingList = Ing.query().fetch()
        template_values = {
            'ingList': ingList,
            'size': len(ingList),
            'curUser': self.request.cookies.get('uName')
        }
        template = JINJA_ENVIRONMENT.get_template('ings.html')
        self.response.write(template.render(template_values))


class RecipeList(webapp2.RequestHandler):

    def get(self):
        recipeList = Recipe.query().fetch()
        template_values = {
            'rList': recipeList,
            'curUser': self.request.cookies.get('uName')
        }
        template = JINJA_ENVIRONMENT.get_template('recs.html')
        self.response.write(template.render(template_values))


class IngredientHandler(webapp2.RequestHandler):

    def get(self, para):
        favCheck = True
        uName = self.request.cookies.get('uName')  # must get user from cookie
        if uName:
            ingFav = Ing.query(Ing.ingName == para).fetch()[0]
            curUser = User.query(User.uName == uName).fetch()[0]

            for i in curUser.favIngs:  # FIXME: Might be able to swap for query
                if i.ingName == ingFav.ingName:
                    favCheck = False

        # if favCheck == True its not in the favs, if false it is in favs
        template_values = {
            'curUser': self.request.cookies.get('uName'),
            'curIng': Ing.query(Ing.ingName == para).fetch()[0],
            'check': favCheck
        }
        template = JINJA_ENVIRONMENT.get_template('ing.html')
        self.response.write(template.render(template_values))

    def post(self, para):  # to favorite items
        try:
            uName = self.request.cookies.get('uName')
            curUser = User.query(User.uName == uName).fetch()[0]
            ingFav = Ing.query(Ing.ingName == para).fetch()[0]

        except IndexError:
            # if not logged in or no user exists
            template_values = {
                'curUser': self.request.cookies.get('uName'),
                'curIng': Ing.query(Ing.ingName == para).fetch()[0],
                'error': 'notLogged'
            }
            template = JINJA_ENVIRONMENT.get_template('error.html')
            self.response.write(template.render(template_values))
            self.redirect('/')

        else:
            favCheck = True
            for i in curUser.favIngs:  # FIXME: Might be able to swap for query
                if i.ingName == ingFav.ingName:
                    favCheck = False
                    break

            if not favCheck:
                template_values = {
                    'curUser': self.request.cookies.get('uName'),
                    'user': User.query(User.uName == self.request.cookies.get('uName')).fetch()[0],
                    'curIng': Ing.query(Ing.ingName == para).fetch()[0],
                    'error': 'favDup'
                }
                template = JINJA_ENVIRONMENT.get_template('user.html')
                self.response.write(template.render(template_values))

            elif curUser.favIngs is None:
                curUser.favIngs = Ing(ingName=ingFav.ingName)
                curUser.put()
                template_values = {
                    'curUser': self.request.cookies.get('uName'),
                    'user': User.query(User.uName == self.request.cookies.get('uName')).fetch()[0],
                    'curIng': Ing.query(Ing.ingName == para).fetch()[0],
                    'succ': 'favAdd'
                }
                template = JINJA_ENVIRONMENT.get_template('user.html')
                self.response.write(template.render(template_values))

            else:
                curUser.favIngs.append(Ing(ingName=ingFav.ingName))
                curUser.put()
                template_values = {
                    'curUser': self.request.cookies.get('uName'),
                    'user': User.query(User.uName == self.request.cookies.get('uName')).fetch()[0],
                    'curIng': Ing.query(Ing.ingName == para).fetch()[0],
                    'succ': 'favAdd'
                }
                template = JINJA_ENVIRONMENT.get_template('user.html')
                self.response.write(template.render(template_values))


class UnFavorite(webapp2.RequestHandler):

    def post(self, para):
        curUser = User.query(
            User.uName == self.request.cookies.get('uName')).fetch()[0]
        ingDel = Ing.query(Ing.ingName == para).fetch()[0]

        for fav in curUser.favIngs:  # FIXME: Might be able to swap for query
            if fav.ingName == ingDel.ingName:
                curUser.favIngs.remove(fav)
                curUser.put()
                break

        msg = ingDel.ingName + " has been removed from your favorites!"
        template_values = {
            'curUser': self.request.cookies.get('uName'),
            'curIng': Ing.query(Ing.ingName == para).fetch()[0],
            'user': User.query(User.uName == self.request.cookies.get('uName')).fetch()[0],
            'succ': 'unFav'
        }

        template = JINJA_ENVIRONMENT.get_template('user.html')
        self.response.write(template.render(template_values))


class RecipeHandler(webapp2.RequestHandler):

    def get(self, para):
        curRec = Recipe.get_by_id(int(para))
        recCal = 0
        recVitA = 0
        recVitB6 = 0
        recVitB12 = 0
        recVitC = 0
        recVitD = 0
        recVitE = 0
        recVitK = 0
        recCalc = 0
        recIron = 0
        recMag = 0
        recPotas = 0
        recSugars = 0
        recProtein = 0
        recTotalFat = 0

        ing_query = Recipe.query()
        mv = ing_query.fetch()

        # Running totals for all nutrients in recipe
        for a in mv:
            for i in a.ings:
                if not i.calories:
                    recCal = 0 + recCal
                else:
                    recCal = i.calories + recCal
                if not i.vitA:
                    recVitA = 0 + recVitA
                else:
                    recVitA = i.vitA + recVitA
                if not i.vitB6:
                    recVitB6 = 0 + recVitB6
                else:
                    recVitB6 = i.vitB6 + recVitB6
                if not i.vitB12:
                    recVitB12 = 0 + recVitB12
                else:
                    recVitB12 = i.vitB12 + recVitB12
                if not i.vitC:
                    recVitC = 0 + recVitC
                else:
                    recVitC = i.vitC + recVitC
                if not i.vitD:
                    recVitD = 0 + recVitD
                else:
                    recVitD = i.vitD + recVitD
                if not i.vitE:
                    recVitE = 0 + recVitE
                else:
                    recVitE = i.vitE + recVitE
                if not i.vitK:
                    recVitK = 0 + recVitK
                else:
                    recVitK = i.vitK + recVitK
                if not i.calcium:
                    recCalc = 0 + recCalc
                else:
                    recCalc = i.calcium + recCalc
                if not i.iron:
                    recIron = 0 + recIron
                else:
                    recIron = i.iron + recIron
                if not i.magnesium:
                    recMag = 0 + recMag
                else:
                    recMag = i.magnesium + recMag
                if not i.totalFat:
                    recTotalFat = 0 + recTotalFat
                else:
                    recTotalFat = i.totalFat + recTotalFat
                if not i.potassium:
                    recPotas = 0 + recPotas
                else:
                    recPotas = i.potassium + recPotas
                if not i.sugars:
                    recSugars = 0 + recSugars
                else:
                    recSugars = i.sugars + recSugars
                if not i.protein:
                    recProtein = 0 + recProtein
                else:
                    recProtein = i.protein + recProtein

        template_values = {
            'curUser': self.request.cookies.get('uName'),
            'curRec': curRec,
            'ingList': Ing.query().fetch(),
            'succ': 'genNutr',
            'cal': recCal,
            'vitA': recVitA,
            'vitB6': recVitB6,
            'vitB12': recVitB12,
            'vitC': recVitC,
            'vitD': recVitD,
            'vitE': recVitE,
            'vitK': recVitK,
            'calcium': recCalc,
            'iron': recIron,
            'magnesium': recMag,
            'totalFat': recTotalFat,
            'potassium': recPotas,
            'sugars': recSugars,
            'protein': recProtein
        }
        template = JINJA_ENVIRONMENT.get_template('rec.html')
        self.response.write(template.render(template_values))


class NewIng(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'curUser': self.request.cookies.get('uName')
        }
        template = JINJA_ENVIRONMENT.get_template('newIng.html')
        self.response.write(template.render(template_values))

    def post(self):
        calories = self.request.get('calories')
        vitA = self.request.get('vitA')
        vitB6 = self.request.get('vitB6')
        vitC = self.request.get('vitC')
        vitD = self.request.get('vitD')
        vitE = self.request.get('vitE')
        vitB12 = self.request.get('vitB12')
        vitK = self.request.get('vitK')
        calcium = self.request.get('calcium')
        iron = self.request.get('iron')
        magnesium = self.request.get('magnesium')
        potassium = self.request.get('potassium')
        totalFat = self.request.get('totalFat')
        protein = self.request.get('protein')
        sugars = self.request.get('sugars')
        ingType = self.request.get('type')
        ingName = self.request.get('name')
        photo = self.request.get('photo')
        photo_url = self.request.get('photo_url')
        try:
            if calories:  # Typecast for each nutrient
                calories = int(calories)
            else:
                calories = 0

            if vitA:
                vitA = int(vitA)
            else:
                vitA = 0

            if vitC:
                vitC = int(vitC)
            else:
                vitC = 0

            if vitD:
                vitD = int(vitD)
            else:
                vitD = 0

            if vitE:
                vitE = int(vitE)
            else:
                vitE = 0

            if vitB6:
                vitB6 = int(vitB6)
            else:
                vitB6 = 0

            if vitB12:
                vitB12 = int(vitB12)
            else:
                vitB12 = 0

            if vitK:
                vitK = int(vitK)
            else:
                vitK = 0

            if iron:
                iron = int(iron)
            else:
                iron = 0

            if calcium:
                calcium = int(calcium)
            else:
                calcium = 0

            if magnesium:
                magnesium = int(magnesium)
            else:
                magnesium = 0

            if potassium:
                potassium = float(potassium)
            else:
                magnesium = 0.0

            if totalFat:
                totalFat = float(totalFat)
            else:
                totalFat = 0.0

            if sugars:
                sugars = float(sugars)
            else:
                sugars = 0.0

            if protein:
                protein = float(protein)
            else:
                protein = 0.0

            if photo_url:
                imgPath = photo_url
            else:
                imgPath = None
            # else:
            #     imgPath = "../img/" + ingName + ".png"
            #     # TODO: Figure out BlobStore
        except:
            template_values = {
                'error': 'typeError',
                'curUser': self.request.cookies.get('uName')
            }
            template = JINJA_ENVIRONMENT.get_template('error.html')
            self.response.write(template.render(template_values))
        else:
            newIng = Ing(calories=calories, vitA=vitA, vitB6=vitB6, vitC=vitC, vitD=vitD, vitB12=vitB12,
                         calcium=calcium, magnesium=magnesium, protein=protein, sugars=sugars, ingType=ingType, ingName=ingName, imgPath=imgPath)

            # checks to see if Ing name is already declared
            checkName = True
            if len(Ing.query(Ing.ingName == newIng.ingName).fetch(1)) == 0:
                checkName = False

            if checkName:
                template_values = {
                    'curUser': self.request.cookies.get('uName'),
                    'error': 'ingDup'
                }
                template = JINJA_ENVIRONMENT.get_template('newIng.html')
                self.response.write(template.render(template_values))
            else:
                newIng.put()
                template_values = {
                    'curUser': self.request.cookies.get('uName'),
                    'curIng': newIng,
                    'succ': 'ingAdd'
                }
                template = JINJA_ENVIRONMENT.get_template('ings.html')
                self.response.write(template.render(template_values))


class NewRecipe(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'curUser': self.request.cookies.get('uName'),
            'ingList': Ing.query().fetch()
        }
        template = JINJA_ENVIRONMENT.get_template('newRec.html')
        self.response.write(template.render(template_values))

    def post(self):
        rName = self.request.get('rName')
        ingAdd = self.request.get('rIng')
        curIng = Ing.query(Ing.ingName == ingAdd).fetch()[0]

        if len(Recipe.query(Recipe.rName == rName).fetch(1)) == 0:
            newRecipe = Recipe(rName=rName, ings=[curIng])
            newRecipe.put()

            template_values = {
                'curUser': self.request.cookies.get('uName'),
                'recipe': newRecipe,
                'ingList': Ing.query().fetch(),
                'succ': 'rAdd'
            }
            template = JINJA_ENVIRONMENT.get_template('newRec.html')
            self.response.write(template.render(template_values))
        else:
            template_values = {
                'curUser': self.request.cookies.get('uName'),
                'recipe': rName,
                'ingList': Ing.query().fetch(),
                'error': 'dupRec'
            }
            template = JINJA_ENVIRONMENT.get_template('newRec.html')
            self.response.write(template.render(template_values))


class UpdateRecipe(webapp2.RequestHandler):

    def get(self, para):
        curRec = Recipe.get_by_id(int(para))
        ingDel = self.request.get('recDel')
        curIng = Ing.query(Ing.ingName == ingDel).fetch()[0]

        ing_query = Recipe.query()
        mv = ing_query.fetch()

        for a in mv:
            for i in a.ings:
                if i.ingName == ingDel:
                    curRec.ings.remove(i)
                    curRec.put()
                    break

        template_values = {
            'curUser': self.request.cookies.get('uName'),
            'curRec': curRec,
            'ingList': Ing.query().fetch(),
            'curIng': curIng,
            'succ': 'ingDel'
        }
        template = JINJA_ENVIRONMENT.get_template('rec.html')
        self.response.write(template.render(template_values))

    def post(self, para):
        curRec = Recipe.get_by_id(int(para))
        ingAdd = self.request.get('recIng')
        curIng = Ing.query(Ing.ingName == ingAdd).fetch()[0]

        curRec.ings.append(curIng)
        curRec.put()

        template_values = {
            'curUser': self.request.cookies.get('uName'),
            'curRec': curRec,
            'ingList': Ing.query().fetch(),
            'curIng': curIng,
            'succ': 'ingAdd'
        }
        template = JINJA_ENVIRONMENT.get_template('rec.html')
        self.response.write(template.render(template_values))


class Register(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'curUser': self.request.cookies.get('uName')
        }
        template = JINJA_ENVIRONMENT.get_template('register.html')
        self.response.write(template.render(template_values))

    def post(self):
        # TODO: Add more try blocks around any data forms
        uName = self.request.get('user')
        raw_password = self.request.get('pass')
        confirm = self.request.get('conf')
        userList = User.query().fetch()
        userCheck = True

        # TODO: hash all passwords from hashlib
        # XXX This is all just a Test XXX
        # salt = os.urandom(16)
        # m = hashlib.md5()
        # m.update(salt + password)
        # m.hexdigest()
        #
        # masterSecret = getpass(raw_password)
        # salt = bcrypt.gensalt()
        #
        # comboPassword = raw_password + salt + masterSecret
        # hashed_password = bcrypt.hashpw(comboPassword, salt)
        # XXX This is all just a Test XXX

        if len(raw_password) <= 7 and raw_password != confirm:
            template_values = {
                'error': 'dubFail',
                'user': uName
            }

            template = JINJA_ENVIRONMENT.get_template('register.html')
            self.response.write(template.render(template_values))

        elif raw_password != confirm or len(raw_password) <= 7:
            userCheck = False
            if len(raw_password) <= 7:
                template_values = {
                    'error': 'lenFail',
                    'user': uName
                }
            else:
                template_values = {
                    'error': 'confFail',
                    'user': uName
                }

            template = JINJA_ENVIRONMENT.get_template('register.html')
            self.response.write(template.render(template_values))

        else:  # if passwords match, then if user already exists
            if len(User.query(User.uName == uName).fetch(1)) == 0:
                userCheck = True
            else:
                userCheck = False

            if userCheck:
                self.response.set_cookie('uName', uName, path="/")
                newUser = User(uName=uName, password=raw_password)
                newUser.put()
                template_values = {
                    'user': newUser,
                    'succ': 'uReg'
                }

                template = JINJA_ENVIRONMENT.get_template('user.html')
                self.response.write(template.render(template_values))
            else:
                template_values = {
                    'error': 'uDup',
                    'user': uName
                }

                template = JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render(template_values))


class Login(webapp2.RequestHandler):

    def post(self):
        uName = self.request.get('loginUser')
        password = self.request.get('loginPass')
        curUser = None

        try:
            curUser = User.query(User.uName == uName).fetch()[0]
        except IndexError:
            if not User.query().fetch():
                template_values = {
                    'user': uName,
                    'error': 'noUsers'
                }
            else:
                template_values = {
                    'user': uName,
                    'error': 'uNotFound'
                }

            template = JINJA_ENVIRONMENT.get_template('register.html')
            self.response.write(template.render(template_values))
        else:
            if curUser and curUser.password == password:  # success
                self.response.set_cookie('uName', uName, path="/")
                template_values = {
                    'user': curUser,
                    'succ': 'login'
                }
                template = JINJA_ENVIRONMENT.get_template('index.html')
                self.response.write(template.render(template_values))

            else:  # fail
                template_values = {
                    'user': uName,
                    'error': 'passFail'
                }
                template = JINJA_ENVIRONMENT.get_template('index.html')
                self.response.write(template.render(template_values))


class LogOut(webapp2.RequestHandler):

    def get(self):
        curUser = self.request.cookies.get('uName')
        tempUser = curUser  # used to display user for user logout

        template_values = {
            'user': tempUser
        }

        self.response.delete_cookie('uName')
        template = JINJA_ENVIRONMENT.get_template('logout.html')
        self.response.write(template.render(template_values))


class UserInfo(webapp2.RequestHandler):

    def get(self, para):
        user = User.query(User.uName == para).fetch()[0]
        rList = Recipe.query().fetch()
        iList = user.favIngs
        canMake = []

        for rec in rList:
            for i in iList:
                for r in rec.ings:
                    if i.ingName == r.ingName and rec not in canMake:
                        canMake.append(rec)

        # NOTE: Since ndb.StructuredProperty is immutable,
        # I can't compare them as subsets.
        # Therefore, above adds them to a list if one ing is found in the rec

        template_values = {
            'user': user,
            'curUser': self.request.cookies.get('uName'),
            'canMake': canMake
        }
        template = JINJA_ENVIRONMENT.get_template('user.html')
        self.response.write(template.render(template_values))


class MainHandler(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'curUser': self.request.cookies.get('uName')
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newIng', NewIng),
    ('/newRec', NewRecipe),
    ('/recList', RecipeList),
    ('/ingList', IngList),
    (r'/ing/(\w+)', IngredientHandler),  # regex
    (r'/rec/(\w+)', RecipeHandler),   # regex
    (r'/upd/(\w+)', UpdateRecipe),  # regex
    (r'/del/(\w+)', UpdateRecipe),  # regex
    ('/reg', Register),
    ('/login', Login),
    ('/logout', LogOut),
    (r'/user/(\w+)', UserInfo),  # regex
    (r'/unfav/(\w+)', UnFavorite)  # regex
], debug=True)
