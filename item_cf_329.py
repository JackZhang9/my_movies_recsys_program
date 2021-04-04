#!/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time : 2021/3/29 10:45
# @Author : CN-JackZhang
# @File: item_cf_329.py
'''item_cf(召回)电影推荐系统的召回'''
'''首先引入用户的点击序列'''
import sys
sys.path.append('../util')
import util.reader_329 as reader
import math
import operator

def base_contribute_score():
    return 1

def cal_item_sim(user_click):
    '''Return:
        dict,key:item_id,value:dict,value_key:item_id,value_value=sim_score
        sim_score是item_idi和item_idj的sim_score'''
    #有多少公共用户分别点击了两个item
    co_appear = {}
    #分母分别除一下这个item被多少用户点击过,用户点击次数
    item_user_click_time = {}
    for user_id, item_id_list in user_click.items():
        for index_i in range(0,len(item_id_list)):
            item_id_i = item_id_list[index_i]
            #由于字典比较多，判断Key是否存在的时候，直接用setdefault()，对于不存在的key可以进行初值设定
            item_user_click_time.setdefault(item_id_i,0)
            item_user_click_time[item_id_i] += 1
            for index_j in range(index_i+1,len(item_id_list)):
                item_id_j = item_id_list[index_j]
                #只要有1个user，分别点击过item_id_i和item_id_j,贡献率就+1，
                co_appear.setdefault(item_id_i,{})
                co_appear[item_id_i].setdefault(item_id_j,0)
                co_appear[item_id_i][item_id_j] += base_contribute_score()

                co_appear.setdefault(item_id_j,{})
                co_appear[item_id_j].setdefault(item_id_i,0)
                co_appear[item_id_j][item_id_i] += base_contribute_score()
    #得到他们的贡献，接着写item_sim_score的计算,首先定义一个{}
    item_sim_score = {}
    #item相似的排序信息
    item_sim_score_sorted = {}
    for item_id_i,relate_item in co_appear.items():
        for item_id_j,co_time in relate_item.items():
            sim_score = co_time/math.sqrt(item_user_click_time[item_id_i]*item_user_click_time[item_id_j])
            item_sim_score.setdefault(item_id_i,{})
            item_sim_score[item_id_i].setdefault(item_id_j,0)
            item_sim_score[item_id_i][item_id_j] = sim_score

    for item_id in item_sim_score:
        item_sim_score_sorted[item_id] = sorted(item_sim_score[item_id].items(),key=operator.itemgetter(1),reverse=True)
    #返回排序完的sim
    return item_sim_score_sorted

def cal_recom_result(user_click,sim_item):
    '''基于item_cf推荐结果,
    Args:
        sim_item:item_sim_dict
        user_click:user_click_dict
    Return:
        dict,key:user_id,value:dict,value_key:item_id,value_value:recom_score'''
    #用User最近点击的3个item，分别找到这个item的相似item，进行推荐
    recent_click_num = 3
    top_k = 5
    #定义一个{}存储推荐结果
    recom_result = {}
    for user in user_click:
        click_list = user_click[user]
        recom_result.setdefault(user,{})
        for item_id in click_list[:recent_click_num]:
            if item_id not in sim_item:
                continue
            #只取5个item最相似的item作为推荐
            for item_id_sim_tup in sim_item[item_id][:top_k]:
                item_sim_id = item_id_sim_tup[0]
                item_sim_score = item_id_sim_tup[1]
                recom_result[user][item_sim_id] = item_sim_score
    return recom_result

def debug_item_sim(item_info,sim_item):
    '''展示item信息'''
    fixed_item_id = '1'
    if fixed_item_id not in item_info:
        print('invalid item id')
        return
    [title_fix,genres_fix] = item_info[fixed_item_id]
    for tup in sim_item[fixed_item_id][:5]:
        item_id_sim = tup[0]
        sim_score = tup[1]
        if item_id_sim not in item_info:
            continue
        [title,genres] = item_info[item_id_sim]
        print(title_fix+'\t'+genres_fix+'\tsim：'+title+'\t'+genres+'\t'+str(sim_score))

def debug_recom_result(recom_result,item_info):
    '''推荐结果'''
    #指定debug的user
    user_id = '1'
    if user_id not in recom_result:
        print('ivalid result')
    for tup in sorted(recom_result[user_id].items(),key=operator.itemgetter(1),reverse=True):
        item_id, score= tup
        if item_id not in item_info:
            continue
        print(','.join(item_info[item_id])+'\t'+str(score))

def main_flow():
    '''主体流程:1.计算得到item的相似度；2.根据Item的相似度进行推荐'''
    #先得到用户点击序列
    user_click = reader.get_user_click('../data/ratings.txt')
    item_info = reader.get_item_info('../data/movies.txt')
    #1.根据用户点击序列得到item相似度
    sim_item = cal_item_sim(user_click)
    #debug一下
    # debug_item_sim(item_info,sim_item)
    # #2.根据用户点击序列和item的相似度去计算推荐结果
    recom_result = cal_recom_result(user_click,sim_item)
    debug_recom_result(recom_result,item_info)
    # return recom_result

if __name__ == '__main__':
    recom_result=main_flow()
    # print(recom_result['1'],len(recom_result['1']))

