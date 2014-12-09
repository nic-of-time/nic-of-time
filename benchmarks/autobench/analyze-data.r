#!/usr/bin/env Rscript

# library(extrafont) # First time: Run font_import() in R shell.
# loadfonts()

library(ggplot2)
library(reshape)

nio40k = as.numeric(read.csv("analysis/40000.0.net_io_192.168.1.5.csv",
  header=F))
nio80k = as.numeric(read.csv("analysis/80000.0.net_io_192.168.1.5.csv",
  header=F))
nio120k = as.numeric(read.csv("analysis/120000.0.net_io_192.168.1.5.csv",
  header=F))
nio160k = as.numeric(read.csv("analysis/160000.0.net_io_192.168.1.5.csv",
  header=F))

df <- data.frame(nio40k,nio80k,nio120k,nio160k)
df_m <- melt(df)
p <- ggplot(df_m,aes(x=value)) +
  xlab("Net IO (Mbps)") +
  ylab("") +
  stat_ecdf(aes(group=variable,colour=variable)) +
  theme_bw() +
  scale_color_manual(
    values = c("#363537", "#ef2d56", "#ed7d3a", "#8cd867"),
    labels=c("40k Request Rate","80k Request Rate","120k Request Rate",
      "160k Request Rate")) +
  theme(legend.title=element_blank()) +
  expand_limits(x=0)
ggsave("analysis/netio.pdf",width=7,height=6)

arr40k = as.numeric(read.csv("analysis/40000.0.avg_rep_rate_192.168.1.5.csv",
  header=F))
arr80k = as.numeric(read.csv("analysis/80000.0.avg_rep_rate_192.168.1.5.csv",
  header=F))
arr120k=as.numeric(read.csv("analysis/120000.0.avg_rep_rate_192.168.1.5.csv",
  header=F))
arr160k=as.numeric(read.csv("analysis/160000.0.avg_rep_rate_192.168.1.5.csv",
  header=F))

df <- data.frame(arr40k,arr80k,arr120k,arr160k)
df_m <- melt(df)
p <- ggplot(df_m,aes(x=value)) +
  xlab("Average Reply Rate (replies/second)") +
  ylab("") +
  stat_ecdf(aes(group=variable,colour=variable)) +
  theme_bw() +
  scale_color_manual(
    values = c("#363537", "#ef2d56", "#ed7d3a", "#8cd867"),
    labels=c("40k Request Rate","80k Request Rate","120k Request Rate",
      "160k Request Rate")) +
  theme(legend.title=element_blank()) +
  expand_limits(x=0)
ggsave("analysis/reply-rate.pdf",width=7,height=6)


n40k = as.numeric(read.csv(
  "analysis/40000.0.net_io_192.168.1.5.none.all.max.min.csv",header=F))
n80k = as.numeric(read.csv(
  "analysis/80000.0.net_io_192.168.1.5.none.all.max.min.csv",header=F))
n120k = as.numeric(read.csv(
  "analysis/120000.0.net_io_192.168.1.5.none.all.max.min.csv",header=F))
n160k = as.numeric(read.csv(
  "analysis/160000.0.net_io_192.168.1.5.none.all.max.min.csv",header=F))

df <- data.frame(
  opts = factor(c(
    "None","All","Max","Min",
    "None","All","Max","Min",
    "None","All","Max","Min",
    "None","All","Max","Min"
  ),levels=c("Min","None","All","Max")),
  reqRate = factor(c(
      "40k Request Rate", "40k Request Rate",
      "40k Request Rate", "40k Request Rate",
      "80k Request Rate", "80k Request Rate",
      "80k Request Rate", "80k Request Rate",
      "120k Request Rate", "120k Request Rate",
      "120k Request Rate", "120k Request Rate",
      "160k Request Rate", "160k Request Rate",
      "160k Request Rate", "160k Request Rate"
    ),
    levels=c("40k Request Rate", "80k Request Rate", "120k Request Rate",
      "160k Request Rate")),
  netIo = append(n40k,append(n80k,append(n120k,n160k))))
ggplot(data=df, aes(x=reqRate, y=netIo, fill=opts)) +
  geom_bar(stat="identity", position=position_dodge(), colour="black") +
  theme_bw() +
  xlab("Number of Parallel Connections") +
  ylab("Net IO (Mbps)") +
  scale_fill_manual(values=c("#6497b1","#005b96","#03396c","#011f4b"))
ggsave("analysis/nio-opts.pdf",width=7,height=6)