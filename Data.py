""""
Created by: Zasko B.
Operates with DB: gets data from DB, adds data to DB or removes data from DB
"""

import random
import operator

from Conn import cursor, cnx

""" SQL queries for getting game info """
SQL_SELECT_GAME = "SELECT * FROM games WHERE id=%s"
SQL_SELECT_PLATFORMS = "SELECT * FROM platforms WHERE id IN" \
                       "(SELECT platformID FROM games_and_platforms WHERE gameId=%s)"
SQL_SELECT_GENRES = "SELECT * FROM genres WHERE id IN" \
                    "(SELECT genreID FROM games_and_genres WHERE gameId=%s)"
SQL_SELECT_THEMES = "SELECT * FROM themes WHERE id IN" \
                    "(SELECT themeID FROM games_and_themes WHERE gameId=%s)"
SQL_SELECT_COMPANY = "SELECT * FROM companies WHERE id IN" \
                        "(SELECT companyID FROM games_and_companies WHERE gameId=%s AND relation=%s)"

""" SQL queries for checking if game in the library or not """
SQL_CHECK_LIBRARY_STATE = "SELECT * FROM library WHERE gameId=%s"

""" SQL query for getting user score for the game in the library """
SQL_CHECK_RATING = "SELECT rating FROM library WHERE gameId=%s"

""" SQL query for getting game by name """
SQL_SELECT_GAME_BY_NAME = "SELECT id FROM games WHERE name=%s"

""" SQL query for getting games for home page of the app """
SQL_SELECT_GAMES = "SELECT id FROM games LIMIT %s OFFSET %s"

""" SQL queries for adding game to the library or removing it """
SQL_INSERT_TO_LIBRARY = "INSERT INTO library (gameId, rating) VALUES (%s, %s)"
SQL_DELETE_FROM_LIBRARY = "DELETE FROM library WHERE gameId=%s"

""" Gets amount of games in library """
SQL_SELECT_LIBRARY = "SELECT COUNT(id) FROM library"

""" SQL query for getting games for library page of the app """
SQL_SELECT_GAMES_FROM_LIBRARY = "SELECT gameId FROM library LIMIT %s OFFSET %s"

""" SQL queries for getting games by chosen characteristic """
SQL_SELECT_GAMES_BY_PLATFORM = "SELECT id FROM games WHERE id IN (SELECT gameId FROM games_and_platforms " \
                               "WHERE platformId = (SELECT id FROM platforms WHERE name=%s)) LIMIT %s OFFSET %s"
SQL_SELECT_GAMES_BY_GENRE = "SELECT id FROM games WHERE id IN (SELECT gameId FROM games_and_genres " \
                               "WHERE genreId = (SELECT id FROM genres WHERE name=%s)) LIMIT %s OFFSET %s"
SQL_SELECT_GAMES_BY_THEME = "SELECT id FROM games WHERE id IN (SELECT gameId FROM games_and_themes " \
                               "WHERE themeId = (SELECT id FROM themes WHERE name=%s)) LIMIT %s OFFSET %s"
SQL_SELECT_GAMES_BY_COMPANY = "SELECT id FROM games WHERE id IN (SELECT gameId FROM games_and_companies " \
                               "WHERE relation=%s AND companyId = (SELECT id FROM companies WHERE name=%s)) " \
                              "LIMIT %s OFFSET %s"

""" Gets max game id (used when getting random game """
cursor.execute("SELECT MAX(id) FROM games")
MAX_ID = cursor.fetchall()[0][0]

""" Gets amount of games in DB """
cursor.execute("SELECT COUNT(id) FROM games")
NUMBER_OF_GAMES = cursor.fetchall()[0][0]

""" Stores amount of games in library; changes only when it's needed """
LEN_OF_LIBRARY = 0

""" Stores amount of recommended games; changes only when it's needed """
LEN_OF_RECOMMENDATIONS = 0


class Game:
    """
    Main entity class. Used for storing info about concrete game and
    operating with this info
    """
    def __init__(self, game_id):
        self.id = game_id
        cursor.execute(SQL_SELECT_GAME, (self.id, ))
        fetched_data = cursor.fetchall()[0]
        self.name = fetched_data[1]
        self.desc = fetched_data[2]
        if self.desc is None:
            self.desc = "N/A"
        self.image = fetched_data[3]
        self.release_date = fetched_data[4]
        if self.release_date is None:
            self.release_date = "N/A"
        cursor.execute(SQL_SELECT_PLATFORMS, (self.id,))
        self.platforms = [platform[1] for platform in cursor.fetchall()]
        cursor.execute(SQL_SELECT_GENRES, (self.id, ))
        self.genres = [genre[1] for genre in cursor.fetchall()]
        cursor.execute(SQL_SELECT_THEMES, (self.id, ))
        self.themes = [theme[1] for theme in cursor.fetchall()]
        cursor.execute(SQL_SELECT_COMPANY, (self.id, "developer"))
        self.developers = [company[1] for company in cursor.fetchall()]
        cursor.execute(SQL_SELECT_COMPANY, (self.id, "publisher"))
        self.publishers = [company[1] for company in cursor.fetchall()]

    @staticmethod
    def generate_text(text, array):
        """
        Generates text string from array for use in GUI game tab

        :param text: Parameter of the game, e.g. genres, publishers, etc.
        :param array: Array of text parameter values
        :return: str
        """
        string = text + ":"
        if len(array) == 0:
            string += " N/A"
            return string
        for i in array:
            temp = i.replace(" ", "_")
            string += " <a href=" + temp + ">" + i + "</a>,"
        return string[:-1]

    def library_state(self):
        """
        Checks if game is in the library or not

        :return: bool
        """
        cursor.execute(SQL_CHECK_LIBRARY_STATE, (self.id,))
        returned_data = cursor.fetchall()
        if len(returned_data) == 1:
            return True
        return False

    def get_rating(self):
        """
        For game in the library, get user rating

        :return: int
        """
        cursor.execute(SQL_CHECK_RATING, (self.id, ))
        return cursor.fetchall()[0][0]

    def add_to_library(self, rating=None):
        """
        Adds game to the library

        :param rating: User rating for the game
        """
        cursor.execute(SQL_INSERT_TO_LIBRARY, (self.id, int(rating)))
        cnx.commit()

    def remove_from_library(self):
        """ Removes game from the library """
        cursor.execute(SQL_DELETE_FROM_LIBRARY, (self.id,))
        cnx.commit()


def random_game():
    """
    Create instance of random game

    :return: Game
    """
    while True:
        game_id = random.randint(1, MAX_ID)
        try:
            game = Game(game_id)
            return game
        except IndexError:
            pass


def game_by_name(string):
    """
    Searches game by the name

    :param string: Search query
    :return: Game or None
    """
    cursor.execute(SQL_SELECT_GAME_BY_NAME, (string,))
    try:
        data = cursor.fetchall()[0]
        return Game(data[0])
    except IndexError:
        return None


def home_page(page, items):
    """
    Gets games for filling home page of the app

    :param page: Page in the app
    :param items: Amount of items per page
    :return: list of Game objects
    """
    cursor.execute(SQL_SELECT_GAMES, (items, (page-1)*items))
    return [Game(game[0]) for game in cursor.fetchall()]


def library_len():
    """
    Counts the number of games in library and stores it to variable
    """
    global LEN_OF_LIBRARY
    cursor.execute(SQL_SELECT_LIBRARY)
    LEN_OF_LIBRARY = cursor.fetchall()[0][0]


def library_page(page, items):
    """
    Gets games for filling library page of the app

    :param page: Page in the app
    :param items: Amount of items per page
    :return: list of Game objects
    """
    cursor.execute(SQL_SELECT_GAMES_FROM_LIBRARY, (items, (page-1)*items))
    return [Game(game[0]) for game in cursor.fetchall()]


def chosen_characteristic(text, characteristic, page=None, items=None):
    """
    Counts the number of games in chosen characteristic query or
    gets games for fulfilling chosen characteristic page of the app

    :param text: Value for parameter characteristic
    :param characteristic: Parameter of the game, e.g. genre, publisher, etc.
    :param page: Page in the app
    :param items: Amount of items per page
    :return: int or list of Game objects
    """
    if page is None:
        limit = NUMBER_OF_GAMES
        offset = 0
    else:
        limit = items
        offset = (page-1)*items
    text = text.replace("_", " ")
    if characteristic == "platform":
        cursor.execute(SQL_SELECT_GAMES_BY_PLATFORM, (text, limit, offset))
    elif characteristic == "genre":
        cursor.execute(SQL_SELECT_GAMES_BY_GENRE, (text, limit, offset))
    elif characteristic == "theme":
        cursor.execute(SQL_SELECT_GAMES_BY_THEME, (text, limit, offset))
    elif characteristic == "developer":
        cursor.execute(SQL_SELECT_GAMES_BY_COMPANY, ("developer", text, limit, offset))
    else:
        cursor.execute(SQL_SELECT_GAMES_BY_COMPANY, ("publisher", text, limit, offset))
    data = cursor.fetchall()
    if page is None:
        return len(data)
    return [Game(game[0]) for game in data]


def analyze_library():
    """
    Analyzes library and returns recommendations

    :return: list of Game objects
    """

    def fill_dicts(items, dict_of, rating):
        """ On-place function used for filling rating dicts """
        for item in items:
            if item in dict_of.keys():
                dict_of[item] += rating
            else:
                dict_of[item] = rating

    global LEN_OF_RECOMMENDATIONS
    cursor.execute(SQL_SELECT_GAMES_FROM_LIBRARY, (NUMBER_OF_GAMES, 0))
    game_ids = [item[0] for item in cursor.fetchall()]
    if len(game_ids) == 0:
        LEN_OF_RECOMMENDATIONS = 0
        return []
    games = [Game(game) for game in game_ids]
    rating_dicts = [{}, {}]
    for game in games:
        game.rating = game.get_rating()
        fill_dicts(game.genres, rating_dicts[0], game.rating)
        fill_dicts(game.platforms, rating_dicts[1], game.rating)
    max_values = []
    for i in range(2):
        try:
            max_values.append(max(rating_dicts[i].items(), key=operator.itemgetter(1))[0])
        except ValueError:
            max_values.append(None)
    returned_platform_ids = []
    returned_genre_ids = []
    if max_values[1] is not None:
        cursor.execute(SQL_SELECT_GAMES_BY_PLATFORM, (max_values[1], NUMBER_OF_GAMES, 0))
        returned_platform_ids = [item[0] for item in cursor.fetchall()]
        returned_platform_ids = list(set(returned_platform_ids) - set(game_ids))
    if max_values[0] is not None:
        cursor.execute(SQL_SELECT_GAMES_BY_GENRE, (max_values[0], NUMBER_OF_GAMES, 0))
        returned_genre_ids = [item[0] for item in cursor.fetchall()]
        returned_genre_ids = list(set(returned_genre_ids) - set(game_ids))
    if len(returned_platform_ids) > 0:
        if len(returned_genre_ids) > 0:
            returned_ids = list(set(returned_platform_ids).intersection(returned_genre_ids))
        else:
            returned_ids = returned_platform_ids
    elif len(returned_genre_ids) > 0:
        returned_ids = returned_genre_ids
    else:
        LEN_OF_RECOMMENDATIONS = 0
        return []
    if len(returned_ids) > 14:
        returned_ids = random.choices(returned_ids, k=14)
    LEN_OF_RECOMMENDATIONS = len(returned_ids)
    return [Game(game) for game in returned_ids]

