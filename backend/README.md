# backend
## Setup (dev)
1. Clone the repo
```
git clone https://github.com/szczursonn/pp5-property-olx
cd pp5-property-olx/backend
```
2. Install dependencies
```
pip install -r requirements.txt
```
or
```
poetry install
```
3. Setup the DB
```
. scripts/quicksetup.sh
```
Superuser email: superuser@gmail.com.invalid  
Superuser password: qwerty123  
*Note: generated city and street names don't match their coordinates - generated offers are based around Kraków between lat 49.3, 50.8 and lng 19.1, 20.9*  

4. Run the server
```
python3 manage.py runserver --ipv6
```  
*Use ipv6 when using localhost because for some reason sveltekit's server-side fetch resolves localhost to [::1]*

5. Setup the scheduled task in admin panel and run django-q in another shell (optional)  
`func: tasks.deactivate_expired_offers`
```
python3 manage.py qcluster
```

## Config
You can set enviroment variables yourself or use a .env file  
|Variable|Description|Required?|
| - | - | - |
|SECRET_KEY|secret key for passwords and stuff|yes|
|DEBUG|debug mode - set to "True" to turn on, else off|no|
|ORIGINS|comma-seperated list of trusted origins for CSRF Tokens and CORS, set frontend url here, example: ORIGINS=http://localhost:8000;https://google.com;http://192.168.0.4:5173|yes|
