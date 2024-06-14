from multiprocessing import Pool


def square(args):
    m, n = args
    return m * n


if __name__ == "__main__":
    tasks = [(1, 2), (3, 4)]
    with Pool(processes=4) as p:
        results = p.map(square, tasks)
        print(results)
