# Technisch Ontwerp 
*Quintin Raemaekers, Mark Muller en Jo Schreurs*

## Routes
### Register - POST
Op deze pagina kan de persoon zich registreren. Men vult hier een unieke gebruikersnaam in en een wachtwoord. Deze worden opgeslagen in de database.
#### Model
- Bestand: models.users.py
- Functie: register(name, password)
    - returnt User/None
#### View
- Template: register.html
- Stylesheet: register.css
#### Controller
- Route: 
    - GET: 
        - laat register.html zien
    - POST:
        - roep models.user.register() aan met het ingevulde wachtwoord en de naam
        - sla user_id in session op als registreren is gelukt
        - redirect naar /homepage.html als registreren is gelukt, anders /register.html

### Login - POST
Op deze pagina kan de persoon inloggen. Men vult hier diens gebruikersnaam en wachtwoord in.
#### Model
- Bestand: models.users.py
- Class: attributen id en naam
- Functie: login(name, password)
    - return User/None
#### View
- Template: login.html
- Stylesheet: login.css
#### Controller
- Route:
    - GET:
        - laat /login.html zien
    - POST:
        - roep models.user.login() aan met het ingevulde wachtwoord en de naam
        - sla user_id in session op als login is gelukt
        - redirect naar /homepage.html als inloggen is gelukt, anders /login.html

### Homepage - POST
Op deze pagina kan men navigeren naar de andere pagina's bovenaan: settings, "tinderpage". Ook kan men oneindig naar onder scrollen om foto's te bekijken van degene die zij volgen en de pagina herladen om de nieuwste foto's in hun tijdlijn te krijgen. Dit moet geprogrammeerd worden met AJAX. De foto's staan op chronologische volgorde. Daarnaast is het mogelijk te liken en te commenten. Ook moet vanuit hier foto's geupload kunnen worden.
#### Model
- Bestand: models.users.py
- Class: voor elke foto
- Functie: homepage(following)
#### View
- Template: homepage.html
- Stylesheet: homepage.css
#### Controller
- Route:
    - GET:
        - laat /homepage.html zien
    - POST:
        - roep models.user.pictures() aan om de foto's uit de database te halen
        - zorg ervoor dat de pagina kan herladen
        - redirect naar /homepage.html, zowel als er een nieuwe foto bij is gekomen en anders gewoon hetzelde als eerst
        - zorgen dat men comments kan schrijven en kan liken en dit in de database opslaan
            - like is een counter

### Foto Uploaden - POST
Op deze pagina kan men foto's op GIFs uploaden en een bijschrift erbij zetten.
#### Model
- Bestand: models.users.py
- Functie: upload()
#### View
- Template: upload.html
- Stylesheet: upload.css
#### Controller
- Route:
    - GET:
        - laat /upload.html zien
    - POST:
        - zet de foto/GIF in de database
        - redirect naar /homepage.html als de foto geupload is
        
### Discoverpagina - POST
Op deze pagina kan men naar een tag zoeken en de profielen met dezelfde tag liken (en ook meteen volgen) of disliken.
#### Model
- Bestand: models.users.py
- Functie: discover()
#### View
- Template: discover.html
- Stylesheet: discover.html
#### Controller
- Route:
    - GET: 
        - laat /discover.html zien
    - POST:
        - roep models.user.pictures() aan om de vier meest recente foto's uit de database te halen
        - roep models.user.tags() aan om de gebruikers met de gezochte tag uit de database te halen
        - op dislike drukken waarna de volgende gebruiker komt
        - op like drukken waarna de user de gelikete gebruiker meteen volgen, redirecten via de route 'follow' dus
        
### Volgen - POST
Dit is geen pagina, maar een route die ervoor zorgt dat de gebruiker de gelikete persoon volgt op het moment dat de like-knop is aangeklikt.
#### Model
- Bestand: models.users.py
- Functie: follow()
#### Controller
- Route:
    - POST:
        - zet in de database dat de ene gebruiker de andere gebruiker volgt
        - zorg ervoor dat de gebruiker de foto's van de ander te zien krijgt
 
### Settings - POST
Dit is een pagina waar de gebruiker kan uitloggen of diens tags aan kan passen. 
#### Model
- Bestand: models.users.py
- Functie: settings()
#### View
- Template: settings.html
- Stylesheet: discover.html
#### Controller
- Route:
    - GET:
        - laat /settings.html zien
    - POST:
        - zorg ervoor dat de gebruiker tot tien tags kan instellen
        - sla de tags op in de database
        - zorg ervoor dat de gebruiker kan uitloggen
        
## Views
<img src='https://i.imgur.com/kjTmSzi.jpg'/>

## Models
### Imports
- **Flask from flask.** Bij deze functie kan er gebruik gemaakt worden van bijvoorbeeld render_template en redirect, waarmee er van de ene pagina naar de andere pagina gegaan kan worden. Ook kunnen er extra functies van flask worden gebruikt, zoals flash, maar dit is nog niet zeker of we dit gaan gebruiken.
- **custom_app_context as pwd_context from passlib.apps.** Bij deze functie kan er bijvoorbeeld een hash aangemaakt worden, zodat het wachtwoord niet te zien is in de database (en waardoor het wachtwoord is beveiligd).
- **wraps from functools.** Hierbij kan er een helper-module gemaakt worden voor een functie dat het wachtwoord vereist is.
- **Session from flask_session.** Voor het hebben van de flask app. 

### Helper modules
We zullen uiteraard een file maken zoals helpers.py van cs50 finance. Hierin komen een aantal zaken in te staan, namelijk deze functies:
- **Apology():** In deze functie wordt aangegeven wanneer iets fout gaat. Deze functie kan opgeroepen worden in de controller als iemand het verkeerde wachtwoord invoert bij de log in pagina. 
- **Login():** Deze functie geeft aan dat iemand ingelogd moet zijn om de functie die in de controller is aangegeven te kunnen uitvoeren. Als dit niet het geval is kan de gebruiker niet naar de aangegeven pagina toe gaan.
- **Lookup():** Deze functie geeft hulp bij het zoeken van de GIFs van de website. 
- **Picture():** Deze functie geeft aan dat er een foto moet worden opgehaald, die op de tijdlijn verschijnt.
- **Lookup_tags():** Deze functie geeft hulp bij het zoeken van de tags die de gebruiker bij instellingen heeft ingevoerd.

## Plugins en frameworks
#### Flask
Wij hebben ervoor gekozen om flask te gebruiken, mede omdat we hier al bekend mee zijn geworden bij cs50 finance. Je hebt hiervoor import functies, zoals beschreven bij models.
http://flask.pocoo.org
#### GIFs
Daarnaast zullen we de voorgestelde gifs gebruiken.
http://api.giphy.com
