import os
import sys
import unittest

sys.path.append('.')  # 项目根目录

from HTMLTestRunner import HTMLTestRunner


def run_all_test_cases():
    status = 0
    ori_path = os.getcwd()
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().discover('./tests/unit_tests/'))
    with open('TestReport.html', 'w') as f:
        runner = HTMLTestRunner(stream=f, title='Test Report', verbosity=2)
        result = runner.run(suite)
        if result.failure_count or result.error_count:
            status = 1

    os.chdir(ori_path)
    return status


if __name__ == '__main__':
    if run_all_test_cases():
        sys.exit(1)
