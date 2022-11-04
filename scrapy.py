import requests
import json
from pyecharts.globals import ThemeType
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
self={
    "url": "",
    "headers": ""
}
self["url"] = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=localCityNCOVDataList,diseaseh5Shelf"
self["headers"] = {
   "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"
}
response = requests.post(self["url"],headers=self["headers"]).json()
data = response["data"]

areaData = data['diseaseh5Shelf']['areaTree']
chinaData = areaData[0]
provinces = chinaData['children']
city = []
province = []
# 以下的都是累计的
confirm = []
dead = []
heal = []

for i in provinces:
    for a in i['children']:
        print(a)
        # 省份名称
        province.append(i['name'])
        # 城市名称
        city.append(a['name'])
        # 确诊总数
        confirm.append(a['total']['confirm'])
        # 治愈总数
        heal.append(a['total']['heal'])
        # 死亡总数
        dead.append(a['total']['dead'])

china_info = pd.DataFrame({'city': city, 'province': province, 'confirm': confirm, 'heal': heal, 'dead': dead,})

map = (
            Map(init_opts=opts.InitOpts()) #这里可以改大小和背景啥的不懂可以看看官方文档
            .add(
                '各省累计确诊人数',
                [list(z) for z in zip(list(china_info["province"]), list(china_info['confirm']))],
                'china',
                is_map_symbol_show=False,
            )
            .set_global_opts(
                title_opts=opts.TitleOpts('中国各省累计确诊人数'),
                visualmap_opts=opts.VisualMapOpts(
                    max_=70000, # 为了实现颜色，这是设置最大值
                    split_number=50,  # 因为跨度有点大我为了区分设置多了点这个大家可以自己设置
                    is_piecewise=True,

                ),

            )
            .render('Try.html')
)


