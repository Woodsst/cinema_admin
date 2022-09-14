import time
from functools import wraps
from src.logging_config import logger
import elasticsearch
import psycopg2


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=25):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        connect_timer = start_sleep_time

        @wraps(func)
        def inner(*args):
            nonlocal connect_timer
            while True:
                time.sleep(connect_timer)
                try:
                    func(*args)
                except psycopg2.OperationalError:
                    logger.warning(
                        f'Database connection refused, the next connection request after {connect_timer} sec')
                    connect_timer = connect_timer * 2 ** factor
                    if connect_timer > border_sleep_time:
                        connect_timer = start_sleep_time

                except psycopg2.InterfaceError:
                    logger.warning(
                        f'Database connection break, the next connection request after {connect_timer} sec')
                    connect_timer = connect_timer * 2 ** factor
                    if connect_timer > border_sleep_time:
                        connect_timer = start_sleep_time

                except elasticsearch.exceptions.ConnectionError:
                    logger.warning(
                        f'Elasticsearch connection refused, the next connection request after {connect_timer} sec')
                    connect_timer = connect_timer * 2 ** factor
                    if connect_timer > border_sleep_time:
                        connect_timer = start_sleep_time
        return inner

    return func_wrapper
