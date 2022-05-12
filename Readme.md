### To create the database (delete old, if exists)-

- Open python interpreter
- from main import db
- db.session.create_all()
- from main import City
- mum=City(city_name='Mumbai')
- db.session.add(mum)
- db.session.commit()