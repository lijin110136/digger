#encoding=utf-8
import logging
import sys
import json
import types
from optparse import OptionParser
logging.basicConfig(format="%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
    filename='3y_cms_stats.log', level=logging.DEBUG)
adDict = {}
productDict = {}
projectDict = {}
groupDict = {}
entryDict = {}

showPvKey = "showPvKey"
showTokenKey = "showTokenKey"
clickPvKey = "clickPvKey"
clickTokenKey = "clickTokenKey"
installPvKey = "installPvKey"
installTokenKey = "installTokenKey"
validClickPvKey = "validClickPvKey"
validClickTokenKey = "validClickTokenKey"
boxshowPvKey = "boxshowPvKey"
boxshowTokenKey = "boxshowTokenKey"
homevisitPvKey = "homevisitPvKey"
homevisitTokenKey = "homevisitTokenKey"
entryvisitPvKey = "entryvisitPvKey"
entryvisitTokenKey = "entryvisitTokenKey"
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
            #处理展示上报日志
            if key == 'show':
                dataArray = map['data']
                #统计入口访问工具箱日志
                key = "\t".join([pkg,lc,v,child,entry,op,pid,tid])
                incrementPVUV(entryDict,key,entryvisitPvKey,entryvisitTokenKey,tk)
                for group in dataArray:
                    gid = str(group['gid'])
                    ids = group['ids']
                    for id in ids:
                        #广告数据统计
                        id = str(id)
                        key = "\t".join([pkg,lc,v,child,entry,op,pid,tid,gid,id])
                        incrementPVUV(adDict,key,showPvKey,showTokenKey,tk)
                        #广告组数据统计
                        key = "\t".join([pkg,lc,v,child,op,pid,tid,gid])
                        incrementPVUV(groupDict,key,showPvKey,showTokenKey,tk)
                        #项目数据统计
                        key = "\t".join([pkg,lc,v,child,op,pid])
                        incrementPVUV(projectDict,key,showPvKey,showTokenKey,tk)

            #处理点击上报日志
            elif key == "tctc":
                gid = str(map['gid'])
                id = str(map['id'])
                #广告数据统计
                key = "\t".join([pkg,lc,v,child,entry,op,pid,tid,gid,id])
                incrementPVUV(adDict,key,clickPvKey,clickTokenKey,tk)
                #广告组数据统计
                key = "\t".join([pkg,lc,v,child,op,pid,tid,gid])
                incrementPVUV(groupDict,key,clickPvKey,clickTokenKey,tk)
                #项目数据统计
                key = "\t".join([pkg,lc,v,child,op,pid])
                incrementPVUV(projectDict,key,clickPvKey,clickTokenKey,tk)
                #产品数据统计
                key = "\t".join([pkg,lc,v,child,ls,op])
                incrementPVUV(productDict,key,clickPvKey,clickTokenKey,tk)
            #处理安装上报日志
            elif key == "thi":
                gid = str(map['gid'])
                id = str(map['id'])
                #广告数据统计
                key = "\t".join([pkg,lc,v,child,entry,op,pid,tid,gid,id])
                incrementPVUV(adDict,key,installPvKey,installTokenKey,tk)
                 #广告组数据统计
                key = "\t".join([pkg,lc,v,child,op,pid,tid,gid])
                incrementPVUV(groupDict,key,installPvKey,installTokenKey,tk)
                #项目数据统计
                key = "\t".join([pkg,lc,v,child,op,pid])
                incrementPVUV(projectDict,key,installPvKey,installTokenKey,tk)
                #产品数据统计
                key = "\t".join([pkg,lc,v,child,ls,op])
                incrementPVUV(productDict,key,installPvKey,installTokenKey,tk)
            #处理有效点击上报日志
            elif key == "tctb" or key == "tctp":
                gid = str(map['gid'])
                id = str(map['id'])
                #广告数据统计
                key = "\t".join([pkg,lc,v,child,entry,op,pid,tid,gid,id])
                incrementPVUV(adDict,key,validClickPvKey,validClickTokenKey,tk)
                 #广告组数据统计
                key = "\t".join([pkg,lc,v,child,op,pid,tid,gid])
                incrementPVUV(groupDict,key,validClickPvKey,validClickTokenKey,tk)
                #项目数据统计
                key = "\t".join([pkg,lc,v,child,op,pid])
                incrementPVUV(projectDict,key,validClickPvKey,validClickTokenKey,tk)
                #产品数据统计
                key = "\t".join([pkg,lc,v,child,ls,op])
                incrementPVUV(productDict,key,validClickPvKey,validClickTokenKey,tk)
            #处理工具箱访问日志
            elif key == "boxshow":
                #产品数据统计
                key = "\t".join([pkg,lc,v,child,ls,op])
                incrementPVUV(productDict,key,boxshowPvKey,boxshowTokenKey,tk)
            #处理应用首页访问日志
            elif key == "homevisit":
                #产品数据统计
                key = "\t".join([pkg,lc,v,child,ls,op])
                incrementPVUV(productDict,key,homevisitPvKey,homevisitTokenKey,tk)
        saveResultAsFile(date_string,adDict,[showPvKey, showTokenKey, clickPvKey, clickTokenKey, installPvKey, installTokenKey, validClickPvKey, validClickTokenKey],"\t".join(["#pkg","lc","v","child" ,"entry","op","pid","tid","gid","id","showpv","showuv","clickpv","clickuv","installpv","installuv","validclickpv","validclickuv"]),"../result/adPv_%s.txt" %(date_string))
        saveResultAsFile(date_string,groupDict,[showPvKey, showTokenKey, clickPvKey, clickTokenKey, installPvKey, installTokenKey, validClickPvKey, validClickTokenKey],"\t".join(["#pkg","lc","v","child" ,"op","pid","tid","gid","showpv","showuv","clickpv","clickuv","installpv","installuv","validclickpv","validclickuv"]),"../result/adGroupPv_%s.txt" %(date_string))
        saveResultAsFile(date_string,projectDict,[showPvKey, showTokenKey, clickPvKey, clickTokenKey, installPvKey, installTokenKey, validClickPvKey, validClickTokenKey],"\t".join(["#pkg","lc","v","child" ,"op","pid","showpv","showuv","clickpv","clickuv","installpv","installuv","validclickpv","validclickuv"]),"../result/projectPv_%s.txt" %(date_string))
        saveResultAsFile(date_string,productDict,[homevisitPvKey,homevisitTokenKey,boxshowPvKey, boxshowTokenKey, clickPvKey, clickTokenKey, installPvKey, installTokenKey, validClickPvKey, validClickTokenKey],"\t".join(["#pkg","lc","v","child" ,"licene","op","homevisitbpv","homevisituv","boxshowpv","boxshowuv","clickpv","clickuv","installpv","installuv","validclickpv","validclickuv"]),"../result/productPv_%s.txt" %(date_string))
        saveResultAsFile(date_string,entryDict,[entryvisitPvKey,entryvisitTokenKey],"\t".join(["#pkg","lc","v","child" ,"entry","op","pid","tid","entryvisitpv","entryvisituv"]),"../result/entryPv_%s.txt" %(date_string))
    except IOError as ioe:
        print >> sys.stderr, "{0}".format(ioe)
        sys.exit(1)
    sys.exit(0)
def saveResultAsFile(date_string,dict,columns,head,output):
    head = head.strip('\n')
    head = head + '\n'
    file = open(output,'w')
    try:
        file.write(head)
        for key,value in dict.items():
            collist = []
            for col in columns:
                colvalue = '0'
                if value.has_key(col):
                    subvalue = value[col]
                    if type(subvalue) is types.IntType:
                        colvalue = str(subvalue)
                    elif isinstance(subvalue,set):
                        colvalue = str(len(subvalue))
                    else:
                        colvalue = str(subvalue)
                collist.append(colvalue)
            file.write("%s\t%s\n" %(key,"\t".join(collist)))
    finally:
        file.close()

def incrementPVUV(dict, key, pvKey,tokenKey, token):
    if not dict.has_key(key):
        value = {pvKey: 1, tokenKey: set()}
        value[tokenKey].add(token)
        dict[key] = value
    else:
        value = dict[key]
        if not value.has_key(pvKey):
            value[pvKey] = 1
        else:
            value[pvKey] += 1
        if not value.has_key(tokenKey):
            value[tokenKey] = set([token])
        else:
            value[tokenKey].add(token)

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