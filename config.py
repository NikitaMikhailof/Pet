from sqlalchemy import create_engine, text

engine = create_engine(url='sqlite+pysqlite:///mydatabase', echo=True)

with engine.connect() as connection:
    result = connection.execute(statement=text("select'Hello world'"))
    print(result.scalar())