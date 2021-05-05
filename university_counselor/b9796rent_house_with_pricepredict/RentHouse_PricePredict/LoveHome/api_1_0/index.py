# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'


from . import api
from LoveHome import redis_store
import logging

@api.route('/index', methods=['get', 'post'])
def index():
    # redis_store.set('name', 'laowang')
    logging.warn('WARN LOG')
    logging.error('ERROR LOG')
    logging.info('INFO LOG')
    logging.debug('DEBUG LOG')
    logging.fatal('FATAL LOG')
    return 'index222'

