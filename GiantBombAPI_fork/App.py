from theme_client import ThemeClient
from genre_client import GenreClient
from platform_client import PlatformClient
from company_client import CompanyClient
from game_client import GameClient
import exceptions

import mysql.connector

my_key = ""
arr = []

cnx = mysql.connector.connect(user="root", password="",
                              host="localhost", database="games")
cursor = cnx.cursor()


def genres(j, k):
    global arr
    sql = "INSERT INTO genres (name, giantBombGenreId) VALUES (%s, %s)"
    client = GenreClient(my_key)
    arr = []
    for i in range(j, k):
        try:
            x = client.fetch(i).results
            print(i, end="; ")
            arr.append((x["name"], x["id"]))
        except Exception as e:
            pass
    print("   ---Done---")
    for i in arr:
        print("+", end="")
        cursor.execute(sql, i)
    print("   ---Done---")
    cnx.commit()


def themes(j, k):
    global arr
    sql = "INSERT INTO themes (name, giantBombThemeId) VALUES (%s, %s)"
    client = ThemeClient(my_key)
    arr = []
    for i in range(j, k):
        try:
            x = client.fetch(i).results
            print(i, end="; ")
            arr.append((x["name"], x["id"]))
        except Exception as e:
            pass
    print("   ---Done---")
    for i in arr:
        print("+", end="")
        cursor.execute(sql, i)
    print("   ---Done---")
    cnx.commit()


def platforms():
    sql = "INSERT INTO platforms (name, abbreviation, deck, giantBombPlatformId) VALUES (%s, %s, %s, %s)"
    client = PlatformClient(my_key)
    arr = []
    for i in range(1, 176):
        try:
            x = client.fetch(i).results
            print(x["name"], end="; ")
            arr.append((x["name"], x["abbreviation"], x["deck"], x["id"]))
        except Exception as e:
            pass
    print("   ---Done---")
    for i in arr:
        print("+", end="")
        cursor.execute(sql, i)
    print("   ---Done---")
    cnx.commit()


def companies(j=1, k=18913):
    global arr
    sql = "INSERT INTO companies (name, deck, giantBombCompanyId) VALUES (%s, %s, %s)"
    client = CompanyClient(my_key)
    arr = []
    for i in range(j, k):
        try:
            x = client.fetch(i).results
            print(i, end="; ")
            arr.append((x["name"], x["deck"], x["id"]))
        except Exception as e:
            pass
    print("   ---Done---")
    for i in arr:
        print("+", end="")
        cursor.execute(sql, i)
    print("   ---Done---")
    cnx.commit()


def games(j=1, k=72822):
    sql = "INSERT INTO games (name, deck, image, release_date, giantBombGameId) VALUES (%s, %s, %s, %s, %s)"
    sql_game = "SELECT max(id) FROM games"
    sql_platforms = "INSERT INTO games_and_platforms (gameId, platformId) VALUES (%s, %s)"
    sql_companies = "INSERT INTO games_and_companies (gameId, companyId, relation) VALUES (%s, %s, %s)"
    sql_genres = "INSERT INTO games_and_genres (gameId, genreId) VALUES (%s, %s)"
    sql_themes = "INSERT INTO games_and_themes (gameId, themeId) VALUES (%s, %s)"
    client = GameClient(my_key)
    return_fields = (
    "id", "name", "platforms", "deck", "developers", "genres", "image", "publishers", "original_release_date", "themes")
    for i in range(j, k):
        try:
            x = client.fetch(i, return_fields).results
            print(i, "fetched", sep=" ", end=",")
            for j in return_fields:
                try:
                    y = x[j]
                except KeyError as ke:
                    x[j] = None
            if x["image"] is None:
                image = None
            else:
                image = x["image"]["small_url"]
            if x["original_release_date"] is None:
                date = None
            else:
                date = x["original_release_date"][:10]
            arr = [x["platforms"], x["developers"], x["publishers"], x["genres"], x["themes"],
                   (x["name"], x["deck"], image, date, x["id"])]
            cursor.execute(sql, arr[5])
            cnx.commit()
            cursor.execute(sql_game)
            game = cursor.fetchall()[0][0]
            if arr[0] is not None:
                for platform in arr[0]:
                    cursor.execute("SELECT id FROM platforms WHERE giantBombPlatformId = {}".format(platform["id"]))
                    platformId = cursor.fetchall()[0][0]
                    cursor.execute(sql_platforms, (game, platformId))
                    cnx.commit()
            if arr[1] is not None:
                for developer in arr[1]:
                    cursor.execute("SELECT id FROM companies WHERE giantBombCompanyId = {}".format(developer["id"]))
                    developerId = cursor.fetchall()[0][0]
                    cursor.execute(sql_companies, (game, developerId, "developer"))
                    cnx.commit()
            if arr[2] is not None:
                for publisher in arr[2]:
                    cursor.execute("SELECT id FROM companies WHERE giantBombCompanyId = {}".format(publisher["id"]))
                    publisherId = cursor.fetchall()[0][0]
                    cursor.execute(sql_companies, (game, publisherId, "publisher"))
                    cnx.commit()
            if arr[3] is not None:
                for genre in arr[3]:
                    cursor.execute("SELECT id FROM genres WHERE giantBombGenreId = {}".format(genre["id"]))
                    genreId = cursor.fetchall()[0][0]
                    cursor.execute(sql_genres, (game, genreId))
                    cnx.commit()
            if arr[4] is not None:
                for theme in arr[4]:
                    cursor.execute("SELECT id FROM themes WHERE giantBombThemeId = {}".format(theme["id"]))
                    themeId = cursor.fetchall()[0][0]
                    cursor.execute(sql_themes, (game, themeId))
                    cnx.commit()
            print(i, "stored", sep=" ")
        except exceptions.InvalidResponseException as e:
            pass
    print("   ---Done---")
