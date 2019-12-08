#!/usr/bin/bpftrace

uprobe:./hello:"main.concatStr"
{
    @start=nsecs;
}

uretprobe:./hello:"main.concatStr"
{
    printf("func took %d ms\n", (nsecs - @start) / 1000);
}
