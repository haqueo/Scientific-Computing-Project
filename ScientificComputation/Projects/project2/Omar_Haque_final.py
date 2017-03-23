import csv
import numpy as np
import sys


def extract_data(file_name):
    """
    This function uses the csv module to extract the 'jobs', 'durations'
    and 'has to be completed before' columns

    :param file_name: a csv file containing the data
    :return: a total_nodesx3 np.array containing the 'jobs', 'durations'
    and 'has to be completed before' columns
    """
    # e.g. file_name = './data/jobslist'
    job = []
    duration = []
    completed_before = []

    # open the file
    with open(file_name, 'r') as file:

        AAA = csv.reader(file)
        # iterate through each row
        for i, row in enumerate(AAA):
            # add the job number
            job.append(int(row[0]))
            # add the duration
            duration.append(int(row[1]))
            # if there are jobs to be completed before, add them
            if len(row) > 2:
                completed_before.append([int(node) for node in row[2:]])

            else:
                # else add an empty list.
                completed_before.append([])

    file.close()

    # combine these together

    data_frame = np.column_stack((np.array(job,dtype=int), np.array(duration,dtype=int), completed_before))

    return data_frame


def generate_weight_matrix(data):
    """
    This function uses the data to create an adjacency matrix, based
    on the rules outlined.

    :param data: three column np.array with 'jobs', 'durations'
    and 'has to be completed before' columns
    :return: the adjacency matrix for this graph
    """
    global total_nodes, virtual_start, virtual_finish,job_duration
    # we start with an array of -1s and populate the entries that
    # correspond to connected nodes.
    total_nodes = data.shape[0]
    weight_matrix = -1 * np.ones((2 * total_nodes + 2, 2 * total_nodes + 2)
                                 , dtype=int)

    # node start is the index of start jobs
    node_start = data[:, 0].astype(int)
    # job_duration are the job durations for each job
    job_duration = data[:, 1].astype(int)

    # joining each node start to node finish, with the weight as that job's
    # duration.
    weight_matrix[node_start, node_start + 13] = job_duration

    # note on efficiency: I could perhaps do the following for
    # loop by flattening the data[:,2] column, but I need to
    # create a list of node_start corresponding to the number of
    # jobs that each job depends on. This is O(N) anyway, so doing
    # this via a for loop isn't slower.

    # note: also, python doesn't like slicing like a[0,[[4,5],[1,2,3]]]

    for row in data:
        jobs2 = row[2]
        node_start2 = row[0]
        for job in jobs2:
            # this is the connections of dependent jobs
            weight_matrix[node_start2 + 13, job] = 0

    # these are the indices for virtual start and finish
    virtual_start = int(weight_matrix.shape[0]) - 2
    virtual_finish = int(weight_matrix.shape[0]) - 1

    # allow movement between virtual start and all the nodes
    weight_matrix[virtual_start, 0:total_nodes] = 0
    # allow movement from all the nodes to virtual finish
    weight_matrix[total_nodes:virtual_start, virtual_finish] = 0

    return weight_matrix


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
            if (w != 1):
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


def iterative_bell(adjusted_weights,start_stop):
    """
    This function uses the Bellman Ford algorithm to iteratively find
    the remaining job sequences in the graph. It adjusts the start_stop
    array

    :param adjusted_weights: A, the negative adjacency matrix
    :param start_stop: the list of earliest start and stop times to be
    edited and updated
    :return: the longest paths used to find the start_stop times
    """

    # create the longest paths list
    longest_paths = []

    # create a copy of the weight matrix
    temp_weights = np.copy(adjusted_weights)

    # create a boolean array of False's. removed_nodes[m] = True if
    # job m has been removed (its value of earliest start and stop
    # has been calculated).
    removed_nodes = np.zeros(13, dtype=bool)

    # a counter so we know when to stop.
    counter = 0

    while counter < 13:  #

        # find the longest path in the graph from virtual start
        # to virtual finish
        job_sequence = updated_bellman_ford(virtual_start,
                                            virtual_finish,
                                            temp_weights)[1:-1:2]

        # remove the connections from those jobs to virtual finish
        temp_weights[np.array(job_sequence)+13,virtual_finish] = 1
        # if we have at least 2 elements, remove the last pair
        if len(job_sequence) > 1:
            temp_weights[job_sequence[-2] + 13,job_sequence[-1]] = 1

        # determine the times using the algorithm derived
        current_time = 0

        # iterate through the jobs in the job sequence
        for job in job_sequence:

            # only add to start_times if you haven't already
            if not removed_nodes[job]:
                # set it to the current time. i.e the sum of jobs before it
                start_stop[job, 0] = current_time
                start_stop[job, 1] = current_time + job_duration[job]
                # add 1 to the counter
                counter += 1

            # update current_time
            current_time += job_duration[job]

        # set all of the nodes in this job sequence to True
        removed_nodes[job_sequence] = True
        # add this job sequence to the list of longest paths
        longest_paths.append(job_sequence)

    return longest_paths

if __name__ == '__main__':

    data = extract_data('./data/jobslist')

    weights = generate_weight_matrix(data)

    adjusted_weights = -1 * weights

    longest_path = updated_bellman_ford(
        virtual_start, virtual_finish, adjusted_weights)[1:-1:2]

    #######################################################################

    start_stop = np.zeros((13, 2), dtype=int)

    longest_paths_list = iterative_bell(adjusted_weights,start_stop)

    full = np.column_stack((data,start_stop))

    print('the longest paths to each node are %s' % str(longest_paths_list))
    print('the start_stop array is')
    print(start_stop)