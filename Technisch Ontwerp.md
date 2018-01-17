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
        - laat login.html zien
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
- Stylesheet: login.css
#### Controller
- Route:
    - GET:
        - laat homepage.html zien
    - POST:
        - roep models.user.pictures() aan om de foto's uit de database te halen
        - 



