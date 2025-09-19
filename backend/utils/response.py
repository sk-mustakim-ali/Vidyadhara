def success(data, code=200):
    return {'status': 'success', 'data': data, 'code': code}

def error(message, code=400):
    return {'status': 'error', 'message': message, 'code': code}
