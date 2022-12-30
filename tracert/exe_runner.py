import subprocess
import threading
from enum import Enum
import os
import os.path


# exe输出结果的处理方法
class ExeProcessType(Enum):
    # 输出结果直接打印到显示屏上
    PRINT = -1,
    # 支持txt的保存
    EXPORT = -2,
    OTHERS = -3


class CustomExeProcessor(threading.Thread):
    def __init__(self,
                 # 线程ID
                 threadID,
                 # 线程名
                 name,
                 # 可执行文件的完整路径名,如果为''则表示为调用系统的终端
                 exepPath='',
                 # 传入的参数,程序会自动用空格隔开
                 argv=[],
                 # 输出的方式
                 type=ExeProcessType.PRINT,
                 # 如果输出方式为文件，那么这里需要指定输出文件名和完整路径
                 export='',
                 # 输出的编码方式
                 encoding='utf-8',
                 # 这里默认选择和主线程并行，也可以设置成串行的工作方式
                 parallel=True):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.exePath = exepPath
        self.argv = argv
        self.type = type
        self.export = export
        self.parallel = parallel
        self.encoding = encoding

    def _getCMD(self):
        self.cmd = self.exePath
        for item in self.argv:
            self.cmd = self.cmd + ' ' + item

    def _dealPipeData(self, input):
        if input.endswith(b'\r\n'):
            input = input[0:len(input) - 2]
        elif input.endswith(b'\n'):
            input = input[0:len(input) - 1]
        return str(input, encoding=self.encoding)

    def run(self):
        super().run()

        # 拼接成指令
        self._getCMD()
        print(self.cmd)

        # 处理输入输出结果
        with subprocess.Popen(self.cmd, shell=True,
                              stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE) as pipe:
            pipe_out = pipe.stdout
            pipe_err = pipe.stderr
            pipe_in = pipe.stdin

            if self.type == ExeProcessType.PRINT:
                print('输出数据\n\n')
                out_data = pipe_out.readline()

                while len(out_data) != 0:
                    out_str = self._dealPipeData(out_data)
                    print(out_str)
                    out_data = pipe_out.readline()

                print('缓冲错误数据\n\n')
                err_data = pipe_err.readline()

                while len(err_data) != 0:
                    err_str = self._dealPipeData(err_data)
                    print(err_str)
                    err_data = pipe_err.readline()

            elif self.type == ExeProcessType.EXPORT:
                # if os.path.isfile(self.export) == False:
                #     print('请输入完整正确的保存路径和txt文件名称')
                #     return

                with open(self.export, 'w', encoding=self.encoding) as file:
                    file.writelines('输出数据\n\n')
                    out_data = pipe_out.readline()
                    while len(out_data) != 0:
                        out_str = self._dealPipeData(out_data)
                        file.writelines(out_str + '\n')
                        out_data = pipe_out.readline()

                    file.writelines('\n\n缓冲错误数据\n\n')
                    err_data = pipe_err.readline()
                    while len(err_data) != 0:
                        err_str = self._dealPipeData(err_data)
                        file.writelines(err_str + '\n')
                        err_data = pipe_err.readline()

                    print('输出结果已成功保存至 {0} 中'.format(self.export))
            else:
                print('写下自定义的处理方法')

    # 总结:线程中start和run的差别--https://www.jb51.net/article/185920.htm
    # run() 方法并不启动一个新线程，就是在主线程中调用了一个普通函数而已。
    # start() 方法是启动一个子线程，线程名就是自己定义的name。
    # 因此，如果你想启动多线程，就必须使用start()方法。
    # 采用异步执行
    def execute(self):
        if self.parallel:
            self.start()
        else:
            self.run()


# 总结:调用exe的三种方法
# 第一种:os.system  串行
# os.system("f:/test.exe 1 2")
#   for i in range(1,1000000):
#     print('ok')

# 第二种:os.popen (利用了管道) 并行
# exe_path='f:/test 1 256'
# f=os.popen(exe_path)
#
# file=open('f:/export.txt','w')
#
# data=f.readline()
# while (len(data)!=0):
#     if '\n' in data:
#         data=data[0:len(data)-1]
#     print(data)
#     file.writelines(data+'\n')
#     data=f.readline()
#
# f.close()
# file.close()

# 第三种:subprocess.Popen 对上面两种的结合(官方推荐用这种方法)
# 可并行也可串行  自定义类选择的就是这个例子，默认采用管道道中按行读取
# pipe=subprocess.Popen('f:/test.exe 1005 2',shell=True,stdout=subprocess.PIPE)
# pipe_out=pipe.stdout
# pipe_error=pipe.stderr
# out_data=pipe_out.readline()
# while (len(out_data) != 0):
#     if out_data.endswith(b'\r\n'):
#         out_data=out_data[0:len(out_data)-2]
#     elif out_data.endswith(b'\n'):
#         out_data=out_data[0:len(out_data)-1]
#
#     print(str(out_data,encoding='utf-8'))
#     print(len(out_data))
#     out_data=pipe_out.readline()

# 并行测试
if __name__ == '__main__':
    exeThread = CustomExeProcessor(threadID=1, name='tracert使用',
                                   argv=['tracert', 'www.baidu.com'],
                                   encoding='gbk',
                                   type=ExeProcessType.EXPORT,
                                   export=os.path.join(os.curdir, 'out.txt'),
                                   parallel=True)
    exeThread.execute()
