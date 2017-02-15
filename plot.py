# 
# plot.py
# 
# This file contains code to display
# graphs of various statistics,
# which can be obtained via functions
# defined in stats.py
# 

def __graph_chars(info):
    '''
    Given a tuple of summary stats
    such as that returned by report_summary
    this function plots character frequency 
    data via matplotlib
    '''

    # retrieve info from summary tuple
    v_counts = info[0]
    c_counts = info[1]

    v_counts.update(c_counts)

    # set up data for x- and y-axes of data plot
    x_labels = [x for x, _ in sorted(v_counts.items())]

    x = list(range(len(v_counts)))
    y = [y for _, y in sorted(v_counts.items())]

    # plot bar graph of letter vs frequency

    bar_width = 1/1.5

    plt.bar(x, y, width=bar_width, tick_label=x_labels)
    
    plt.show()

def __graph_words(info):
    '''
    This function is similar to the __graph_chars
    function, except that it plots word frequencies
    instead of character frequencies
    '''

    # retrieve appropriate summary stats
    w_counts = info[2]

    # set up data for x- and y-axes
    x = list(range(len(w_counts)))
    y = [c for _, c in sorted(w_counts.items())]

    x_labels = [w for w, _ in sorted(w_counts.items())]

    # plot frequencies on a bar graph
    plt.xticks(x, x_labels, rotation='vertical')

    bar_width = 1/1.5

    plt.bar(x, y, width=bar_width)

    plt.subplots_adjust(bottom=0.15)

    plt.show()
