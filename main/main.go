package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	//加载服务器配置
	networkConfig := readJsonFromFileAndGetMap("./config/config.json")

	//加载模板
	templates := loadTemplates()

	//服务器启动
	server := http.Server{
		Addr: fmt.Sprintf("%s:%s", networkConfig["ip"], networkConfig["port"]),
		//配置默认是"localhost:8080",
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

	http.Handle("/css/", http.FileServer(http.Dir("res")))
	http.Handle("/img/", http.FileServer(http.Dir("res")))
	http.Handle("/script/", http.FileServer(http.Dir("res")))

	//加载json数据
	http.HandleFunc("/json_data", func(writer http.ResponseWriter, request *http.Request) {

		//data := readJsonFromFile("./res/json_data/app.json")
		//data := readJsonFromFile("./res/json_data/app2.json")
		data := readJsonFromFile("./res/json_data/out.json")
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
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		fmt.Println(err)
	}

	return string(data)
}

//从json文件中读取并转换为map类型
func readJsonFromFileAndGetMap(fileName string) map[string]interface{} {
	data := readJsonFromFile(fileName)
	res := make(map[string]interface{})
	json.Unmarshal([]byte(data), &res)
	return res
}
