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
commands+=("python -u main_incremental.py --approach aux.freezing --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1336")
commands+=("python -u main_incremental.py --approach aux.freezing --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1337")
commands+=("python -u main_incremental.py --approach aux.freezing --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1338")

commands+=("python -u main_incremental.py --approach aux.finetuning --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1336")
commands+=("python -u main_incremental.py --approach aux.finetuning --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1337")
commands+=("python -u main_incremental.py --approach aux.finetuning --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1338")

commands+=("python -u main_incremental.py --approach aux.ewc --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1336")
commands+=("python -u main_incremental.py --approach aux.ewc --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1337")
commands+=("python -u main_incremental.py --approach aux.ewc --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1338")

commands+=("python -u main_incremental.py --approach aux.path_integral --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1336")
commands+=("python -u main_incremental.py --approach aux.path_integral --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1337")
commands+=("python -u main_incremental.py --approach aux.path_integral --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --exp-name prim --seed 1338")

commands+=("python -u main_incremental.py --approach aux.lwf --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --seed 1336")
commands+=("python -u main_incremental.py --approach aux.lwf --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --seed 1337")
commands+=("python -u main_incremental.py --approach aux.lwf --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --seed 1338")

commands+=("python -u main_incremental.py --approach aux.lwm --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --seed 1336")
commands+=("python -u main_incremental.py --approach aux.lwm --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --seed 1337")
commands+=("python -u main_incremental.py --approach aux.lwm --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --seed 1338")

commands+=("python -u main_incremental.py --approach aux.mas --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --seed 1336")
commands+=("python -u main_incremental.py --approach aux.mas --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --seed 1337")
commands+=("python -u main_incremental.py --approach aux.mas --dataset imagenet_subset --aux-type in --aux-frac 0.5 --network resnet18 --batch-size 256 --nepochs 100 --num-workers 4 --seed 1338")


MAXPROC=3

for index in ${!commands[@]}; do
  echo -en "\033[0;1;31mRUN ($((${index} + 1))|${#commands[@]}): \033[0m"
  run "${commands[${index}]}" &
  jobmax $MAXPROC
  sleep 61
done
wait # Wait for the rest
