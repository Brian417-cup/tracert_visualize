import os
from tracert import exe_runner, constants
from tracert.my_tracerter import MyTracerter

'''
生成在constants.websites中网站列表的所有结果，放置在'./tracert_out_txts/'中
'''
if __name__ == '__main__':
    my_tracerter = MyTracerter(encoding='gbk',
                               type=exe_runner.ExeProcessType.EXPORT,
                               tracert_websites=constants.websites,
                               is_ipv4=True,
                               export_path_base=os.path.join(os.path.curdir, 'tracert_out_txts'))

    my_tracerter.run()
