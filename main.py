from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__,static_url_path='/')

variable = 5
array = []
skaiciai = 0 # su siuo elementu ruosiamas automatinis uzrasines uzrasu skaiciavimas kairiame sone
connection = sqlite3.connect("./NotesDatabase.db")

#titulinis puslapis

@app.route("/",methods=["GET","POST"])
def titulinio_funkcija():
    rez = ""
    if (request.method == "POST"):
        usern = request.form.get("username")
        passw = request.form.get("password")
        if usern and passw:
            rez = insert_into_db_registration(usern,passw)
            print(usern,passw)
        else:
            rez = "Neuzpildyti privalomi laukeliai"
    return render_template('./titulinis.html', status = rez)

#miscellanous keliai

@app.route("/test")
def test():
    return render_template('./index.html', var = plus_one())

#miscellanous keliai

@app.route("/debug")
def plus_one():
    global variable
    variable = variable + 1
    return str(variable)

#kuriamas kelias i uzrasus

@app.route("/notes",methods=["GET","POST"])
def notes():
    if(request.method == "POST"):
        global array
        args = request.form.get("note2")

        if(args):
            array.append(args)
            insert_into_db(args)
            print(array)
        #if(request.form.get("note1")):
            #array.append(request.form.get("note1"))
            #print(array)
        
        return render_template('./notes.html', note = select_from_db())
    else:
        
        return render_template('./notes.html', note = select_from_db())

#sukuriama duomenu baze

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

#ivedimas i duomenu baze

def insert_into_db(note):
    conn = sqlite3.connect("./NotesDatabase.db")
    queryString = """
        INSERT INTO Sheets (name) VALUES (?)
    """

    cur = conn.cursor()
    cur.execute(queryString,(note,))
    conn.commit()

#informacijos paemimas is duomenu bazes

def select_from_db():
    conn = sqlite3.connect("./NotesDatabase.db")
    queryString="""
        SELECT name FROM Sheets
    """
    cur = conn.cursor()
    array = cur.execute(queryString).fetchall()

    return array

def createDBforReg():
    registration_connection = sqlite3.connect("./Registration.db")

    cursor = registration_connection.cursor()

    createTableString = """CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL UNIQUE
    ) """

    cursor.execute(createTableString)

def insert_into_db_registration(username,password):
    conn = sqlite3.connect("./Registration.db")
    reg = ""
    queryString = """
        INSERT INTO Users (username,password) VALUES (?,?)
    """

    cur = conn.cursor()
    
    try:
        cur.execute(queryString,(username,password,))
        reg = "Registracija sekminga"

    except sqlite3.IntegrityError as e:
        print(e)
        reg = "Registruoti vartotojo nepavyko"
        print(reg)
        
    conn.commit()
    return reg


if __name__ == "__main__":
    createDB()
    createDBforReg()
    app.run(debug = "true")
