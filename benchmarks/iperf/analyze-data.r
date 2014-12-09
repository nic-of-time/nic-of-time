#!/usr/bin/env Rscript

# library(extrafont) # First time: Run font_import() in R shell.
# loadfonts()

library(ggplot2)
library(reshape)

u1 = as.numeric(read.csv("analysis/udp.1.bw.means.csv",header=F))
t1 = as.numeric(read.csv("analysis/tcp.1.bw.means.csv",header=F))
u2 = as.numeric(read.csv("analysis/udp.2.bw.means.csv",header=F))
t2 = as.numeric(read.csv("analysis/tcp.2.bw.means.csv",header=F))
u4 = as.numeric(read.csv("analysis/udp.4.bw.means.csv",header=F))
t4 = as.numeric(read.csv("analysis/tcp.4.bw.means.csv",header=F))

df <- data.frame(u1,u2,u4,t1,t2,t4)
df_m <- melt(df)
p <- ggplot(df_m,aes(x=value)) +
  xlab("Bandwidth (Gbps)") +
  ylab("") +
  stat_ecdf(aes(group=variable,colour=variable)) +
  theme_bw() +
  scale_color_manual(
    values = c("#B2B2FF","#7A7AFF","#0000E6","#D69999","#AD3333","#7A0000"),
    labels=c("UDP, 1 Parallel","UDP, 2 Parallel","UDP, 4 Parallel",
      "TCP, 1 Parallel","TCP, 2 Parallel","TCP, 4 Parallel")) +
  theme(legend.title=element_blank()) +
  scale_x_continuous(
    limits=c(0,max(df)),
    breaks=seq(0,max(df),5),
    minor_breaks=seq(0,max(df),1))
ggsave("analysis/bw.pdf",width=7,height=6)


u1 = as.numeric(read.csv("analysis/udp.1.cpu.meanR.csv",header=F))
t1 = as.numeric(read.csv("analysis/tcp.1.cpu.meanR.csv",header=F))
u2 = as.numeric(read.csv("analysis/udp.2.cpu.meanR.csv",header=F))
t2 = as.numeric(read.csv("analysis/tcp.2.cpu.meanR.csv",header=F))
u4 = as.numeric(read.csv("analysis/udp.4.cpu.meanR.csv",header=F))
t4 = as.numeric(read.csv("analysis/tcp.4.cpu.meanR.csv",header=F))

df <- data.frame(u1,u2,u4,t1,t2,t4)
df_m <- melt(df)
p <- ggplot(df_m,aes(x=value)) +
  xlab("CPU Utilization") +
  ylab("") +
  stat_ecdf(aes(group=variable,colour=variable)) +
  theme_bw() +
  scale_color_manual(
    values = c("#B2B2FF","#7A7AFF","#0000E6","#D69999","#AD3333","#7A0000"),
    labels=c("UDP, 1 Parallel","UDP, 2 Parallel","UDP, 4 Parallel",
      "TCP, 1 Parallel","TCP, 2 Parallel","TCP, 4 Parallel")) +
  theme(legend.title=element_blank()) +
  scale_x_continuous(
    limits=c(0,max(df)),
    breaks=seq(0,max(df),5),
    minor_breaks=seq(0,max(df),1))
ggsave("analysis/cpu-meanR.pdf",width=7,height=6)

u1 = as.numeric(read.csv("analysis/udp.1.cpu.meanH.csv",header=F))
t1 = as.numeric(read.csv("analysis/tcp.1.cpu.meanH.csv",header=F))
u2 = as.numeric(read.csv("analysis/udp.2.cpu.meanH.csv",header=F))
t2 = as.numeric(read.csv("analysis/tcp.2.cpu.meanH.csv",header=F))
u4 = as.numeric(read.csv("analysis/udp.4.cpu.meanH.csv",header=F))
t4 = as.numeric(read.csv("analysis/tcp.4.cpu.meanH.csv",header=F))

df <- data.frame(u1,u2,u4,t1,t2,t4)
df_m <- melt(df)
p <- ggplot(df_m,aes(x=value)) +
  xlab("CPU Utilization") +
  ylab("") +
  stat_ecdf(aes(group=variable,colour=variable)) +
  theme_bw() +
  scale_color_manual(
    values = c("#B2B2FF","#7A7AFF","#0000E6","#D69999","#AD3333","#7A0000"),
    labels=c("UDP, 1 Parallel","UDP, 2 Parallel","UDP, 4 Parallel",
      "TCP, 1 Parallel","TCP, 2 Parallel","TCP, 4 Parallel")) +
  theme(legend.title=element_blank()) +
  scale_x_continuous(
    limits=c(0,max(df)),
    breaks=seq(0,max(df),5),
    minor_breaks=seq(0,max(df),1))
ggsave("analysis/cpu-meanH.pdf",width=7,height=6)

ru1 = as.numeric(read.csv("analysis/udp.1.cpu.meanR.csv",header=F))
ru2 = as.numeric(read.csv("analysis/udp.2.cpu.meanR.csv",header=F))
ru4 = as.numeric(read.csv("analysis/udp.4.cpu.meanR.csv",header=F))
hu1 = as.numeric(read.csv("analysis/udp.1.cpu.meanH.csv",header=F))
hu2 = as.numeric(read.csv("analysis/udp.2.cpu.meanH.csv",header=F))
hu4 = as.numeric(read.csv("analysis/udp.4.cpu.meanH.csv",header=F))

df <- data.frame(ru1,ru2,ru4,hu1,hu2,hu4)
df_m <- melt(df)
p <- ggplot(df_m,aes(x=value)) +
  xlab("CPU Utilization") +
  ylab("") +
  stat_ecdf(aes(group=variable,colour=variable)) +
  theme_bw() +
  scale_color_manual(
    values = c("#B2B2FF","#7A7AFF","#0000E6","#D69999","#AD3333","#7A0000"),
    labels=c("Remote, 1 Parallel","Remote, 2 Parallel","Remote, 4 Parallel",
      "Host, 1 Parallel","Host, 2 Parallel","Host, 4 Parallel")) +
  theme(legend.title=element_blank()) +
  scale_x_continuous(
    limits=c(0,max(df)),
    breaks=seq(0,max(df),5),
    minor_breaks=seq(0,max(df),1))
ggsave("analysis/cpu-udp.pdf",width=7,height=6)

rt1 = as.numeric(read.csv("analysis/tcp.1.cpu.meanR.csv",header=F))
rt2 = as.numeric(read.csv("analysis/tcp.2.cpu.meanR.csv",header=F))
rt4 = as.numeric(read.csv("analysis/tcp.4.cpu.meanR.csv",header=F))
ht1 = as.numeric(read.csv("analysis/tcp.1.cpu.meanH.csv",header=F))
ht2 = as.numeric(read.csv("analysis/tcp.2.cpu.meanH.csv",header=F))
ht4 = as.numeric(read.csv("analysis/tcp.4.cpu.meanH.csv",header=F))

df <- data.frame(rt1,rt2,rt4,ht1,ht2,ht4)
df_m <- melt(df)
p <- ggplot(df_m,aes(x=value)) +
  xlab("CPU Utilization") +
  ylab("") +
  stat_ecdf(aes(group=variable,colour=variable)) +
  theme_bw() +
  scale_color_manual(
    values = c("#B2B2FF","#7A7AFF","#0000E6","#D69999","#AD3333","#7A0000"),
    labels=c("Remote, 1 Parallel","Remote, 2 Parallel","Remote, 4 Parallel",
      "Host, 1 Parallel","Host, 2 Parallel","Host, 4 Parallel")) +
  theme(legend.title=element_blank()) +
  scale_x_continuous(
    limits=c(0,max(df)),
    breaks=seq(0,max(df),5),
    minor_breaks=seq(0,max(df),1))
ggsave("analysis/cpu-tcp.pdf",width=7,height=6)


udp_bw1 = as.numeric(read.csv("analysis/udp.1.bw.means.csv",header=F))
udp_cpuR1 = as.numeric(read.csv("analysis/udp.1.cpu.meanR.csv",header=F))

df <- data.frame(udp_bw1,udp_cpuR1)
p <- ggplot(df) +
  xlab("CPU Utilization (%)") +
  ylab("Bandwidth") +
  geom_point(aes(x=udp_cpuR1,y=udp_bw1)) +
  geom_smooth(aes(x=udp_cpuR1,y=udp_bw1),method="lm", formula = y~x,
    fullrange=TRUE) +
  theme_bw() +
  theme(legend.title=element_blank()) +
  expand_limits(x=0,y=0)
  #geom_text(aes(x=udp_cpuR1,y=udp_bw1,label=udp_cpuR1,
  #  size=1,hjust=0,vjust=0))
ggsave("analysis/udp.1.cpu-bandwidth.pdf",width=7,height=6)

tcp_bw1 = as.numeric(read.csv("analysis/tcp.1.bw.means.csv",header=F))
tcp_cpuR1 = as.numeric(read.csv("analysis/tcp.1.cpu.meanR.csv",header=F))
tcp_cpuH1 = as.numeric(read.csv("analysis/tcp.1.cpu.meanH.csv",header=F))
tcp_cpuAvg1 = colMeans(rbind(tcp_cpuR1,tcp_cpuH1))

df <- data.frame(tcp_bw1,tcp_cpuAvg1)
p <- ggplot(df) +
  xlab("CPU Utilization (%)") +
  ylab("Bandwidth") +
  geom_point(aes(x=tcp_cpuAvg1, y=tcp_bw1)) +
  geom_smooth(aes(x=tcp_cpuAvg1, y=tcp_bw1), method="lm", formula = y~x,
    fullrange=TRUE) +
  theme_bw() +
  theme(legend.title=element_blank()) +
  expand_limits(x=0,y=0)
ggsave("analysis/tcp.1.cpu-bandwidth.pdf",width=7,height=6)

udp_bw2 = as.numeric(read.csv("analysis/udp.2.bw.means.csv",header=F))
udp_cpuR2 = as.numeric(read.csv("analysis/udp.2.cpu.meanR.csv",header=F))

df <- data.frame(udp_bw2,udp_cpuR2)
p <- ggplot(df) +
  xlab("CPU Utilization (%)") +
  ylab("Bandwidth") +
  geom_point(aes(x=udp_cpuR2,y=udp_bw2)) +
  geom_smooth(aes(x=udp_cpuR2,y=udp_bw2),method="lm", formula = y~x,
    fullrange=TRUE) +
  theme_bw() +
  theme(legend.title=element_blank()) +
  expand_limits(x=0,y=0)
  #geom_text(aes(x=udp_cpuR2,y=udp_bw2,label=udp_cpuR2,
  #  size=1,hjust=0,vjust=0))
ggsave("analysis/udp.2.cpu-bandwidth.pdf",width=7,height=6)

tcp_bw2 = as.numeric(read.csv("analysis/tcp.2.bw.means.csv",header=F))
tcp_cpuR2 = as.numeric(read.csv("analysis/tcp.2.cpu.meanR.csv",header=F))
tcp_cpuH2 = as.numeric(read.csv("analysis/tcp.2.cpu.meanH.csv",header=F))
tcp_cpuAvg2 = colMeans(rbind(tcp_cpuR2,tcp_cpuH2))

df <- data.frame(tcp_bw2,tcp_cpuAvg2)
p <- ggplot(df) +
  xlab("CPU Utilization (%)") +
  ylab("Bandwidth") +
  geom_point(aes(x=tcp_cpuAvg2, y=tcp_bw2)) +
  geom_smooth(aes(x=tcp_cpuAvg2, y=tcp_bw2), method="lm", formula = y~x,
    fullrange=TRUE) +
  theme_bw() +
  theme(legend.title=element_blank()) +
  expand_limits(x=0,y=0)
  #geom_text(aes(x=tcp_cpuR2,y=tcp_bw2,label=tcp_cpuR2,
  #  size=1,hjust=0,vjust=0))
ggsave("analysis/tcp.2.cpu-bandwidth.pdf",width=7,height=6)

udp_bw4 = as.numeric(read.csv("analysis/udp.4.bw.means.csv",header=F))
udp_cpuR4 = as.numeric(read.csv("analysis/udp.4.cpu.meanR.csv",header=F))

udp_mask_indices = as.numeric(
  read.csv("analysis/tx-sg-tso-gro-rxhash.bw-indices.csv",header=F))
masked_idx = 1
udp_bw4_masked <- c()
udp_cpuR4_masked <- c()
for (idx in udp_mask_indices) {
  udp_bw4_masked[masked_idx] = udp_bw4[idx]
  udp_cpuR4_masked[masked_idx] = udp_cpuR4[idx]
  masked_idx <- masked_idx + 1
}
print(length(udp_cpuR4_masked))
print(length(udp_bw4_masked))

#df <- data.frame(udp_bw4,udp_cpuR4)
p <- ggplot() +
  xlab("CPU Utilization (%)") +
  ylab("Bandwidth") +
  geom_point(aes(x=udp_cpuR4,y=udp_bw4)) +
  geom_point(aes(x=udp_cpuR4_masked, y=udp_bw4_masked,color='masked')) +
  geom_smooth(aes(x=udp_cpuR4,y=udp_bw4),method="lm", formula = y~x,
    fullrange=TRUE) +
  theme_bw() +
  theme(legend.title=element_blank()) +
  expand_limits(x=0,y=0) +
  scale_color_manual(
    name="",
    values = c("masked"="#FF8080"),
    labels = c("tx, sg, tso, gro, rxhash"))
  #geom_text(aes(x=udp_cpuR4,y=udp_bw4,label=udp_cpuR4,
  #  size=1,hjust=0,vjust=0))
ggsave("analysis/udp-4-cpu-bandwidth.pdf",width=7,height=6)

tcp_bw4 = as.numeric(read.csv("analysis/tcp.4.bw.means.csv",header=F))
tcp_cpuR4 = as.numeric(read.csv("analysis/tcp.4.cpu.meanR.csv",header=F))
tcp_cpuH4 = as.numeric(read.csv("analysis/tcp.4.cpu.meanH.csv",header=F))
tcp_cpuAvg4 = colMeans(rbind(tcp_cpuR4,tcp_cpuH4))

tcp_mask_indices = as.numeric(
  read.csv("analysis/tx-sg-tso.bw-indices.csv",header=F))
masked_idx = 1
tcp_bw4_masked <- c()
tcp_cpuAvg4_masked <- c()
for (idx in tcp_mask_indices) {
  tcp_bw4_masked[masked_idx] = tcp_bw4[idx]
  tcp_cpuAvg4_masked[masked_idx] = tcp_cpuAvg4[idx]
  masked_idx <- masked_idx + 1
}

df <- data.frame(tcp_bw4,tcp_cpuAvg4)
p <- ggplot(df) +
  xlab("CPU Utilization (%)") +
  ylab("Bandwidth") +
  geom_point(aes(x=tcp_cpuAvg4, y=tcp_bw4)) +
  geom_point(aes(x=tcp_cpuAvg4_masked, y=tcp_bw4_masked,color='masked')) +
  geom_smooth(aes(x=tcp_cpuAvg4, y=tcp_bw4), method="lm", formula = y~x,
    fullrange=TRUE) +
  theme_bw() +
  theme(legend.title=element_blank()) +
  expand_limits(x=0,y=0) +
  scale_color_manual(
    name="",
    values = c("masked"="#FF8080"),
    labels = c("tx, sg, tso"))
  # geom_text(aes(x=tcp_cpuR4,y=tcp_bw4,label=tcp_cpuR4,
    # size=1,hjust=0,vjust=0,color=tcp_cpuR4))
ggsave("analysis/tcp-4-cpu-bandwidth.pdf",width=7,height=6)

u1b = as.numeric(read.csv("analysis/udp.1.bw.none.all.max.min.csv",header=F))
u2b = as.numeric(read.csv("analysis/udp.2.bw.none.all.max.min.csv",header=F))
u4b = as.numeric(read.csv("analysis/udp.4.bw.none.all.max.min.csv",header=F))

df <- data.frame(
  opts = factor(c(
    "None","All","Max","Min",
    "None","All","Max","Min",
    "None","All","Max","Min"
  ),levels=c("Min","None","All","Max")),
  numParallel = factor(c(
      "1 Parallel","1 Parallel","1 Parallel","1 Parallel",
      "2 Parallel","2 Parallel","2 Parallel","2 Parallel",
      "4 Parallel","4 Parallel","4 Parallel","4 Parallel"
    ),
    levels=c("1 Parallel","2 Parallel","4 Parallel")),
  bandwidth = append(u1b,append(u2b,u4b)))
ggplot(data=df, aes(x=numParallel, y=bandwidth, fill=opts)) +
  geom_bar(stat="identity", position=position_dodge(), colour="black") +
  theme_bw() +
  xlab("Number of Parallel Connections") +
  ylab("Bandwidth (Gbps)") +
  scale_fill_manual(values=c("#6497b1","#005b96","#03396c","#011f4b"))
ggsave("analysis/udp-opts.pdf",width=7,height=6)

t1b = as.numeric(read.csv("analysis/tcp.1.bw.none.all.max.min.csv",header=F))
t2b = as.numeric(read.csv("analysis/tcp.2.bw.none.all.max.min.csv",header=F))
t4b = as.numeric(read.csv("analysis/tcp.4.bw.none.all.max.min.csv",header=F))

df <- data.frame(
  opts = factor(c(
    "None","All","Max","Min",
    "None","All","Max","Min",
    "None","All","Max","Min"
  ),levels=c("Min","None","All","Max")),
  numParallel = factor(c(
      "1 Parallel","1 Parallel","1 Parallel","1 Parallel",
      "2 Parallel","2 Parallel","2 Parallel","2 Parallel",
      "4 Parallel","4 Parallel","4 Parallel","4 Parallel"
    ),
    levels=c("1 Parallel","2 Parallel","4 Parallel")),
  bandwidth = append(t1b,append(t2b,t4b)))
ggplot(data=df, aes(x=numParallel, y=bandwidth, fill=opts)) +
  geom_bar(stat="identity", position=position_dodge(), colour="black") +
  theme_bw() +
  xlab("Number of Parallel Connections") +
  ylab("Bandwidth (Gbps)") +
  scale_fill_manual(values=c("#6497b1","#005b96","#03396c","#011f4b"))
ggsave("analysis/tcp-opts.pdf",width=7,height=6)