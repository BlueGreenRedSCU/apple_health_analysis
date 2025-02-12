#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2025/2/12 2:54 PM
# @Author : ritong.lan
# @File : analyze_hilking_mac.py

import re
from datetime import datetime
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Songti']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False

def main(path):
    # import matplotlib.font_manager as fm
    #
    # # 获取所有可用字体
    # for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    #     print(font)
    #
    # # 获取所有可用字体
    # for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    #     print(font)

    time, elevation = [], []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        current_ele, next_ele = -10000, 0
        ele_increase, ele_decrease = 0, 0

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line.startswith("<trkpt"):
                continue

            # 找时间
            time_pattern = r"<time>(.*)</time>"
            find_time = re.search(time_pattern, stripped_line)
            dt = datetime.strptime(find_time.group(1), "%Y-%m-%dT%H:%M:%SZ")
            timestamp = int(dt.timestamp())
            time.append(timestamp)

            # 找海拔
            elevation_pattern = r"<ele>(.*)</ele>"
            find_elevation = re.search(elevation_pattern, stripped_line)
            next_ele = float(find_elevation.group(1))
            elevation.append(next_ele)

            if current_ele == -10000:
                current_ele = next_ele
                continue
            if current_ele >= next_ele:
                ele_decrease += (current_ele - next_ele)
            else:
                ele_increase += (next_ele - current_ele)
            current_ele = next_ele

    draw_plot_for_time_and_elevation(time, elevation, ele_increase, ele_decrease)


def draw_plot_for_time_and_elevation(time, elevation, ele_increase, ele_decrease):
    plt.figure(figsize=(8, 6))

    plt.text(0.5, 0.5, r"累计上升：{} 米/n累计下降：{} 米".format(ele_increase, ele_decrease), fontsize=12, ha='center', va='center')

    plt.scatter(time, elevation, c='b', marker='o', label="Data Points")  # 绘制散点图
    plt.xlabel("Time (s)")  # X 轴标签
    plt.ylabel("Elevation (m)")  # Y 轴标签
    plt.title("Scatter Plot of Longitude vs Latitude")  # 标题
    plt.legend()
    plt.grid()

    # 显示图像
    plt.show()


if __name__ == "__main__":
    file_path = "./activity_data/route_2025-02-01_3.22pm.gpx"
    main(file_path)