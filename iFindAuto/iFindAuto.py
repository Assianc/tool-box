import datetime
import time
import pyautogui
import psutil

# 日历
calendar_site = (180, 245)
calendar_x = [150, 205, 260, 315, 370, 425, 480]
calendar_y = [410, 455, 500, 545, 590, 635]


def close_excel_processes():
    # 关闭运行的Excel
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'EXCEL.EXE':
            proc.kill()


def save_data(start, file_name):
    # 提取数据
    extract_data = (90, 190)

    # 导出
    export_data = (245, 190)
    export_excel = (285, 230)

    # 保存
    file_site = (900, 180)
    file_path = r"D:\ths"
    text_box = (727, 655)
    save = (1145, 755)

    # 1.点击截至日期框
    pyautogui.click(calendar_site[0], calendar_site[1])
    # 2.点击日期
    pyautogui.click(calendar_x[start[0]], calendar_y[start[1]])
    # 3.点击提取数据
    pyautogui.click(extract_data[0], extract_data[1])
    time.sleep(5)
    # 4.导出数据
    # 循环，直到按钮可点击
    flag = 0
    while True:
        # 获取鼠标指针下像素的颜色
        color = pyautogui.pixel(export_data[0], export_data[1])

        # 检查按钮是否可点击
        if color == (155, 207, 242):
            color_extract = pyautogui.pixel(24, 378)
            if color_extract != (217, 231, 254) and flag < 3:
                pyautogui.click(extract_data[0], extract_data[1])
                flag = flag + 1
                time.sleep(1)
                if flag == 3:
                    print(file_name)
                    return 0
            else:
                # 按钮可点击
                pyautogui.click(export_data[0], export_data[1])
                break

    pyautogui.click(export_excel[0], export_excel[1])

    # 保存数据到excel
    # 将鼠标移动到文本框的位置
    # pyautogui.moveTo()
    # 单击鼠标左键以选中文本框
    pyautogui.click(text_box[0], text_box[1])
    # 输入 `Ctrl+A` 快捷键
    pyautogui.hotkey('ctrl', 'a')
    # 文件名
    pyautogui.typewrite(file_name)
    pyautogui.click(save[0], save[1])

    # 循环，直到按钮可点击
    while True:
        # 获取鼠标指针下像素的颜色
        color = pyautogui.pixel(1900, 18)

        # 检查按钮是否可点击
        if color == (232, 237, 241):
            time.sleep(3)
            # 按钮可点击
            pyautogui.click(1885, 35)
            break
    # close_excel_processes()


def main():
    pyautogui.PAUSE = 1.5

    start_date = datetime.date(2022, 7, 15)
    end_date = datetime.date(2024, 1, 31)

    # 开始时坐标
    start = [5, 2]

    for current_date in range((end_date - start_date).days + 1):
        current_date = start_date + datetime.timedelta(days=current_date)
        if current_date.day == 2:
            if current_date.weekday() == 6:
                start[1] = 1
            else:
                start[1] = 0

        if not current_date.weekday() in [5, 6]:
            file_name = current_date.strftime("%Y%m%d")
            save_data(start, file_name)
        elif current_date.day == 1:
            pyautogui.click(calendar_site[0], calendar_site[1])
            pyautogui.click(calendar_x[start[0]], calendar_y[start[1]])

        start[0] = start[0] + 1
        if start[0] == 7:
            start[1] = start[1] + 1
            start[0] = 0


if __name__ == '__main__':
    main()
