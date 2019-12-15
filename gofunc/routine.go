package main

import (
	"fmt"
	"time"
)

func main() {

	t := time.NewTicker(1 * time.Second)
	done := make(chan bool)

	go func() {
		for {
			select {
			case _ = <-t.C:
				_ = concatStr("a", "b")
			case <-done:
			}
		}
	}()

	time.Sleep(5 * time.Second)
	done <- true
}

func concatStr(s1, s2 string) string {
	return fmt.Sprintf("%s%s", s1, s2)
}
