import os
import json
import re
from black import check_stability_and_equivalence
from pandas import concat

# 翻译音Key的字典
dict = {
    '0': 'A1();', '1': 'A2();', '2': 'A3();', '3': 'A4();', '4': 'A5();',
    '5': 'A6();', '6': 'A7();', '7': 'B1();', '8': 'B2();', '9': 'B3();',
    '10': 'B4();', '11': 'B5();', '12': 'B6();', '13': 'B7();', '14': 'C1();',
}

# 读取文件名


def readname():
    filePath = 'chart/'
    name = os.listdir(filePath)
    return name


# 读取解析SkyStuDio乐谱
def read_chart(name):
    outputjs = []
    chartName = []
    for i in name:
        sleep1 = 0
        output_js = ""
        chartName.append(i[0:len(i)-4])
        with open((r"chart/%s" % i), 'r', encoding='utf-16le') as rd:
            chart_txt = rd.read()
            Rd = chart_txt[(chart_txt.find('[', 3)+1):len(chart_txt)-4]
            list_Rd = Rd[1:len(Rd)-1].split("},{")
            for i in list_Rd:
                str_Rd = '{'+i+'}'
                dict_Rd = json.loads(str_Rd)
                if dict_Rd['time'] - sleep1 >= 0:
                    if 'sleep(%d)' % (dict_Rd['time'] - sleep1) == 'sleep(0)':
                        key = re.search(r'\d+', ((dict_Rd['key'])[1:]))
                        output_js = output_js + dict[key.group()]
                        continue
                    else:
                        output_js = output_js + \
                            'sleep(%d);' % (dict_Rd['time'] - sleep1)
                        key = re.search(r'\d+', ((dict_Rd['key'])[1:]))
                        output_js = output_js + dict[key.group()]
                        sleep1 = dict_Rd['time']
                else:
                    key = re.search(r'\d+', ((dict_Rd['key'])[1:]))
                    output_js = output_js + dict[key.group()]
                    continue
            outputjs.append(output_js)
    return chartName, outputjs


# 写入JS乐谱


def write_chart(chartName, outputjs):
    str = open('chart.txt','r',encoding='utf-8')
    cHart = str.read()
    x = 0
    for name in chartName:
        with open((r"autojs/%s" % name+'.js'), 'w', encoding='utf-8') as wc:
            wc.write(cHart+'\n'+outputjs[x])
            x += 1


if __name__ == "__main__":
    name = readname()
    chartName, outputjs = read_chart(name)
    write_chart(chartName, outputjs)
    print('全部解析完成！')
