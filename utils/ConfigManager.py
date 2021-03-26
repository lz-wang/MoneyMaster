#  Copyright (c) lzwang 2020-2021, All Rights Reserved.
#  File info: ConfigManager.py in MoneyMaster (version 0.1)
#  Author: Liangzhuang Wang
#  Email: zhuangwang82@gmail.com
#  Last modified: 2021/3/26 下午10:44


import os
import yaml


class ConfigTool(object):
    def __init__(self):
        self.project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
        self.cfg_root = os.path.join(self.project_root, 'layout/config/MoneyConfig.yaml')

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
                print('read cfg SUCCESS')
                return self.cfg_maker(cfg)
        except Exception as e:
            print('read cfg Failed, REASON: %s' % e)
            return None

    def cfg_maker(self, cfg:dict):
        cfg_abs: dict = {}

        for name, items in cfg.items():
            cfg_abs[name]: dict = {}
            cfg_abs[name]['root'] = os.path.join(self.project_root, items.get('path'))
            for k, v in items.items():
                if k == 'path':
                    continue
                cfg_abs[name][k] = cfg_abs[name]['root'] + '/' + v

        return cfg_abs


if __name__ == '__main__':
    ct = ConfigTool()
    ct.run_test()
