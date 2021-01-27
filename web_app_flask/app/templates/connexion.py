import mysql.connector
import requests
import webbrowser

urlpost = "accueil.html"
userpost = requests.post(url = urlpost, data = 'username')
mdppost = requests.post(url = urlpost, data = 'mdp')

conn = mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="root",
                                  database="banque"
                                  )

if userpost and mdppost:

    mycursor = conn.cursor()
    mycursor.execute("SELECT username, mdp FROM users")
    myresult = mycursor.fetchall()


    if myresult:

        if userpost == myresult['username'] and mdppost == myresult['mdp']:

            webbrowser.open("dashboard.py")
else:
    webbrowser.open("accueil.html")

conn.close()