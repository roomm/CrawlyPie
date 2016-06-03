import mysql.connector
import sqlalchemy
from sqlalchemy import text


class Persistor:
    def __init__(self):
        engine = sqlalchemy.create_engine("mysql+mysqlconnector://root@localhost/recetarium")
        self.db = engine.connect()
        # self.cnx = mysql.connector.connect(user='root', database='recetarium', charset='utf8')
        self.select_recipe = "SELECT id FROM recipe WHERE web_id=:web_id"
        self.add_recipe = "INSERT INTO recipe (web_id, name, photo, instructions, time, level, commensal, site) VALUES (:web_id, :name, :photo, :instructions, :time, :level, :commensal, :site)"
        self.add_ingredient = "INSERT INTO ingredient (name) VALUES (:name)"
        self.select_ingredient = "SELECT id FROM ingredient WHERE name=:name"
        self.add_ingredient_in_recipe = "INSERT INTO ingredient_in_recipe (id_recipe, id_ingredient, quantity) VALUES (:id_recipe, :id_ingredient, :quantity)"

    def save_recipe(self, recipe):

        sql = text(self.select_recipe)
        insert = self.db.execute(sql, web_id=unicode(recipe.web_id))
        recip_id = insert.fetchone()

        if recip_id is None:
            sql = text(self.add_recipe)
            insert = self.db.execute(sql, web_id=unicode(recipe.web_id), name=unicode(recipe.name), photo=unicode(recipe.photo), instructions=unicode(recipe.instructions), time=unicode(recipe.tiempo),
                                     level=unicode(recipe.dificultad), commensal=unicode(recipe.personas), site=unicode(recipe.site))
            recip_id = insert.lastrowid
        else:
            recip_id = recip_id[0]

        for ing in recipe.ingredients:
            ing_nam = self.remove_accents_and_n(ing.split(" de ", 1)[1].strip().lower())
            ing_qty = ing.split(" de ", 1)[0].strip().lower()
            sql = text(self.select_ingredient)
            insert = self.db.execute(sql, name=unicode(ing_nam))
            ing_id = insert.fetchone()
            if ing_id is None:
                sql = text(self.add_ingredient)
                insert = self.db.execute(sql, name=unicode(ing_nam))
                ing_id = insert.lastrowid
            else:
                ing_id = ing_id[0]

            sql = text(self.add_ingredient_in_recipe)
            self.db.execute(sql, id_recipe=recip_id, id_ingredient=ing_id, quantity=unicode(ing_qty))

        self.db.close()

    def remove_accents_and_n(self, strn):
        try:
            tmp = strn.decode('utf-8', 'ignore')
        except:
            tmp = strn

        tmp = tmp.replace(unichr(225), "a").replace(unichr(193), "A") \
            .replace(unichr(192), "A").replace(unichr(224), "a") \
            .replace(unichr(201), "E").replace(unichr(233), "e") \
            .replace(unichr(200), "E").replace(unichr(232), "e") \
            .replace(unichr(205), "I").replace(unichr(237), "i") \
            .replace(unichr(204), "I").replace(unichr(236), "i") \
            .replace(unichr(207), "I").replace(unichr(239), "i") \
            .replace(unichr(211), "O").replace(unichr(243), "o") \
            .replace(unichr(210), "O").replace(unichr(242), "o") \
            .replace(unichr(218), "U").replace(unichr(250), "u") \
            .replace(unichr(220), "U").replace(unichr(252), "u") \
            .replace(unichr(217), "U").replace(unichr(249), "u") \
            .replace(unichr(209), "N").replace(unichr(241), "n") \
            .replace(".", "")
        return tmp
