#!/bin/bash

CUR_FILE=${BASH_SOURCE[0]}
CUR_DIR=$(cd `dirname $CUR_FILE`;pwd)
SERVER_FILE="start_server.py"
SERVER_PATH=$CUR_DIR/$SERVER_FILE
LOG_FILE="log_"$HOSTNAME".out"

process_num(){
    process_num=$(ps -ef | grep $SERVER_FILE | grep -v grep | wc -l)
    echo $process_num
}

start(){
    process_num=$(process_num)

    if [[ ${process_num} -ne 0 ]]; then
        echo "Service is running. Please restart firstly."
        return 1
    else
        echo "Service being started."
        nohup python -u $SERVER_PATH &> $CUR_DIR/log/$LOG_FILE 2>&1 &
        sleep 1
        process_num=$(process_num)
        if [[ ${process_num} -ne 0 ]]; then
            echo "Service started successfully."
        else
            echo "Service started unsuccessfully"
        fi
    fi
}

stop(){
    process_num=$(ps -ef | grep $SERVER_FILE | grep -v grep | wc -l)

    if [[ ${process_num} -eq 0 ]]; then
        echo "Service is not running."
        return 1
    else
        echo "Service being stopped."
        ps -ef | grep $SERVER_FILE | grep -v grep | awk '{print $2}' | xargs kill -9
        sleep 1
        process_num=$(process_num)
        if [[ ${process_num} -eq 0 ]]; then
            echo "Service stopped successfully."
        else
            echo "Service stopped unsuccessfully."
        fi
    fi
}

restart(){
    stop
    sleep 1
    start
}

status(){
    ps -ef | grep $SERVER_FILE | grep -v grep
}

help(){
    echo "bash $CUR_FILE start: start the server"
    echo "bash $CUR_FILE stop: stop the server"
    echo "bash $CUR_FILE restart: restart the server"
    echo "bash $CUR_FILE status: check server status"
    echo "bash $CUR_FILE process_num: get server process number"
}

case $1 in
    start|stop|restart|status|process_num)
    $1
    ;;
    *)
    help
    exit
esac
