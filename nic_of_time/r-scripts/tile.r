#!/usr/bin/env Rscript

library(ggplot2)
library(reshape2)

args <- commandArgs(trailingOnly = TRUE)

parse_1d_str_args <- function(str) {
  return(unlist(strsplit(str,",")))
}

parse_2d_numeric_args <- function(str) {
  return(lapply(unlist(strsplit(str,";")),function(s) as.numeric(parse_1d_str_args(s))==1))
}

data <- data.frame(parse_2d_numeric_args(args[1]))
data_labels <- parse_1d_str_args(args[2])
names(data) <- data_labels
#print(data)

output_files <- parse_1d_str_args(args[3])
#print(output_files)

## ggplot(data=df, aes(x=numParallel, y=data, fill=opts)) +
##   geom_bar(stat="identity", position=position_dodge(), colour="black") +
##   theme_bw() +
##   xlab(xlabel) +
##   ylab(ylabel) +
##   scale_fill_manual(values=stat_colors)

melted <- melt(data.matrix(data))
melted$value = as.logical(melted$value)

ggplot(melted,aes(x=Var2,y=Var1,fill=value)) +
  geom_tile() +
      theme_bw() +
        theme(legend.position = "none",
              axis.text.x = element_text(angle=25,hjust=1)) +
              ## axis.text.y = element_blank()) +
          xlab("") +
            ylab("") +
              scale_fill_manual(values = c("white","black")) +
                scale_y_continuous(breaks=seq(0,
                                     nrow(data),nrow(data)/4),
                                   labels=c("0.00","0.25","0.50","0.75","1.00"))

#print(output_files)
lapply(output_files, function(f) ggsave(f,width=7,height=6))
