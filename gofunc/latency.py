#!/usr/bin/python3
#
# Computes latency of go function unsing BPF

from bcc import BPF
from time import sleep
import os, argparse, subprocess

help="""help:
    ./latency.py -n binary -f function
"""

parser = argparse.ArgumentParser(
    description="Measure latency go binary (GC)",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=help)
parser.add_argument("-n", "--name",
    type=str,
    help="binary name",
    required=True)
parser.add_argument("-f", "--func",
    type=str,
    help="function to measure",
    required=True)
args = parser.parse_args()

bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/blkdev.h>

BPF_HISTOGRAM(dist);
BPF_HASH(start, u32);

int start_f(struct pt_regs *ctx) {
    u64 ts;
    u32 tid = bpf_get_current_pid_tgid();

    ts = bpf_ktime_get_ns();
    start.update(&tid, &ts);
    return 0;
}

int end_f(struct pt_regs *ctx) {
    u64 *tsp, delta;
    u32 tid = bpf_get_current_pid_tgid();

    tsp = start.lookup(&tid);
    if (tsp != 0) {
        delta = bpf_ktime_get_ns() - *tsp;
        dist.increment(bpf_log2l(delta/1000));
    }
    return 0;
}
"""

path = os.getcwd() + "/" + args.name
rets = []
out = subprocess.check_output("/usr/bin/objdump --disassemble=" + args.func \
        + " " + path \
        + " | /usr/bin/awk '/\<c3|c2\>/{print substr($1, 1, length($1)-1)}'", \
        stderr=subprocess.STDOUT, \
        shell=True).decode("utf-8").split("\n")

rets += out[:-1]
b = BPF(text=bpf_text)
b.attach_uprobe(name=path, sym=args.func, fn_name="start_f")
for elt in rets:
    b.attach_uprobe(name=path, addr=int(elt, 16), fn_name="end_f")

dist = b.get_table("dist")
while 1:
    try:
        sleep(99999999)
    except KeyboardInterrupt:
        pass

    dist.print_log2_hist("usecs")
    dist.clear()
    exit()

