from datetime import datetime


def bot_logger(func):
    def log_func(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('vk_bot/bot_log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.today()} {func.__name__} ответ: {result[0]} user_id: {result[1]}\n')
        return result
    return log_func