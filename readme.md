# 爬取指定咸鱼用户发布文章
获取其文章链接，点赞数，浏览量，信用评价及主页照片并写入文档

## 爬取过程中遇到的问题
- 咸鱼的风控规则会检测当前浏览器行为，当发现是无头浏览器时不会有数据返回，针对该问题使用playwright的有头模式处理
- 同一ip频繁访问也会认定为非人类行为，进而会触发风控，解决办法采用代理ip访问+页面随机停顿模拟真人行为

## 文件说明
- 脚本每次执行都会生成一个 linksYYYY_MM_DD.csv的文件和pic文件中以帖子专业命名的帖子图片
- linksYYYY_MM_DD.csv中第一部分是写入帖子up主当前页面的信用评价，获取发表时间和评语写入，第二部分的链接是帖子up所有帖子链接，第三部分是帖子的想要的人数喜欢
   的人数已经帖子文章内容
- proxy_ip.txt 由于咸鱼的风控规则会检测当前的ip访问频率，该文件中存储了代理ip池用以绕过风控规则，目前代理ip书写方式如下   <p style="color:yellow;">*该功能暂未实现*</p>

   ```bash
    IP1:port1
    IP2:port2
   ```

## 使用说明
- 项目下载到本地后执行如下脚本安装依赖
   ```bash
      pip install -r requirements.txt
   ```  
- 执行如下脚本运行程序
   ```bash
      python get_data.py
   ```  