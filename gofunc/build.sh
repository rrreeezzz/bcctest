#!/bin/bash

# no inlining
go build -gcflags '-l' hello.go
