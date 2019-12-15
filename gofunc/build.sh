#!/bin/bash

# no inlining for tests purposes
go build -gcflags '-l' hello.go
go build -gcflags '-l' routine.go
