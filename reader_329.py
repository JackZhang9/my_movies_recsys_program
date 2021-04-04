#!/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time : 2021/3/29 0:33
# @Author : CN-JackZhang
# @File: reader_329.py
'''抽取信息
从rating中抽取用户地点击序列，
从movies中得到item地详情信息'''
import os

def get_user_click(rating_file):
    '''得到用户点击列表
    Return:
        dict key:user_id,value:user_click_list,for example:[item1,item2,..]'''
    #先判断文件是否存在
    if not os.path.exists(rating_file):
        return {}
    #打开文件句柄
    with open(rating_file) as fp:
        #按行处理这个文件,这个文件第一行是不可用的，所以声明一个计数器num
        num = 0
        user_click = {}
        for line in fp:
            if num == 0:
                num += 1
                continue
            #每行有4列，以逗号分隔
            item = line.strip().split(',')
            #判断异常行，如果有小于4列的行，直接过滤
            if len(item)<4:
                continue
            [user_id,item_id,rating,timestamp] = item
            if float(rating)<3:
                continue
            #生成key:userid,value:[user_id,item_id,rating,timestamp]
            if user_id not in user_click:
                user_click[user_id] = []
            user_click[user_id].append(item_id)
        fp.close()
        return user_click

def get_item_info(item_file):
    '''得到item的info,
    得到item的title,genres
    Return:
        dict,key:item_id,value:[title,genres]'''
    #先判断文件是否存在
    if not os.path.exists(item_file):
        return {}
    #用句柄打开
    num = 0
    item_info = {}
    with open(item_file) as fp:
        #按行读取,第一行无用数据
        for line in fp:
            if num == 0:
                num += 1
                continue
            #字符串切分
            item = line.strip().split(',')
            #判断异常行
            if len(item) < 3:
                continue
            if len(item) == 3:
                [item_id,title,genres] = item
            if len(item) > 3:
                item_id = item[0]
                genres = item[-1]
                title = ','.join(item[1:-1])
            if item_id not in item_info:
                item_info[item_id] = [title,genres]
        fp.close()
    return item_info

if __name__ == '__main__':
    user_click = get_user_click('../data/ratings.txt')
    print('len:{}\nuser1:{}'.format(len(user_click),user_click['1']))
    print(user_click)
    item_info = get_item_info('../data/movies.txt')
    print(item_info,'\n',len(item_info),item_info['11'])

