package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	//加载模板
	templates := loadTemplates()

	//服务器启动
	server := http.Server{
		Addr: "localhost:8080",
	}

	//模式串匹配并载入网页
	http.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
		//获取要被解析的html模板名,做切片去掉斜线
		fileName := request.URL.Path[1:]
		t := templates.Lookup(fileName)

		if t != nil {
			err := t.Execute(writer, nil)

			if err != nil {
				log.Fatalln(err.Error())
			}
		} else {
			writer.WriteHeader(http.StatusNotFound)
		}
	})

	//载入css、其他资源和脚本文件

	http.Handle("/css/", http.FileServer(http.Dir("src")))
	http.Handle("/img/", http.FileServer(http.Dir("src")))
	http.Handle("/script/", http.FileServer(http.Dir("src")))

	//加载json数据
	http.HandleFunc("/json_data", func(writer http.ResponseWriter, request *http.Request) {
		//writer.Write([]byte("我们的歌声"))

		data := readJsonFromFile("./src/json_data/app.json")
		//fmt.Println(data)

		writer.Header().Set("Content-Type", "application/json")

		writer.Write([]byte(data))

	})

	server.ListenAndServe()
}

//加载html模板
func loadTemplates() *template.Template {
	result := template.New("templates")
	result, err := result.ParseGlob("templates/*.html")

	template.Must(result, err)

	return result
}

//从json文件中读取
func readJsonFromFile(fileName string) string {
	data, err := ioutil.ReadFile("./src/json_data/app.json")
	if err != nil {
		fmt.Println(err)
	}

	return string(data)
}
