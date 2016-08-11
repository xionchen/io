#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Xion Chen  <xionchen@foxmail.com>

import action.action
import csv

config={}
config['project'] = u'openstack/neutron'
config['status'] = u'merged'






title = [u'project',u'change_id',u'author',u'time',u'file',u'line',u'message']

dict_writer = csv.DictWriter(file('test.csv','wb'),fieldnames=title)
# dict_writer.writerow(title)

for x in action.action.find_changes(config):
    comments = action.action.find_comments(x)
    for comment in comments:
        for key in comment.keys():
            s = comment[key]
            comment[key] = (s.encode('utf-8' if type(s) is unicode else s))
    dict_writer.writerows(comments)




