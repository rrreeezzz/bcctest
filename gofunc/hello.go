package main

import "fmt"

func main() {
	fmt.Println(concatStr("Hello", " world!"))
}

func concatStr(a, b string) string {
	return fmt.Sprintf("%s%s", a, b)
}
