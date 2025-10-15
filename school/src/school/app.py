"""
校园网络登录助手 - 简化稳定版
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from playwright.sync_api import sync_playwright
import threading

class SchoolApp(toga.App):
    def __init__(self):
        super().__init__(
            formal_name="校园网络登录助手",
            app_id="com.school.network"
        )
        self.is_started = False

    def startup(self):
        # 创建主界面
        main_box = toga.Box(style=Pack(direction=COLUMN, margin=20))

        # 标题
        title_label = toga.Label(
            "校园网络登录助手",
            style=Pack(font_size=16, font_weight="bold", text_align="center", margin_bottom=20)
        )

        # 按钮
        self.action_button = toga.Button(
            '启动浏览器并访问校园网',
            on_press=self.toggle_browser,
            style=Pack(padding=10, margin=10)
        )

        # 状态显示
        self.status_label = toga.Label(
            '点击按钮启动浏览器访问校园网络',
            style=Pack(text_align="center", margin=10)
        )

        # 组装界面
        main_box.add(title_label)
        main_box.add(self.action_button)
        main_box.add(self.status_label)

        # 显示窗口
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def toggle_browser(self, widget):
        """切换浏览器状态"""
        if not self.is_started:
            # 启动浏览器
            self.action_button.text = '关闭浏览器'
            self.status_label.text = '正在启动浏览器...'
            self.is_started = True

            # 在新线程中启动浏览器
            thread = threading.Thread(target=self.open_browser)
            thread.daemon = True
            thread.start()
        else:
            # 关闭浏览器
            self.action_button.text = '启动浏览器并访问校园网'
            self.status_label.text = '浏览器已关闭'
            self.is_started = False

    def open_browser(self):
        """打开浏览器并访问网站"""
        playwright = None
        browser = None

        try:
            # 启动 Playwright
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()

            # 更新状态
            self.update_status('正在访问校园网络...')

            # 访问网站
            page.goto('http://210.45.92.67/')
            self.update_status('校园网络访问成功！')

            # 等待用户手动关闭浏览器
            print("浏览器已打开，请在浏览器窗口中操作...")

        except Exception as e:
            error_msg = f'操作失败: {str(e)}'
            print(error_msg)
            self.update_status(error_msg)
            self.is_started = False
            self.action_button.text = '启动浏览器并访问校园网'

        # 注意：这里不自动关闭浏览器，让用户手动关闭

    def update_status(self, message):
        """安全地更新状态标签"""
        def safe_update():
            self.status_label.text = message

        # 在主线程中执行UI更新
        self.main_window.app._impl.loop.call_soon_threadsafe(safe_update)

def main():
    return SchoolApp()

if __name__ == "__main__":
    app = main()
    app.main_loop()