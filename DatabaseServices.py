import mysql.connector
from mysql.connector import Error
import consts

def addNewAnnouncements (LastFiveAnnouncements) :
    connection = None
    cursor = None
    new_duyuru = []

    try:
        connection = mysql.connector.connect(host=consts.DbHost,
                                             database=consts.DbName,
                                             user=consts.DbUser,
                                             password=consts.DbPassword)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM announcement ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()
            if LastFiveAnnouncements and LastFiveAnnouncements[0][1] != row[2]:
                for duyuru in LastFiveAnnouncements:
                    if duyuru[1] != row[2]:
                        new_duyuru.append(duyuru)
                    else:
                        break
                new_duyuru.reverse()
                for duyuru in new_duyuru:
                    cursor.execute("INSERT INTO announcement (title, url, image_url, publish_date) VALUES (%s, %s, %s, %s)", duyuru)
                connection.commit()
                print({"message": "Data inserted successfully into MySQL database"})
            else:
                print({"message": "There is No New Announcement"})
    except Error as e:
        print({'error': f"Error inserting data into MySQL table: {e}"})
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print({"message": "MySQL connection is closed"})