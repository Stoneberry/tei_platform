# tei_platform

The main idea of the algorithm goes as follows: there are two separate folders at the top level of the structure, one for the user's application, the other for the TEI viewer interface. 

Two applications are combined together using the ```dispatcher.py``` script with the help of ```DispatcherMiddleware``` module. The user's application is the basis for the entire resource. The viewer will be located at ```/tei_viewer```. However, it is not necessary that the user’s application is also written in Flask. It can be any WSGI application.

You can launch the program by running the ```run.py``` script. By default, the test server ```run_simple``` from ```werkzeug.serving``` is selected. In order to use the program in production, a proper deployment server has to be chosen.

There are also two data folders: 

* library 
* page_content.

All data for visualization is stored inside the ```library``` folder. The program goes to this folder, selects XML files, extracts meta information such as author name, document title, etc and forms a SQL database. 
 
The project description and any additional information that needs to be displayed on the corpus part of the program should be put in the ```page_content``` folder. The data must be written in Markdown and have the ```.md``` extension. This gives the user the ability to edit the content without having to study the HTML in depth. 

Additional ```.md``` files have to be named either ```about.md``` or ```guide.md``` for for the corresponding site pages. All the images have to be located in ```page_content/static/img```.

## Setup

To setup the application, open a command line, select a folder, where you whant your application to be and execute following commands:


### Create application environment

* Create a folder ```mkdir tei_platform```
* Go to folder ```cd tei_platform```
* Create a virtual environment ```python3 -m venv env``` for MacOS/Linux or ```py -m venv env``` for Windows
* Activating a virtual environment ```source env/bin/activate``` for MacOS/Linux or ```.\env\Scripts\activate``` for Windows

### Setup app architecture

* ```git init```
* ```git remote add origin -f https://github.com/Stoneberry/tei_platform.git```
* ```git pull origin main```


### Install dependencies

* ```npm install```
* ```pip3 install -r requirements.txt```

* ```mkdir app_tei/static/docs```
* ```mkdir app_tei/static/img```

* ```cd app_tei/static/css```
* ```ln -s ../../../node_modules/bootstrap/dist/css/bootstrap.min.css```
* ```ln -s ../../../node_modules/bootstrap-icons/font/bootstrap-icons.css```
* ```ln -s ../../../node_modules/bootstrap-select/dist/css/bootstrap-select.min.css```
* ```ln -s ../../../node_modules/jquery-ui-dist/jquery-ui.min.css```

* ```cd ../js```
* ```ln -s ../../../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js```
* ```ln -s ../../../node_modules/jquery/dist/jquery.min.js```
* ```ln -s ../../../node_modules/bootstrap-select/dist/js/bootstrap-select.min.js```
* ```ln -s ../../../node_modules/jquery-ui-dist/jquery-ui.min.js```


The repository has pre-installed files for demonstration. You can delete them and put your files in the folder. Then run the following commands to create the database.

###  Setup database

* ```cd ../../../app_tei```
* ```python3 library_setup.py```
* ```deactivate```









