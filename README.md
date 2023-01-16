# 效果预览
用networkx做一个tracert路由跟踪可视化界面，并计算相关的网络参数  

完整视频最终演示：https://www.bilibili.com/video/BV1mx4y1u7zj/?vd_source=cc8f9c73a4be52090ddab10fcc659535

![tracert_visualize](https://github.com/Brian417-cup/tracert_visualize/blob/main/imgs/img1.png "tracert_visualize")  

![tracert_visualize](https://github.com/Brian417-cup/tracert_visualize/blob/main/imgs/img2.png "tracert_visualize")  

![tracert_visualize](https://github.com/Brian417-cup/tracert_visualize/blob/main/imgs/img3.png "tracert_visualize")  

![tracert_visualize](https://github.com/Brian417-cup/tracert_visualize/blob/main/imgs/img4.png "tracert_visualize")  

# 工程介绍  

## main分支
### 环境要求 Python 3.8
### tracert模块
  点击运行./tracert/main.py即可获取所有位于constants.py中的所有目标网址  
### combine模块
  点击运行./combine/main.py合并其他源的tracert结果  
### attribute模块
  利用Networkx库，主要针对无向图网络的网络直径、同配系数等参数计算
### main.py
  点击运行main.py,导出ECharts Graph图类型支持的JSON序列化格式，默认保存在./export/下
 
 
 ##  visualize_complex分支
 ###  环境要求 GoLang >= 1.14
 ###  运行方式
 将main分支导出的源数据放入./res/json_data/下，运行main.go启动服务器，之后在服务器中输入"http://localhost:8080/network_visualize_main.html"即可出现可视化页面
 ###  配置修改
 #### 网络修改
 ./config/config.json中修改"port"和./res/script/config.js中修改ip和port的值
 #### 结点修改
 鉴于ECharts在网页中显示太多结点会出现卡顿的情况，这里默认只展示前800个统计到的结点，若需修改，可在可在./res/script/config.js中修改maxNodesCnt的值再重新运行即可
 
 #  可执行程序  
 
 本项目有一个已编译好的版本，你可以选择直接下载查看效果 https://drive.google.com/drive/folders/1XJ2pbWurrPPn7a3eEqkzG1u6TD5I_GvQ?usp=share_link
