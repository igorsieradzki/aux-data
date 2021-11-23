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
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach finetuning --seed 1336")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach finetuning --seed 1337")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach finetuning --seed 1338")

commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach freezing --seed 1336")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach freezing --seed 1337")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach freezing --seed 1338")

commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach ewc --seed 1336")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach ewc --seed 1337")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach ewc --seed 1338")

commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach joint --seed 1336")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach joint --seed 1337")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach joint --seed 1338")

commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach lwf --seed 1336")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach lwf --seed 1337")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach lwf --seed 1338")

commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach lwm --seed 1336")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach lwm --seed 1337")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach lwm --seed 1338")

commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach mas --seed 1336")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach mas --seed 1337")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach mas --seed 1338")

commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach path_integral --seed 1336")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach path_integral --seed 1337")
commands+=("python -u main_incremental.py --datasets flowers_subset scenes_subset cubs_subset cars_subset aircrafts_subset actions_subset --num-tasks 1 --network resnet18 --batch-size 32 --gridsearch-tasks 6 --approach path_integral --seed 1338")


MAXPROC=3

for index in ${!commands[@]}; do
  echo -en "\033[0;1;31mRUN ($((${index} + 1))|${#commands[@]}): \033[0m"
  run "${commands[${index}]}" &
  jobmax $MAXPROC
  sleep 61
done
wait # Wait for the rest
