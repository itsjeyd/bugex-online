# BugEx Online

A web application front end for BugEx, a tool that aims at helping developers understand a failure. Developed in the course of the Software Engineering lecture, summer term 2012, at the Software Engineering Chair, Saarland University, Saarbrücken, Germany. 

For further information, see http://www.st.cs.uni-saarland.de/edu/se/2012/ and http://www.st.cs.uni-saarland.de/bugex .

### Collaborators:

* Amir Baradaran
* Tim Krones
* Frederik Leonhardt
* Christos Monogios
* Akmal Qodirov
* Iliana Simova
* Peter Stahl

### Installation and Running

#### Prerequisites

* [Python](http://python.org/download/releases/2.7.3/) (version 2.7.*) and [Django](https://www.djangoproject.com/download/) (version 1.4). 
* For the user registration captcha field we used django-simple-captcha (version 0.3.5). To install it follow these [instructions](http://django-simple-captcha.readthedocs.org/en/latest/usage.html#installation). Please note that django-simple-captcha requires the python imaging library [PIL](http://www.pythonware.com/products/pil/) (version 1.1.7) to be installed. 
* MySQL server
* The python-mysql connector (install python-mysqldb via your prefered package manager)

#### MySQL configuration

The default configuration of BugExOnline uses the following data for accessing the MySQL database:
* User: bugex
* Password: bugex
* Database: bugexonline

You can change the credentials in */bugex_online/settings.py*

#### Running the project

1. Download and extract the project archive.
2. Navigate to the folder _bugex_online_ (should contain a file named _manage.py_).
3. To generate the required database tables, run the following command:  
<pre><code>python manage.py syncdb</code></pre>
4. All static files have to be collected into a common directory. This is necessary for deploying the project, i.e. having access to CSS, JavaScript and image files. To collect all static files into a directory named *static*, run the following command:
<pre><code>python manage.py collectstatic</code></pre>
5. Start the Django development server:  
<pre><code>python manage.py runserver</code></pre>  
You’ll see the following output on the command line:  
<pre><code>Validating models...      
0 errors found
Django version 1.4, using settings 'bugex_online.settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.</code></pre>

5. Enter the URL http://127.0.0.1:8000/ in your browser to start using the system. Detailed instructions on how to use it can be found on its HowTo page. 

### License

Please see [LICENSE](LICENSE.md) for details.