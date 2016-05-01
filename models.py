from google.appengine.ext import ndb


class Ing(ndb.Model):
    calories = ndb.IntegerProperty(indexed=False)
    vitA = ndb.IntegerProperty(indexed=False)
    vitB6 = ndb.IntegerProperty(indexed=False)
    vitC = ndb.IntegerProperty(indexed=False)
    vitD = ndb.IntegerProperty(indexed=False)
    vitE = ndb.IntegerProperty(indexed=False)
    vitB12 = ndb.IntegerProperty(indexed=False)
    vitK = ndb.IntegerProperty(indexed=False)
    calcium = ndb.IntegerProperty(indexed=False)
    iron = ndb.IntegerProperty(indexed=False)
    magnesium = ndb.IntegerProperty(indexed=False)
    totalFat = ndb.FloatProperty(indexed=False)
    potassium = ndb.FloatProperty(indexed=False)
    sugars = ndb.FloatProperty(indexed=False)
    protein = ndb.FloatProperty(indexed=False)
    ingType = ndb.StringProperty(indexed=False)
    ingName = ndb.StringProperty(indexed=True)  # NOTE: IngName nonrepeatable
    imgPath = ndb.StringProperty(indexed=False)
    # img = ndb.BlobProperty(indexed=False)  # TODO: Solve Blobstore


class Recipe(ndb.Model):
    rName = ndb.StringProperty(indexed=True)
    calories = ndb.IntegerProperty(indexed=False)
    ings = ndb.StructuredProperty(Ing, repeated=True)


class User(ndb.Model):
    uName = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty(indexed=False)
    favIngs = ndb.StructuredProperty(Ing, repeated=True)
