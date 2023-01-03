from dataclasses import dataclass


@dataclass
class GraphAttribute:
    diameter: float
    degree_distribution: list
    clustering: dict
    is_assortative: bool
    assortativity_cofficient: float

    def custom_dict(self):
        xAxis_data = 'xAxis_data'
        yAxis_data = 'yAxis_data'
        subtitle = 'subtitle'
        res = {xAxis_data: [], yAxis_data: []}
        for degree, cnt in enumerate(self.degree_distribution):
            if cnt == 0:
                continue

            res[xAxis_data].append(degree)
            res[yAxis_data].append(cnt)

        network_type = '同配网络' if self.is_assortative else '异配网络'

        res[subtitle] = f'网络直径为:{self.diameter},同配系数为{self.assortativity_cofficient}, 网络类型为{network_type}'

        print(res)

        return dict(res)
