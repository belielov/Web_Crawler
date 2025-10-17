# -*- coding: utf-8 -*-
import requests  # 导入请求模块
import json  # 导入json模块
import time  # 导入时间模块
import xlsxwriter


def migration_index_inner_mongolia(FileTittle, classname):
    """
    获取内蒙古自治区的迁徙规模指数
    FileTittle: 文件标题
    classname: 类别，这里应该是'province'
    """
    # 内蒙古自治区代码
    InnerMongolia_Code = 150000

    # 创建一个workbook
    workbook = xlsxwriter.Workbook(f'{FileTittle}.xlsx')
    worksheet = workbook.add_worksheet('Sheet')

    # 设置表头
    worksheet.write(0, 0, '日期')
    worksheet.write(0, 1, '迁入规模指数')
    worksheet.write(0, 2, '迁出规模指数')

    # 获取迁入数据
    url_in = f'http://huiyan.baidu.com/migration/historycurve.jsonp?dt={classname}&id={InnerMongolia_Code}&type=move_in'
    print(f'内蒙古迁入数据:{url_in}')

    try:
        response_in = requests.get(url_in, timeout=10)
        time.sleep(3)
        r_in = response_in.text[4:-1]  # 去头去尾
        data_dict_in = json.loads(r_in)  # 字典化

        if data_dict_in['errmsg'] == 'SUCCESS':
            data_list_in = data_dict_in['data']['list']
        else:
            print('迁入数据获取失败')
            data_list_in = {}
    except Exception as e:
        print(f'迁入数据请求失败: {e}')
        data_list_in = {}

    # 获取迁出数据
    url_out = f'http://huiyan.baidu.com/migration/historycurve.jsonp?dt={classname}&id={InnerMongolia_Code}&type=move_out'
    print(f'内蒙古迁出数据:{url_out}')

    try:
        response_out = requests.get(url_out, timeout=10)
        time.sleep(3)
        r_out = response_out.text[4:-1]  # 去头去尾
        data_dict_out = json.loads(r_out)  # 字典化

        if data_dict_out['errmsg'] == 'SUCCESS':
            data_list_out = data_dict_out['data']['list']
        else:
            print('迁出数据获取失败')
            data_list_out = {}
    except Exception as e:
        print(f'迁出数据请求失败: {e}')
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

    workbook.close()
    print(f'数据已保存，共{row - 1}天的数据')


if __name__ == "__main__":
    migration_index_inner_mongolia('内蒙古自治区迁徙规模指数', 'province')
    print('全部完成')
