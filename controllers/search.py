from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.search_model import get_genre, get_publisher, get_author, get_book, add_book_reader

import numpy as np

def to_tuple(list_char):
    tup = tuple(np.array(list_char + ['-1'], int))
    return tup

@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()
    df_genre = get_genre(conn)
    df_publisher = get_publisher(conn)
    df_author = get_author(conn)
    reader_id = request.values.get('reader_id')

    list_genre = ()
    list_author = ()
    list_publisher = ()
    
    if request.values.getlist('genre[]'):
        list_genre = to_tuple(request.values.getlist('genre[]'))

    if request.values.getlist('author[]'):
        list_author = to_tuple(request.values.getlist('author[]'))

    if request.values.getlist('publisher[]'):
        list_publisher = to_tuple(request.values.getlist('publisher[]'))
    
    if request.values.get('Очистить'):
        list_genre = ()
        list_author = ()
        list_publisher = ()


    df_book_search = get_book(conn, list_genre, list_author, list_publisher)

    html = render_template(
        'search.html',
        reader_id = session['reader_id'],
        list_genre=list_genre,
        genre=df_genre,
        list_author=list_author,
        author=df_author,
        list_publisher=list_publisher,
        publisher=df_publisher,
        book_search=df_book_search,
        len=len
    )
    return html


