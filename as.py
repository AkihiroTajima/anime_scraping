import requests 
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt

def get_url():
    url = "https://anime.nicovideo.jp/period/2019-summer.html?from=nanime_header"
    r = requests.get(url) 
    response = requests.get(url)
    response.encoding = response.apparent_encoding
 
    #bs = BeautifulSoup(response.text, 'html.parser')
    # or
    bs = BeautifulSoup(r.content, 'lxml') ##要素の抽出
    title_part = bs.find_all("script", {"type": "application/ld+json"})
    res = []
    for i in title_part:
        title = i.get_text() ##タグの中のtext部分のみを指定
        a = json.loads(title)
        a = a ["itemListElement"]     
        for x in a:
            if 'url' in x:
                #print(x['url'])
                res.append(x['url'])
    return res

def count_nums(target_url):
    print(target_url)
    r = requests.get(target_url) 
    response = requests.get(target_url)
    response.encoding = response.apparent_encoding
 
    #bs = BeautifulSoup(response.text, 'html.parser')
    # or
    bs = BeautifulSoup(r.content, 'lxml') ##要素の抽出
    class_str_list = ['dt__ch', 'dt__d-anime']

    res = []
    for class_str in class_str_list:
        # print(class_str)
        res.append(extraction(class_str, bs))
    
    return res

def extraction(class_str, bs):
    sessions = bs.find_all("section", {"class":class_str})
    # print(class_str)
    if len(sessions) != 0:
        play_count = sessions[0].find_all("span", {"class":"list--video__item__data__item play-count"})
        comment_count = sessions[0].find_all("span", {"class":"list--video__item__data__item comment-count"})
        mylist_count = sessions[0].find_all("span", {"class":"list--video__item__data__item mylist-count"})

        play_count_list = []
        comment_count_list = []
        mylist_count_list = []

        for t in play_count:
            play_count_list.append(t.get_text())
        
        for t in comment_count:
            comment_count_list.append(t.get_text())
        
        for t in mylist_count:
            mylist_count_list.append(t.get_text())
        
        res = []
        res.append(play_count_list[::-1])
        res.append(comment_count_list[::-1])
        res.append(mylist_count_list[::-1])

        if len(play_count_list) == 0 or len(comment_count_list) == 0 or len(mylist_count_list) == 0:
                return [['0'],['0'],['0']]

        print(play_count_list[::-1])
        print(comment_count_list[::-1])
        print(mylist_count_list[::-1])
        
        return res
    return [['0'],['0'],['0']]



if __name__ == "__main__":
    # for data in out[0]:
    #     nums = [int(i) for i in data]
    #     plt.plot(nums)

    # plt.show()


    path_w = 'out.csv'

    with open(path_w, mode='w') as f:
        for url in get_url():
            out = count_nums(url) 
            f.write(url + ",")
            for d in out[0][0]:
                f.write(d + ',')
            f.write('\n')


