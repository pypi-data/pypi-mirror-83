class BaseDAO:

    def toDatetime(self, datetime):
        if datetime == None: return None
        return datetime.strftime('%Y-%m-%d %H:%M:%S')

    def formatDatetime(self, dt):
        if dt == None: return None
        return dt.strftime('%Y-%m-%d %H:%M:%S')
