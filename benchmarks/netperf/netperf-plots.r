#!/usr/bin/env Rscript

# library(extrafont) # First time: Run font_import() in R shell.
# loadfonts()

library(ggplot2)
library(reshape)

dat1 = read.csv("netperf/1/plot-data.csv")
dat2 = read.csv("netperf/2/plot-data.csv")

df = data.frame(dat1$Threads,
                dat1$BandwidthBitsPerSecond/1E6,
                dat2$BandwidthBitsPerSecond/1E6
  )
colnames(df) <- c("ClientThreads", "1", "2")
df.melted <- melt(df, id='ClientThreads')

ggplot(data=df.melted, aes(x=ClientThreads,y=value,color=variable)) +
  geom_point() +
  geom_line()
ggsave("/tmp/e1.pdf",width=7,height=6)

# ggplot(data=dat , aes(x=Threads,y=BandwidthBitsPerSecond)) +
#   geom_line() +
#   geom_point(shape=1) +
#   # scale_x_continuous(breaks=round(seq(minTol,maxTol,by=16),1),expand=c(0,0)) +
#   # scale_y_continuous(limits=c(0,1),expand=c(0,0)) +
#   theme_bw() +
#   # theme(text=element_text(family="CM Roman", size=18)) +
#   xlab("Number of Client Threads")
# ggsave("/tmp/e1.pdf",width=7,height=6)
