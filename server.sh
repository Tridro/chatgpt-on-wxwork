#!/bin/bash
export LANG="zh_CN.UTF-8"
source /venv/bin/activate

# start or stop or restart
optype=$1

# 进程名称, 修改此处
PROG_NAME='chatgpt-on-wxwork'
DATE=$(date  "+%Y%m%d")
PROG_DIR=$(dirname "$0")

if [ x"${optype}" = x ] ; then
    optype=start
fi

start() {
    # 检查进程数量
    prog_num=$(ps -ef | grep $PROG_NAME | grep -v grep -c)
    if [ "$prog_num" -eq 0 ] ; then
        echo "starting $PROG_NAME"
        nohup python3 -u main.py > "$PROG_DIR"/log/app_info_"$DATE".log  2>&1 &
    else
        echo "$PROG_NAME is started"
    fi
}



stop() {
    # 检查进程数量
    prog_num=$(ps -ef | grep $PROG_NAME | grep -v grep -c)
    if [ "$prog_num" -eq 0 ] ; then
      echo "$PROG_NAME is not running"
      return
    fi

    # 查出所有进程
    prog_ids=$(ps -ef | grep $PROG_NAME | grep -v grep | awk '{print $2}')
    for pid in $prog_ids;
    do
        kill -15 "$pid";
    done
    echo "stopping $PROG_NAME"

    # 再次检查进程数量
    while :
    do
        sleep 1
        prog_num=$(ps -ef | grep $PROG_NAME | grep -v grep -c)
        if [ "$prog_num" -eq 0 ] ; then
          echo "$PROG_NAME is stopped"
          return
        fi
    done
}



case "$optype" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    *)
        echo "Only support start|stop|restart"
        exit 1
esac