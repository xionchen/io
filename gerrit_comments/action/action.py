#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Xion Chen  <xionchen@foxmail.com>

import restbase
import csv


def find_changes(config):
    """

    :return: a list of {change_id,project_name,version_nubmer}
    """
    queryargs = ''
    query_list = []

    for x in config.keys():
        if config.get(x) is not None:
            query_list.append('%s:%s' % (x, config.get(x)))

    if len(query_list) != 0:
        queryargs = '?q=' + '%20'.join(query_list)

    querystr = '/changes/' + queryargs + '&o=ALL_REVISIONS'
    print querystr
    result = restbase.GerritRestAPI().get(querystr)
    parsed_result = []
    for x in result:
        attr = {}
        # print len(x['revisions'])
        attr[u'id'] = x[u'id']
        attr[u'project'] = x[u'project']
        attr[u'revisions_numbers'] = len(x['revisions'])
        parsed_result.append(attr)
    return parsed_result

def find_comments(config):
    """

    :param config:{project, change_id, revisions_numbers}
    :return:[{project, author, time,file, corereveiw,comment,}]
    """
    comments = []
    for i in range(1,config['revisions_numbers']+1):
        comment_querystr = '/changes/%s/revisions/%d/comments' \
                           % (config[u'id'],i)

        print comment_querystr
        result = restbase.GerritRestAPI().get(comment_querystr)


        change_id = config[u'id']
        project = config[u'project']
        for filename in result.keys():
            for comment in result[filename]:
                attr = {}
                name = comment[u'author'][u'name']
                line = comment[u'line']
                time = comment[u'updated'].split()[0]
                message = comment[u'message']
                attr[u'project'] = project
                attr[u'change_id'] = change_id
                attr[u'author'] = name
                attr[u'time'] = time
                attr[u'file'] = filename
                attr[u'line'] = line
                attr[u'message'] = message
                comments.append(attr)
    return comments


