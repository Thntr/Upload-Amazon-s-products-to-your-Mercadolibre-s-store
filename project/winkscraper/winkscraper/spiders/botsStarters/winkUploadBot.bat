@ECHO OFF
ECHO Running the Wink Synchoronizer
call C:\ProgramData\Miniconda3\Scripts\activate.bat
set "url=https://auth.mercadolibre.com.mx/authorization?client_id=7933855856355346&response_type=code&redirect_uri=https://winktechnologies.herokuapp.com/"
for /l %%x in (1, 1, 10) do (
start cmd /k "cd /d C:\Users\ramzhacker\Documents\MEGA\TheHuntersCarpet\Wink_Inc\WinkAI\##WinkMLApp\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper & scrapy crawl winkUpload"
start chrome "%url%"
)
PAUSE