1) plot_speedup.py: 
    Plots speedup -- Normalized lines from single file
    Plots Throughput -- Non-Normalized lines from single file

2) plot_bars_normailized.py:
    Plots normalized bars from multiple files --> generates one plot

3) one_line_per_plot.py:
    Reads from multiple files, plots one simple line per plot

4) plot_event_counters.py:
    * Uses argparse
    * reads files from input directory
    * reads reference files from reference directory
    * generates multiple plots in output directory
    * uses plt.subplots()
    * reads events that need to be plotted
    * reads input from multiple files
    * plots few lines per subplot

5) plot_columns_having.py:
    * Reads input from given files, produces one line per input file
    * uses axvline
    * uses group_by
    * plots errorbars

6) plot_counters.py:
    * uses twinx() (dual axis)
    * plots bars
    * reads from multiple files in input directory
    * generates one plot

7) plot_lines_metrics.py:
    * reads from single file
    * creates one subplot for each given metric
    * few lines per subplot

8) plot_columns_normalized.py:
    * hard coded approach
    * Reads input files 
    * reads reference files
    * for each file, reads reference and input
    * divides them and plots the result

9) plot_columns.py:
    * hard coded approach
    * Reads input files 
    * for each file plots a column of the file

10) plot_phasespace.py:
    * plots de and dt from an input file

11) plot_time_multithread_mixed.py:
    * reads frmo two files
    * creates one subplot per file
    * plots few lines per subplot

12) plot_bars_percentage.py:
    * reads single file
    * plots few bars 

13) plotting_utilities.py:
    * Library script
    * annotate, annotate_min, annotate_max
    * group_by
    * keep_only
    * autolabel for bars