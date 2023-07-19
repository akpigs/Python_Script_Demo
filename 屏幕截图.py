import time
import os
from PIL import ImageGrab

def capture_screenshot():
    # 创建保存截图的目录
    if not os.path.exists("images"):
        os.makedirs("images")

    # 设置截图计数器
    count = 1

    try:
        while count <= 1000:
            # 获取当前时间戳
            timestamp = int(time.time())

            # 拼接保存截图的文件路径
            filename = f"images/screenshot_{timestamp}.png"

            # 使用Pillow库的ImageGrab模块进行屏幕截图
            try:
                screenshot = ImageGrab.grab()
                # 保存截图
                screenshot.save(filename)
                print(f"Screenshot saved: {filename}")
                count += 1
            except OSError as e:
                print(f"Failed to capture screenshot: {e}")

            # 每隔1秒进行下一次截图
            time.sleep(8)

    except KeyboardInterrupt:
        print("Screenshot capturing stopped by user.")

capture_screenshot()
