import re
from urllib.request import urlretrieve, urlopen
from fontTools.ttLib import TTFont


def process_font(url):
    # loc.woff是事先下载好的字体文件
    # 可以通过font1.saveXML()来了解文件的结构, font1就像一个的字典, XML文件里的tag可以对font1用字典的方法获取
    font1 = TTFont('loc.woff')
    # 使用百度的FontEditor手动确认本地字体文件name和数字之间的对应关系, 保存到字典中
    loc_dict = {'uniE8B2': '5', 'uniF818': '3', 'uniECCC': '8', 'uniE622': '1', 'uniEC92': '2', 'uniF31A': '4',
                'uniE86D': '9', 'uniE33C': '6', 'uniE1FA': '7', 'uniE13E': '0'}
    # 获取字符的name列表, 打印出来后发现第一个和最后一个name所对应的不是数字, 所以切片
    uni_list1 = font1.getGlyphNames()[1: -1]

    # 网页源码
    rsp = urlopen(url).read().decode()
    # 获取动态的字体文件并下载
    font_url = 'http://' + re.findall(r'url\(\'//(.*?\.woff)', rsp)[0]
    # web字体文件落地名
    filename = font_url.split('/')[-1]
    # 下载web字体文件
    urlretrieve(font_url, filename)

    # 打开web字体文件
    font2 = TTFont(filename)
    # 获取字符的name列表
    uni_list2 = font2.getGlyphNames()[1: -1]

    # web字体文件中name和num映射
    new_map = {}

    for uni2 in uni_list2:
        # 获取name 'uni2' 在font2中对应的对象
        obj2 = font2['glyf'][uni2]
        for uni1 in uni_list1:
            # 获取name 'uni1' 在font1中对应的对象
            obj1 = font1['glyf'][uni1]
            # 如果两个对象相等, 说明对应的数字一样
            if obj1 == obj2:
                # 将name键num值对加入new_map
                new_map[uni2] = loc_dict[uni1]

    # 将数字替换至源码
    for i in uni_list2:
        pattern = '&#x' + i[3:].lower() + ';'
        rsp = re.sub(pattern, new_map[i], rsp)

    # 返回处理处理后的源码
    return rsp


if __name__ == '__main__':
    # 猫眼国内实时票房top10
    url = 'https://maoyan.com/board/1'
    # 替换数字后的网页源码
    res = process_font(url)
