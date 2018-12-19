import redis
import settings
from db.models import SESSION, TelemetryState, CustomsState, FirmInfo, UserInfo
from sqlalchemy import func
from datetime import datetime

"""
type = 0 - telemetry
type = 1 - customs
"""
REDIS = redis.StrictRedis(**settings.DATABASES['REDIS'])


def add_state(dict_to_insert, state_type=0):
    postgres = SESSION()
    dict_to_insert['received_time'] = str(datetime.now())
    cont_id = (dict_to_insert.get('cont_id')
               if state_type == 0
               else dict_to_insert.get('cont_id') + '_customs')
    try:
        REDIS.hmset(cont_id, dict_to_insert)
        REDIS.expire(cont_id, 864000)  # key expires in 15days
        if state_type == 0:
            postgres.add(TelemetryState(**dict_to_insert))
        else:
            postgres.add(CustomsState(**dict_to_insert))
            postgres.commit()
    except Exception as e:
        # logger
        postgres.rollback()
        print(e)
    finally:
        postgres.close()


def get_state(cont_id, state_type):
    postgres = SESSION()
    try:
        cont_info = REDIS.hgetall(cont_id
                                  if state_type == 0 else cont_id + '_customs')
        if cont_info == {}:
            if state_type == 0:
                cont_info = postgres.query(TelemetryState).filter(
                    TelemetryState.cont_id == cont_id,
                    TelemetryState.id == postgres.query(
                        func.max(TelemetryState.id))
                ).first()
            else:
                cont_info = postgres.query(CustomsState).filter(
                    TelemetryState.cont_id == cont_id,
                    TelemetryState.id == postgres.query(
                        func.max(TelemetryState.id))
                ).first()
            cont_info = cont_info.__dict__
            cont_info.pop('_sa_instance_state')
            cont_info.pop('id')
            cont_info['received_time'] = datetime.strptime(
                cont_info['received_time'], '%Y-%m-%d %H:%M:%S.%f')
            REDIS.hmset(cont_info['cont_id'], cont_info)
        REDIS.expire(cont_id, 864000)  # key expires in 15days
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


def check_user_permission(nickname):
    postgres = SESSION()
    permission = postgres.query(UserInfo).filter(
        UserInfo.nickname == nickname).first()
    postgres.close()
    return permission.permission

# expire( имя , время )
# rom sqlalchemy import create_engine
# from sqlalchemy.engine.url import URL
# engine  = create_engine(URL(**settings.DATABASES['POSTGRES']))
# store_dt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
