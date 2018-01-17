# Technisch Ontwerp 
*Quintin Raemaekers, Mark Muller en Jo Schreurs*

## Routes
### Register
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

### Login
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

### Homepage
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

### Foto Uploaden
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
        
### Discoverpagina
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
        
### Volgen
Dit is geen pagina, maar een route die ervoor zorgt dat de gebruiker de gelikete persoon volgt op het moment dat de like-knop is aangeklikt.
#### Model
- Bestand: volgen.users.py
- Functie: follow()
#### View
- Template


        
        





