# BScanner
一直没有顺手的扫描器，那就自己写一个吧

# 下面是参数说明

## 必选参数：

- -u 扫描目录
- --test 测试，现在默认扫描http://testphp.vulnweb.com/(用的看到demo,如果侵权请告知我)

## 可选参数：

- -t,--thread   线程数，默认为30，可选(1~50)
- -e,--ext  是否使用文件类型拓展，默认为关闭，现在的拓展为['.bak','.orig','.inc','.swp','~']
- -f,--filename  字典拓展，默认为./dic/php.txt
- -s,--sleeptime 每次请求的睡眠时间，由于是多线程的，所以这里大一点儿也没关系. 默认1（0-10）
- -l    记录log的等级，默认为2（1-5）
        分别为 1：CRITICAL
               2：ERROR
               3：WARN
               4：INFO
               5：DEBUG

# 目录结构
```
BScanner
├─dic
│      ASP.txt
│      ASPX.txt
│      DIR.txt
│      JSP.txt
│      MDB.txt
│      PHP.txt
│      test.txt
│
├─lib
│      bruter.py
│      config.py
│      log.py
│      options.py
│      wordbuild.py
│      __init__.py
│
└─log
        test.log
        __init_.py
```
- dic 目录是默认字典，现在只有默认的一部分字典，支持拓展
- lib lib为核心文件目录
    - bruter.py 请求网页函数
    - config.py 配置文件，里面带有ua,和版本设置
    - log.py 处理log日志的地方，还很粗糙
    - options.py 处理参数，执行多线程扫描任务
    - wordbulid.py 处理字典，加入队列
- log log日志文件夹，默认log文件为域名+.log

# 更新日志
- V1.0 2016/06/29 基础框架完成
- V1.1 2016/06/29 加入延时，并修复拓展文件类型
- V1.2 2016/06/29 修改延时默认为1，并修复部分bug
- V1.3 2016/06/30 代码重构
- V1.3.1 2016/06/30 修改.gitignore，修复部分bug
- V1.3.2 2016/07/01 加入log
- V1.3.3 2016/07/01 添加部分log记录
- V1.3.4 2016/07/01 添加部分log记录
- V1.3.5 2016/07/02 添加延时判断
- V1.3.6 2016/07/02 修复bug
- V1.3.7 2016/08/20 修复了进度条