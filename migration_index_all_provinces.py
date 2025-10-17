# -*- coding: utf-8 -*-
import requests  # 导入请求模块
import json  # 导入json模块
import time  # 导入时间模块
import xlsxwriter

# 省级行政单位代码字典
ProvinceCode = {
    '北京市': 110000, '天津市': 120000, '河北省': 130000, '山西省': 140000, '内蒙古自治区': 150000,
    '辽宁省': 210000, '吉林省': 220000, '黑龙江省': 230000,
    '上海市': 310000, '江苏省': 320000, '浙江省': 330000, '安徽省': 340000, '福建省': 350000, '江西省': 360000,
    '山东省': 370000,
    '河南省': 410000, '湖北省': 420000, '湖南省': 430000, '广东省': 440000, '广西壮族自治区': 450000, '海南省': 460000,
    '重庆市': 500000, '四川省': 510000, '贵州省': 520000, '云南省': 530000, '西藏自治区': 540000,
    '陕西省': 610000, '甘肃省': 620000, '青海省': 630000, '宁夏回族自治区': 640000, '新疆维吾尔自治区': 650000,
    '台湾省': 710000, '香港特别行政区': 810000, '澳门特别行政区': 820000
}


def migration_index_all_provinces(FileTittle, classname):
    """
    获取所有省级行政单位的迁徙规模指数
    FileTittle: 文件标题
    classname: 类别，这里应该是'province'
    """
    # 创建一个workbook
    workbook = xlsxwriter.Workbook(f'{FileTittle}.xlsx')

    # 遍历所有省份
    for province_name, province_code in ProvinceCode.items():
        print(f'正在处理 {province_name} 的数据...')

        # 为每个省份创建一个worksheet
        # 工作表名称不能超过31个字符，且不能包含特殊字符
        sheet_name = province_name[:31]  # 限制工作表名称长度
        worksheet = workbook.add_worksheet(sheet_name)

        # 设置表头
        worksheet.write(0, 0, '日期')
        worksheet.write(0, 1, '迁入规模指数')
        worksheet.write(0, 2, '迁出规模指数')

        # 获取迁入数据
        url_in = f'http://huiyan.baidu.com/migration/historycurve.jsonp?dt={classname}&id={province_code}&type=move_in'
        print(f'{province_name}迁入数据:{url_in}')

        try:
            response_in = requests.get(url_in, timeout=10)
            time.sleep(3)  # 添加延时，避免请求过快
            r_in = response_in.text[4:-1]  # 去头去尾
            data_dict_in = json.loads(r_in)  # 字典化

            if data_dict_in['errmsg'] == 'SUCCESS':
                data_list_in = data_dict_in['data']['list']
            else:
                print(f'{province_name}迁入数据获取失败')
                data_list_in = {}
        except Exception as e:
            print(f'{province_name}迁入数据请求失败: {e}')
            data_list_in = {}

        # 获取迁出数据
        url_out = f'http://huiyan.baidu.com/migration/historycurve.jsonp?dt={classname}&id={province_code}&type=move_out'
        print(f'{province_name}迁出数据:{url_out}')

        try:
            response_out = requests.get(url_out, timeout=10)
            time.sleep(3)  # 添加延时，避免请求过快
            r_out = response_out.text[4:-1]  # 去头去尾
            data_dict_out = json.loads(r_out)  # 字典化

            if data_dict_out['errmsg'] == 'SUCCESS':
                data_list_out = data_dict_out['data']['list']
            else:
                print(f'{province_name}迁出数据获取失败')
                data_list_out = {}
        except Exception as e:
            print(f'{province_name}迁出数据请求失败: {e}')
            data_list_out = {}

        # 处理并写入数据
        # 获取所有日期（合并迁入和迁出的日期）
        all_dates = set(data_list_in.keys()) | set(data_list_out.keys())
        sorted_dates = sorted(all_dates)

        row = 1  # 从第1行开始（第0行是表头）
        for date in sorted_dates:
            # 写入日期
            worksheet.write(row, 0, str(date))

            # 写入迁入规模指数
            in_index = data_list_in.get(date, 0)
            worksheet.write(row, 1, float(in_index))

            # 写入迁出规模指数
            out_index = data_list_out.get(date, 0)
            worksheet.write(row, 2, float(out_index))

            row += 1

        print(f'{province_name}数据已保存，共{row - 1}天的数据')
        print('-' * 50)

    workbook.close()
    print('所有省份数据已保存完成')


if __name__ == "__main__":
    migration_index_all_provinces('全国各省份迁徙规模指数', 'province')
    print('全部完成')
