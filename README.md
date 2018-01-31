# Tinderest
*Quintin Raemaekers, Mark Muller en Jo Schreurs*

<img src='https://i.imgur.com/diNk5WB.jpg'/>
<img src='https://i.imgur.com/QwActBD.jpg'/>
<img src='https://i.imgur.com/AKVYutH.jpg'/>
<img src='https://i.imgur.com/diNk5WB.jpg'/>
<img src='https://i.imgur.com/diNk5WB.jpg'/>




## Inloggen en Registreren
### Models
register: de nieuwe gebruiker en het wachtwoord worden opgeslagen in de database 'users'.

login: de gegevens van de inloggende gebruiker worden opgehaald uit de database 'users'.

### Views
register.html

login.html

### Controllers
**Logout (@app.route("/logout"))**

Door middel van POST kan de gebruiker zich uitloggen, geen aparte pagina.

De gebruiker wordt teruggestuurd naar login.


**Login (@app.route("/login"))**

Door middel van POST kan de gebruiker inloggen en wordt deze doorverwezen naar de index.


**Register (@app.route(/register))**

Door middel van POST kan de gebruiker zich registreren, en wordt deze als alles klopt doorverwezen naar de homepagina.



## Commenten en liken
### Models
comment: voegt de comments toe aan de database 'comments'.

get_comments: haalt de comments op vanuit de database 'comments'.

like: voegt een like toe aan de database 'images'.

### Views
comment.html

Comments en likes worden weergeven op homepage.html

### Controllers
**Like (@app.route("/like"))**

Er kan een like toegevoegd aan de foto.


**Comment (@app.route("/comment"))**

Er kunnen comments aan de foto's worden toegevoegd.



## Post foto en gifs
### Models
upload_file: voegt een afbeelding toe aan de database 'images'.

giphy: voegt een gif toe aan de database 'images'.

key: geeft de API_KEY mee.

### Views
post.html

gif.html

### Controllers
**Post (@app.route("/post"))**

Foto's met description worden geupload.


**Gifsearch (@app.route("/gifsearch"))**

Zoekt de gifs van api.giphy.com.

**LET OP: voor het werken van de API_KEY is het nodig om een key in de terminal in te voeren, met export API_KEY=
achter het '=' teken gelijk de key.**

Als de gebruiker op een gif heeft gezocht, wordt hij/zij naar gif.html gestuurd.

Als de gebruiker een gif heeft geselecteerd, wordt hij/zij naar de homepagina gestuurd.


**Storegif (@app.route("/storegif"))**

Zet de gif als url.


**Getgif (@app.route("/getgif"))**

Geeft de juiste url van de gif weer zonder aanverwanten van cs50 IDE.



## Settings
### Models
tag: voegt 10 tags toe aan de database 'users'.

### Views
register.html

### Controllers
**Settings (@app.route("/settings"))**

Geeft de tags mee aan het account van de ingelogde gebruiker.



## Discover
### Models
discover: geeft profielen weer met de tags waarop gezocht is.

status_update: update de status van de ingelogde gebruiker.

follow: update welke gebruiker wie volgt.

pics: selecteert de foto's vanuit de database.

username: haalt de username vanuit de database op.

### Views
discover.html

discover_profile.html

### Controllers
**Search (@app.route("/search"))**

Zoekt op de ingevoerde tag. Hierna wordt de ingelogde gebruiker doorgestuurd naar discover_profile.html

**Discover (@app.route("/discover"))**

Zoekt op de profielen met de ingevoerde tag.

Als er geen profielen meer zijn, wordt er een apology  gereturned



## Homepage
### Models
display: geeft de foto's weer.

### Views
homepage.html

### Models
**Homepage (@app.route("/homepage"))**

Geeft de homepagina weer met de foto's en description, en de likes en de comments erbij.
