<h1>Movies Catalog</h1>
It's A 'Movies Catalog App' where every year contain a list of movies issued in that time.
and where users can Create, Update, and Delete Moviess and a whole Years with each filled with it's Movies.

<h2>How To Run Project</h2>
<ul>
  <li> Unzip the compressed project folder </li>
  <li> Run python DB_setup.py to create database </li>
  <li> Run python MoviesLists.py to Populate the database </li>
  <li> Run python MoviesCatalog.py </li>
  <li> visit http://localhost:8000 </li>
</ul>

<h3> Needed Tools </h3>

1. Python3

2. Vagrant

3. VitualBox


<h3> How To Run </h3>

1. Unzip and place the Item Catalog folder in your Vagrant directory

2. Launch Vagrant

3. Change directory to `/vagrant/Catalog Project`

4. Initialize the database

5. Populate the database with some initial data

6. Open the browser and go to http://localhost:8000

<h3>Using Google Login</h3>

1- Go to your app's page in the Google APIs Console — https://console.developers.google.com/apis
  
2- Choose Credentials from the menu on the left.

3- Create an OAuth Client ID.

4- choose Web application.

5- You will then be able to get the client ID and client secret.

6- put your client secret.json on prjoect path 