import requests
import logging
import json
from pymongo import MongoClient
import pandas as pd
from CTsystem2 import settings


client = MongoClient(host=settings.MONGOENGINE['HOST'], port=settings.MONGOENGINE['PORT'])
database = client['CTsystem']
logger = logging.getLogger()
logger.setLevel('DEBUG')
BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()
chlr.setFormatter(formatter)
chlr.setLevel('INFO')
logger.addHandler(chlr)
certificate_collection = database['certificate']


def get_user_info(cecid):
    response = requests.get('https://orgstats.cisco.com/api/1/entries?users=' + cecid)
    message = eval(response.text)
    collection = database['user_info']
    result = list(collection.find({"cecid": cecid}, {"_id": 0}))
    if message:
        firstname = message[0]['N']
        departid = message[0]['O']
        employid = message[0]['i']
        active = message[0]['a']
        if 'r' in message[0]:
            subordinate = message[0]['r']
        else:
            subordinate = []
        if active == 1:
            active = "true"
        else:
            active = "false"
        title = message[0]['t']
        manager = message[0]['m']
        organazation = message[0]['o']
        if 'C' in message[0]:
            country = message[0]['C']
        else:
            country = ""
        if 's' in message[0]:
            site = message[0]['s']
        else:
            site = ""
        badge = ''
        if 'R' in message[0]:
            badge = 'regular_employee'
        elif 'T' in message[0]:
            badge = 'temp_employee'
        elif 'V' in message[0]:
            badge = 'vendor'
        dic = {
            'cecid': cecid,
            'name': firstname,
            'gender': "",
            'title': title,
            'manager': manager,
            'subordinate': subordinate,
            'departid': departid,
            'employid': employid,
            'organazation': organazation,
            'badge': badge,
            'site': site,
            'country': country,
            'active': active,
        }
        if not result:
            collection.insert_one(dic)
            logger.info("insert %s message" % cecid)
        else:
            collection.update_one({"cecid": cecid}, {"$set": dic})
            logger.info("update %s message" % cecid)
    else:
        if result:
            collection.update_one({"cecid": cecid}, {"$set": {"active": "false"}})


def get_user_info_simple(cecid):
    response = requests.get('https://orgstats.cisco.com/api/1/entries?users=' + cecid)
    message = eval(response.text)
    collection = database['user_info']
    result = list(collection.find({"cecid": cecid}, {"_id": 0}))
    if not result:
        if message:
            firstname = message[0]['N']
            departid = message[0]['O']
            employid = message[0]['i']
            active = message[0]['a']
            if 'r' in message[0]:
                subordinate = message[0]['r']
            else:
                subordinate = []
            if active == 1:
                active = "true"
            else:
                active = "false"
            title = message[0]['t']
            manager = message[0]['m']
            organazation = message[0]['o']
            if 'C' in message[0]:
                country = message[0]['C']
            else:
                country = ""
            if 's' in message[0]:
                site = message[0]['s']
            else:
                site = ""
            badge = ''
            if 'R' in message[0]:
                badge = 'regular_employee'
            elif 'T' in message[0]:
                badge = 'temp_employee'
            elif 'V' in message[0]:
                badge = 'vendor'
            dic = {
                'cecid': cecid,
                'name': firstname,
                'gender': "",
                'title': title,
                'manager': manager,
                'subordinate': subordinate,
                'departid': departid,
                'employid': employid,
                'organazation': organazation,
                'badge': badge,
                'site': site,
                'country': country,
                'active': active,
            }
            collection.insert_one(dic)
            logger.info("insert %s message" % cecid)
        else:
            dic = {}
            logger.info("no such name")
    else:
        dic = list(collection.find({"cecid": cecid, 'active': "true"}, {"_id": 0}))[0]

    return dic


def getReportline(cecid):
    c = 0
    init = [cecid]
    while c in range(0, len(init)):
        sublist = get_user_info_simple(init[c]).get('subordinate')
        lst = sublist
        for i in lst:
            if i not in init:
                init.append(i)
                logger.info("%s in the list" % i)
        c += 1

    return {
        cecid: init,
        'total_count': len(init)
    }


def getBadge(reportline):
    bluebadge_count = 0
    redbadge_count = 0
    user_collection = database['user_info']
    for i in reportline:
        a = list(user_collection.find({'cecid': i, 'active': 'true'}, {'_id': 0, 'badge': 1}))[0]
        if a.get('badge') in ['temp_employee', 'vendor']:
            redbadge_count += 1
        else:
            bluebadge_count += 1
    return dict(bluebadge_count=bluebadge_count, redbadge_count=redbadge_count)


if __name__ == "__main__":
    dic = {
        'hwen': ['hwen', 'geoukim', 'daviyan', 'wangxun', 'nzhang', 'xiaoma', 'yiling', 'eddlee', 'yiwang4', 'xinpxu',
                 'guoxli', 'rochi', 'mima2', 'rohao', 'xueshao', 'xuezhu', 'mecai', 'donan', 'sarzheng', 'shengch',
                 'vyao', 'jiawa2', 'gavlam', 'shlin2', 'erixiao', 'shdai', 'xizha2', 'mingjjia', 'xinzha2', 'yukli',
                 'wunyang', 'xuejzhao', 'wli6', 'zhecao', 'tuliu', 'kuiliu', 'liangwa3', 'zhigfang', 'qiulv', 'cshiyou',
                 'kanw', 'icwang', 'hansu', 'hongftan', 'cniu', 'xilowang', 'nicge', 'chejiao', 'shenlu', 'chwang2',
                 'jaroyu', 'zhenghua', 'wzhigang', 'pinxu', 'yukkimur', 'qianjun', 'hancai', 'sunnliu', 'liwan3',
                 'fayawang', 'zixu', 'terwu', 'natezhan', 'fechao', 'yuyu3', 'qingzhan', 'roncheng', 'zuxiao', 'fangni',
                 'kaifen', 'pengpche', 'yonyi', 'fmo', 'zhangwan', 'lintlin', 'jimmjin', 'zhihli', 'crhe', 'jianli5',
                 'weilv', 'changxyu', 'peisun', 'jialliu', 'jinfzhan', 'xiuzhao', 'kingjin', 'haifwang', 'yusuda',
                 'lichu', 'fpavlovi', 'foxwang', 'jisun3', 'chaoyzha', 'yufeng', 'ninliang', 'jizhang3', 'xiangjin',
                 'tiajin', 'rongzli', 'haimjian', 'hongkjin', 'yijin2', 'lianl', 'wenfwu', 'duzjiang', 'jiangjin',
                 'minhjin', 'yinzshen', 'mingzli', 'lonjiang', 'jinglwu', 'meilzhao', 'xigjin', 'zhenlli', 'jingccui',
                 'yunfcui', 'dinbai', 'wenhali', 'fejin2', 'yanji2', 'zhenglia', 'xianljin', 'hecui', 'yuxshi',
                 'memeng', 'quachi', 'chenjia', 'yangta', 'hanso', 'pingch', 'zhuhjian', 'weiswang', 'zhecui',
                 'haifeli', 'fguo2', 'anyfan', 'zihxu', 'haorzhao', 'dongzwan', 'yinghjin', 'xiaoqiz', 'xuetilv',
                 'meilsong', 'xixu3', 'zuowang', 'yunjzhao', 'zhuali', 'yusxiao', 'xupeng', 'qutan', 'yinba', 'chundli',
                 'linlinwa', 'hajia', 'zhahong', 'hasun2', 'xubai', 'mingzeng', 'haiszhan', 'zhiwqin', 'haozhan3',
                 'xiaomshi', 'fengwguo', 'dawchu', 'jiaweiwa', 'jzhang5', 'chunylu', 'zhutian', 'mengxlia', 'lingywu',
                 'yanjli', 'shaswang', 'bhaiyan', 'shiszhan', 'lyzhang', 'diwa2', 'pfei', 'sishao', 'weinacha',
                 'janlian', 'puwang', 'xudzheng', 'xintsong', 'haifzhan', 'hainzhao', 'owzhang', 'wupiao', 'mannwang',
                 'xxin2', 'xiaowwa2', 'yixxing', 'txiong', 'cwan2', 'hawu3', 'juwang4', 'siyhan', 'manchen', 'xiaotzha',
                 'lingljia', 'yawzhu', 'linlren', 'yuewang4', 'xiju', 'tazheng', 'junzhe', 'qianzha3', 'haoslian',
                 'yuazhan3', 'yonglizh', 'xiaogfen', 'ykai', 'xiaoshwa', 'qiyu2', 'xiya2', 'duozhang', 'yaohuan',
                 'jinycui', 'tinqiu', 'hailmao', 'xiaoyash', 'yirshi', 'yingj', 'socui', 'qingyuzh', 'yuxwu',
                 'yonghjia', 'yongxjin', 'liyxuan', 'yuanzhzh', 'qiya', 'huijjin', 'jiel5', 'jial5', 'yingnxu',
                 'wenlzhao', 'hanwzhao', 'borzheng', 'minpiao', 'huali5', 'bchen3', 'jixqu', 'jingyu3', 'memiao',
                 'xintonwa', 'mengtyan', 'yixing2', 'xiaoli4', 'rejin', 'linchen2', 'nsugawar', 'guangy', 'lohe',
                 'evyi', 'haiyanx', 'shpiao', 'lil6', 'wensha', 'yuanstan', 'yanzhen2', 'yancao2', 'chanwan2',
                 'meilijin', 'ningjxu', 'huany', 'toseto', 'yuecui', 'jienzhan', 'dandsong', 'danso', 'xiaol3',
                 'jianl5', 'micui', 'ruirliu', 'yinrjin', 'xiaoh', 'xujzhao', 'yilli', 'weitli', 'xiaolguo', 'qingjin',
                 'takkawam', 'yaxian', 'hozhao2', 'zunwang', 'yinghqi', 'xinliu4', 'zhmengya', 'mingzesu', 'alechen2',
                 'yajiang2', 'zijliu', 'xueshan', 'jingjiwa', 'lighao', 'yutshan', 'kecui', 'yonglv', 'jinlizhu',
                 'miahe', 'yifshi', 'weyi', 'xianxjin', 'xinjchen', 'jiaxzhao', 'jianpenz', 'wenwan2', 'hualyu',
                 'tianmyan', 'xinmeng', 'xiaocson', 'peiwu2', 'zhihxu', 'yaqsong', 'yiywang', 'xixia', 'xuz2',
                 'qianluo', 'frfeng', 'nindai', 'jiabwei', 'ningyxu', 'elazhang', 'kryin', 'shuawan2', 'bellwang',
                 'xiangyl2', 'rliu3', 'xiawe', 'tianxie', 'yucjiao', 'chaoya2', 'fenfliu', 'luwa2', 'rosfeng', 'cran',
                 'jlu4', 'miaow', 'caicai', 'marksun', 'lawli', 'viclin', 'hualiu3', 'meiyujia', 'leihan', 'suzliu',
                 'leilsun', 'yingjliu', 'sijzheng', 'yanch4', 'haoli3', 'chudu', 'husxu', 'louiliu', 'sihli', 'tingke',
                 'johnsun', 'mariwen', 'honpiao', 'yingytan', 'qinshen', 'ninsun', 'xiaobawa', 'siysun', 'yil8',
                 'jilu4', 'yazhao4', 'enyliu', 'ailchen', 'qao', 'ivali', 'daiszhan', 'dongmli', 'jingyul', 'beiyu',
                 'rinsu', 'zhilowan', 'sunnwang', 'lupzhu', 'xmi', 'xiaoygao', 'minghli', 'chenli3', 'haozhe',
                 'yifeiwa', 'danlv', 'hongliw', 'shasjian', 'ninlan', 'yuexi', 'shijiliu', 'yingliu5', 'zhonjian',
                 'yingfen', 'jli7', 'lliu5', 'jiaqfang', 'yanjxie', 'xianyli', 'zhazhong', 'jiaqiu', 'xiangw',
                 'weilchen', 'jimiliu', 'shcheng2', 'guyan', 'shlan', 'jiawewan', 'jianzha4', 'qiqguo', 'yulidai',
                 'kaiyua', 'feihliu', 'weihlin', 'xiche4', 'qiz3', 'jiangazh', 'fengjia', 'tingluo', 'jingyan3',
                 'xinyache', 'guanlliu', 'megsun', 'chlv', 'pinan', 'xiaodizh', 'linhfeng', 'manyua', 'lomu', 'jianxma',
                 'fengsh', 'jinlliu', 'hongyli2', 'jonzhou', 'xucu', 'hangyliu', 'songlli', 'guaqu', 'xiama2', 'zhli4',
                 'kevifan', 'chunliwa', 'lequ', 'mingzwu', 'jushao', 'ninding', 'chubshan', 'chulian', 'yihli', 'xuqli',
                 'decong', 'zhihuich', 'kaiguo', 'yeyua2', 'cma2', 'yongz2', 'leizho2', 'jiman', 'qizchen', 'hongyi',
                 'puzha', 'chengrfa', 'xianshen', 'mingyan2', 'zhicfeng', 'zimingw', 'shoujche', 'hobai', 'xiaolis',
                 'xiangmen', 'caiswang', 'yukwang', 'chshang', 'jiaqfeng', 'frjin', 'taosun2', 'huanwa2', 'zidzhao',
                 'yangli4', 'yanswang', 'xinychen', 'nanwe', 'yanqwang', 'mingjiga', 'guama', 'chaoz2', 'jiabu',
                 'hongysun', 'yibinzha', 'xuasong', 'fushuang', 'zhibowan', 'dinwang', 'cnao', 'jiangygu', 'yizhou3',
                 'ningzh', 'hejyang', 'siyxiao', 'pebao', 'siniu', 'hongan', 'kaiji', 'niwang2', 'bowji', 'shengbiy',
                 'songwa', 'shlei', 'tzhai', 'weidhuan', 'huaizhao', 'xisun2', 'xiangyuz', 'ailinwan', 'pli3',
                 'xiaoyugu', 'dawang', 'chenhwan', 'qianlu', 'lchuan', 'jiayingw', 'hanl2', 'fucchen', 'siytang',
                 'yondong', 'yangzho2', 'yuxuliu', 'zhenguo', 'dawzhou', 'yanlsun', 'qifawu', 'gyu2', 'didi2',
                 'jingliu4', 'xinzh3', 'xiaofsun', 'jiewen', 'xuefejin', 'yuljin', 'jiedeng', 'wepiao', 'mige', 'bijin',
                 'baoyin', 'yudliu', 'minghaol', 'qiuxia', 'ninwang2', 'yuanhluo', 'jingjjin', 'chunjwu', 'szong',
                 'xincizha', 'donwang2', 'taijjin', 'zhekang', 'yiding2', 'qyong', 'chosong', 'yuancli', 'chengson',
                 'kaijiang', 'weiyji', 'yangliu4', 'linxu3', 'xuefyang', 'yuhon', 'yueqin', 'zhanqing', 'lilqi',
                 'huangao', 'zhengyl3', 'yiqzeng', 'haiypiao', 'yipguo', 'yiyma', 'yumewang', 'carche', 'xiaojguo',
                 'enbzhou', 'nayan', 'nanwang2', 'fusong', 'qinghan', 'yinan', 'yutdong', 'dongl2', 'xiaokawa',
                 'guanghan', 'shiyliu', 'rcong', 'chenche3', 'meihjin', 'jinzhan5', 'yangwan4', 'yma3', 'ruizhan3',
                 'jinghozh', 'minghzha', 'koyong', 'oqiu', 'wepeng', 'charlizh', 'aleli', 'maju', 'qiangche', 'chencai',
                 'vijavenu', 'deyli', 'frankwon', 'jinri', 'qihlu', 'pelong', 'honglsun', 'hacai', 'zyunpeng', 'gayou',
                 'weichi', 'qimiao', 'necarino', 'xianl3', 'zhzhou2', 'axu2', 'nanmin', 'xiangjme', 'jeswu', 'zhejian',
                 'zhijli', 'cjunhua', 'liuzeng', 'siliu2', 'xiaohazh', 'xiaobbai', 'hazhou2', 'bog2', 'liru', 'xueqian',
                 'yuncai', 'scong', 'chenjin', 'xuewang3', 'yuanche2', 'dongfzha', 'leisu', 'linli6', 'hongxuch',
                 'xianfu', 'hyin2', 'zhaoya', 'tianyuan', 'wenbliu', 'jianqi', 'zeryu', 'zhenswan', 'zonzhao', 'haob',
                 'guojyu', 'nsha', 'wexin', 'zhinzhan', 'yufhan', 'liyzhao', 'yinzhan', 'yuanl3', 'keluzha', 'bopa',
                 'danl4', 'menwei', 'wtan2', 'yawang4', 'juyao', 'zhaozh', 'xiul', 'guanlu', 'xingjin2', 'zongzli',
                 'danyzhan', 'razheng', 'xuanzh', 'mingdwan', 'jianl4', 'chuanzzh', 'yunlhe', 'yinliu4', 'xiaoshya',
                 'weichen3', 'zhiroli', 'ruitang', 'zhisong', 'haigujin', 'chulyu', 'guodoli', 'jingm2', 'kyoshita',
                 'tingwa2', 'yil7', 'jianzh3', 'yuanyawa', 'xukang', 'lianggu', 'wangyli', 'wantwang', 'wanyili',
                 'xiaotosu', 'ejaphet', 'yuanyao2', 'faxu', 'dingxwan', 'guobwang', 'guozhao', 'xincheng', 'yipihuan',
                 'yeschen', 'richuang', 'jiaxlin', 'guowli', 'zihaowa', 'siwsong', 'chunz', 'congw', 'vinechan',
                 'xiangw2', 'alhao', 'hli6', 'xinghwan', 'bawei', 'billwan', 'andrwan2', 'mencao', 'chezhou2',
                 'yaojian', 'yuewen', 'yuhu2', 'yaoszhan', 'yuanlliu', 'binguo', 'zhenyxu', 'jhuangfu', 'taoji',
                 'jielfu', 'rniu', 'pontin', 'yutjiao', 'anqhu', 'shufu', 'lxuqi', 'ganyu', 'haomshi', 'taowan3',
                 'amiwang', 'xiaoyil', 'feiyang2', 'yuegao2', 'yuhzhang', 'yibhuang', 'juntan', 'lsha', 'wakong',
                 'allayu', 'caishi', 'jamexu', 'yeechan', 'miju', 'zhinji', 'jichi', 'jiaoyli', 'sidong', 'juhan2',
                 'chunyali', 'lingwa', 'chenxxu', 'jacgao', 'yyang3', 'djin2', 'yaoyli', 'guowwang', 'wenweli',
                 'yongfwu', 'yusozhao', 'haoyuwan', 'zichuang', 'xinyji', 'zhiyyao', 'yinglv', 'linz3', 'xuezhen',
                 'waxie', 'mujiang', 'gpi', 'jializha', 'kexli', 'yixinzh', 'songwan2', 'wzheng3', 'xiafan', 'xilbai',
                 'jliu6', 'suxing', 'xianliu2', 'wenjiawa', 'danxu2', 'yiyali', 'yuymeng', 'xuedo', 'wehou', 'sunnlin',
                 'xiangylu', 'martiliu', 'yuyli', 'xinxiwan', 'aesmaeil', 'tqu2', 'beyin', 'huipa', 'tazou', 'jingw5',
                 'qianjliu', 'yapzheng', 'qirshao', 'lukl', 'xiaoqjin', 'songwa2', 'hethan', 'jiaxtian', 'shilyan',
                 'yiysun', 'wageng', 'xihuli', 'kachen3', 'hunmeng', 'neiren', 'wenpliu', 'bilwu2', 'fulliu', 'yishan',
                 'xiaoyji', 'mengwa', 'danishao', 'zicui', 'mskrebts', 'ifomin', 'abatyrov', 'pdziarha', 'sartemov',
                 'sshumikh', 'nevgenie', 'paliakse', 'semarkov', 'fstorozh', 'esvetlik', 'isheev', 'mfedotov',
                 'bgorbach', 'abrelins', 'tingqzha', 'hushang', 'shuangli', 'raxing', 'jihao', 'qixing', 'ruihache',
                 'jiayao2', 'edisonl', 'xiangbwa', 'tingsun', 'kangl', 'tongyzha', 'yuniu', 'ywanxin', 'weduan',
                 'lingyxia', 'xuxing', 'limwu', 'fanan', 'chaofluo', 'yangl4', 'yingkang', 'xuesjia', 'guangxil',
                 'junnyang', 'shache', 'mingmsun', 'maoyang', 'peren', 'panli2', 'yajli', 'dizhan', 'yiy2', 'siwzhao',
                 'suhmeng', 'sevexu', 'feifyu', 'hongjish', 'jinli6', 'dongpli', 'luliu3', 'haiyjian', 'caquan',
                 'makaji', 'zhenxzho', 'junpmao', 'yueyuli', 'hongz2', 'yiliu3', 'metian', 'chuchida', 'jingwa6',
                 'yanyjiao', 'kungao', 'hongwez2', 'chayu2', 'jialzhan', 'xiaolil2', 'xiantli', 'yingcui', 'kuliu2',
                 'liaji', 'xiaoxqin', 'qiwa4', 'lingguo', 'yanli7', 'jiaw3', 'zhongtal', 'chunxyan', 'xiaoyunw',
                 'linhzeng', 'liuliu4', 'wwang8', 'zhengzen', 'wenwxu', 'jinghuji', 'siycao', 'shuow2', 'xiaocwu',
                 'liyansun', 'janezh', 'qinlu2', 'changjdi', 'yumsun', 'txin', 'stepliu2', 'marzhao', 'paliang',
                 'philzhan', 'bos2', 'shanygua', 'chran', 'eldli', 'lianwan3', 'yuwzhang', 'depzhang', 'kanewang',
                 'necwang', 'frguo', 'dezhou', 'kaixliu', 'yangyuan', 'meilyan', 'minzzuo', 'jwang6', 'zhajin', 'kimli',
                 'ziyuliu'], 'total_count': 962}
    # lst = ['ninsun', 'zhenxzho', 'siwsong', 'xueshao', 'sunnliu', 'mengwa', 'yingwa3', 'ninshan', 'yaqsong']
    # support_collection = database['support_admin']
    # for i in lst:
    #     support_collection.update_one({"cecid": i}, {"$set": {"cecid": i, "reportline": getReportline(
    #         get_user_info_simple(i).get('manager')).get(get_user_info_simple(i).get('manager')), "active": "true"}})

    # ops_team = database['ops_team']
    # print(list(ops_team.find({"cecid": 'shirlewa', "active": "true"}, {"_id": 0})))
    # ops_team.insert_one({"cecid": "jialliu","active":"true","belongs_to":"hwen"})
    testdic = {
        "cecid":"",
        "name":"",
        "title":"",
        "region":"",
        "badge":"",
        "certificate_record":{
            'certificate_name': '',
            'certificate_type': '',
            'exam_date': '',
            'score_date': '',
            'description': '',
        }
    }
    #
    certificate_collection.update_many({},{"$set":{'status':'true'}})

