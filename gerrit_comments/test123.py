#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Xion Chen  <xionchen@foxmail.com>

import action.action


config={}
config['project'] = u'openstack/neutron'
config['status'] = u'merged'

for x in action.action.find_changes(config):
    action.action.find_comments(x)