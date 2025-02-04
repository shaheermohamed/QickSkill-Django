import urllib
from urllib.request import urlopen
import re
import json
from pprint import pprint


allowed_categid = [27, 28]
courses = ['web development', 'app development', 'devops', 'machine learning']


def process(keyword):
    black_list = set()
    f_data = {}
    video_ids = []
    full_data = {}
    rm_categ_id = []
    try:
        html = urlopen(
            "https://www.youtube.com/results?search_query={}&sp=EgIYAg%253D%253D".format(keyword.replace(" ", "")))

        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_ids = list(dict.fromkeys(video_ids))

    except urllib.error.HTTPError:
        pass
    finally:
        i = 0
        for id in video_ids:
            sngl_vdo_dtl = {}
            url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&part=statistics&part=' \
                  'contentDetails&id=%s&t&key=AIzaSyAvp49alnVMEPxu-DVV1j8SSkowIrtLCjQ' % id
            print(i)
            i += 1
            print(url)
            sngl_vdo_dtl.update({'url': url})
            response = urlopen(url)
            raw_data = response.read()
            encoding = response.info().get_content_charset('utf8')  # JSON default
            data = json.loads(raw_data.decode(encoding))
            items = data['items']
            sngl_vdo_dtl.update({'v_id': id})
            print(items[0]['id'])
            sngl_vdo_dtl.update({'chnlid': items[0]['snippet']['channelId']})
            print(items[0]['snippet']['channelId'])
            statistics = items[0]['statistics']
            sngl_vdo_dtl.update({'cid': int(items[0]['snippet']['categoryId'])})
            print('category : ', int(items[0]['snippet']['categoryId']))
            if int(items[0]['snippet']['categoryId']) not in allowed_categid:
                rm_categ_id.append(int(items[0]['snippet']['categoryId']))
            sngl_vdo_dtl.update({"title": items[0]['snippet']['title']})
            print(items[0]['snippet']['title'])

            try:
                sngl_vdo_dtl.update({'view_count': statistics['viewCount']})
            except:
                sngl_vdo_dtl.update({'view_count': 'None'})
            try:
                sngl_vdo_dtl.update({'like_count': statistics['likeCount']})
            except:
                sngl_vdo_dtl.update({'like_count': 'None'})
            try:
                sngl_vdo_dtl.update({'dislike_count': statistics['dislikeCount']})
            except:
                sngl_vdo_dtl.update({'dislike_count': 'None'})
            try:
                sngl_vdo_dtl.update({'lang': items[0]['snippet']['defaultAudioLanguage']})
            except:
                sngl_vdo_dtl.update({'lang': 'None'})
            full_data.update({id: sngl_vdo_dtl})

        print('---------------------len---', len(full_data))
        for itm in full_data:
            if 'en' not in full_data[itm]['lang']:
                black_list.add(itm)
            if full_data[itm]['cid'] not in allowed_categid:
                black_list.add(itm)

        for i in black_list:
            del full_data[i]
        print('---------------------len---', len(full_data))
        count = 0
        for item in full_data:
            if count < 5:
                f_data.update({item: full_data[item]})
                count += 1
        print('lllllllllllllllllllllllllllllllllll len = ', len(f_data.keys()))

        for i in f_data:
            print(f_data[i]['lang'])
        print('\n\n')
        for i in f_data:
            print(f_data[i]['cid'])
    return f_data


def my_form_post(keyword):
    search_keyword = keyword
    global skill_set
    skill_set = []
    complt_data = []
    if search_keyword.lower() in courses:
        f = open('scraper/skill/{}.json'.format(search_keyword.lower()), 'r')
        f = json.load(f)
        for skill in f['topic']:
            if type(skill) == type(list()):
                sub_data = {}
                sub_data.update({'nested': True})
                videos = []
                for sub_skill in skill:
                    print('************************{}*************************'.format(sub_skill))
                    f_data = process(sub_skill)  # .replace('\n', ''))
                    f_data.update({'skill': sub_skill})
                    if skill.index(sub_skill) == 0:
                        sub_data.update({'skill': sub_skill})
                    # else:
                    #     f_data.update({'title': False, 'choice': True})
                    videos.append(f_data)
                sub_data.update({'videos': videos, 'count': len(videos)})
                complt_data.append(sub_data)
            else:
                print('************************{}*************************'.format(skill.replace('\n', '')))
                f_data = process(skill)
                f_data.update({'skill': skill, 'nested': False})
                complt_data.append(f_data)

    else:
        f_data = process(search_keyword)
        f_data.update({'skill': search_keyword.title(), 'nested': False})
        complt_data.append(f_data)
        pprint(complt_data)

        for j in complt_data[0]:
            print(j)

    return complt_data

