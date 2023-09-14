import sqlite3

stephen_king_adaptations_list = []
with open("stephen_king_adaptations.txt", "r") as file:
    for line in file:
        data = line.strip().split(",")
        stephen_king_adaptations_list.append(data)

connection = sqlite3.connect("stephen_king_adaptations.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
        movieID TEXT,
        movieName TEXT,
        movieYear INTEGER,
        imdbRating REAL
    )
""")

for data in stephen_king_adaptations_list:
    cursor.execute("""
        INSERT INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating)
        VALUES (?, ?, ?, ?)
    """, data)

connection.commit()
connection.close()

while True:
    print("Please select an option:")
    print("1. Search movie by name")
    print("2. Search movie by year")
    print("3. Search movie by rating")
    print("4. STOP")
    search_option = input("Enter your option (1-4): ")

    if search_option == "1":
        movie_name = input("Enter the movie name: ")
        connection = sqlite3.connect("stephen_king_adaptations.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName LIKE ?", (f"%{movie_name}%",))
        result = cursor.fetchall()
        connection.close()
        if len(result) > 0:
            for row in result:
                print(f"Movie ID: {row[0]}")
                print(f"Movie Name: {row[1]}")
                print(f"Year: {row[2]}")
                print(f"IMDB Rating: {row[3]}")
        else:
            print("No such movie exists in our database")

    elif search_option == "2":
        movie_year = input("Enter the movie year: ")
        connection = sqlite3.connect("stephen_king_adaptations.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?", (movie_year,))
        result = cursor.fetchall()
        connection.close()
        if len(result) > 0:
            for row in result:
                print(f"Movie ID: {row[0]}")
                print(f"Movie Name: {row[1]}")
                print(f"Year: {row[2]}")
                print(f"IMDB Rating: {row[3]}")
        else:
            print("No movies were found for that year in our database")

    elif search_option == "3":
        rating_limit = input("Enter the minimum rating: ")
        connection = sqlite3.connect("stephen_king_adaptations.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating_limit,))
        result = cursor.fetchall()
        connection.close()
        if len(result) > 0:
            for row in result:
                print(f"Movie ID: {row[0]}")
                print(f"Movie Name: {row[1]}")
                print(f"Year: {row[2]}")
                print(f"IMDB Rating: {row[3]}")
        else:
            print("No movies at or above that rating were found in the database")

    elif search_option == "4":
        break

    else:
        print("Invalid option. Please try again.")