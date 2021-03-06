虽然本系统可以在linux/osx/windows上部署，
但是本系统文档是根据osx系统进行测试，小细节可能有出入，
请感觉细节进行修改。

1. 
whole project based on python3
(project should work at all versons above python3.5 [include python3.5] )
python3安装步骤博客：
https://www.runoob.com/python3/python3-install.html


create virtual environment:
python3 -m venv  movie-env

then enter virtual environment:
Windows run:
movie-env\Scripts\activate.bat

Unix/MacOS run:
source movie-env/bin/activate


2. 
安装pip3： 
阅读介绍博客：https://www.runoob.com/w3cnote/python-pip-install-usage.html
然后执行
pip3 install -r requirements.txt

3.
确保mysql 在你的系统上正常安装：
（偶在osx是mysql  Ver 8.0.19 for osx10.14 on x86_64 (Homebrew)）
并且服务都运行起来了

4.
在mysql执行sql: create database movie;
创建好名字叫 moive的数据库


5.
进入app目录，找到abel_import_all_to_db.py
在命令行地下运行python3 abel_import_all_to_db.py
该命令确保说有的数据建立表和用户，角色……各种数据必要操作

6.
如果你的mysql使用的不是特定的用户名和密码，
进入文件app文件夹，找到__init__.py文件，请修改下面文件：
修改改文件第7行：app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@127.0.0.1:3306/movie"
把"mysql://root@127.0.0.1:3306/movie"中的root替换为 username:password

7.
安装好依赖库和数据库服务启动，数据库相关操作脚本已经顺利执行后，
启动整体程序: 命令行底下，进入manage.py 所在目录，执行:
python3 manage.py

8.
后台管理员登录url
http://127.0.0.1:5000/admin/login/

前台用户登录和注册url：
http://127.0.0.1:5000/regist/
http://127.0.0.1:5000/login/

用户主页url：
http://127.0.0.1:5000/user/