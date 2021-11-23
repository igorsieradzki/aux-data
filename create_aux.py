import os
from scipy import io
from time import time
import numpy as np

TI_PATH = './data/tiny_images'


def get_background_img(n_samples):

    tiny_path = os.path.join(TI_PATH, 'tiny_images.bin')
    meta_path = os.path.join('tiny_index.mat')
    meta = io.loadmat(meta_path)

    offsets =  meta['offset'][0]
    num_imgs = meta['num_imgs'][0]

    all_imgs = offsets[-1] + num_imgs[-1]

    assert all_imgs == 79302017

    cfr_cls_inds = [1250, 7745, 11852, 12533, 19325, 20657, 27040, 32956, 61244, 70218] + found_indices

    img_size = 32 * 32 * 3
    cifar_ranges = [(offsets[word_ind] * img_size , offsets[word_ind + 1] * img_size) for word_ind in cfr_cls_inds]

    def get_rand_ind():
        while True:
            ind = np.random.randint(low=0, high=all_imgs)
            proper = True
            for cls_low, cls_high in cifar_ranges:
                if cls_low < ind < cls_high:
                    proper = False
                    break
            if proper:
                break

        return ind

    output = np.zeros((n_samples, 3, 32, 32), dtype=np.uint8)
    offsets = np.zeros(n_samples, dtype=int)
    for i in range(n_samples):
        offsets[i] = get_rand_ind()

    ind = np.argsort(offsets)

    with open(tiny_path, 'rb') as tiny_file:

        for i in range(n_samples):
            if i % 1000 == 0:
                print(i)
            rand_ind = 3072 * offsets[ind[i]]
            tiny_file.seek(rand_ind)
            data = tiny_file.read(3072)
            x = np.fromstring(data, dtype='uint8')
            output[ind[i], :, :, :] = x.reshape(32, 32, 3, order='F').transpose(2, 0, 1)  # pytorch order

    return output, offsets


if __name__ == '__main__':

    cls_indices = np.load('resources/tiny_images_remove_indices.npz')
    found_indices = cls_indices['arr_0'].tolist()

    t0 = time()
    output, offsets = get_background_img(100*10000)
    print()
    print('Built aux-data in {:.1f}s'.format(time()-t0))
    print(output.shape, offsets.shape)

    np.savez_compressed('./data/aux.npz', output)
    np.savez_compressed('./data/aux_offsets.npz', offsets)