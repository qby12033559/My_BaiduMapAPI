import requests
import json
from PythonMysqlAPI import Sql


def spider(url,datas):
    #伪装请求头信息
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        "Host" : "api.map.baidu.com",
    }
    #调用百度地图API接口
    my_json = requests.get(url,headers=headers,params=datas)
    #print(my_json.text)
    my_json = my_json.text
    #返回数据
    return my_json

def parse_search(r_json):
    #解析json数据
    r_json = json.loads(r_json)
    print(r_json['message'])
    jsons = r_json['results']
    total = r_json['total']
    for js in jsons:
        try:
            name = js['name'] #百度地图的名称
        except Exception as e:
            name = None
        try:
            lat = js['location']['lat'] #坐标
        except Exception as e:
            lat = None
        try:
            lng = js['location']['lng'] #坐标
        except Exception as e:
            lng = None
        try:
            address = js['address'] #地址
        except Exception as e:
            address = None
        try:
            province = js['province'] #省
        except Exception as e:
            province = None
        try:
            city = js['city'] #市
        except Exception as e:
            city = None
        try:
            area = js['area'] #区
        except Exception as e:
            area = None
        try:
            street_id = js['street_id'] #实景ID
        except Exception as e:
            street_id = None
        try:
            uid = js['uid'] #uid 详细信息的id
        except Exception as e:
            uid = None
        #调用api得详细信息查询接口获取Uid得详细信息
        d_json = parse_detail(uid)
        d_json = json.loads(d_json)
        try:
            telephone = d_json['result']['telephone']
        except Exception as e:
            telephone = None
        try:
            shop_hours = d_json['result']['detail_info']['shop_hours']
        except Exception as e:
            shop_hours = None
        try:
            detail_url = d_json['result']['detail_info']['detail_url']
        except Exception as e:
            detail_url = None
        try:
            scope_type = d_json['result']['detail_info']['scope_type']
        except Exception as e:
            scope_type = None
        try:
            content_tag = d_json['result']['detail_info']['content_tag']
        except Exception as e:
            content_tag = None

        #调用sql将数据插入数据库
        Sql.insert(name,lat,lng,address,province,city,area,street_id,uid,telephone,shop_hours,detail_url,scope_type,content_tag)
    #返回当前的total数值，用于判断是否还有后续的数据用来继续查询。
    return total
def parse_detail(uid):
    url = 'http://api.map.baidu.com/place/v2/detail'
    datas = {
        "uid" : uid,
        "output" : "json",
        "ak" : "对应的AK数据，百度申请",#ak数据
        "scope" : 2,
    }
    d_json = spider(url, datas)
    return d_json

def baidusearch(page_num,cityname,myquery):
    #url与查询数据
    url = 'http://api.map.baidu.com/place/v2/search'
    datas = {
        "query" : myquery,
        "region" : cityname,
        "output" : "json",
        "ak" : "对应的AK数据，百度申请",#ak数据
        "page_size" : 20,
        "page_num" : page_num,
        "city_limit" : "True"
    }
    # 拼接数据后调用 spider方法 获取返回数据
    r_json = spider(url,datas)

    # 将返回数据解析并存入数据库，判断total ，当total 为0 时表示没有后续数据
    total = parse_search(r_json)
    #当total不为0时，表示可以继续查询
    if total:
        page_num += 1
        baidusearch(page_num,cityname,myquery)

if __name__ == '__main__':
    #取全国城市名称数据
    myquery = input("请输入您要查询得数据名称：")
    citynames = Sql.select()
    for cityname in citynames:
        # 设置查询页码，接口默认从第0页等于第一页
        page_num = 0
        print("开始查询{}的数据，目前是第{}页".format(cityname[0],page_num))
        baidusearch(page_num,cityname[0],myquery)

