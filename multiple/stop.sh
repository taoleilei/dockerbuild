#!/bin/bash
ps ax|grep "0.0.0.0:8000"|grep -v grep|awk '{print $1}'|xargs kill -9
ps ax|grep "mqreceiver"|grep -v grep|awk '{print $1}'|xargs kill -9
ps ax|grep "msgsender"|grep -v grep|awk '{print $1}'|xargs kill -9
ps ax|grep "rqworker"|grep -v grep|awk '{print $1}'|xargs kill -9

ps ax|grep "nginx"|grep -v grep|awk '{print $1}'|xargs kill -9
