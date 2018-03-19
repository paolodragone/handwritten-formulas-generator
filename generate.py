
import os
import numpy as np
from matplotlib.image import imread


def process_image(file_path):
    img = imread(file_path)
    return (img <= 128).astype(np.int)


def generate(args):
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '=']
    dirs = [os.path.join(args.base_dir, s) for s in symbols]
    files = [os.listdir(d) for d in dirs]

    X, Y = [], []

    for i in range(args.n_samples):
        print('Generating sample n. {}'.format(i), end='\r')

        n1 = np.random.randint(0, args.max_value // 2)
        n2 = np.random.randint(0, args.max_value // 2)
        n3 = n1 + n2

        digits_1 = [int(d) for d in str(n1)]
        digits_2 = [int(d) for d in str(n2)]
        digits_3 = [int(d) for d in str(n3)]

        images_1 = []
        images_2 = []
        images_3 = []

        for d in digits_1:
            digit_file = np.random.choice(files[d])
            digit_path = os.path.join(dirs[d], digit_file)
            digit_image = process_image(digit_path)
            images_1.append(digit_image)

        plus_file = np.random.choice(files[10])
        plus_path = os.path.join(dirs[10], plus_file)
        plus_image = process_image(plus_path)

        for d in digits_2:
            digit_file = np.random.choice(files[d])
            digit_path = os.path.join(dirs[d], digit_file)
            digit_image = process_image(digit_path)
            images_2.append(digit_image)

        equal_file = np.random.choice(files[11])
        equal_path = os.path.join(dirs[11], equal_file)
        equal_image = process_image(equal_path)

        for d in digits_3:
            digit_file = np.random.choice(files[d])
            digit_path = os.path.join(dirs[d], digit_file)
            digit_image = process_image(digit_path)
            images_3.append(digit_image)

        images = np.array(
            images_1 + [plus_image] + images_2 + [equal_image] + images_3
        )
        sequence = np.array(digits_1 + [10] + digits_2 + [11] + digits_3)
        length = len(images)
        assert length == len(sequence)

        X.append({'length': length, 'images': images})
        Y.append({'sequence': sequence})

    print('\nDone.')

    return np.array(X), np.array(Y)


def main(args):
    import pickle
    with open(args.output_file, 'wb') as f:
        pickle.dump(generate(args), f)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('base_dir')
    parser.add_argument('-n', '--n_samples', type=int, default=10000)
    parser.add_argument('-o', '--output-file', default='formulas.pickle')
    parser.add_argument('-m', '--max_value', type=int, default=999)
    args = parser.parse_args()

    main(args)

