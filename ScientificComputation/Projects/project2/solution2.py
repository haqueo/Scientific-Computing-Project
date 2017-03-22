import csv
import numpy as np
import sys

def generate_weight_matrix(data):
    """
    This function uses the data to create an adjacency matrix, based
    on the rules outlined.

    :param data: three column np.array with 'jobs', 'durations'
    and 'has to be completed before' columns
    :return: the adjacency matrix for this graph
    """
    global total_nodes,virtual_start,virtual_finish
    # we start with an array of -1s and populate the entries that correspond to
    # connected nodes.
    total_nodes = data.shape[0]
    weight_matrix = -1 * np.ones((2 * total_nodes + 2, 2 * total_nodes + 2), dtype=int)

    # node start is the index of start jobs
    node_start = data[:,0].astype(int)
    # job_duration are the job durations for each job
    job_duration = data[:,1].astype(int)

    # joining each node start to node finish, with the weight as that job's
    # duration.
    weight_matrix[node_start, node_start+13] = job_duration

    # note on efficiency: I could perhaps do the following for loop by flattening
    # the data[:,2] column, but I need to create a list of node_start coresponding
    # to the number of jobs that each job depends on. This is O(N) anyway, so doing
    # this via a for loop isn't slower.

    for row in data:
        jobs2 = row[2]
        node_start2 = row[0]
        for job in jobs2:
            # this is the connections of dependent jobs
            weight_matrix[node_start2+13, job] = 0


    virtual_start = int(weight_matrix.shape[0]) - 2
    virtual_finish = int(weight_matrix.shape[0]) - 1


    weight_matrix[virtual_start, 0:total_nodes] = 0
    weight_matrix[total_nodes:virtual_start, virtual_finish] = 0

    return weight_matrix


def extract_data(file_name):
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


def find_threads(start_stop_adjusted_input):
    start_stop_vector = np.copy(start_stop_adjusted_input)

    threads = [[0, 1, 4]]

    current_thread = []

    jobs_to_do = range(13)
    jobs_to_do.remove(0)
    jobs_to_do.remove(1)
    jobs_to_do.remove(4)

    while len(jobs_to_do) != 0:

        # start a new thread

        condition = True
        current = 0

        while condition:

            condition1 = np.asarray([current >= start_stop_vector[:, 0]])
            condition2 = np.asarray([start_stop_vector[:, 1] - start_stop_vector[:, 0] <= 130 - current])

            possible_jobs = start_stop_vector[condition1[0] & condition2[0], 2]


            if len(possible_jobs) != 0:

                # find the job which minimises abs(current - earliest_start of job)
                # or equivalently, maximises -1 * abs(current - earliest_start of job)

                # there may be many possible jobs equally distant.. we need to choose the longest one
                current_max = -1000
                current_length = 0

                for job in possible_jobs:
                    if job not in current_thread:
                        time_difference = -1 * np.abs(start_stop_vector[job, 0] - current)

                        if (time_difference >= current_max) and (
                                        start_stop_vector[job, 1] - start_stop_vector[job, 0] >= current_length):
                            current_max = time_difference
                            current_length = start_stop_vector[job, 1] - start_stop_vector[job, 0]
                            minimising_job = job



                # we now have the job that is closest to current, and also with the longest job time.

                # add this job to current thread
                current_thread.append(minimising_job)
                jobs_to_do.remove(minimising_job)
                # update current
                current += start_stop_vector[minimising_job, 1] - start_stop_vector[minimising_job, 0]

                # hard bit - delete it from start_stop
                start_stop_vector[minimising_job, 0] = 10000
                start_stop_vector[minimising_job, 1] = 20000


            else:

                if (len(start_stop_vector[condition1[0], 2]) == 0) and (len(jobs_to_do) != 0):
                    current += 10
                else:
                    threads.append(current_thread)
                    current_thread = []
                    condition = False

    return threads


if __name__ == '__main__':

    data = extract_data('./data/jobslist')
    print(data)

    weights = generate_weight_matrix(data)



    adjusted_weights = -1 * weights

    longest_path = updated_bellman_ford(26, 27, adjusted_weights)[1:-1:2]

    #######################################################################

    start_times = np.zeros(13, dtype=int)

    iterative_bell(adjusted_weights, data[:, 1])

    stop_times = [data[:, 1][i] + start_times[i] for i in range(13)]

    start_stop = np.column_stack((start_times, stop_times))

    ######################################################################

    start_stop2 = np.column_stack((start_stop, range(13)))
    start_stop2[[0, 1, 4], 0] = 10000  # this effectively means deletion
    start_stop2[[0, 1, 4], 1] = 20000  # this effectively means deletion
    print(find_threads(start_stop2))
