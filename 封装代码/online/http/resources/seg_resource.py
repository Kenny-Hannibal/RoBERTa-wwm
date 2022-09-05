import json
import time

from flask import request
from flask_restful import Resource

from online import logger


class SegResource(Resource):
    """
    分词路由
    主要调用segment.seg
    """
    def __init__(self, segment):
        # 使用传过来的segment对象，进行后面的分词
        self.segment = segment

    def post(self):
        data = request.get_json()  # 解析输入json为一个dict

        init_time = time.time()
        result = {
            'status': 'OK',  # 本次请求返回状态
            'msg': ''  # 额外说明
        }

        request_id = data.get('request_id')  # 支持传入request_id，便于线上追踪请求

        try:
            assert data, "请确保输入不为空"

            # 从data取用户输入的各种参数
            content, model, enable_offset, enable_stop_word, use_ner = \
                data['content'], data.get('model'), data.get('enable_offset', False), \
                data.get('enable_stop_word', False), data.get('use_ner', False)
            logger.info('request_id: {}, model: {}, enable_offset: {}, enable_stop_word: {}, use_ner: {}, '
                        'content: {} ...'.format(request_id, model, enable_offset, enable_stop_word, use_ner,
                                                 content[:100]))

            # 调用segment对象的seg方法
            r = self.segment.seg(content, model=model, enable_offset=enable_offset,
                                 enable_stop_word=enable_stop_word, use_ner=use_ner)
            result['result'] = list(r)  # 将分词结果存放在result里面

        except Exception as e:
            # 出现异常，打印异常栈，更改本次请求状态为ERROR
            logger.exception(e)
            result['status'] = 'ERROR'
            result['msg'] = str(e)

        logger.info('request_id: {}, result: {} ..., cost time: {}s'.format(
            request_id, json.dumps(result, ensure_ascii=False)[:200], time.time() - init_time)
        )

        return result
