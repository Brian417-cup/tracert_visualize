import glob
import os
from combine import ip_utils


# 每个文件操作
def get_all_routes_from_txts(base_path: str, encoding: str, need_combine_and_out=False):
    # 用键值对维护最终的每个路径
    result = dict()

    for item in glob.glob(os.path.join(base_path, '*.txt')):
        cur_routes = []
        # print(item)
        with open(item, mode='r', encoding=encoding) as f:
            data = f.readlines()
            # print(data)
            s, e = find_start_and_end_in_tracert(data)
            print(f'{s}  {e}')
            data = data[s:e + 1]
            # 每行判断
            for sentence in data:
                # 每行中以空格隔断，提取其中的ipv4地址
                small_patterns = sentence.split(' ')
                for ip_candidate in small_patterns:
                    # 因为tracert的时候规定了只有ipv4地址，因此这里只需要判断ipv4
                    # 当然这里还要考虑到最后整合的时候其他人的结果是有ipv6的可能
                    # if ip_utils.is_ipv4(ip_candidate) and cur_routes.count(ip_candidate) == 0:
                    if ip_utils.is_ip(ip_candidate) and cur_routes.count(ip_candidate) == 0:
                        cur_routes.append(ip_candidate)
                        break

            result[os.path.basename(item)] = cur_routes

    print(result)

    if need_combine_and_out:
        with open('my_result.txt', mode='w', encoding=encoding) as f:
            for key in result:
                f.writelines(f'{key}\n')
                cur_values = result[key]
                for i, value in enumerate(cur_values):
                    f.write(value)

                    if i != len(cur_values) - 1:
                        f.write('-')
                f.write('\n')

    return result


# 找到开始记录的第一个路由下标
def find_start_and_end_in_tracert(data: list):
    sr = '通过最多 30 个跃点跟踪\n'
    er = '跟踪完成。\n'

    s, e = data.index(sr) + 3, data.index(er) - 2
    return s, e


'''
对./tracert/main.py中提取到的30个tracert文件,进行合并，最终提取出各个链路的ip在out.txt中
'''
if __name__ == '__main__':
    get_all_routes_from_txts(base_path=os.path.join('..', 'tracert', 'tracert_out_txts'),
                             encoding='gbk',
                             need_combine_and_out=True
                             )
