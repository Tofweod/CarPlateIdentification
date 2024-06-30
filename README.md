# CarPlateIdentification

## Descripiton

​	基于摄像头进行的简单的车牌识别，可部署在Web应用中。其中CarPlateIdentification是Web应用，通过`RESTful API`与后端ServerEnd通信。ServerEnd是车牌识别的核心框架，实现了图像分割、图像预处理以及车牌识别等功能，其作为一个单独的模块也可用于嵌入式设备中。


## Framework

- Springboot(springboot2.7.4+java17)
- flask
- pytorch(python3.11)
- palledocr

## Usage

​	Springboot前端和flask后端相互通信，因此在使用前需要正确配置host和port
​    
- CarPlateIdentifaction
  

​	在`application.yml`中配置flask，默认设置`localhost`以及`5001`端口
​    

- flask
  

​	在`ServerEnd`目录下的`config.py`里配置Springboot，默认设置`localhost`以及`44906`端口



- 使用


​	分别启动ServerEnd后端和CarPlateIdentifcation前端，在网页中输入`localhost:44906`即可开始使用，默认已拥有摄像头设备

## Build

- 在Pycharm打开ServerEnd目录，（可选）创建虚拟环境venv或使用conda环境，执行`pip install -r requirements.txt`安装相关依赖，

- 在IDEA中打开CarPlateIdentifaction目录，执行`maven install`命令，然后运行`src.main.java.com.example.carplateidentification.CarPlateIdentification.java`
- 

## LICENCSE

​	本项目基于Apache-2.0-license,如有疑问请联系

