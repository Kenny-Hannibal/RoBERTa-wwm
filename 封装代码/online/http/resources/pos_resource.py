import json
import time

from flask import request
from flask_restful import Resource

from online import logger


class PosResource(Resource):
    """
    词性路由
    主要调用segment.pos
    """
    def __init__(self, segment):
        self.segment = segment

    def post(self):
        data = request.get_json()

        init_time = time.time()
        result = {
            'status': 'OK',
            'msg': ''
        }

        request_id = data.get('request_id')
        try:
            content, model, enable_offset, enable_stop_word, use_ner = \
                data['content'], data.get('model'), data.get('enable_offset', False), \
                data.get('enable_stop_word', False), data.get('use_ner', False)
            logger.info('request_id: {}, model: {}, enable_offset: {}, enable_stop_word: {}, use_ner: {}, '
                        'content: {} ...'.format(request_id, model, enable_offset, enable_stop_word, use_ner,
                                                 content[:100]))
            r = self.segment.pos(data['content'], model=model, enable_offset=enable_offset,
                                 enable_stop_word=enable_stop_word, use_ner=use_ner)
            result['result'] = list(r)
        except Exception as e:
            logger.exception(e)
            result['status'] = 'ERROR'
            result['msg'] = str(e)
        logger.info('request_id: {}, result: {} ..., cost time: {}s'.format(
            request_id, json.dumps(result, ensure_ascii=False)[:200], time.time() - init_time)
        )

        return result
