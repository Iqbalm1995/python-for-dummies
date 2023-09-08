class ResponseModel:
    def __init__(self, status_code, message, count, count_total, data):
        self.status_code = status_code
        self.message = message
        self.count = count
        self.count_total = count_total
        self.data = data

    def to_dict(self):
        return {
            'statusCode': self.status_code,
            'message': self.message,
            'count': self.count,
            'countTotal': self.count_total,
            'data': self.data
        }
