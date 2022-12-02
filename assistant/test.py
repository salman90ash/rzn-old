from assistant.settings import API_TG_TOKEN

def token_verification():
    global API_TG_TOKEN
    def decorator(func):
        def wrapper(*args, **kwargs):
            if API_TG_TOKEN == kwargs['token']:
                return func(*args, **kwargs)
            return False

        return wrapper

    return decorator


@token_verification()
def sum(token, chat_id):
    return token


print(sum(token='znxNeJXS5xPnK2rAcx_hW:8jcQSqBbU3yGay4rFWaB:BIS', chat_id=321))

# def sum(*args, **kwargs):
#     res = 0
#     for number in args:
#         res += number
#     return res
#
#
# print(sum(1, 2))
