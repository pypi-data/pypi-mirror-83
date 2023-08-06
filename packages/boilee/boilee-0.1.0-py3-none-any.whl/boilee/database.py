from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Path(Base):
    __tablename__ = "paths"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    content = Column(String)
    is_directory = Column(Boolean)


class Database:
    def __init__(self, directory):
        self.database = f"sqlite:///{directory}/database.sqlite"
        engine = create_engine(self.database, echo=True)

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def commit(self):
        self.session.commit()

    def add_path(self, path, content, is_directory):
        new_path = Path(path, content, is_directory)
        self.session.add(new_path)
