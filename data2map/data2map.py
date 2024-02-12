import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

# 设置excel数据
file_path = 'data2map.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 将数据转换为列表
datas = df.values.tolist()
namemap = {
    "南京市": "南京"
}
# 创建地图对象
m = Map()

# 添加数据项
m.add(
    series_name="test",
    data_pair=datas,
    maptype="江苏",
    # 添加标签选项
    label_opts=opts.LabelOpts(
        is_show=True,  # 显示标签
        formatter="{b} \n {c}",  # 自定义标签格式
        position="center",  # 设置标签位置
        font_size=6,
        # font_weight="lighter",
    ),
    is_map_symbol_show=False,  # 隐藏地图上的圆点
    name_map=namemap,
)

# 设置全局选项
m.set_global_opts(
    title_opts=opts.TitleOpts(title="data2map", is_show=False),  # 设置标题
    legend_opts=opts.LegendOpts(is_show=False),  # 隐藏series_name
    visualmap_opts=opts.VisualMapOpts(
        is_show=False,
        max_=8,  # 设置最大值
        range_color=["#E8E8E8", "#E12D5A"],  # 设置颜色范围
        is_piecewise=False,  # 设置分段显示
        pieces=[  # 设置分段范围和颜色
            {"min": 1, "max": 1000, "color": "#FFE4E1"},  # 粉红色（最低）
            {"min": 1000, "max": 2000, "color": "#FFA07A"},  # 浅鲑鱼色
            {"min": 2000, "max": 3000, "color": "#FF6347"},  # 番茄色
            {"min": 3000, "max": 4000, "color": "#FF4500"},  # 橙红色
            {"min": 4000, "max": 5000, "color": "#FF0000"},  # 红色（最高）
            {"value": 0, "color": "#FFFFFF"},  # 设置 0 值为白色
        ],
    ),

)

make_snapshot(snapshot, m.render("data2map.html"), "data2map.png")
