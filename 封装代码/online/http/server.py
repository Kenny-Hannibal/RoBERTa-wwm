import sys

from flask import Flask
from flask_restful import Api

from online import logger
from online.http.resources.dict_resource import DictResource
from online.http.resources.hello_resource import HelloResource
from online.http.resources.pos_resource import PosResource
from online.http.resources.seg_resource import SegResource
from segment.segment import Segment


def start_server(port=8000):
    # 如果输入第1个参数，将第1个参数解析为端口号
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    # 实例化flask app
    app = Flask(__name__)
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))  # 设置ensure_ascii=False，确保接口返回的中文正常
    api = Api(app)

    # 实例化segment对象，准备传入到各个resource里面
    segment = Segment()
    resource_class_kwargs = {'segment': segment}

    # 为api添加hello路由、seg路由、pos路由、dict路由
    api.add_resource(HelloResource, '/')  # hello路由用于快速检查服务可用性
    api.add_resource(SegResource, '/seg', resource_class_kwargs=resource_class_kwargs)  # seg路由用于分词
    api.add_resource(PosResource, '/pos', resource_class_kwargs=resource_class_kwargs)  # pos路由用于词性标注
    api.add_resource(DictResource, '/dict', resource_class_kwargs=resource_class_kwargs)  # dict路由用于管理词典

    # 启动服务，设置host port
    # host='0.0.0.0'，表示外部机器可以访问，必须设置为0.0.0.0
    # threaded=False，表示我们的主程序是单线程模式，需要一个一个处理请求
    # （我们的word_graph对象不是线程安全的）
    logger.info('server starts port {}'.format(port))
    app.run(debug=False, host='0.0.0.0', port=port, threaded=False)


if __name__ == '__main__':
    start_server()
