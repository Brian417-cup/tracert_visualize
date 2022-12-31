package main

type Graph struct {
	Nodes      []Nodes      `json:"nodes"`
	Links      []Links      `json:"links"`
	Categories []Categories `json:"categories"`
}
type Nodes struct {
	ID         string  `json:"id"`
	Name       string  `json:"name"`
	SymbolSize float64 `json:"symbolSize"`
	X          float64 `json:"x"`
	Y          float64 `json:"y"`
	Value      float64 `json:"value"`
	Category   int     `json:"category"`
}
type Links struct {
	Source string `json:"source"`
	Target string `json:"target"`
}
type Categories struct {
	Name string `json:"name"`
}
