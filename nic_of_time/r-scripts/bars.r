#!/usr/bin/env Rscript

library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)

parse_1d_str_args <- function(str) {
  return(unlist(strsplit(str,",")))
}

parse_1d_numeric_args <- function(str) {
  return(as.numeric(parse_1d_str_args(str)))
}

data <- parse_1d_numeric_args(args[1])
stats <- parse_1d_str_args(args[2])
stat_colors <- parse_1d_str_args(args[3])
ylabel <- args[4]
output_files <- parse_1d_str_args(args[5])

df <- data.frame(x=factor(stats,level=stats),
                 y=data,
                 fill=factor(stats,level=stats))
ggplot(df,aes(x=x,y=y,fill=fill)) +
  geom_bar(stat="identity",colour="black") +
  theme_bw() +
  xlab("") +
  ylab(ylabel) +
  theme(legend.position="none") +
  scale_fill_manual(values=stat_colors)
lapply(output_files, function(f) ggsave(f,width=7,height=6))
