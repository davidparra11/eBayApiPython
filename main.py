import functions
import dominate
import sys
from dominate.tags import *

doc = dominate.document(title='Challenge Aflore')

if __name__ == '__main__':
	if  len(sys.argv)==1:
		print("We need to put more than one argument [--help, --build, --render code]")
	else:
		if sys.argv[1]=='--build':
			print("wait...")
			functions.create_table()
			functions.data_entry()
			listado = functions.data_out()

			with doc.head:
			    link(rel='stylesheet', href='style.css')
			    script(type='text/javascript', src='script.js')

			with doc:
			    with div(id='header').add(ol()):
			        for i in listado:
			        	yy = list(i)
			        	y = yy[0]
			        	string = "Id: " + yy[0] +  ". -Category: " + yy[1] + ". -Level: " + yy[2]
			        	li(a(string.title()))

			    with div():
			        attr(cls='body')
			        p('David Parra.')

			Html_file= open("categoriesPage.html","w")
			Html_file.write(str(doc))
			Html_file.close()
			print("List Categories page created!")

		elif sys.argv[1]=='--render':
			t = sys.argv[2]
			string = functions.specific_data_out(t)
			stringList = list(string)

			with doc.head:
			    link(rel='stylesheet', href='style.css')
			    script(type='text/javascript', src='script.js')

			with doc:
			    with div(id='header').add(ol()):
			    	for i in stringList:
			    		li(i.title())

			    with div():
			        attr(cls='body')
			        p('David Parra.')

			Html_file= open("specificCategory.html","w")
			Html_file.write(str(doc))
			Html_file.close()

			print("Specific category Created!")

		elif sys.argv[1]=='--help':			
			print("Use one of them argument [--help, --build, --render code]!")
			print("1st --build")
			print("2nd --render")
			print("remember put CODE category in front of --render argument !")


		else:
			print("Something´s wrong")