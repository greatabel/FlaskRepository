测试是在osx平台，实际可以在（windows/osx/linux系统上运行）

1.
安装python3.6 以上版本

2. 
安装pip3 

3.
可选（创建python3虚拟目录，隔绝不同版本库之间相互影响）
https://docs.python.org/zh-cn/3/tutorial/venv.html

4.


terminal底下进入工程目录下，在requirements.txt同级目录下运行：
pip3 install --upgrade -r requirements.txt


5.
terminal 里面cd 到 b9792music_recommend 文件夹

then enter virtual environment:
Windows run:
movie-env\Scripts\activate.bat

Unix/MacOS run:
source movie-env/bin/activate

6.

新开一个命令行，进入虚拟环境，进入 b9792music_recommend/i2website下，运行
python3 app.py


7.
浏览器访问 http://127.0.0.1:8000/
