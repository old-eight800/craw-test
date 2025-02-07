#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : test.py
Description      : 
Time             : 2025/01/12 14:55:05
Author           : AllenLuo
Version          : 1.0
'''


import os
import fnmatch
from loguru import logger
from playwright.sync_api import sync_playwright
import random
import re
import datetime
import time
import requests
import csv
import glob
import traceback


def get_new_article(url):
  """
  获取最新的文章帖子
  """
  # 使用 Playwright 打开浏览器并获取页面内容
  with sync_playwright() as p:
      # 启动浏览器（默认为 Chromium）
      browser = p.chromium.launch(headless=False)  # headless=False 表示显示浏览器窗口
      page = browser.new_page(viewport= {'width': 1280, 'height': 1024 })
      # 访问目标网页
      logger.info(f"开始分析{url}")
      index = https_links.index(url)
      page.goto(url)
      # 等待页面加载完成（可以根据需要调整等待时间或条件）
      page.wait_for_load_state("networkidle")
      page.wait_for_timeout(random.uniform(2000, 5000))
      # 修改所有链接的 target 属性
      page.evaluate(
          """
          document.querySelectorAll("a[target='_blank']").forEach(link => {
              link.target = "_self";
          });
          """
      )

      # 访问主页
      user_selector = "#content > div.item-container--yLJD5VZj > div.item-user-container--fbTUeNre > a > div > div.item-user-info-text--tKOlwunK > div.item-user-info-main--iHQtqVC2 > div.item-user-info-nick--rtpDhkmQ"

      page.click(user_selector)
      page.wait_for_load_state("networkidle")
      page.wait_for_timeout(random.uniform(2000, 5000))
      try:
        # 获取页面中的所有链接
        links = page.eval_on_selector_all('a', 'elements => elements.map(element => element.href)')
        link_lists = []
        # 打印所有链接
        for link in links:
            if 'categoryId' in link:
              link_lists.append(link)
        logger.info(link_lists)
        with open(latest_csv_file, mode="r", newline="", encoding="utf-8") as file:
          content = file.read()
        result = [item for item in link_lists if item in content]
        user_name_seletor = "#content > div.personal--b5L38iZ7 > div > div > div > div.container--rklFh1rU > div.info--VwAm9wKs > div.infoTop--m9NGZu3u > span"
        user_name = page.query_selector(user_name_seletor).inner_text()
        if result:
           logger.info(f"{user_name}没有获取到新帖子，将爬取下一个用户帖子")
        else:
              page.get_by_text("信用及评价").nth(1).click()
              page.wait_for_timeout(random.uniform(2000, 5000))
              try:
                rate_element = page.query_selector(':has-text("信用及评价")')
                if rate_element:
                  result_list=[]
                  evaluation_value = ['评价内容']
                  evaluation_time = ['评价时间']

                  pattern = r'([^\n]+)\n(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
                  # 查找所有匹配
                  matches = re.findall(pattern, rate_element.inner_text().strip())
                  if matches:
                    for match in matches:
                      text_before_time = match[0] # 时间前面的文字
                      time_str = match[1]  # 时间本身
                      logger.info(f"评价内容: {text_before_time}")
                      logger.info(f"评价时间: {time_str}")
                      evaluation_value.append(text_before_time)
                      evaluation_time.append(time_str)
                      result_list.append(f'{text_before_time}')
                      result_list.append(f'{time_str}')
              except BaseException as e:
                  logger.warning(e)

              logger.info(f"检测到{user_name}更新了帖子，将爬取并写入文件")
              # with open(f"links{today}.csv", mode="a", newline="", encoding="utf-8") as file:
              #     writer = csv.writer(file)
              #     # 写入表头
              #     writer.writerow([major_name[index],user_name])

              with open(f"links{today}.csv", mode="a", newline="", encoding="utf-8") as file:
                  writer = csv.writer(file)
                  # 写入表头
                  writer.writerow(evaluation_time)    
                  writer.writerow(evaluation_value)    

              # 修改所有链接的 target 属性
              page.evaluate(
                  """
                  document.querySelectorAll("a[target='_blank']").forEach(link => {
                      link.target = "_self";
                  });
                  """
              )
              for i in link_lists:
                logger.info(f"开始获取{i}的数据")
                page.goto(i)
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(3000)
                count_favorite = 0
                extracted_text = '无'
                try:
                  # 获取所有 style="text-align: justify;" 的元素
                  elements = page.query_selector_all('[style="text-align: justify;"]')
                  # 提取这些元素下的文本
                  extracted_text_list = [element.inner_text() for element in elements]      
                  extracted_text = ' '.join([item.replace('\n', ' ') for item in extracted_text_list])
                except BaseException as e:
                   logger.warning(e)

                try:
                  browse_element = page.query_selector(':has-text("浏览")')
                  if browse_element:
                    full_text = browse_element.inner_text()
                    pattern = r'(\d+)\s*浏览'
                    # 在文本中搜索匹配项
                    match = re.search(pattern, full_text)
                    if match:
                      # 提取匹配的数字
                      count_favorite = match.group(1)
                    else:
                      logger.info("该文章暂未浏览")
                  else:
                    logger.info("未找到包含“浏览”文本的元素")
                except BaseException as e:
                   logger.warning(e)
                
                count_wants = 0
                try:
                  wants_element = page.query_selector(':has-text("人想要")')
                  if wants_element:
                    wants_full_text = browse_element.inner_text()
                    pattern = r'(\d+)\s*人想要'
                    # 在文本中搜索匹配项
                    match = re.search(pattern, wants_full_text)
                    if match:
                      # 提取匹配的数字
                      count_wants = match.group(1)
                    else:
                      count_wants = 0
                      logger.info("该文章暂未有人想要")
                  else:
                    logger.info("未找到包含“人想要”文本的元素")
                except BaseException as e:
                  logger.warning(e)
                  count_wants = 0
                
                with open(f"links{today}.csv", mode="a", newline="", encoding="utf-8") as file:
                  writer = csv.writer(file)
                  # 写入内容
                  writer.writerow([major_name[index],user_name,page.url,f"{count_wants}人想要",f"{count_favorite}浏览",extracted_text])
                  writer.writerow('')  #写入空行
                logger.info(f'想要的数量是：{count_wants}')
                logger.info(f'喜欢的数量是：{count_favorite}')
                logger.info(extracted_text)

                elements = page.query_selector_all('[src]')
                # 定义目标 style
                target_style = "object-fit: contain; width: 100%; height: 100%; cursor: zoom-in;"
                # 提取符合条件的 src 链接
                target_links = []
                for element in elements:
                    src = element.get_attribute('src')
                    style = element.get_attribute('style')
                    if src and src.startswith('//img.alicdn.com/bao/') and style == target_style:
                        target_links.append("https:"+src)
                # 本地保存路径script_directory
                img_path = os.path.join(script_directory, 'img', f'{major_name[index]}-{int(time.time())}.jpg')
                # 发送 HTTP 请求下载图片
                response = requests.get(target_links[0], stream=True)
                # 将图片内容写入本地文件
                with open(img_path, "wb") as file:
                  for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                logger.info(f"图片已下载到: {img_path}")
                logger.info('\n')

      except BaseException as e:
        logger.warning(f'未找到元素，开始下一个{e}')
        # 获取详细的错误信息
        error_traceback = traceback.format_exc()
        logger.info(error_traceback)

      browser.close()


if __name__ == "__main__":
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    # 获取脚本所在的目录
    script_directory = os.path.dirname(script_path)
    csv_files = glob.glob(os.path.join(script_directory, '*.csv'))
    # 按创建时间排序，获取最新的文件
    latest_csv_file = max(csv_files, key=os.path.getctime)
    # 获取当前日期
    today = datetime.date.today()
    # 获取当前日期的前一天
    pass_date = today -   datetime.timedelta(days=1)
    detail_urls_file='detail_urls.txt'
    with open(detail_urls_file) as urls_list:
      txt_content = urls_list.read()
      https_links = re.findall(r'https://[^\s]+', txt_content)
      major_name = re.findall(r'(.+?)\s+http', txt_content)
    with open("proxy_ip.txt") as file:
       proxy_ip = [i.replace('\n', '') for i in file.readlines()]
       logger.info(proxy_ip)       
    for url in https_links:
      get_new_article(url)
      random_init = random.randint(20*60, 60*30)
      logger.info(f"开始暂停{random_init}秒")
      time.sleep(random_init)

