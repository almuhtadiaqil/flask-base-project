class BaseResponse(object):

    data = None
    status = 200
    message = None

    def __init__(self, data, exception, page, limit, total, status):
        self.total = total
        self.page = page
        self.limit = limit
        self.data = data
        self.message = str(exception) if exception is not None else None
        self.status = status

    def serialize(self):
        return {
            # message / status/ data
                'data':{
                    'list': self.data,
                    "total": self.total,
                    "page": self.page,
                    "limit": self.limit
                }, 
                
            'status': self.status,
            'message': self.message,
        }