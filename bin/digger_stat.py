#encoding=utf-8
import logging
import sys
import json
from optparse import OptionParser
logging.basicConfig(format="%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
    filename='3y_cms_stats.log', level=logging.DEBUG)
adDict = {}

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
            #工具箱的module为adsdk
            if(not mdu == "adsdk"):
                continue
            child = list[2]
            tk = list[3]
            lc = list[4]
            op = str(list[5])
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
            pid = str(map['pid'])
            tid = str(map['tid'])
            if not map.has_key('key'):
                continue
            key = map['key']
            if key == 'show':
                dataArray = map['data']
                key = "\t".join([entry,pid,tid,pkg,lc,op,v])
                handleShow(key=key,groups=dataArray,tk=tk);
            elif key == "tctc":
                gid = str(map['gid'])
                id = str(map['id'])
                key = "\t".join([entry,pid,tid,pkg,lc,op,v,gid,id])
                handleClick(key, tk)
            elif key == "thi":
                handleInstall()
            elif key == "tctb" or key == "tctp":
                handleValidClick()
        saveResultAsFile(date_string,adDict,"\t".join(["#entry","pid","tid","pkg" ,"lc","op","v","showpv","showuv","clickpv","clickuv"]),"../result/showResult.log.%s" %(date_string))
        #saveResultAsFile(date_string,adDict,"\t".join(["#entry","pid","tid","gid","pkg" ,"lc","op","v","pv","uv","pv/uv"]),"../result/clickResult.log.%s" %(date_string))
    except IOError as ioe:
        print >> sys.stderr, "{0}".format(ioe)
        sys.exit(1)
    sys.exit(0)
def saveResultAsFile(date_string,dict,head,output):
    head = head.strip('\n')
    head = head + '\n'
    file = open(output,'w')
    try:
        file.write(head)
        for key,value in dict.items():
            showPv = value["showPvKey"]
            showUv = len(value['showTokenKey'])
            clickPv = value["clickPvKey"]
            clickUv = len(value['clickTokenKey'])
            file.write("%s\t%s\t%s\t%s\t%s\n" %(key,showPv,showUv,clickPv,clickUv))
    finally:
        file.close()

def incrementPVUV(dict, key, pvKey,tokenKey, token):
    if not dict.has_key(key):
        value = {pvKey: 1, tokenKey: set()}
        value[tokenKey].add(token)
        dict[key] = value
    else:
        value = dict[key]
        value[pvKey] += 1
        value[tokenKey].add(token)


#处理展示上报日志
def handleShow(key=None,groups=None,tk=None):
    basekey = key
    tokenKey = "showTokenKey"
    pvKey = "showPvKey"
    for group in groups:
        gid = group['gid']
        ids = group['ids']
        for id in ids:
            key =  "%s\t%s\t%s" %(basekey,gid,id)
            incrementPVUV(adDict,key,pvKey,tokenKey,tk)

#处理点击上报日志
def handleClick(key=None,tk=None):
    tokenKey = "clickTokenKey"
    pvKey = "clickPvKey"
    incrementPVUV(adDict,key,pvKey,tokenKey,tk)

#处理安装上报日志
def handleInstall():
    pass
#处理有效点击上报日志
def handleValidClick():
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