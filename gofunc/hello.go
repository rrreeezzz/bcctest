package main

import "fmt"

func main() {
    fmt.Println("Hello world !")

    fmt.Println(concatStr("a", "b"))
}

func concatStr(s1, s2 string) string {
    return fmt.Sprintf("%s%s", s1, s2)
}

