# Scrabble_Assistant
Scrabble assistant written using pygame gives the maximum possible scoring Scrabble word

    To run:
    CD to project directory 
    run >> pip install -r requirements.txt
    run >> python scrabble.py




    To build as executable:
    Change value of 'pathex' in scrabble.spec file to project directory on your computer.
    run >> pyinstaller --onefile --add-data  'scrabble_words.json:.' --add-data 'COMIC.TTF:.'  scrabble.py
