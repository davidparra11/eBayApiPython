from ebaysdk.trading import Connection as Trading
import sqlite3

conn = sqlite3.connect('categoriesDB.db')
c = conn.cursor()

api = Trading(config_file=None, domain='api.sandbox.ebay.com', 
              appid="EchoBay62-5538-466c-b43b-662768d6841",
              devid="16a26b1b-26cf-442d-906d-597b60c41c19",
              certid="00dd08ab-2082-4e3c-9518-5f4298f296db",
              token="AgAAAA**AQAAAA**aAAAAA**PMIhVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**IahulXaONmBwi/Pzhx0hMqjHhVAz9/qrFLIkfGH5wFH8Fjwj8+H5FN4NvzHaDPFf0qQtPMFUaOXHpJ8M7c2OFDJ7LBK2+JVlTi5gh0r+g4I0wpNYLtXnq0zgeS8N6KPl8SQiGLr05e9TgLRdxpxkFVS/VTVxejPkXVMs/LCN/Jr1BXrOUmVkT/4Euuo6slGyjaUtoqYMQnmBcRsK4xLiBBDtiow6YHReCJ0u8oxBeVZo3S2jABoDDO9DHLt7cS73vPQyIbdm2nP4w4BvtFsFVuaq6uMJAbFBP4F/v/U5JBZUPMElLrkXLMlkQFAB3aPvqZvpGw7S8SgL7d2s0GxnhVSbh4QAqQrQA0guK7OSqNoV+vl+N0mO24Aw8whOFxQXapTSRcy8wI8IZJynn6vaMpBl5cOuwPgdLMnnE+JvmFtQFrxa+k/9PRoVFm+13iGoue4bMY67Zcbcx65PXDXktoM3V+sSzSGhg5M+R6MXhxlN3xYfwq8vhBQfRlbIq+SU2FhicEmTRHrpaMCk4Gtn8CKNGpEr1GiNlVtbfjQn0LXPp7aYGgh0A/b8ayE1LUMKne02JBQgancNgMGjByCIemi8Dd1oU1NkgICFDbHapDhATTzgKpulY02BToW7kkrt3y6BoESruIGxTjzSVnSAbGk1vfYsQRwjtF6BNbr5Goi52M510DizujC+s+lSpK4P0+RF9AwtrUpVVu2PP8taB6FEpe39h8RWTM+aRDnDny/v7wA/GkkvfGhiioCN0z48")

callData = {
            'DetailLevel': 'ReturnAll',
            'CategorySiteID': 101,
            'LevelLimit': 4,
        }

response = api.execute('GetCategories', callData)
categoryArray = response.dict()['CategoryArray']['Category']
clist = []
clist1 = []
clist2 = []
clist3 = []
clist4 = []
htmlArray = []

def drop_tables():
    c.execute("DROP TABLE IF EXISTS ebayCategories")
    c.execute("DROP TABLE IF EXISTS ebayCategories1")
    c.execute("DROP TABLE IF EXISTS ebayCategories2")
    c.execute("DROP TABLE IF EXISTS ebayCategories3")
    c.execute("DROP TABLE IF EXISTS ebayCategories4")


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS ebayCategories(idCategory INT, category TEXT, level INT, bestOffer BOOLEAN, categoryParentId INT)")

def create_table1():
    c.execute("CREATE TABLE IF NOT EXISTS ebayCategories1(idCategory INT, category TEXT, level INT, bestOffer BOOLEAN, categoryParentId INT)")


def create_table2():
    c.execute("CREATE TABLE IF NOT EXISTS ebayCategories2(idCategory INT, category TEXT, level INT, bestOffer BOOLEAN, categoryParentId INT, FOREIGN KEY(categoryParentId) REFERENCES ebayCategories1(idCategory))")

def create_table3():
    c.execute("CREATE TABLE IF NOT EXISTS ebayCategories3(idCategory INT, category TEXT, level INT, bestOffer BOOLEAN, categoryParentId INT, FOREIGN KEY(categoryParentId) REFERENCES ebayCategories2(idCategory))")

def create_table4():
    c.execute("CREATE TABLE IF NOT EXISTS ebayCategories4(idCategory INT, category TEXT, level INT, bestOffer BOOLEAN, categoryParentId INT, FOREIGN KEY(categoryParentId) REFERENCES ebayCategories3(idCategory))")

def data_entry():
  """Return a list with 5 columns : CategoryID, CategoryName, CategoryLevel, bestOffer, categoryParentId. From ebay API """
  for row in categoryArray:
    idCategory = row['CategoryID']
    categories = row['CategoryName']
    levels = row['CategoryLevel']
    bestOffer = row['BestOfferEnabled']
    categoryParentId = row['CategoryParentID']

    lista = (idCategory, categories, levels, bestOffer, categoryParentId)
    clist.append(lista)

    if levels=='1':
      clist1.append(lista)
    elif levels=='2':
      clist2.append(lista)
    elif levels=='3':
      clist3.append(lista)
    else:
      clist4.append(lista)

  
  c.executemany("INSERT INTO ebayCategories VALUES (?,?,?,?,?)", clist)
  conn.commit()
  c.executemany("INSERT INTO ebayCategories1 VALUES (?,?,?,?,?)", clist1)
  conn.commit()
  c.executemany("INSERT INTO ebayCategories2 VALUES (?,?,?,?,?)", clist2)
  conn.commit()
  c.executemany("INSERT INTO ebayCategories3 VALUES (?,?,?,?,?)", clist3)
  conn.commit()
  c.executemany("INSERT INTO ebayCategories4 VALUES (?,?,?,?,?)", clist4)
  conn.commit()


def specific_data_out(t):
  """Return a multiple rows with 5 columns : CategoryID, CategoryName, CategoryLevel, bestOffer, categoryParentId. from Database """
  c.execute('SELECT level FROM ebayCategories WHERE idCategory=?', (t,))
  integer = c.fetchone()
  string = str(integer)
  if string=='(1,)':
    c.execute('SELECT * FROM ebayCategories1 WHERE categoryParentId=?', (t,))
    string1 = c.fetchone()
    lista1 = list(string1)
    parentId = lista1[0]
    htmlArray.append(string1)
    c.execute('SELECT * FROM ebayCategories2 WHERE categoryParentId=?', (parentId,))
    string2 = c.fetchall()
    lista2 = list(string2)
    parentId = lista2[0][0]
    htmlArray.extend(string2)
    c.execute('SELECT * FROM ebayCategories3 WHERE categoryParentId=?', (parentId,))
    string3 = c.fetchall()
    if not string3:
      return htmlArray
    lista3 = list(string3)
    parentId = lista3[0][0]
    htmlArray.extend(string3)
    c.execute('SELECT * FROM ebayCategories4 WHERE categoryParentId=?', (parentId,))
    string4 = c.fetchall()
    if not string4:
      return htmlArray
    lista4 = list(string4)
    htmlArray.extend(string4)
    return htmlArray
  elif string=='(2,)':
    c.execute('SELECT * FROM ebayCategories2 WHERE idCategory=?', (t,))
    string2 = c.fetchone()    
    lista2 = list(string2)
    parentId = lista2[0]
    htmlArray.append(string2)
    c.execute('SELECT * FROM ebayCategories3 WHERE categoryParentId=?', (parentId,))
    string3 = c.fetchall()
    if not string3:
      return htmlArray
    lista3 = list(string3)
    parentId = lista3[0][0]
    htmlArray.extend(string3)
    c.execute('SELECT * FROM ebayCategories4 WHERE categoryParentId=?', (parentId,))
    string4 = c.fetchall()
    if not string4:
      return htmlArray
    lista4 = list(string3)
    htmlArray.extend(string4)
    return htmlArray
  elif string=='(3,)':
    c.execute('SELECT * FROM ebayCategories3 WHERE idCategory=?', (t,))
    string3 = c.fetchone()
    lista3 = list(string3)
    parentId = lista3[0]
    htmlArray.append(string3)
    c.execute('SELECT * FROM ebayCategories4 WHERE categoryParentId=?', (parentId,))
    string4 = c.fetchall()
    if not string4:
      return htmlArray
    lista4 = list(string4)
    htmlArray.extend(string4)
    return htmlArray
  elif string=='(4,)':
    c.execute('SELECT * FROM ebayCategories4 WHERE idCategory=?', (t,))
    string4 = c.fetchone()
    lista4 = list(string4)
    htmlArray.append(string4)
    return htmlArray
  else:
    print("Without category")
    return 


  
