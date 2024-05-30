import pandas as pd 

def get_genre(conn):
    return pd.read_sql('''
        SELECT genre.*, count(*) AS count_item
        FROM genre
        JOIN book USING (genre_id)
        GROUP BY genre.genre_id
        ORDER BY 2''', conn)

def get_author(conn):
    return pd.read_sql('''
        SELECT author.*, count(*) AS count_item
        FROM author
        JOIN book_author USING (author_id)
        GROUP BY author.author_id
        ORDER BY 2''', conn)

def get_publisher(conn):
    return pd.read_sql('''
        SELECT publisher.*, count(*) AS count_item
        FROM publisher
        JOIN book USING (publisher_id)
        GROUP BY publisher.publisher_id
        ORDER BY 2''', conn)

def get_book(conn, list_genre, list_author, list_publisher):
    search_str = '''WHERE  '''
    if len(list_genre) != 0:
        search_str += f'''genre.genre_id IN {tuple(list_genre)} AND '''

    if len(list_author) != 0:
        search_str += f'''author.author_id IN {tuple(list_author)} AND '''

    if len(list_publisher) != 0:
        search_str += f'''publisher.publisher_id IN {tuple(list_publisher)} AND '''

    search_str += '''1=1'''

    return pd.read_sql(f'''
        SELECT book.book_id AS book_id, title AS Название, GROUP_CONCAT(author_name) AS Авторы,
           genre_name AS Жанр, publisher_name AS Издательство,
           year_publication AS Год_издания, available_numbers AS Количество
        FROM genre
        JOIN book USING (genre_id)
        JOIN publisher USING (publisher_id)
        JOIN book_author USING (book_id)
        JOIN author USING (author_id) {search_str}
        GROUP BY title
        ORDER BY Название''', conn)

def add_book_reader(conn, reader_id, book_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO book_reader (book_id, reader_id, borrow_date)
        VALUES (:p_book_id, :p_reader_id, DATE('now'))
    ''', {"p_book_id": book_id, "p_reader_id": reader_id})
    
    cur.execute('''
        UPDATE book
        SET available_numbers = available_numbers - 1
        WHERE book_id = :p_book_id
    ''', {"p_book_id": book_id})

    conn.commit()
    return True
