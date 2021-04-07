#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: ConfigManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/4/7 下午10:30

import os
import yaml
from utils.LogManager import MoenyLogger

CFG_YAML = 'layout/config/MoneyConfig.yaml'
ROOT_KEY = 'MoneyMaster'


class ConfigTool(object):
    def __init__(self):
        self.log = MoenyLogger().logger
        self.project_root = self.find_project_root()
        self.cfg_root = os.path.join(self.project_root, CFG_YAML)

    @staticmethod
    def find_project_root():
        cwd = os.path.abspath(os.getcwd())
        if os.name == 'posix':
            a = cwd.split('/')
            for idx, word in enumerate(a[::-1]):
                if word == ROOT_KEY:
                    a = a[:-idx]
                    break
            return '/'.join(a)

    def run_test(self):
        cfg = self.cfg_reader()
        print('123')

    def cfg_reader(self, cfg_yaml=None):
        if cfg_yaml is not None:
            self.cfg_root = cfg_yaml

        try:
            with open(self.cfg_root, 'r') as f:
                yaml_str = f.read()
                cfg = yaml.safe_load(yaml_str)
                self.log.info('read cfg SUCCESS')
                return self.cfg_maker(cfg)
        except Exception as e:
            self.log.exception('read cfg Failed, REASON: %s' % e)
            return None

    def cfg_maker(self, cfg: dict):
        cfg_paths: dict = {}
        cfg_names: dict = {}

        for key, items in cfg.items():
            if items.get('path'):
                cfg_paths[key]: dict = {}
                cfg_paths[key]['root'] = os.path.join(self.project_root, items.get('path'))
                for k, v in items.items():
                    if k == 'path':
                        continue
                    cfg_paths[key][k] = cfg_paths[key]['root'] + '/' + v
            if items.get('names'):
                cfg_names[key]: dict = {}
                for _, all_names in items.items():
                    for k, v in all_names.items():
                        cfg_names[key][k] = v

        return {'paths': cfg_paths, 'names': cfg_names}


if __name__ == '__main__':
    ct = ConfigTool()
    ct.run_test()
