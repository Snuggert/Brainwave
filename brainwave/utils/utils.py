from datetime import datetime, timedelta

# Serialiation function to serialize any dicts or lists containing sqlalchemy
# objects. This is needed for conversion to JSON format.
def serialize_sqla(data):
    # If has to_dict this is asumed working and it is used
    if hasattr(data, 'to_dict'):
        return data.to_dict()

    if hasattr(data, '__dict__'):
        return data.__dict__

    # DateTime objects should be returned as isoformat
    if hasattr(data, 'isoformat'):
        return str(data.isoformat())

    # Items in lists are iterated over and get serialized separetly
    if isinstance(data, (list, tuple, set)):
        return [serialize_sqla(item) for item in data]

    # Dictionaries get iterated over
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = serialize_sqla(value)

        return result

    # Just hope it works
    return data


def floor_time(tm, by_minutes):
    tm = datetime.combine(datetime.today(), tm);
    tm = tm - timedelta(minutes=tm.minute % by_minutes,
                        seconds=tm.second,
                        microseconds=tm.microsecond)
    return tm.time()


def row2dict(row):
    if row == None:
        return None
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
    return d


def updatedict(dict1, dict2):
    if(dict1 == None):
        return None
    if(dict2 == None):
        return dict1
    dict1.update(dict2)
    return dict1
