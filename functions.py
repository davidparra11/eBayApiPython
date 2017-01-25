from ebaysdk.trading import Connection as Trading
import sqlite3

conn = sqlite3.connect('categoriesDB.db')
c = conn.cursor()

api = Trading(config_file=None, domain='api.sandbox.ebay.com', 
              appid="EchoBay62-5538-466c-b43b-662768d6841", devid="16a26b1b-26cf-442d-906d-597b60c41c19", certid="00dd08ab-2082-4e3c-9518-5f4298f296db", token="AgAAAA**AQAAAA**aAAAAA**PMIhVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**IahulXaONmBwi/Pzhx0hMqjHhVAz9/qrFLIkfGH5wFH8Fjwj8+H5FN4NvzHaDPFf0qQtPMFUaOXHpJ8M7c2OFDJ7LBK2+JVlTi5gh0r+g4I0wpNYLtXnq0zgeS8N6KPl8SQiGLr05e9TgLRdxpxkFVS/VTVxejPkXVMs/LCN/Jr1BXrOUmVkT/4Euuo6slGyjaUtoqYMQnmBcRsK4xLiBBDtiow6YHReCJ0u8oxBeVZo3S2jABoDDO9DHLt7cS73vPQyIbdm2nP4w4BvtFsFVuaq6uMJAbFBP4F/v/U5JBZUPMElLrkXLMlkQFAB3aPvqZvpGw7S8SgL7d2s0GxnhVSbh4QAqQrQA0guK7OSqNoV+vl+N0mO24Aw8whOFxQXapTSRcy8wI8IZJynn6vaMpBl5cOuwPgdLMnnE+JvmFtQFrxa+k/9PRoVFm+13iGoue4bMY67Zcbcx65PXDXktoM3V+sSzSGhg5M+R6MXhxlN3xYfwq8vhBQfRlbIq+SU2FhicEmTRHrpaMCk4Gtn8CKNGpEr1GiNlVtbfjQn0LXPp7aYGgh0A/b8ayE1LUMKne02JBQgancNgMGjByCIemi8Dd1oU1NkgICFDbHapDhATTzgKpulY02BToW7kkrt3y6BoESruIGxTjzSVnSAbGk1vfYsQRwjtF6BNbr5Goi52M510DizujC+s+lSpK4P0+RF9AwtrUpVVu2PP8taB6FEpe39h8RWTM+aRDnDny/v7wA/GkkvfGhiioCN0z48")

callData = {
            'DetailLevel': 'ReturnAll',
            'CategorySiteID': 101,
            'LevelLimit': 4,
        }

response = api.execute('GetCategories', callData)
categoryArray = response.dict()['CategoryArray']['Category']
clist = []

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS ebayCategories(idCategory TEXT, category TEXT, level TEXT)")

def data_entry():
  """Return a list with 3 columns : CategoryID, CategoryName, CategoryLevel. From ebay API """
  for row in categoryArray:
   	idCategory = row['CategoryID']
   	categories = row['CategoryName']
   	levels = row['CategoryLevel']
   	lista = (idCategory, categories, levels)
   	clist.append(lista)

  c.executemany("INSERT INTO ebayCategories VALUES (?,?,?)", clist)
  conn.commit()

def data_out():
  """Return a list with 3 columns : CategoryID, CategoryName, CategoryLevel, From Database"""
  c.execute("SELECT * FROM ebayCategories")
  listado = c.fetchall()
  return listado

def specific_data_out(t):
  """Return a unique row with 3 columns : CategoryID, CategoryName, CategoryLevel from Database """
  c.execute('SELECT * FROM ebayCategories WHERE idCategory=?', (t,))
  string = c.fetchone()
  return string
  
