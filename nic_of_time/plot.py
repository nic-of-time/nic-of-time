from subprocess import Popen,PIPE

from nic_of_time.helper import mkdir_p

def bars(opts, analyses, stats, stat_colors,
                 ylabel, output_files):
    print("Plotting: grouped_bars")
    mkdir_p(opts[0].plot_dir)
    all_stats = []
    assert(len(opts) == len(analyses)) # TODO Exception
    assert(len(stats) == len(stat_colors)) # TODO Exception
    for v in all_stats+stats+stat_colors:
        assert("," not in v)
        assert(";" not in v)
    for idx,opt in enumerate(opts):
        with open(opt.analysis_dir + "/" + analyses[idx],"r") as f:
            opt_data = [float(x) for x in f.readline().split(",")]
            none_data = float(f.readline())
            all_data = float(f.readline())
        stat_vals = []
        for stat in stats:
            stat = stat.lower()
            if stat == "min":
                stat_vals.append(min(opt_data))
            elif stat == "max":
                stat_vals.append(max(opt_data))
            elif stat == "none":
                stat_vals.append(none_data)
            elif stat == "all":
                stat_vals.append(all_data)
            else:
                raise Exception("Unrecognized stat: {}".format(stat))
        all_stats.append(",".join(str(x) for x in stat_vals))
    cmd = [opts[0].r_dir+"/bars.r",
        ";".join(all_stats),
        ",".join(stats),
        ",".join(stat_colors),
        ylabel,
        ",".join(opts[0].plot_dir+"/"+x for x in output_files)
    ]
    print("  + {}".format(" ".join(cmd)))
    p = Popen(cmd)
    p.communicate()
    if p.returncode != 0:
        raise Exception("Plot failed.")

def tile(opts,data,data_labels,output_files):
    print("Plotting: grouped_bars")
    mkdir_p(opts.plot_dir)
    assert(len(data) == len(data_labels)) # TODO Exception
    cmd = [opts.r_dir+"/tile.r",
        ";".join([",".join(row) for row in data]),
        ",".join(data_labels),
        ",".join(opts.plot_dir+"/"+x for x in output_files)
    ]
    print("  + {}".format(" ".join(cmd)))
    p = Popen(cmd)
    p.communicate()
    if p.returncode != 0:
        raise Exception("Plot failed.")

def grouped_bars(opts, analyses, data_labels, stats, stat_colors,
                 ylabel, xlabel, output_files):
    print("Plotting: grouped_bars")
    mkdir_p(opts[0].plot_dir)
    all_stats = []
    assert(len(opts) == len(analyses)) # TODO Exception
    assert(len(opts) == len(data_labels)) # TODO Exception
    assert(len(stats) == len(stat_colors)) # TODO Exception
    for idx,opt in enumerate(opts):
        with open(opt.analysis_dir + "/" + analyses[idx],"r") as f:
            opt_data = [float(x) for x in f.readline().split(",")]
            next_line = f.readline()
            if len(next_line) > 0:
                none_data = float(next_line)
            else:
                none_data = None
            next_line = f.readline()
            if len(next_line) > 0:
                all_data = float(next_line)
            else:
                all_data = None
        stat_vals = []
        for stat in stats:
            stat = stat.lower()
            if stat == "min":
                stat_vals.append(min(opt_data))
            elif stat == "max":
                stat_vals.append(max(opt_data))
            elif stat == "none":
                stat_vals.append(none_data)
            elif stat == "all":
                stat_vals.append(all_data)
            else:
                raise Exception("Unrecognized stat: {}".format(stat))
        all_stats.append(",".join(str(x) for x in stat_vals))
    cmd = [opts[0].r_dir+"/grouped_bars.r",
        ";".join(all_stats),
        ",".join(data_labels),
        ",".join(stats),
        ",".join(stat_colors),
        ylabel,
        xlabel,
        ",".join(opts[0].plot_dir+"/"+x for x in output_files)
    ]
    print("  + {}".format(" ".join(cmd)))
    p = Popen(cmd)
    p.communicate()
    if p.returncode != 0:
        raise Exception("Plot failed.")

def cdf(opts, analyses, data_labels, colors, xlabel, output_files):
    mkdir_p(opts[0].plot_dir)
    in_files = []
    assert(len(opts) == len(analyses)) # TODO Exception
    assert(len(opts) == len(data_labels)) # TODO Exception
    assert(len(opts) == len(colors)) # TODO Exception
    for idx,opt in enumerate(opts):
        in_files.append(opt.analysis_dir + "/" + analyses[idx])
    cmd = [opts[0].r_dir+"/ecdf.r",
        ",".join(in_files),
        ",".join(data_labels),
        ",".join(colors),
        xlabel,
        ",".join(opts[0].plot_dir+"/"+x for x in output_files)
    ]
    print("  + {}".format(" ".join(cmd)))
    p = Popen(cmd)
    p.communicate()
    if p.returncode != 0:
        raise Exception("Plot failed.")

def scatter(opts, analyses, convex_hull, xlabel, ylabel, output_files,
            show_fit="False", include_origin="False"):
    mkdir_p(opts[0].plot_dir)
    assert(len(opts) == 2) # TODO Exception
    assert(len(opts) == len(analyses)) # TODO Exception
    in_files = []
    for idx,opt in enumerate(opts):
        in_files.append(opt.analysis_dir + "/" + analyses[idx])
    cmd = [opts[0].r_dir+"/scatter.r",
        ",".join(in_files),
        str(show_fit),
        str(include_origin),
        str(convex_hull),
        xlabel,
        ylabel,
        ",".join(opts[0].plot_dir+"/"+x for x in output_files)
    ]
    print("  + {}".format(" ".join(cmd)))
    p = Popen(cmd)
    p.communicate()
    if p.returncode != 0:
        raise Exception("Plot failed.")
