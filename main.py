from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__,static_url_path='/')


variable = 5
array = []
skaiciai = 0 # su siuo elementu ruosiamas automatinis uzrasines uzrasu skaiciavimas kairiame sone
connection = sqlite3.connect("./NotesDatabase.db")

@app.route("/")
def mano_funkcija():
    return("Labas")

@app.route("/test")
def test():
    return render_template('./index.html', var = plus_one())

@app.route("/debug")
def plus_one():
    global variable
    variable = variable + 1
    return str(variable)

@app.route("/notes",methods=["GET","POST"])
def notes():
    if(request.method == "POST"):
        global array
        request.form.get("note2")

        if(request.form.get("note2")):
            array.append(request.form.get("note2"))
            print(array)
        #if(request.form.get("note1")):
            #array.append(request.form.get("note1"))
            #print(array)
        
        return render_template('./notes.html', note = array)
    else:
        return render_template('./notes.html', note = array)
    
def createDB():
    global connection

    cursor = connection.cursor()

    createTableString = """CREATE TABLE IF NOT EXISTS Sheets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL 
    ) """

    createNotesTableString = """CREATE TABLE IF NOT EXISTS Notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sheetId,
        header TEXT,
        text TEXT,
        FOREIGN KEY (sheetId) REFERENCES Sheets(id)
    ) """

    cursor.execute(createTableString)
    cursor.execute(createNotesTableString)

def insert_into_db():
    queryString = """
        INSERT INTO Sheets (name) VALUES (?)
    """

    cur = connection.cursor()
    cur.execute(queryString,('test',))

if __name__ == "__main__":
    createDB()
    insert_into_db()
    app.run(debug = "true")