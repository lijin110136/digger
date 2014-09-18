#encoding=utf-8
import logging
import sys
import json
from optparse import OptionParser
logging.basicConfig(format="%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
    filename='3y_cms_stats.log', level=logging.DEBUG)
def execute(date_string, access_log, output_dir):

    try:
        if access_log:
            fp = open(access_log, 'r')
        else:
            fp = sys.stdin
        for line in fp:
            list = line.strip('\n').split('\t')
            #list[0]格式如下：2014-09-18 11:10:14 [-7329942015814772154]- com.dianxinos.dxbh
            pkg = list[0][list[0].rfind('-')+2:]
            mdu = list[1]
            child = list[2]
            tk = list[3]
            lc = list[4]
            adsdkv = list[6]
            v = list[7]
            ts = list[8]
            ls = list[9]
            ts = list[10]
            data = list[12]
            #解析JSON数据
            map = json.loads(data)
            logid = map['logid']
            entry = map['entry']
            pid = map['pid']
            tid = map['tid']
            if not map.has_key('key'):
                continue
            key = map['key']
            if key == 'show':
                dataArray = map['data']
                handleShow(logid=logid,entry=entry,pid=pid,tid=tid,groups=dataArray,tk=tk);
            elif key == "tctc":
                handleClick()
            elif key == "thi":
                handleInstall()

    except IOError as ioe:
        print >> sys.stderr, "{0}".format(ioe)
        sys.exit(1)
    sys.exit(0)
#处理展示上报日志
def handleShow(logid=None,entry=None,pid=None,tid=None,groups=None,tk=None):
    for group in groups:
        ids = group['ids']
        for id in ids:
            print id
    pass
#处理点击上报日志
def handleClick():
    pass
#处理安装上报日志
def handleInstall():
    pass

def main():
    usage_str = "usage: %prog [options] date [access_log]"
    version_str = "%prog 1.0.0"
    parser = OptionParser(usage=usage_str, version=version_str)
    parser.add_option("-o", "--output", dest="output", default="result/", type="string",
        help="set output directory")
    (options, args) = parser.parse_args()
    nargs = len(args)
    if nargs < 1 or nargs > 2:
        parser.error("incorrect number of arguments")
        sys.exit(1)
    date = args[0]
    access_log = None
    if nargs > 1:
        access_log = args[1]
    execute(date, access_log, options.output)

if __name__ == '__main__':
    main()