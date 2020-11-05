import requests
import time


location = {"深圳": 16496, "长春": 25160, "成都": 33489, "青岛": 33494, "重庆": 36785, "广州": 47667, "济南": 59532, "沈阳": 103995, "武汉": 104007, "大连": 104009, "西安": 104038, "厦门": 104085, "南京": 452439, "杭州": 452792, "宁波": 452799, "河南": 593588, "山东": 593590, "浙江": 593594,
            "安徽": 593596, "江西": 593597, "湖南": 593598, "湖北": 593599, "新疆": 593600, "云南": 593601, "贵州": 593602, "福建": 593603, "宁夏": 593604, "西藏": 593605, "四川": 593606, "广西": 593608, "海南": 593609, "青海": 593610, "甘肃": 593611, "陕西": 593612, "广东": 593613, "哈尔滨": 104006, "新疆生产建设兵团": 593600}

namespace = {"浙江": "zhejiang33", "安徽": "anhui34", "福建": "fujian35", "江西": "jiangxi36", "山东": "shandong37", "河南": "henan41", "湖北": "hubei42", "湖南": "hunan43", "广东": "guangdong44", "广西": "guangxi45", "海南": "hainan46", "重庆": "chongqing50", "四川": "sichuan51", "贵州": "guizhou52", "云南": "yunnan53", "西藏": "xizang54", "陕西": "shanxi61", "甘肃": "gansu62",
             "青海": "qinghai63", "宁夏": "ningxia64", "新疆": "xinjiang65", "沈阳": "shenyang", "大连": "dalian", "长春": "changchun", "南京": "nanjing", "杭州": "hangzhou", "宁波": "ningbo", "厦门": "xiamen", "济南": "jinan", "青岛": "qingdao", "武汉": "wuhan", "广州": "guangzhou", "深圳": "shenzhen", "成都": "chengdu", "西安": "xian", "哈尔滨": "haerbin", "新疆生产建设兵团": "bingtuan"}


def main():
    """
    docstring
    """
    for key, value in location.items():
        for index in range(1, 5):
            profix = namespace[key]
            username = f"{profix}_0{index}"
            data = {
                "username": username,
                "sex": 0,
                "loc_id": value,
                "password": 123456,
                "account": username,
            }
            requests.post(
                url="http://192.168.119.18/competition/add_alt_get_game_user/", data=data)
            time.sleep(0.5)


main()
