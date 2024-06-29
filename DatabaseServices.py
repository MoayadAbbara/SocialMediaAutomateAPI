import mysql.connector
from mysql.connector import Error
import consts

def addNewAnnouncements(LastFiveAnnouncements):
    connection = None
    cursor = None
    new_announcements = []

    try:
        # Establishing the connection to the database
        connection = mysql.connector.connect(
            host=consts.DbHost,
            database=consts.DbName,
            user=consts.DbUser,
            password=consts.DbPassword
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Fetch the latest two announcements from the database
            cursor.execute('SELECT * FROM announcement ORDER BY id DESC LIMIT 2')
            rows = cursor.fetchall()

            if not rows:
                print({"message": "No announcements in the database"})
                return

            latest_announcement = rows[0]
            second_latest_announcement = rows[1] if len(rows) > 1 else None

            # Check if the first new announcement matches the second latest in the database
            if second_latest_announcement and LastFiveAnnouncements and LastFiveAnnouncements[0][1] == second_latest_announcement[2]:
                # Delete the latest announcement from the database
                cursor.execute('DELETE FROM announcement WHERE id = %s', (latest_announcement[0],))
                connection.commit()
                return

            # Check if there are any new announcements
            if LastFiveAnnouncements and LastFiveAnnouncements[0][1] != latest_announcement[2]:
                for announcement in LastFiveAnnouncements:
                    if announcement[1] != latest_announcement[2]:
                        new_announcements.append(announcement)
                    else:
                        break

                # Reverse the new announcements to maintain order
                new_announcements.reverse()

                # Insert new announcements into the database
                insert_query = "INSERT INTO announcement (title, url, image_url, publish_date) VALUES (%s, %s, %s, %s)"
                cursor.executemany(insert_query, new_announcements)
                connection.commit()
                print({"message": "Data inserted successfully into MySQL database"})
            else:
                print({"message": "There is No New Announcement"})
    except Error as e:
        print({'error': f"Error inserting data into MySQL table: {e}"})
    finally:
        # Ensure the cursor is closed
        if cursor is not None:
            cursor.close()
        # Ensure the connection is closed
        if connection is not None and connection.is_connected():
            connection.close()
            print({"message": "MySQL connection is closed"})

