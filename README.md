# Code for the "Class Incremental Learning and Auxiliary Unlabelled Data:The Importance of Neutral Examples"

## Requirements 

### Environment
Conda is recommended to create an environment:

`conda create --name aux-data --file requirements.txt`

### Data sets

The default data directory is set to `./data` in the main repository directory, this can be changed 
in the `./datasets/dataset_config,oy` file. Same goes for results path, set to `./results` as a default
argument in the `./main_incremental.py`.

_CIFAR10_ and _CIFAR100_ will be downloaded when running their corresponding scripts. 

The _ILSVRC12_ dataset is required for ImageNet experiments and the six datasets are required for large 
domain shift: _Oxford Flowers, MIT Indoor Scenes, CUB-200-2011 Birds, Stanford Cars, FGVC Aircraft, 
Stanford Actions_.

For auxiliary dataset for CIFAR and domain shift experiments the _tiny-images_ dataset is required. 
The `./create_aux.py` script needs to be executed to create the auxiliary set for those experiments. 

## Experiments 

To reproduce all the experiments from our paper simply run all the scripts from the `./scripts` directory.