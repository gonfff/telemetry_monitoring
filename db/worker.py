import redis
import settings
from db.models import SESSION, TelemetryState, FirmInfo, UserInfo, UserContainer
from sqlalchemy import func
from datetime import datetime

'''
Сборник методов для работы с базой
'''
REDIS = redis.StrictRedis(**settings.DATABASES['REDIS'])


def row_to_dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


def add_state(dict_to_insert):
    postgres = SESSION()
    dict_to_insert['received_time'] = str(datetime.now())
    cont_id = dict_to_insert.get('cont_id')
    try:
        REDIS.hmset(cont_id, dict_to_insert)
        REDIS.expire(cont_id, 864000)  # key expires in 10days
        postgres.add(TelemetryState(**dict_to_insert))
        postgres.commit()
    except Exception as e:
        # logger
        postgres.rollback()
        print(e)
    finally:
        postgres.close()


def get_state(cont_id):
    postgres = SESSION()
    try:
        cont_info = REDIS.hgetall(cont_id)
        if cont_info == {}:
            cont_info = postgres.query(TelemetryState).filter(
                TelemetryState.cont_id == cont_id,
                TelemetryState.id == postgres.query(
                    func.max(TelemetryState.id))
            ).first()
            cont_info['received_time'] = datetime.strptime(
                cont_info['received_time'], '%Y-%m-%d %H:%M:%S.%f')
            REDIS.hmset(cont_info['cont_id'], cont_info)
            REDIS.expire(cont_id, 864000)  # key expires in 10days
    except Exception as e:
        # logger
        postgres.rollback()
        print(e)
    finally:
        postgres.close()
        return cont_info  # mb {} or None


def add_firm(dict_to_insert):
    postgres = SESSION()
    try:
        postgres.add(FirmInfo(**dict_to_insert))
        postgres.commit()
    except Exception as e:
        # logger
        postgres.rollback()
        print(e)
    finally:
        postgres.close()


def add_user(dict_to_insert):
    postgres = SESSION()
    try:
        postgres.add(UserInfo(**dict_to_insert))
        postgres.commit()
    except Exception as e:
        # logger
        postgres.rollback()
        print(e)
    finally:
        postgres.close()


def user_permission(nickname):
    postgres = SESSION()
    permission = postgres.query(UserInfo).filter(
        UserInfo.nickname == nickname).first()
    postgres.close()
    return permission.permission


def autonotification_list():
    postgres = SESSION()
    container_list = (postgres.query(UserContainer).all())
    postgres.close()
    return container_list


def delete_from_notification(container):
    postgres = SESSION()
    postgres.query(UserContainer).filter(
        UserContainer.cont_id == container).delete()
    postgres.commit()
    postgres.close()


def add_notification(user, container):
    postgres = SESSION()
    try:
        postgres.add(UserContainer(user_id=user, cont_id=container))
        postgres.commit()
    except Exception as e:
        # logger
        postgres.rollback()
        print(e)
    finally:
        postgres.close()

# expire( имя , время )
# rom sqlalchemy import create_engine
# from sqlalchemy.engine.url import URL
# engine  = create_engine(URL(**settings.DATABASES['POSTGRES']))
# store_dt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
