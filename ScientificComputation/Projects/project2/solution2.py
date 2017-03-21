import csv
import numpy as np
import sys


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

    virtual_start = int(weight_matrix.shape[0]) - 2
    virtual_finish = int(weight_matrix.shape[0]) - 1
    no_nodes = (int(weight_matrix.shape[0]) - 2) / 2

    weight_matrix[virtual_start, 0:no_nodes] = 0
    weight_matrix[no_nodes:virtual_start, virtual_finish] = 0

    return weight_matrix


def generate_connectivity(file_name):
    global completed_before, duration
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

    data_frame = np.column_stack((job, duration, completed_before))

    return data_frame


def updated_bellman_ford(ist, isp, wei):
    # ----------------------------------
    #  ist:    index of starting node
    #  isp:    index of stopping node
    #  wei:    adjacency matrix (V x V)
    #
    #  shpath: shortest path
    # ----------------------------------

    V = wei.shape[1]

    # step 1: initialization
    Inf = sys.maxint
    d = np.ones((V), float) * np.inf
    p = np.zeros((V), int) * Inf
    d[ist] = 0

    # step 2: iterative relaxation
    for i in range(0, V - 1):
        for u in range(0, V):
            for v in range(0, V):
                w = wei[u, v]
                if (w != 1):
                    if d[u] + w < d[v]:
                        d[v] = d[u] + w
                        p[v] = u

    # step 3: check for negative-weight cycles
    for u in range(0, V):
        for v in range(0, V):
            w = wei[u, v]
            if (w != 0):
                if (d[u] + w < d[v]):
                    # print('graph contains a negative-weight cycle')
                    pass

    # step 4: determine the shortest path
    shpath = [isp]
    while p[isp] != ist:
        shpath.append(p[isp])
        isp = p[isp]
    shpath.append(ist)

    return shpath[::-1]


def iterative_bell(adjusted_weights, edge_values):
    # create a copy of the weight matrix
    temp_weights = np.copy(adjusted_weights)

    # This is a list of 13 Falses
    # If a node appears in a job sequence (i.e. we know its start time)
    # it turns to true.
    removed_nodes = np.zeros(13, dtype=bool)
    counter = 0

    while counter < 13:  # O(1)

        job_sequence = updated_bellman_ford(26, 27, temp_weights)[1:-1:2]  # O(13*E) # all we can change is E
        print(job_sequence)
        # we write k = len(job_sequence)

        temp_weights[[node + 13 for node in job_sequence], 27] = 1  # O(k)

        current_time = 0  # O(1)

        for job in job_sequence:  # O(k)

            if not removed_nodes[job]:  # O(1)

                start_times[job] = current_time  # O(1)
                counter += 1  # O(1)

            current_time += edge_values[job]  # O(1)

        # so the for loop is O(k) in total

        removed_nodes[job_sequence] = True  # O(1)


def index_of(row, matrix):
    """find the first occurence of a row in a matrix"""

    for i,g_row in enumerate(matrix):
        if np.array_equal(row,g_row):
            return i

    return -1


def find_threads(start_stop_adjusted_input):

    start_stop_vector = np.copy(start_stop_adjusted_input)

    threads = [[0,1,4]]

    current_thread = []

    while len(start_stop_vector) != 0:

        # start a new thread

        condition = True
        current = 0

        while(condition):

            condition1 = np.asarray([current >= start_stop_adjusted[:, 0]])
            condition2 = np.asarray([start_stop_adjusted[:, 1] - start_stop_adjusted[:, 0] <= 130 - current])

            possible_jobs = start_stop_vector[condition1[0] & condition2[0],2]

            if len(possible_jobs)!=0:

                # find the job which minimises current - earlieststart of job
                time_differences = np.abs(start_stop_adjusted[possible_jobs, 0]-current)
                argmin = possible_jobs[np.argmax(time_differences)]

                # there may be jobs equally distant.. we need to choose the longest one
                equally_distant = possible_jobs[po]

                current_thread.append(argmin)

                ##hard bit - delete it from start_stop

            else:
                threads.append(current_thread)
                current_thread = []
                condition = False



            real_possible_nodes = possible_nodes4[data[:,1][possible_nodes4[:,2]] <= 130-current]

            # 2.) if there exists one such that x[0] + current <= 130:
            if len(real_possible_nodes) != 0:
                # add to current thread
                current_thread.append(real_possible_nodes[0,2])
                # remove from start_stop_times_dict
                # index = np.argmax(,axis=9)
                # print(index)

                index = index_of(real_possible_nodes[0],start_stop_vector)
                print(start_stop_vector)
                print(real_possible_nodes[0])
                print(index)
                print('current is %i' % current)

                start_stop_vector = np.delete(start_stop_vector,index,0)
                # start_stop2.remove(start_stop_times[real_possible_nodes[0,2]])
                # update current
                current += data[real_possible_nodes[0,2],1]
            else:
                # this thread is over. start a new one.
                threads.append(current_thread)
                current_thread = []
                condition = False

        print("THE THREADS ARE")
        print(threads)
        break
    # print(threads)






if __name__ == '__main__':

    data = generate_connectivity('./data/jobslist')

    weights = generate_weight_matrix(data)

    adjusted_weights = -1 * weights

    longest_path = updated_bellman_ford(26, 27, adjusted_weights)[1:-1:2]

    #######################################################################

    start_times = np.zeros(13, dtype=int)

    iterative_bell(adjusted_weights, data[:, 1])

    stop_times = [data[:, 1][i] + start_times[i] for i in range(13)]

    start_stop = np.column_stack((start_times, stop_times))

    # print(start_stop)

    ######################################################################

    start_stop2 = np.column_stack((start_stop, range(13)))

    start_stop_adjusted = np.delete(start_stop2,[0,1,4],axis=0)

    # find_threads(start_stop_adjusted)

    current = 0
    condition1 = np.asarray([current >= start_stop_adjusted[:, 0]])
    condition2 = np.asarray([start_stop_adjusted[:,0] - start_stop_adjusted[:,1] <= 130 - current])

    # print(type(condition1[0]))

    possible_nodes = start_stop_adjusted[condition1[0] & condition2[0],2]

    print(possible_nodes)

    possible_weights = data[possible_nodes, 1] - current
    print("possible_weights is ")
    print(possible_weights)
    minus_possible_weights = np.abs(data[possible_nodes, 1] - current)
    argmin = np.argmax(minus_possible_weights)
    print(argmin)

    #
    # print('\n')
    # start_stop2 = np.column_stack((start_stop, range(13)))
    # print(start_stop2)
    # print('\n')
    # possible_nodes = sorted(start_stop2[0 >= start_stop2[:, 0]], key=lambda x: (x[0], -x[1]))
    # print(possible_nodes)
    #
    #
    # possible_nodes3 = np.reshape(possible_nodes,(4,3))
    #
    # print(possible_nodes3)
    # print(data[:, 1][possible_nodes3[-1][2]])
    #
    # REAL_possible = possible_nodes3[data[:,1][possible_nodes3[:,2]] + 50 <= 130]
    # print(REAL_possible)
    # # possible_nodes2 = possible_nodes[data[:,1][possible_nodes[:][2]] + 0 <= 130]
    # # print(possible_nodes2)