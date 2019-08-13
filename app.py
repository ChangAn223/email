from view_func import db,app
from manage import manager


if __name__ == "__main__":
    db.create_all()
    manager.run()
    app.run()
