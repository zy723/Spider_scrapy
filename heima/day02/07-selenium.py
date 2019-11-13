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





if __name__ == '__main__':
    # selenium_test()
    selenium_test02()
