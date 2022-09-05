import time

from flask import request
from flask_restful import Resource

from online import logger


class DictResource(Resource):
    """
    词典路由
    暴露加词、删词接口，供业务方控制业务词典
    主要调用segment.add_word, segment.disable_word
    """
    def __init__(self, segment):
        self.segment = segment

    def post(self):
        """加词"""
        data = request.get_json()

        init_time = time.time()
        result = {
            'status': 'OK',
            'msg': ''
        }
        try:
            self.segment.add_word(data['word'], data['pos'], int(data['freq']))
            logger.info('add word: {}, pos: {}, freq: {}'.format(data['word'], data['pos'], data['freq']))
        except Exception as e:
            logger.exception(e)
            result['status'] = 'ERROR'
            result['msg'] = str(e)

        logger.info('result: {}, cost time: {}s'.format(result, time.time() - init_time))
        return result

    def delete(self):
        """删词"""
        data = request.get_json()

        init_time = time.time()
        result = {
            'status': 'OK',
            'msg': ''
        }
        try:
            pos = data.get('pos', '')
            self.segment.disable_word(data['word'])
            logger.info('delete word: {}, pos: {}'.format(data['word'], pos))
        except Exception as e:
            logger.exception(e)
            result['status'] = 'ERROR'
            result['msg'] = str(e)

        logger.info('result: {}, cost time: {}s'.format(result, time.time() - init_time))
        return result
