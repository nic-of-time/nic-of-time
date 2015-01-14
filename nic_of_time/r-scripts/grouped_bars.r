#!/usr/bin/env Rscript

library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)

parse_1d_str_args <- function(str) {
  return(unlist(strsplit(str,",")))
}

parse_2d_numeric_args <- function(str) {
  return(lapply(unlist(strsplit(str,";")),function(s) as.numeric(parse_1d_str_args(s))))
}

data <- unlist(parse_2d_numeric_args(args[1]))
data_labels <- parse_1d_str_args(args[2])
stats <- parse_1d_str_args(args[3])
stat_colors <- parse_1d_str_args(args[4])
ylabel <- args[5]
xlabel <- args[6]
output_files <- parse_1d_str_args(args[7])

df <- data.frame(
  opts = factor(rep(stats,length(data_labels)),levels=stats),
  numParallel = factor(
    unlist(lapply(data_labels, function(x) rep(x,length(stats)))),
    levels=data_labels),
  data=data)
ggplot(data=df, aes(x=numParallel, y=data, fill=opts)) +
  geom_bar(stat="identity", position=position_dodge(), colour="black") +
  theme_bw() +
  xlab(xlabel) +
  ylab(ylabel) +
  scale_fill_manual(values=stat_colors)
lapply(output_files, function(f) ggsave(f,width=7,height=6))
