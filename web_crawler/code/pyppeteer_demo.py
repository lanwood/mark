import asyncio
from pyppeteer import launch
from lxml import etree
async def main():
  # headless参数设为False，则变成有头模式
  browser = await launch(
      headless=False
  )
  page1 = await browser.newPage()
  # 设置页面视图大小
  await page1.setViewport(viewport={'width': 1280, 'height': 800})
  await page1.goto('https://www.toutiao.com/')
  await asyncio.sleep(2)
  # 打印页面文本
  page_text = await page1.content()
  page2 = await browser.newPage()
  await page2.setViewport(viewport={'width': 1280, 'height': 800})
  await page2.goto('https://news.163.com/domestic/')
  await page2.evaluate('window.scrollTo(0,document.body.scrollHeight)')
  page_text1 = await page2.content()
  await browser.close()
  return {'wangyi':page_text1,'toutiao':page_text}
def parse(task):
  content_dic = task.result()
  wangyi = content_dic['wangyi']
  toutiao = content_dic['toutiao']
  tree = etree.HTML(toutiao)
  a_list = tree.xpath('//div[@class="title-box"]/a')
  for a in a_list:
      title = a.xpath('./text()')[0]
      print('toutiao:',title)
  tree = etree.HTML(wangyi)
  div_list = tree.xpath('//div[@class="data_row news_article clearfix "]')
  print(len(div_list))
  for div in div_list:
      title = div.xpath('.//div[@class="news_title"]/h3/a/text()')[0]
      print('wangyi:',title)
tasks = []
task1 = asyncio.ensure_future(main())
task1.add_done_callback(parse)
tasks.append(task1)
asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))