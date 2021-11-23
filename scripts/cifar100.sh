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
commands+=("python -u main_incremental.py --approach joint --gridsearch-tasks 3 --seed 1336")
commands+=("python -u main_incremental.py --approach joint --gridsearch-tasks 3 --seed 1337")
commands+=("python -u main_incremental.py --approach joint --gridsearch-tasks 3 --seed 1338")

commands+=("python -u main_incremental.py --approach freezing --gridsearch-tasks 3 --seed 1336")
commands+=("python -u main_incremental.py --approach freezing --gridsearch-tasks 3 --seed 1337")
commands+=("python -u main_incremental.py --approach freezing --gridsearch-tasks 3 --seed 1338")

commands+=("python -u main_incremental.py --approach finetuning --gridsearch-tasks 3 --seed 1336")
commands+=("python -u main_incremental.py --approach finetuning --gridsearch-tasks 3 --seed 1337")
commands+=("python -u main_incremental.py --approach finetuning --gridsearch-tasks 3 --seed 1338")
#
commands+=("python -u main_incremental.py --approach ewc --gridsearch-tasks 3 --seed 1336")
commands+=("python -u main_incremental.py --approach ewc --gridsearch-tasks 3 --seed 1337")
commands+=("python -u main_incremental.py --approach ewc --gridsearch-tasks 3 --seed 1338")

commands+=("python -u main_incremental.py --approach lwf --gridsearch-tasks 3 --seed 1336")
commands+=("python -u main_incremental.py --approach lwf --gridsearch-tasks 3 --seed 1337")
commands+=("python -u main_incremental.py --approach lwf --gridsearch-tasks 3 --seed 1338")

commands+=("python -u main_incremental.py --approach lwm --gridsearch-tasks 3 --seed 1336")
commands+=("python -u main_incremental.py --approach lwm --gridsearch-tasks 3 --seed 1337")
commands+=("python -u main_incremental.py --approach lwm --gridsearch-tasks 3 --seed 1338")

commands+=("python -u main_incremental.py --approach mas --gridsearch-tasks 3 --seed 1336")
commands+=("python -u main_incremental.py --approach mas --gridsearch-tasks 3 --seed 1337")
commands+=("python -u main_incremental.py --approach mas --gridsearch-tasks 3 --seed 1338")

commands+=("python -u main_incremental.py --approach path_integral --gridsearch-tasks 3 --seed 1336")
commands+=("python -u main_incremental.py --approach path_integral --gridsearch-tasks 3 --seed 1337")
commands+=("python -u main_incremental.py --approach path_integral --gridsearch-tasks 3 --seed 1338")


MAXPROC=3

for index in ${!commands[@]}; do
  echo -en "\033[0;1;31mRUN ($((${index} + 1))|${#commands[@]}): \033[0m"
  run "${commands[${index}]}" &
  jobmax $MAXPROC
  sleep 61
done
wait # Wait for the rest
