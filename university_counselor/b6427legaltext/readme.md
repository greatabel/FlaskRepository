step1:

安装python3 和 pip3


step2:
在命令行中进入到 b6427legaltext 文件夹，然后执行：
pip3 install --upgrade -r requirements.txt

step3（可选）:
如果测试数据过多，想清空数据库，可以直接删除掉b6427legaltext文件夹下面 legaltext.db
然后在命令行中执行:  python3 i0create_db.py
就可以重新构建数据库结构

step4:
运行网站前后端服务，需要在命令行中来到 b6427legaltext 文件夹，然后执行：
python3 app.py

访问网站：
添加功能在： http://127.0.0.1:5000/add
搜索功能在： http://127.0.0.1:5000/search