import csv
import numpy as np


def node_finish(node):
    return node + 13


def generate_weight_matrix(data):
    total_nodes = data.shape[0]
    weight_matrix = -1 * np.ones((2 * total_nodes + 2, 2 * total_nodes + 2), dtype=int)

    for row in data:

        node_start = row[0]
        weight = row[1]
        jobs = row[2]

        weight_matrix[node_start, node_finish(node_start)] = weight

        for job in jobs:
            weight_matrix[node_finish(node_start), job] = 0

    ## virtual start = 26
    ## virtual finish = 27
    ## nodes = 13

    weight_matrix[26,0:13] = 0
    weight_matrix[13:26,27] = 0

    return weight_matrix


def generate_connectivity(file_name):
    # e.g. file_name = './data/jobslist'
    job = []
    duration = []
    completed_before = []

    with open(file_name, 'r') as file:

        AAA = csv.reader(file)

        for i, row in enumerate(AAA):

            job.append(int(row[0]))

            duration.append(int(row[1]))

            if len(row) > 2:
                completed_before.append([int(node) for node in row[2:]])

            else:
                completed_before.append([])

    file.close()

    dataframe = np.column_stack((job, duration, completed_before))

    return dataframe


def updated_bellman_ford(ist, isp, wei):
    pass


if __name__ == '__main__':

    data = generate_connectivity('./data/jobslist')

    weights = generate_weight_matrix(data)
