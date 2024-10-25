# 你是一个Python编程专家，要完成一个网页保存的脚本，具体步骤如下：打开网页：https://www.tisi.org/?page_id=28888&page={pagenumber}(参数pagenumber的值是从1到14)；
# 定位网页中所有class="title text-with-shadow"的div标签，定位div标签中的a标签，提取其href属性值，作为网页URL；
# 提取a标签的文本内容，作为网页标题；用playwright来控制Chrome浏览器，调用Chrome浏览器的“打印-另存为PDF”功能，将这个网页打开，保存为PDF文件
# 保存在文件夹：F:\研报下载，PDF文件名为网页标题名；
# 注意：每一步都要输出信息到屏幕上网页标题名称中包含“｜”等特殊符号，不符合Windows系统文件命名规范，在保存PDF文件之前要对标题名进行处理；
# 使用 async_playwright 来代替 sync_playwright，并确保所有操作都在异步上下文中进行

import asyncio
import os
import re
from playwright.async_api import async_playwright

async def save_page_as_pdf(page, url, title):
    await page.goto(url)
    print(f"正在打开网页: {url}")
    
    # 处理文件名，移除不合法字符
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
    pdf_path = os.path.join(r".\研报下载", f"{safe_title}.pdf")
    
    print(f"正在保存PDF: {pdf_path}")
    await page.pdf(path=pdf_path)
    print(f"PDF保存成功: {pdf_path}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for page_number in range(1, 3):  # 1到14页
            url = f"https://www.tisi.org/?page_id=28888&page={page_number}"
            await page.goto(url)
            print(f"正在处理第 {page_number} 页")

            # 等待页面加载完成
            await page.wait_for_load_state('networkidle')

            # 使用 evaluate 直接在页面上下文中执行 JavaScript 来获取所需信息
            articles = await page.evaluate('''
                () => {
                    const divs = document.querySelectorAll('div.title.text-with-shadow');
                    return Array.from(divs).map(div => {
                        const a = div.querySelector('a');
                        return a ? {href: a.href, title: a.innerText} : null;
                    }).filter(item => item !== null);
                }
            ''')

            for article in articles:
                print(f"找到文章: {article['title']}")
                await save_page_as_pdf(page, article['href'], article['title'])

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
