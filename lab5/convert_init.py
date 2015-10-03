from configparser import ConfigParser
from collections import OrderedDict
import yaml
import argparse


class MyParser(ConfigParser):
    def as_dict(self):
        d = OrderedDict(self._sections)
        for k in d:
            d[k] = OrderedDict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d
    optionxform = str


parser = argparse.ArgumentParser()
parser.add_argument('ini_file',type=str,help='init file name')
parser.add_argument('yaml_file',type=str,help='yaml file name')
args=parser.parse_args()

    
Config = MyParser()
Config.read(args.ini_file)
run1=Config.as_dict()
test=OrderedDict()
for section in Config.sections():
    test[section]=OrderedDict()
    for key,value in Config[section].items():
        test[section][key]=float(value)

def represent_ordereddict(dumper, data):
    value = []
    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        value.append((node_key, node_value))
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.add_representer(OrderedDict, represent_ordereddict)

with open(args.yaml_file,'w') as f:
    out=yaml.dump(test,f)

