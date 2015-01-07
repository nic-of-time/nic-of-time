#!/usr/bin/env Rscript

# library(extrafont) # First time: Run font_import() in R shell.
# loadfonts()

library(ggplot2)
library(reshape)

s = as.numeric(read.csv("analysis/tcp_sendfile.throughput.csv",header=F))
t = as.numeric(read.csv("analysis/tcp_stream.throughput.csv",header=F))
u = as.numeric(read.csv("analysis/udp_stream.throughput.csv",header=F))

p <- ggplot() +
  stat_ecdf(data=data.frame(s),aes(x=s,colour="s")) +
  stat_ecdf(data=data.frame(t),aes(x=t,colour="t")) +
  stat_ecdf(data=data.frame(u),aes(x=u,colour="u")) +
  xlab("Bandwidth (Mbps)") +
  ylab("") +
  theme_bw() +
  scale_color_manual(
    name="",
    values = c("s"="#B2B2FF","t"="#7A7AFF","u"="#0000E6"),
    labels = c("s"="TCP_SENDFILE","t"="TCP_STREAM","u"="UDP_STREAM")) +
  theme(legend.title=element_blank()) +
  expand_limits(x=0)
ggsave("analysis/throughput.pdf",width=7,height=6)


sr = as.numeric(read.csv("analysis/tcp_sendfile.util_recv.csv",header=F))
ss = as.numeric(read.csv("analysis/tcp_sendfile.util_send.csv",header=F))
ts = as.numeric(read.csv("analysis/tcp_stream.util_send.csv",header=F))
tr = as.numeric(read.csv("analysis/tcp_stream.util_recv.csv",header=F))
ur = as.numeric(read.csv("analysis/udp_stream.util_recv.csv",header=F))
us = as.numeric(read.csv("analysis/udp_stream.util_send.csv",header=F))

p <- ggplot() +
  stat_ecdf(data=data.frame(sr),aes(x=sr,colour="sr")) +
  stat_ecdf(data=data.frame(ss),aes(x=ss,colour="ss")) +
  stat_ecdf(data=data.frame(tr),aes(x=tr,colour="tr")) +
  stat_ecdf(data=data.frame(ts),aes(x=ts,colour="ts")) +
  stat_ecdf(data=data.frame(ur),aes(x=ur,colour="ur")) +
  stat_ecdf(data=data.frame(us),aes(x=us,colour="us")) +
  xlab("CPU Utilization (%)") +
  ylab("") +
  theme_bw() +
  scale_color_manual(
    name="",
    values = c("sr"="#B2B2FF","ss"="#0000E6",
               "tr"="#84D179","ts"="#169905",
               "ur"="#D69999","us"="#7A0000"),
    labels = c("sr"="TCP_SENDFILE recv","ss"="TCP_SENDFILE send",
               "tr"="TCP_STREAM recv","ts"="TCP_STREAM send",
               "ur"="UDP_STREAM recv","us"="UDP_STREAM send")) +
  theme(legend.title=element_blank()) +
  expand_limits(x=0)
ggsave("analysis/cpu.pdf",width=7,height=6)

tsend = as.numeric(read.csv(
  "analysis/tcp_sendfile.throughput.none.all.max.min.csv",header=F))
tstream = as.numeric(read.csv(
  "analysis/tcp_stream.throughput.none.all.max.min.csv",header=F))
ustream = as.numeric(read.csv(
  "analysis/udp_stream.throughput.none.all.max.min.csv",header=F))

df <- data.frame(
  opts = factor(c(
    "None","All","Max","Min",
    "None","All","Max","Min",
    "None","All","Max","Min"
  ),levels=c("Min","None","All","Max")),
  mode = factor(c(
      "TCP_SENDFILE","TCP_SENDFILE","TCP_SENDFILE","TCP_SENDFILE",
      "TCP_STREAM","TCP_STREAM","TCP_STREAM","TCP_STREAM",
      "UDP_STREAM","UDP_STREAM","UDP_STREAM","UDP_STREAM"
    ),
    levels=c("TCP_SENDFILE","TCP_STREAM","UDP_STREAM")),
  throughput = append(tsend,append(tstream,ustream)))
ggplot(data=df, aes(x=mode, y=throughput, fill=opts)) +
  geom_bar(stat="identity", position=position_dodge(), colour="black") +
  theme_bw() +
  xlab("Mode") +
  ylab("Throughput (Mbps)") +
  scale_fill_manual(values=c("#6497b1","#005b96","#03396c","#011f4b"))
ggsave("analysis/throughput-opts.pdf",width=7,height=6)
