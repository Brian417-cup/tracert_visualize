from tracert import exe_runner
from tracert import constants
import os


class MyTracerter:
    def __init__(self,
                 encoding: str,
                 type: exe_runner.ExeProcessType,
                 tracert_websites: list,
                 is_ipv4: bool,
                 export_path_base: str):
        self.encoding = encoding
        self.type = type
        self.tracert_websites = tracert_websites
        self.export_base = export_path_base
        self.tracert_cmd = 'tracert'
        self.ip_type = '-4' if is_ipv4 else '-6'

    def run(self):
        for i, item in enumerate(self.tracert_websites):
            exe_runner.CustomExeProcessor(threadID=i,
                                          name=f'tracert {item}',
                                          argv=[self.tracert_cmd, self.ip_type, item],
                                          encoding=self.encoding,
                                          type=self.type,
                                          export=os.path.join(self.export_base, f'tracert_{item}_export.txt'),
                                          parallel=True
                                          ).execute()
