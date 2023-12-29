import json
import sys
import yaml

class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

sys.stdout.write(yaml.dump(json.load(sys.stdin), sort_keys=False, Dumper=MyDumper, default_flow_style=False))
