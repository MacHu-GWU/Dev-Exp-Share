#!/bin/bash

cat data.json | jq '[ { "fullname": .[] | "\(.firstname) \(.lastname)" } ]'
