# HXDataScience

1.
安装python3.6 以上版本

2. 
安装pip3 

如果是osx/linux，可以跳过 步骤3，4，因为我已经打包了虚拟环境,
虚拟环境在web_platform的 mlsystem-env

3.
可选（创建python3虚拟环境，隔绝不同版本库之间相互影响）
https://docs.python.org/zh-cn/3/tutorial/venv.html

create virtual environment:
python3 -m venv  mlsystem-env


4.
(如果进行了步骤3， 就进入虚拟环境，执行后面的，没有就直接执行4)
terminal底下进入工程目录下，在requirements.txt同级目录下运行：
pip3 install --upgrade -r requirements.txt

5.
命令行进入web_platform目录,执行下列命令，进入虚拟环境
then enter virtual environment:
Windows run:
mlsystem-env\Scripts\activate.bat

Unix/MacOS run:
source mlsystem-env/bin/activate


6.
在虚拟环境中，命令行进入web_platform目录，执行：
python3 wsgi.py

7. 
本机测试
浏览器访问首页: http://127.0.0.1:5000/home

如果提供接口给外部访问，确保操作系统防火墙运行了权限和5000端口等，
然后让用户访问 http://服务器ip:5000/home



