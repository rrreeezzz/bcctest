#!/usr/bin/python3
#
# Computes latency of go function unsing BPF

from bcc import BPF
from time import sleep
import os

bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/blkdev.h>

BPF_HISTOGRAM(dist);
BPF_HASH(start);

int start_f(struct pt_regs *ctx) {
    u64 ts, key = 0;

    ts = bpf_ktime_get_ns();
    start.update(&key, &ts);
    return 0;
}

int end_f(struct pt_regs *ctx) {
    u64 *tsp, delta, key = 0;

    tsp = start.lookup(&key);
    if (tsp != 0) {
        delta = bpf_ktime_get_ns() - *tsp;
        dist.increment(bpf_log2l(delta/1000));
    }
    return 0;
}
"""

path = os.getcwd() + "/hello"
b = BPF(text=bpf_text)
b.attach_uprobe(name=path, sym="main.concatStr", fn_name="start_f")
b.attach_uretprobe(name=path, sym="main.concatStr", fn_name="end_f")

dist = b.get_table("dist")
while 1:
    dist.print_log2_hist("usecs")
    dist.clear()
    sleep(1)
