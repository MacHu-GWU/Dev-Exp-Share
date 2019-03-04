#!/bin/bash

exit-zero() {
    exit 0
}

exit-one() {
    exit 0
}


exit-one
if [ -z $? ]; then
    echo "Yes"
fi

