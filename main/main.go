package main

import (
	"html/template"
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

	http.Handle("/css/",http.FileServer(http.Dir("src")))
	http.Handle("/img/",http.FileServer(http.Dir("src")))
	http.Handle("/script/",http.FileServer(http.Dir("src")))

	server.ListenAndServe()
}

func loadTemplates() *template.Template {
	result := template.New("templates")
	result, err := result.ParseGlob("templates/*.html")

	template.Must(result, err)

	return result
}
