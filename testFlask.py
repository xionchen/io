#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Xion Chen  <xionchen@foxmail.com>
from flask import Flask

app = Flask(__name__)

@app.route("/<projectname>",methods=[''GET])
def show():
    if request.method == 'GET':
        do_the_get()
    else:
        show_404()


if __name__ == '__main__':
    app.run()
