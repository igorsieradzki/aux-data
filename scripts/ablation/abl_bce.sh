#!/bin/bash

run () {
  echo -e "\033[0;1;32m${1}\033[0m"
  eval "$1" > /dev/null
}

## Running a limited number of child processes in parallel in bash
function jobmax() {
  typeset -i MAXJOBS=$1
  sleep .1
  while (( ($(pgrep -P $$ | wc -l) - 1) >= $MAXJOBS ));	do
    sleep .1
  done
}

declare -a commands=()

# add tasks here
commands+=("python -u main_incremental.py --approach lwm --bce --seed 1336 --gridsearch-tasks 3 --exp-name bce")
commands+=("python -u main_incremental.py --approach lwm --bce --seed 1337 --gridsearch-tasks 3 --exp-name bce")
commands+=("python -u main_incremental.py --approach lwm --bce --seed 1338 --gridsearch-tasks 3 --exp-name bce")

commands+=("python -u main_incremental.py --approach lwf --bce --seed 1336 --gridsearch-tasks 3 --exp-name bce")
commands+=("python -u main_incremental.py --approach lwf --bce --seed 1337 --gridsearch-tasks 3 --exp-name bce")
commands+=("python -u main_incremental.py --approach lwf --bce --seed 1338 --gridsearch-tasks 3 --exp-name bce")

commands+=("python -u main_incremental.py --approach freezing --bce --seed 1336 --gridsearch-tasks 3 --exp-name bce")
commands+=("python -u main_incremental.py --approach freezing --bce --seed 1337 --gridsearch-tasks 3 --exp-name bce")
commands+=("python -u main_incremental.py --approach freezing --bce --seed 1338 --gridsearch-tasks 3 --exp-name bce")


MAXPROC=3

for index in ${!commands[@]}; do
  echo -en "\033[0;1;31mRUN ($((${index} + 1))|${#commands[@]}): \033[0m"
  run "${commands[${index}]}" &
  jobmax $MAXPROC
  sleep 61
done
wait # Wait for the rest
