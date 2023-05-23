class BaseResponseSingle(object):

    data = None
    status = 200
    message = None

    def __init__(self, data, exception, status):
        self.data = data
        self.message = str(exception) if exception is not None else None
        self.status = status

    def serialize(self):
        return {
            # message / status/ data
            'data':self.data, 
            'status': self.status,
            'message': self.message,
        }