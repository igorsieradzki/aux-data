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

commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1336 --aux-frac 0.1 --exp-name frac01")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1337 --aux-frac 0.1 --exp-name frac01")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1338 --aux-frac 0.1 --exp-name frac01")

commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1336 --aux-frac 0.3 --exp-name frac03")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1337 --aux-frac 0.3 --exp-name frac03")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1338 --aux-frac 0.3 --exp-name frac03")

commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1336 --aux-frac 0.5 --exp-name frac05")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1337 --aux-frac 0.5 --exp-name frac05")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1338 --aux-frac 0.5 --exp-name frac05")

commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1336 --aux-frac 1.0 --exp-name frac10")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1337 --aux-frac 1.0 --exp-name frac10")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1338 --aux-frac 1.0 --exp-name frac10")

commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1336 --aux-frac 1.5 --exp-name frac15")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1337 --aux-frac 1.5 --exp-name frac15")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1338 --aux-frac 1.5 --exp-name frac15")

commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1336 --aux-frac 2.0 --exp-name frac20")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1337 --aux-frac 2.0 --exp-name frac20")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1338 --aux-frac 2.0 --exp-name frac20")

commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1336 --aux-frac 2.5 --exp-name frac25")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1337 --aux-frac 2.5 --exp-name frac25")
commands+=("python -u main_incremental.py --approach aux.lwf --gridsearch-tasks 3 --network resnet32cov --seed 1338 --aux-frac 2.5 --exp-name frac25")


commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1336 --gridsearch-tasks 3 --aux-frac 0.1 --exp-name frac01")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1337 --gridsearch-tasks 3 --aux-frac 0.1 --exp-name frac01")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1338 --gridsearch-tasks 3 --aux-frac 0.1 --exp-name frac01")

commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1336 --gridsearch-tasks 3 --aux-frac 0.3 --exp-name frac03")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1337 --gridsearch-tasks 3 --aux-frac 0.3 --exp-name frac03")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1338 --gridsearch-tasks 3 --aux-frac 0.3 --exp-name frac03")

commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1336 --gridsearch-tasks 3 --aux-frac 0.5 --exp-name frac05")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1337 --gridsearch-tasks 3 --aux-frac 0.5 --exp-name frac05")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1338 --gridsearch-tasks 3 --aux-frac 0.5 --exp-name frac05")

commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1336 --gridsearch-tasks 3 --aux-frac 1.0 --exp-name frac10")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1337 --gridsearch-tasks 3 --aux-frac 1.0 --exp-name frac10")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1338 --gridsearch-tasks 3 --aux-frac 1.0 --exp-name frac10")

commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1336 --gridsearch-tasks 3 --aux-frac 1.5 --exp-name frac15")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1337 --gridsearch-tasks 3 --aux-frac 1.5 --exp-name frac15")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1338 --gridsearch-tasks 3 --aux-frac 1.5 --exp-name frac15")

commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1336 --gridsearch-tasks 3 --aux-frac 2.0 --exp-name frac20")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1337 --gridsearch-tasks 3 --aux-frac 2.0 --exp-name frac20")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1338 --gridsearch-tasks 3 --aux-frac 2.0 --exp-name frac20")

commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1336 --gridsearch-tasks 3 --aux-frac 2.5 --exp-name frac25")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1337 --gridsearch-tasks 3 --aux-frac 2.5 --exp-name frac25")
commands+=("python -u main_incremental.py --approach aux.lwm --gridsearch-tasks 3 --seed 1338 --gridsearch-tasks 3 --aux-frac 2.5 --exp-name frac25")


MAXPROC=3

for index in ${!commands[@]}; do
  echo -en "\033[0;1;31mRUN ($((${index} + 1))|${#commands[@]}): \033[0m"
  run "${commands[${index}]}" &
  jobmax $MAXPROC
  sleep 61
done
wait # Wait for the rest
