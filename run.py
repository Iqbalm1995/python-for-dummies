from app.app import app
from database import db

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=6300)  # Change 6300 to the port you want to use
