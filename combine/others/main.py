import os
from combine import ip_utils


def find_start_and_end_idx_1(src_path: str, txt_encoding: str = 'gbk',
                             start_str: str = '的路由', start_offset: int = 2,
                             end_str: str = '结束', end_offset: int = -1):
    start_idx = []
    end_idx = []
    with open(src_path, 'r', encoding=txt_encoding) as f:
        str_list = f.readlines()
        for i, item in enumerate(str_list):

            if item.__contains__(start_str):
                start_idx.append(i + start_offset)

            if item.__contains__(end_str):
                end_idx.append(i + end_offset)

    return start_idx, end_idx


def deal_with_idxs_and_1(src_path: str, txt_encoding: str = 'gbk',
                         replace_to_space_list: list = ['\n', '[', ']'], sep_str: str = ' ',
                         start_idxs: list = [], end_idxs: list = []):
    ip_lists = []

    with open(src_path, 'r', encoding=txt_encoding) as f:
        str_list = f.readlines()
        for i in range(len(start_idxs)):
            s = start_idxs[i]
            e = end_idxs[i]
            cur_list = []
            for i in range(s, e + 1):
                line = str_list[i]

                for replace_item in replace_to_space_list:
                    line = line.replace(replace_item, sep_str)

                for item in line.split(sep_str):
                    # if ip_utils.is_ip(item) and cur_list.__contains__(item)==False:
                    # 只合并ipv4,同时对当前链路的输入保证去重
                    if ip_utils.is_ipv4(item) and cur_list.__contains__(item)==False:
                        cur_list.append(item)

            ip_lists.append(cur_list)

    print(f'总统计到的长度为: {len(ip_lists)}')
    return ip_lists


def export_ip_list(export_path: str = '', txt_encoding: str = 'gbk', ip_list: list = []):
    with open(export_path, 'w', encoding=txt_encoding) as f:
        for i, line_list in enumerate(ip_list):
            f.writelines(f'{i}\n')
            for j, item in enumerate(line_list):
                f.write(item)
                if j != len(line_list) - 1:
                    f.write('-')
            f.write('\n')


if __name__ == '__main__':
    start_list, end_list = find_start_and_end_idx_1(src_path=os.path.join('txts', '6.txt'),
                                                    # txt_encoding='gbk',
                                                    txt_encoding='utf-8',
                                                    start_str='的路由', start_offset=4,
                                                    # start_str='访问', start_offset=1,
                                                    end_str='跟踪完成', end_offset=-4)
                                            # end_str='结束', end_offset=-1)
    ip_lists = deal_with_idxs_and_1(src_path=os.path.join('txts', '6.txt'),
                                    # txt_encoding='gbk',
                                    txt_encoding='utf-8',
                                    replace_to_space_list=['\n', '[', ']'], sep_str=' ',
                                    start_idxs=start_list, end_idxs=end_list)
    export_ip_list(export_path=os.path.join('export', '6_out.txt'), ip_list=ip_lists)
