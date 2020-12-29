package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
)

func main() {
	file, err := os.Open("test.txt")

	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	result := make(map[string]int)

	for scanner.Scan() {
		for _, word := range strings.Fields(scanner.Text()) {
			if _, ok := result[word]; ok {
				result[word] += 1
			} else {
				result[word] = 1
			}
		}
	}

	fmt.Println(result)
}
