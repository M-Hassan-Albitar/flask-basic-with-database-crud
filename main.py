from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
# create the extension
db = SQLAlchemy()

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Books.db"
# initialize the app with the extension
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # if len(all_books) == 0:
    #     message = "Library is empty."
    # else:
    #     message = ''
    books = db.session.execute(
        db.select(Book).order_by(Book.title)
    ).scalars()
    return render_template('index.html', books=books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # title = request.form.get('bookname')
        # author = request.form.get('bookauthor')
        # rating = request.form.get('bookrating')
        with app.app_context():
            new_book = Book(
                title=request.form.get('bookname'),
                author=request.form.get('bookauthor'),
                rating=request.form.get('bookrating')
            )
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book_to_edit = db.get_or_404(Book, id)
    if request.method == 'POST':
        book_to_edit.rating = request.form.get('rate')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book_to_edit)


@app.route('/<int:id>')
def delete(id):
    book_to_delete = db.session.execute(
        db.select(Book).where(Book.id == id)
    ).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
