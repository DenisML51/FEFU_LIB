from app import app 
from flask import render_template, request, session 

from utils import get_db_connection
from models.index_model import get_reader, get_book_reader, get_new_reader, borrow_book, return_book
from models.search_model import add_book_reader
@app.route('/', methods=['get'])

def index():
    conn = get_db_connection()

    if request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id

    elif request.values.get('new_reader'):
        new_reader = request.values.get('new_reader')
        session['reader_id'] = get_new_reader(conn, new_reader)

    elif request.values.get('Сдать'):
        book_reader_id = int(request.values.get['book_reader_id'])
        return_book(conn, book_reader_id, session['reader_id'])

    elif request.values.get('Выбрать'):
        reader_id = session['reader_id']
        book_id = int(request.values.get('book_id'))
        add_book_reader(conn, reader_id, book_id)
    
    elif request.values.get('reader_id'):
        reader_id = int(request.values.get('reader_id'))
        session['reader_id'] = reader_id

    elif request.values.get('noselect'):
        a = 1

    else:
        session['reader_id'] = 1


    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, session['reader_id'])

    html = render_template(
        'index.html',
        reader_id = session['reader_id'],
        combo_box = df_reader,
        book_reader = df_book_reader,
        len = len)

    return html
