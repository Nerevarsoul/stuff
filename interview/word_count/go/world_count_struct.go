package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)


type Pair struct {
    Key string
    Value int
}

func addWord(word string, pairList []Pair) []Pair {
	fmt.Println(word)

    for i, pair := range pairList {

    	if pair.Key == word {
    		pair.Value += 1
    		pairList[i] = pair
    		return pairList
	    }
	}

    pairList = append(pairList, Pair{Key: word, Value: 1})

    return pairList
}

func main() {
	file, err := os.Open("test.txt")

	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	var result []Pair

	for scanner.Scan() {
		for _, word := range strings.Fields(scanner.Text()) {

			result = addWord(word, result)
		}
	}

	fmt.Println(result)
}
