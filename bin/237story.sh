#!/bin/bash
#####################
####
#### This script it's use to start/stop/reload flasblog app
#### with WSGI unicorn
####
#####################

gunicorn="/usr/local/bin/gunicorn"
prog="237story.entreprendre.cm"
STORY_HOME="/appli/$prog/"
LOG_FILE="/var/log/gunicorn/237story.log"
pid="/var/lock/$prog"

RETVAL=0

start() {
    echo -n $"Starting $prog:"
    cd $STORY_HOME
    $gunicorn --daemon --pid=$pid --log-file=$LOG_FILE run:app
    RETVAL=$?
    cd -
    echo
    [ $RETVAL -eq 0 ] && touch $pid
    return $RETVAL
}

stop() {
    echo -n $"Stopping $prog:"
    kill -9 `cat $pid`
    RETVAL=$?
    echo
    [ $RETVAL -eq 0 ] && rm -f $pid
    return $RETVAL
}

reload() {
    echo -n $"Reloading $prog:"
    kill -HUP `cat $pid`
    RETVAL=$?
    echo
    return $RETVAL
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    reload)
        reload
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|reload}"
        RETVAL=1
        ;;
esac
exit $RETVAL