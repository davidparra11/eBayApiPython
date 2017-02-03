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
			functions.drop_tables()
			functions.create_table()
			functions.create_table1()
			functions.create_table2()
			functions.create_table3()
			functions.create_table4()
			functions.data_entry()
			
			print("List Categories DB has been builded!")

		elif sys.argv[1]=='--render':
			print("wait...")
			t = sys.argv[2]
			string = functions.specific_data_out(t)
			if (string is None):
				print("The ID: " + t + "  not exist")
				sys.exit()

			stringList = list(string)#list

			with doc.head:
			    link(rel='stylesheet', href='style.css')
			    script(type='text/javascript', src='script.js')

			with doc:
			    with div(id='header').add(ol()):
			    	for i in string:
			    		yy = list(i)
			    		y = yy[0]
			    		string = "Id: " + str(yy[0]) +  ". -Category: " + str(yy[1]) + ". -Level: " + str(yy[2])
			    		li(a(string.title()))

			    with div():
			        attr(cls='body')
			        p('David Parra.')

			Html_file= open("" + t + ".html","w")
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