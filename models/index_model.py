import pandas as pd 

def get_reader(conn):

    return pd.read_sql(
        '''SELECT * FROM reader''', conn)

def get_book_reader(conn, reader_id):
    return pd.read_sql(
        '''WITH get_authors(book_id, authors_name)
        AS (
        SELECT book_id, GROUP_CONCAT(author_name)
        FROM author JOIN book_author USING (author_id)
        GROUP BY book_id
        )

        SELECT title as Название, authors_name as Авторы,
        borrow_date as Дата_выдачи, return_date as Дата_возврата,
        book_reader_id
        FROM reader
        JOIN book_reader USING (reader_id)
        JOIN book USING (book_id)
        JOIN get_authors USING (book_id)
        WHERE reader.reader_id = :id
        ORDER BY 3
    ''', conn, params={"id": reader_id})

def get_new_reader(conn, new_reader):
    cur = conn.cursor()
    cur.execute(
        '''insert into reader(reader_name) VALUES (:p_new_reader)''', {"p_new_reader": new_reader}
    )
    conn.commit()
    return cur.lastrowid

def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    cur.execute('''
INSERT INTO book_reader (book_id, reader_id, borrow_date)
                VALUES (:p_book_id, :p_reader_id, date('now'))''', {"p_book_id": book_id, "p_reader_id": reader_id})
    cur.execute('''update book
                set available_numbers = available_nambers - 1
                where book_id = :p_book_id''', {"p_book_id": book_id})
    conn.commit()
    return True 

def return_book(conn, book_reader_id, reader_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE book_reader
        SET return_date = date('now')
        WHERE book_reader_id = :p_book_reader_id AND reader_id = :p_reader_id
    ''', {"p_book_reader_id": book_reader_id, "p_reader_id": reader_id})

    cur.execute('''
        UPDATE book
        SET available_numbers = available_numbers + 1
        WHERE book_id = (
            SELECT book_id
            FROM book_reader
            WHERE book_reader_id = :p_book_reader_id
        )
    ''', {"p_book_reader_id": book_reader_id})

    conn.commit()
    return True



