#!/bin/bash

export DJANGO_TEST_PROCESSES="1"
TESTS=`dirname $0`
VENV=$TESTS/../$1
shift
. $VENV/bin/activate && $@
