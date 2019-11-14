from selenium import webdriver
import time

"""
 selenium 浏览器学习

"""


def selenium_test():
    # 创建浏览器对象
    driver = webdriver.Chrome()
    # 发送 get 请求
    driver.get('https://www.baidu.com')
    # 获取截屏
    driver.save_screenshot('baidu.png')
    # 获取渲染完毕后的数据 page_source
    data = driver.page_source

    print(data)

    # 关闭页面
    driver.close()
    # 关闭浏览器
    driver.quit()


def selenium_test02():
    driver = webdriver.Chrome()
    driver.get('https://www.json.cn')
    input_element = driver.find_element_by_id('json-src')
    input_element.send_keys('{"a":10, "b":20}')

    # 点击转换
    xml_element = driver.find_element_by_class_name('xml')
    xml_element.click()
    # time.sleep(1)
    # driver.find_element_by_xpath('/html/body/main/div[2]/div[1]/a[2]').click()
    # 关闭浏览器
    # driver.quit()

    time.sleep(3)

    driver.get('https://www.jd.com')

    # 查看页面
    print(driver.window_handles)

    # 跳转到指定页面
    driver.switch_to.window(driver.window_handles[1])

    time.sleep(3)
    driver.save_screenshot('04.png')


def selenium_test03():
    # 设置无头浏览器 Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    # 设置方法
    options.headless = True

    # 创建浏览器对象
    driver = webdriver.Chrome(options=options)

    driver.get('https://www.baidu.com')

    # 获取数据 str
    data = driver.page_source
    print(data)

    time.sleep(4)

    # 关闭浏览器
    driver.close()


def selenium_test04():
    """
    模拟登陆QQ邮箱
    :return:
    """
    # 创建浏览器对象
    driver = webdriver.Chrome()
    # 发送请求
    driver.get('https://mail.qq.com/cgi-bin/loginpage')
    # 找到iframe 切换
    ifame_element = driver.find_element_by_id('login_frame')
    # 切换进去
    driver.switch_to.frame(ifame_element)

    # 输入用户名
    driver.find_element_by_id('u').send_keys('100086')
    # 输入密码
    driver.find_element_by_id('p').send_keys('100086')
    # 点击登陆
    driver.find_element_by_id('login_button').click()

    time.sleep(2)

    # 切换为原来的ifame 以下二选一
    # driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.default_content()

    # 获取关于我们内容 属性
    our_element = driver.find_elements_by_xpath('/html/body/div/div[3]/a[5]')
    print(our_element.__str__())
    print(our_element.get_attribute('href'))

    # 关闭浏览器
    driver.close()


def selenium_test05():
    """
    执行js代码

    :return:
    """

    driver = webdriver.Chrome()

    # 发送请求
    driver.get('https://www.yuntongxun.com/')

    # 执行js代码滚动到最后
    code_js = 'window.scrollTo(0, document.body.scrollHeight)'
    driver.execute_script(code_js)

    time.sleep(1)
    driver.save_screenshot('001.png')
    driver.close()


def selenium_test06():
    """
    反爬虫 user-agent
          ip
    :return:
    """
    options = webdriver.ChromeOptions()
    # 添加user-agent
    options.add_argument('--user-agent=myuseragent')
    # 添加代理
    # options.add_argument('--proxy-server=http:127.0.0.1:1080')

    # 创建浏览器
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.baidu.com')

    # print(driver.page_source)

    # cookies = driver.get_cookies()
    # print(cookies)

    # 把cooks 转换为字典

    cooks_dic = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
    print(cooks_dic)
    time.sleep(2)
    driver.close()


if __name__ == '__main__':
    # selenium_test()
    # selenium_test02()
    # selenium_test03()
    # selenium_test04()
    # selenium_test05()
    selenium_test06()
