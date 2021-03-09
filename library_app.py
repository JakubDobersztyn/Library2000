from flask import Flask, request, render_template
from psycopg2 import connect
from datetime import date

con = connect(host='localhost', user='postgres', password='coderslab', dbname='library_db')
con.autocommit = True
app = Flask(__name__)


@app.route('/add_book', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'GET':
        return render_template("add_book.html")
    isbn = request.form['book_isbn']
    name = request.form['book_name']
    desc = request.form['book_desc']
    author = request.form['book_author']
    cur = con.cursor()
    cur.execute("insert into book (isbn, name, description, author_id) values (%s, %s, %s, %s)",
                (isbn, name, desc, author))
    return render_template("add_book.html", sukces=True)


@app.route('/books')
def movies():
    cur = con.cursor()
    cur.execute("select * from book")
    result = cur.fetchall()
    return render_template("books.html", books=result)


@app.route('/book_detail/<id>')
def view_movie(id):
    cur = con.cursor()
    cur.execute("SELECT isbn, name, description, author_id FROM book WHERE id=%s", (id,))
    book = cur.fetchone()
    if book is None:
        return '<h1>nie ma takiego numeru</h1>'
    return render_template("book_det_id.html", book=book)


@app.route('/del_book/<id>')
def del_movie(id):
    cur = con.cursor()
    cur.execute("select * from book where id=%s", (id,))
    book_n = cur.fetchone()

    cur.execute("delete from book where id=%s", (id,))

    return render_template("del_book.html", book_id=id, book_name=book_n)


@app.route('/clients')
def clients():
    cur = con.cursor()
    cur.execute("select * from client")
    result = cur.fetchall()
    return render_template("clients.html", clients=result)


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'GET':
        return render_template("add_client.html")
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    cur = con.cursor()
    cur.execute("insert into client (first_name, last_name) values (%s, %s)", (first_name, last_name))
    return render_template("add_client.html", sukces=True)


@app.route('/del_client/<id>')
def del_client(id):
    cur = con.cursor()
    cur.execute("select * from client where id=%s", (id,))
    client_n = cur.fetchone()

    cur.execute("delete from client where id=%s", (id,))

    return render_template("del_client.html", client_id=id, client_name=client_n)


@app.route('/client_detail/<id>')
def view_client(id):
    cur = con.cursor()
    cur.execute(
        "select first_name, last_name, name, book_id, client.id from client left join client_books on client.id=client_books.client_id left join book on client_books.book_id=book.id where client.id=%s",
        (id,))
    client = cur.fetchall()
    if client is None:
        return '<h1>nie ma takiego numeru</h1>'
    return render_template("client_details.html", client=client)


@app.route('/loan', methods=['GET', 'POST'])
def loan():
    cur = con.cursor()
    if request.method == 'GET':
        cur.execute("select * from client")
        clients = cur.fetchall()
        cur.execute("select * from book where is_loaned=False")
        books = cur.fetchall()
        return render_template("loan.html", clients=clients, books=books)
    else:
        client = request.form['client_id']
        book = request.form['book_id']
        today = date.today()
        cur.execute("insert into client_books (client_id, book_id, loan_date) values (%s, %s, %s)",
                    (client, book, today))
        cur.execute("update book set is_loaned=True where id=%s", (book,))
        cur.execute("select first_name, last_name from client where id=%s", (client,))
        c_name = cur.fetchone()
        cur.execute("select name from book where id=%s", (book,))
        b_name = cur.fetchone()
        return render_template("loan_info.html", client=c_name, book=b_name)


app.run(debug=False)
