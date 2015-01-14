from subprocess import Popen,PIPE

from nic_of_time.helper import mkdir_p

# env = Environment(loader=FileSystemLoader("../templates")) # TODO

# def run(opts):
#     print("Plotting data.")

#     for analysis in opts.analyses:
#         analysis_out = opts.analysis_dir+"/"+analysis.output_dir
#         with open("test.r","w") as f:
#             f.write(env.get_template("ecdf.r").render(
#                 csv_path = "../"+analysis.
#                 x_label = analysis.sort_by_key,
#                 output_location = analysis.sort_by_key+".pdf",
#             ))

def grouped_bars(opts, analyses, data_labels, stats, stat_colors, ylabel, xlabel, output_files):
    print("Plotting: grouped_bars")
    mkdir_p(opts[0].plot_dir)
    all_stats = []
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
