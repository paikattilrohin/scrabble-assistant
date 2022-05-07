# Scrabble Assistant
Scrabble assistant written using pygame gives the maximum possible scoring Scrabble word

https://user-images.githubusercontent.com/39897345/153726942-e28a7429-8586-4450-84af-f7f0fd53e385.mp4


    To run:
    CD to project directory 
    run >> pip install -r requirements.txt
    run >> python scrabble.py




    To build as executable:
    Change value of 'pathex' in scrabble.spec file to project directory on your computer.
    run >> pyinstaller --onefile --add-data  'scrabble_words.json:.' --add-data 'COMIC.TTF:.'  scrabble.py



