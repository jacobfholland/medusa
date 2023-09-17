from datetime import date, datetime, time


def serializer(obj):
    if isinstance(obj, (datetime, date, time)):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
    raise TypeError(f"Type {type(obj)} not serializable")
