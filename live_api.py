#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
from flask import request

from zxproject_back.utils.live_tools import *
from zxproject_back import zx_app
from zxproject_back.utils.return_tools import return_results, request_pre_handler
from config.config import *
from zxproject_back.utils.log_tools import Logging

LOGGER = Logging.get_logger()


@zx_app.route("/", methods=["GET"])
@request_pre_handler("index")
def hello_zx(request_info):
    return "Zhongxin_back Project\n"


"""
@api {post} http://123.56.75.209:3003/live/operate 开通直播流接口
@apiVersion 1.0.0
@apiGroup ZhongXinGuoAn_BACK_API

@apiParam {String} ACCESS_KEY 签名
@apiParam {String} SIGN_KEY 签名
@apiParam {String} channelidcode 频道ID
@apiParam {String} livestreamaddr 频道直播流地址
@apiParam {int} timestamp 当前时间时间戳(秒)
@apiParam {int} status 0:关闭该直播频道,1:开启该直播频道

@apiSuccess {int} status_code 1000:操作成功  ,2001:禁止访问,3001:参数错误,4000:内部错误
@apiSuccess {string} status_info success
@apiSuccess {dict} results 返回结果

@apiSuccessExample Success-Response:
 HTTP/1.1 200 OK
{
    "status_code": 1000,
    "status_info": "success",
    "results": {}
}
"""

@zx_app.route("/live/operate", methods=["GET", "POST"])
def __live_operate():
    try:
        LOGGER.debug("__live_operate BEGIN:" + request.data) 
        live_data = json.loads(request.data)
        access_key = live_data.get("ACCESS_KEY", "")
        timestamp = live_data.get("timestamp", "")
        channelidcode = live_data.get("channelidcode", "")
        livestreamaddr = live_data.get("livestreamaddr", "")
        open_status = int(live_data.get("status"))
        if not (access_key and timestamp and channelidcode and livestreamaddr and open_status in [0, 1]):
            return return_results(INVALID_PARAM, {})
    except:
        LOGGER.exception("live_data = json.loads(request.data) error")
        return return_results(INVALID_PARAM, {})

    res = sign_verfication(live_data)
    if not res:
        status_code = NO_PERMISSION
    else:
        try:
            if open_status:
                # run in background, or the program won"t run continually
                os.popen("./pts_v3 %s &"%livestreamaddr)
                LOGGER.info("Add channel %s success"%channelidcode)
            else:
                # kill process
                os.popen("pgrep -f 'pts_v3 %s' | xargs kill"%livestreamaddr)
                LOGGER.info("Remove channel %s success"%channelidcode)
            status_code = SUCCESS
        except:
            LOGGER.error("The channel %s can't run the commond pts_v3"%channelidcode)
            status_code = INTERNAL_ERROR
    return return_results(status_code, {})
    LOGGER.debug("__live_operate END:" + str(status_code)) 

