#!/usr/bin/env Rscript

library(ggplot2)
library(reshape)

args <- commandArgs(trailingOnly = TRUE)

parse_1d_str_args <- function(str) {
  return(unlist(strsplit(str,",")))
}

in_files <- parse_1d_str_args(args[1])
data_labels <- parse_1d_str_args(args[2])
colors <- parse_1d_str_args(args[3])
xlabel <- args[4]
output_files <- parse_1d_str_args(args[5])

in_data <- lapply(in_files, function(f) as.numeric(read.csv(f,header=F,nrow=1)))

df <- transform(melt(in_data),L1=as.factor(L1))
print(sapply(df,class))
p <- ggplot(df, aes(x=value)) +
  stat_ecdf(aes(group=L1,colour=L1)) +
  scale_color_manual(
    name="",
    values=colors,
    labels=data_labels
  ) +
  theme(legend.title=element_blank()) +
  xlab(xlabel) +
  ylab("") +
  theme_bw() +
  theme(legend.position="bottom") +
  expand_limits(x=0,y=0)
lapply(output_files, function(f) ggsave(f,width=7,height=6))
