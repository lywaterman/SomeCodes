package main

import (
	"crypto/tls"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
)

func main() {
	//从环境变量中获取监听端口号，如果没有设置则使用默认值
	port := os.Getenv("LISTEN_PORT")
	if port == "" {
		port = "28888"
	}

	ngrokUrl := os.Getenv("NGROK_URL")
	if ngrokUrl == "" {
		ngrokUrl = "https://3fd3-8-210-47-108.ngrok-free.app/"
	}

	//将所有请求转发到此目标URL
	target, err := url.Parse(ngrokUrl)
	if err != nil {
		log.Fatalf("Error parsing target URL: %s", err)
	}

	//创建自定义传输
	transport := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}

	//创建反向代理服务器
	proxy := httputil.NewSingleHostReverseProxy(target)
	proxy.Transport = transport

	//使用自定义处理函数包装反向代理
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Request received at: %s", r.URL.Path)

		//更改请求头中的Host字段，将其设置为要代理到的目标域名
		r.Host = target.Host

		//将请求转发到后端服务器
		proxy.ServeHTTP(w, r)
	})

	//启动HTTP服务器
	log.Printf("Listening on port %s..., url is %s", port, ngrokUrl)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
