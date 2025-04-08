import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory_ = None


def global_init(db_file):
    global __factory_

    if __factory_:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine_ = sa.create_engine(conn_str, echo=False)
    __factory_ = orm.sessionmaker(bind=engine_)

    from . import __canteen_models

    SqlAlchemyBase.metadata.create_all(engine_)


def create_session() -> Session:
    global __factory_
    return __factory_()
