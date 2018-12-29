import pymysql

#连接数据库
db = pymysql.connect('IP','user','password','databasename')
cursor = db.cursor()

class Sql():
    @classmethod
    def insert(cls,name,lat,lng,address,province,city,area,street_id,uid,telephone,shop_hours,detail_url,scope_type,content_tag):
        sql = "insert into baiduspider(name,lat,lng,address,province,city,area,street_id,uid,telephone,shop_hours,detail_url,scope_type,content_tag)" \
              "values (%(name)s,%(lat)s,%(lng)s,%(address)s,%(province)s,%(city)s,%(area)s,%(street_id)s,%(uid)s,%(telephone)s,%(shop_hours)s,%(detail_url)s,%(scope_type)s,%(content_tag)s)"
       # print(sql)
        values = {
        'name' : name,
        'lat':lat,
        'lng':lng,
        'address':address,
        'province':province,
        'city':city,
        'area':area,
        'street_id':street_id,
        'uid':uid,
        'telephone':telephone,
        'shop_hours':shop_hours,
        'detail_url':detail_url,
        'scope_type':scope_type,
        'content_tag':content_tag
        }

        try:
            cursor.execute(sql,values)
            db.commit()
            print("{}数据插入成功".format(name))
        except Exception as e:
            print("{}插入失败~~~".format(name),e)
            db.rollback()

    @classmethod
    def select(cls):
        sql = "select cityname from baidu_city "
        cursor.execute(sql)
        data = cursor.fetchall()
        #print(data)
        return data

