from os.path import join

_BASE_DATA_PATH = "../data/"

dataset_config = {
    'mnist': {
        'path': join(_BASE_DATA_PATH, 'mnist'),
        'normalize': ((0.1307,), (0.3081,)),
        # Use the next 3 lines to use MNIST with a 3x32x32 input
        # 'extend_channel': 3,
        # 'pad': 2,
        # 'normalize': ((0.1,), (0.2752,))    # values including padding
    },
    'svhn': {
        'path': join(_BASE_DATA_PATH, 'svhn'),
        'resize': (224, 224),
        'crop': None,
        'flip': False,
        'normalize': ((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    },
    'cifar100': {
        'path': join(_BASE_DATA_PATH, 'cifar100'),
        'resize': None,
        'normalize': ((0.5071, 0.4866, 0.4409), (0.2009, 0.1984, 0.2023))
    },
    'cifar100_icarl': {
        'path': join(_BASE_DATA_PATH, 'cifar100'),
        'resize': None,
        'pad': 4,
        'crop': 32,
        'flip': True,
        'normalize': ((0.5071, 0.4866, 0.4409), (0.2009, 0.1984, 0.2023)),
        'class_order': [
            68, 56, 78, 8, 23, 84, 90, 65, 74, 76, 40, 89, 3, 92, 55, 9, 26, 80, 43, 38, 58, 70, 77, 1, 85, 19, 17, 50,
            28, 53, 13, 81, 45, 82, 6, 59, 83, 16, 15, 44, 91, 41, 72, 60, 79, 52, 20, 10, 31, 54, 37, 95, 14, 71, 96,
            98, 97, 2, 64, 66, 42, 22, 35, 86, 24, 34, 87, 21, 99, 0, 88, 27, 18, 94, 11, 12, 47, 25, 30, 46, 62, 69,
            36, 61, 7, 63, 75, 5, 32, 4, 51, 48, 73, 93, 39, 67, 29, 49, 57, 33
        ]
    },
    'vggface2': {
        'path': join(_BASE_DATA_PATH, 'VGGFace2'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.5199, 0.4116, 0.3610), (0.2604, 0.2297, 0.2169))
    },
    'imagenet_256': {
        'path': join(_BASE_DATA_PATH, 'ILSVRC12_256'),
        'resize': None,
        'crop': 224,
        'flip': True,
        'normalize': ((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    },
    'imagenet_subset_masana': {
        'path': join(_BASE_DATA_PATH, 'ILSVRC12_256'),
        'resize': None,
        'crop': 224,
        'flip': True,
        'normalize': ((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        'class_order': [
            68, 56, 78, 8, 23, 84, 90, 65, 74, 76, 40, 89, 3, 92, 55, 9, 26, 80, 43, 38, 58, 70, 77, 1, 85, 19, 17, 50,
            28, 53, 13, 81, 45, 82, 6, 59, 83, 16, 15, 44, 91, 41, 72, 60, 79, 52, 20, 10, 31, 54, 37, 95, 14, 71, 96,
            98, 97, 2, 64, 66, 42, 22, 35, 86, 24, 34, 87, 21, 99, 0, 88, 27, 18, 94, 11, 12, 47, 25, 30, 46, 62, 69,
            36, 61, 7, 63, 75, 5, 32, 4, 51, 48, 73, 93, 39, 67, 29, 49, 57, 33
        ]
    },
    'imagenet_subset': {
        'path': join(_BASE_DATA_PATH, 'ILSVRC12_256'),
        'resize': None,
        'crop': 224,
        'flip': True,
        'normalize': ((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        'class_order': [977,  15,  56, 801, 747, 811, 115, 845, 457, 259, 387, 312,  89,
                        323, 176,  12, 461,  95, 730, 782, 718, 217, 320,  71, 399, 576,
                        658,  13, 147, 949, 777, 908, 600, 971,  96, 985,  94,  83, 407,
                        922, 765, 724, 140, 413, 392, 819, 559, 756, 198, 517, 425, 667,
                        344,  24, 565, 988,  28, 611, 537, 950, 345, 888, 209, 487, 181,
                        491,   9,  34, 127, 401, 148, 915, 991, 479, 619, 437, 126, 910,
                        934, 277, 409, 899, 863, 247, 781, 755, 166, 821, 798,  30, 984,
                        914, 172, 733,  69, 552, 474, 430, 535, 134]
    },
    'imagenet_32_reduced': {
        'path': join(_BASE_DATA_PATH, 'ILSVRC12_32'),
        'resize': None,
        'pad': 4,
        'crop': 32,
        'flip': True,
        'normalize': ((0.481, 0.457, 0.408), (0.260, 0.253, 0.268)),
        'class_order': [
            472, 46, 536, 806, 547, 976, 662, 12, 955, 651, 492, 80, 999, 996, 788, 471, 911, 907, 680, 126, 42, 882,
            327, 719, 716, 224, 918, 647, 808, 261, 140, 908, 833, 925, 57, 388, 407, 215, 45, 479, 525, 641, 915, 923,
            108, 461, 186, 843, 115, 250, 829, 625, 769, 323, 974, 291, 438, 50, 825, 441, 446, 200, 162, 373, 872, 112,
            212, 501, 91, 672, 791, 370, 942, 172, 315, 959, 636, 635, 66, 86, 197, 182, 59, 736, 175, 445, 947, 268,
            238, 298, 926, 851, 494, 760, 61, 293, 696, 659, 69, 819, 912, 486, 706, 343, 390, 484, 282, 729, 575, 731,
            530, 32, 534, 838, 466, 734, 425, 400, 290, 660, 254, 266, 551, 775, 721, 134, 886, 338, 465, 236, 522, 655,
            209, 861, 88, 491, 985, 304, 981, 560, 405, 902, 521, 909, 763, 455, 341, 905, 280, 776, 113, 434, 274, 581,
            158, 738, 671, 702, 147, 718, 148, 35, 13, 585, 591, 371, 745, 281, 956, 935, 346, 352, 284, 604, 447, 415,
            98, 921, 118, 978, 880, 509, 381, 71, 552, 169, 600, 334, 171, 835, 798, 77, 249, 318, 419, 990, 335, 374,
            949, 316, 755, 878, 946, 142, 299, 863, 558, 306, 183, 417, 64, 765, 565, 432, 440, 939, 297, 805, 364, 735,
            251, 270, 493, 94, 773, 610, 278, 16, 363, 92, 15, 593, 96, 468, 252, 699, 377, 95, 799, 868, 820, 328, 756,
            81, 991, 464, 774, 584, 809, 844, 940, 720, 498, 310, 384, 619, 56, 406, 639, 285, 67, 634, 792, 232, 54,
            664, 818, 513, 349, 330, 207, 361, 345, 279, 549, 944, 817, 353, 228, 312, 796, 193, 179, 520, 451, 871,
            692, 60, 481, 480, 929, 499, 673, 331, 506, 70, 645, 759, 744, 459]
    },
    'cifar10': {
        'path': join(_BASE_DATA_PATH, 'cifar10'),
        'resize': None,
        'normalize': ((0.4914, 0.4822, 0.4465), (0.0610, 0.0593, 0.0684)),
        'class_order': [0, 6, 1, 5, 3, 9, 7, 8, 2, 4]
    },
    'cubs': {
        'path': join(_BASE_DATA_PATH, 'cubs_cropped'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4627, 0.4542, 0.3896), (0.2364, 0.2321, 0.2529))
    },
    'flowers': {
        'path': join(_BASE_DATA_PATH, 'flowers'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.5147, 0.4158, 0.3393), (0.2942, 0.2484, 0.2883))
    },
    'cars': {
        'path': join(_BASE_DATA_PATH, 'stanford_cars_cropped'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4235, 0.3955, 0.4035), (0.2849, 0.2796, 0.2846))
    },
    'scenes': {
        'path': join(_BASE_DATA_PATH, 'indoor_scenes'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4961, 0.4359, 0.3743), (0.2588, 0.2518, 0.2539))
    },
    'actions': {
        'path': join(_BASE_DATA_PATH, 'stanford_actions'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4706, 0.4373, 0.3991), (0.2700, 0.2608, 0.2695))
    },
    'aircrafts': {
        'path': join(_BASE_DATA_PATH, 'fgvc-aircraft'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4881, 0.5154, 0.5353), (0.2235, 0.2159, 0.2443))
    },
    'cubs_subset': {
        'path': join(_BASE_DATA_PATH, 'cubs_cropped'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4627, 0.4542, 0.3896), (0.2364, 0.2321, 0.2529)),
        'class_order': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    'flowers_subset': {
        'path': join(_BASE_DATA_PATH, 'flowers'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.5147, 0.4158, 0.3393), (0.2942, 0.2484, 0.2883)),
        'class_order': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    'cars_subset': {
        'path': join(_BASE_DATA_PATH, 'stanford_cars_cropped'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4235, 0.3955, 0.4035), (0.2849, 0.2796, 0.2846)),
        'class_order': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    'scenes_subset': {
        'path': join(_BASE_DATA_PATH, 'indoor_scenes'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4961, 0.4359, 0.3743), (0.2588, 0.2518, 0.2539)),
        'class_order': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    'actions_subset': {
        'path': join(_BASE_DATA_PATH, 'stanford_actions'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4706, 0.4373, 0.3991), (0.2700, 0.2608, 0.2695)),
        'class_order': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    'aircrafts_subset': {
        'path': join(_BASE_DATA_PATH, 'fgvc-aircraft'),
        'resize': 256,
        'crop': 224,
        'flip': True,
        'normalize': ((0.4881, 0.5154, 0.5353), (0.2235, 0.2159, 0.2443)),
        'class_order': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    }
}

# Add missing keys:
for dset in dataset_config.keys():
    for k in ['resize', 'pad', 'crop', 'normalize', 'class_order', 'extend_channel', 'kind']:
        if k not in dataset_config[dset].keys():
            dataset_config[dset][k] = None
    if 'flip' not in dataset_config[dset].keys():
        dataset_config[dset]['flip'] = False
