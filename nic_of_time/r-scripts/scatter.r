#!/usr/bin/env Rscript

library(ggplot2)
library(reshape)

args <- commandArgs(trailingOnly = TRUE)

parse_1d_str_args <- function(str) {
  return(unlist(strsplit(str,",")))
}

in_files <- parse_1d_str_args(args[1])
show_fit <- args[2]
include_origin <- args[3]
show_convex_hull <- args[4]
xlabel <- args[5]
ylabel <- args[6]
output_files <- parse_1d_str_args(args[7])

x = as.numeric(read.csv(in_files[[1]],header=F,nrow=1))
y = as.numeric(read.csv(in_files[[2]],header=F,nrow=1))

df = data.frame(x,y)

convex_hull <- df[chull(df$x,df$y),]
names(convex_hull) <- c("hull_x","hull_y")
df <- merge(df,convex_hull)

p <- ggplot(df) +
  xlab(xlabel) +
  ylab(ylabel) +
  geom_point(aes(x=x,y=y)) +
  theme_bw() +
  theme(legend.title=element_blank(),legend.position="bottom")
if (show_fit=="True") {
  p <- p + geom_smooth(aes(x=x,y=y),method="lm",formula=y~x,fullrange=TRUE)
}
if (include_origin=="True") {
  p <- p + expand_limits(x=0,y=0)
}
if (show_convex_hull=="True") {
  p <- p + geom_polygon(aes(x=hull_x,y=hull_y),alpha=0.2)
}
lapply(output_files, function(f) ggsave(f,width=7,height=6))
