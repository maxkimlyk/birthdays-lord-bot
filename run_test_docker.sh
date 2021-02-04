#!/bin/bash

export TELEGRAM_API_TOKEN="334131527:AAHPUaJNEX39HOkTRAptWs2ccQ9Vgv58z3M"
export TELEGRAM_USER_ID="187193654"
docker build -t bitrthday-lord-bot ./ && docker run -it --rm --name bitrthday-lord-bot --mount type=bind,source=$PWD/cache,target=/var/cache --env TELEGRAM_API_TOKEN=$TELEGRAM_API_TOKEN --env TELEGRAM_USER_ID=$TELEGRAM_USER_ID bitrthday-lord-bot
