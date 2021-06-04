# tei_platform

The main idea of the algorithm goes as follows: there are two separate folders at the top level of the structure, one for the user's application, the other for the TEI viewer interface. Two applications are combined together using the dispatcher.py script with the help of DispatcherMiddleware module. The user's application is the basis for the entire resource. The viewer will be located at /tei_viewer. However, it is not necessary that the user’s application is also written in Flask. It can be any WSGI application.

You can launch the program by running the run.py script. By default, the test server run_simple from werkzeug.serving is selected. In order to use the program in production, a proper deployment server has to be chosen.

 There are also two data folders: library and page_content. All data for visualization is stored inside the library folder. The program goes to this folder, selects XML files, extracts meta information such as author name, document title, etc and forms a SQL database. 
 
The project description and any additional information that needs to be displayed on the corpus part of the program should be put in the page_content folder. The data must be written in Markdown and have the .md extension. This gives the user the ability to edit the content without having to study the HTML in depth. 
