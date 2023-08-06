import csv
import datetime
import os
import re
import zipfile

import geopandas as gpd
import numpy as np
import pandas as pd
from tqdm import tqdm


def ext(filepath):
    """扩展名"""
    return os.path.splitext(filepath)[1]


def fn(filepath):
    """路径及文件名（不含扩展名）"""
    return os.path.splitext(filepath)[0]


def max_grid():
    """防止单个单元格文件过大而报错"""
    import sys
    maxInt = sys.maxsize
    decrement = True
    while decrement:
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt / 10)
            decrement = True


def versionCompare(smaller: str, bigger: str, n=3):
    lis1 = smaller.split('.')
    lis2 = bigger.split('.')
    lis1 = [to_float(i) for i in lis1]
    lis2 = [to_float(i) for i in lis2]
    for i in range(n):
        if lis1[i] > lis2[i]:
            return False
    return True


def rdf(filepath: str) -> pd.DataFrame:
    """
    常用文件读取函数，支持.csv/.xlsx/.shp

    :param filepath: 文件路径
    :return: dataframe
    """
    max_grid()
    if ext(filepath) == '.csv':
        try:
            df = pd.read_csv(filepath, engine='python', encoding='utf-8-sig')
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, engine='python')
    elif ext(filepath) == '.xls':
        df = pd.read_excel(filepath)
    elif ext(filepath) == '.xlsx':
        df = pd.read_excel(filepath)
    elif ext(filepath) == '.shp':
        try:
            df = gpd.GeoDataFrame.from_file(filepath)
        except UnicodeEncodeError:
            df = gpd.GeoDataFrame.from_file(filepath, encoding='GBK')
    else:
        raise Exception('未知文件格式')
    return df


def save2csv(df, filename: str, encoding='GBK'):
    df.to_csv(filename, index=0, encoding=encoding)


def to_csv_by_line(filename: str, data: list):
    with open(filename, 'a') as f:
        csv_write = csv.writer(f, dialect='excel')
        csv_write.writerow(data)


def plate_format(filename, name_col='板块', plate_name=True):
    """
    自动处理板块名

    :param filename: 文件路径
    :param name_col: 有板块名的列
    :param plate_name: 是否增加“板块名”这一列
    :return:
    """
    import warnings
    if plate_name:
        if '脉策板块' not in filename:
            warnings.warn('非脉策板块不应该有板块名，请确认是否正确', UserWarning)
    else:
        if '脉策板块' in filename:
            warnings.warn('脉策板块应该有板块名，请确认是否正确', UserWarning)
    df = rdf(filename)
    valid_check(df)
    df['name'] = df[name_col]
    df['板块名'] = df[name_col]
    if plate_name:
        df = df[['name', name_col, '板块名', 'geometry']]
    else:
        df = df[['name', name_col, 'geometry']]
    df.to_csv(filename, index=False, encoding='utf-8')
    return df


def ensure_lnglat(df) -> pd.DataFrame:
    """将df中的经纬度重命名为lng和lat"""
    from warnings import warn

    from ricco import to_lnglat_dict
    df.rename(columns=to_lnglat_dict, inplace=True)
    if ('lng' not in df.columns) or ('lat' not in df.columns):
        warn('转换失败，输出结果无lng或lat字段')
    return df


def read_and_rename(file: str) -> pd.DataFrame:
    """读取文件并将经纬度统一为lng和lat，并按照经纬度排序"""
    df = rdf(file)
    df = ensure_lnglat(df)
    if 'lat' in df.columns:
        df.sort_values(['lat', 'lng'], inplace=True)
        df = df.reset_index(drop=True)
    return df


def reset2name(df: pd.DataFrame, origin: bool = False) -> pd.DataFrame:
    """
    重置索引，并重命名为name， 默认将索引重置为有序完整的数字（重置两次）

    :param origin: 为True时，将原来的索引作为name列（重置一次）
    """
    if not origin:
        df = df.reset_index(drop=True)
    df = df.reset_index().rename(columns={'index': 'name'})
    return df


def pinyin(word: str) -> str:
    """将中文转换为汉语拼音"""
    import pypinyin
    if isinstance(word, str):
        s = ''
        for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            s += ''.join(i)
    else:
        raise TypeError('输入参数必须为字符串')
    return s


def mkdir_2(path: str):
    """新建文件夹，忽略存在的文件夹"""
    if not os.path.isdir(path):
        os.makedirs(path)


def dir2zip(filepath, delete_exist=True, delete_origin=False):
    """压缩文件夹"""
    zipfilename = filepath + '.zip'
    if delete_exist:
        if os.path.exists(zipfilename):
            os.remove(zipfilename)
            print(f'文件已存在，delete {zipfilename}')
    print(f'saving {zipfilename}')
    z = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            filepath_out = os.path.join(dirpath, filename)
            filepath_in = os.path.join(os.path.split(dirpath)[-1], filename)
            z.write(filepath_out, arcname=filepath_in)
    z.close()
    if delete_origin:
        print(f'delete {filepath}')
        del_file(filepath)


def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    import shutil
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    shutil.rmtree(filepath)


def zip_format_dir(root_dir, pattern=r'.*Update20\d{6}', delete_origin=False):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if re.match(pattern, dirpath):
            dir2zip(dirpath, delete_origin=delete_origin)


def split_csv(filename: str, n: int = 5, encoding: str = 'utf-8'):
    """将文件拆分为多个同名文件，放置在与文件同名文件夹下的不同Part_文件夹中"""
    dir_name = fn(os.path.basename(filename))
    abs_path = os.getcwd()
    df = rdf(filename)
    t = len(df)
    p = int(t / n)
    for i in tqdm(range(n)):
        low = i * p
        high = (i + 1) * p
        dir_name2 = 'Part_' + str(i)
        save_path = os.path.join(abs_path, dir_name, dir_name2)
        savefile = os.path.join(save_path, filename)
        mkdir_2(save_path)
        if i == n - 1:
            add = df.iloc[low:, :]
        else:
            add = df.iloc[low: high, :]
        add.to_csv(savefile, index=0, encoding=encoding)


def per2float(string: str) -> float:
    if '%' in string:
        string = string.replace('%', '')
        return float(string) / 100
    else:
        return float(string)


def extract_num(string: str,
                num_type: str = 'str',
                method: str = 'list',
                join_list: bool = False,
                ignore_pct: bool = True,
                multi_warning=False):
    """
    提取字符串中的数值，默认返回所有数字组成的列表

    :param string: 输入的字符串
    :param num_type:  输出的数字类型，int/float/str，默认为str
    :param method: 结果计算方法，对结果列表求最大/最小/平均/和等，numpy方法，默认返回列表本身
    :param join_list: 是否合并列表，默认FALSE
    :param ignore_pct: 是否忽略百分号，默认True
    :return:
    """
    import re
    from warnings import warn

    import numpy

    string = str(string)
    if ignore_pct:
        lis = re.findall(r"\d+\.?\d*", string)
    else:
        lis = re.findall(r"\d+\.?\d*%?", string)
    lis2 = [getattr(numpy, num_type)(per2float(i)) for i in lis]
    if len(lis2) > 0:
        if method != 'list':
            if join_list:
                raise ValueError("计算结果无法join，只有在method='list'的情况下, 才能使用join_list=True")
            if multi_warning & (len(lis2) >= 2):
                warn(f'有多个值进行了{method}运算')
            res = getattr(numpy, method)(lis2)
        else:
            if num_type == 'str':
                res = ['{:g}'.format(float(j)) for j in lis2]
            else:
                res = lis2
            if join_list:
                res = ''.join(res)
    else:
        res = None
    return res


def to_float(string,
             rex_method: str = 'mean',
             ignore_pct: bool = False,
             multi_warning=True):
    """
    字符串转换为float
    """
    return extract_num(string,
                       num_type='float',
                       method=rex_method,
                       ignore_pct=ignore_pct,
                       multi_warning=multi_warning)


def serise_to_float(serise: pd.Series, rex_method: str = 'mean'):
    """pandas.Series: str --> float"""
    return serise.apply(lambda x: to_float(x, rex_method=rex_method))


def excel2date(dates):
    """excel的数字样式时间格式转日期格式"""
    if len(str(dates)) == 5:
        try:
            dates = int(dates)
            delta = datetime.timedelta(days=dates)
            today = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + delta
            dates_ = datetime.datetime.strftime(today, '%Y-%m-%d')
            return dates_
        except ValueError:
            return None
    else:
        return dates


def ensure_list(val):
    """将标量值和Collection类型都统一转换为LIST类型"""
    if val is None:
        return []
    if isinstance(val, list):
        return val
    if isinstance(val, (set, tuple)):
        return list(val)
    return [val]


def segment(x, gap: (list, float, int), sep: str = '-', unit: str = '') -> str:
    """
    区间段划分工具

    :param x: 数值
    :param gap: 间隔，固定间隔或列表
    :param unit: 单位，末尾
    :param sep: 分隔符，中间
    :return: 区间段 'num1分隔符num2单位'：‘80-100米’
    """

    def between_list(x, lis):
        for i in reversed(range(len(lis) - 1)):
            if x >= lis[i]:
                return lis[i], lis[i + 1]

    x = to_float(x)
    if (x is None) | (x == np.nan) | (x == '') | (x == float('nan')):
        return ''
    elif isinstance(gap, list):
        gap = sorted(list(set(gap)))
        if x < gap[0]:
            return '%d%s以下' % (gap[0], unit)
        elif x >= gap[-1]:
            return '%d%s以上' % (gap[-1], unit)
        else:
            l = between_list(x, gap)[0]
            h = between_list(x, gap)[1]
            s = '%d%s%d%s' % (l, sep, h, unit)
    elif isinstance(gap, (int, float)):
        if x >= 0:
            l = int(x / gap) * gap
            h = l + gap
            s = '%d%s%d%s' % (l, sep, h, unit)
        else:
            l = int(x / gap) * gap
            h = l - gap
            s = '%d%s%d%s' % (h, sep, l, unit)
    else:
        raise TypeError('gap参数数据类型错误')
    return s


def standard(serise: (pd.Series, list),
             q: float = 0.01,
             min_score: float = 0,
             minus: bool = False) -> (pd.Series, list):
    if minus:
        serise = 1 / (serise + 1)
    max_ = serise.quantile(1 - q)
    min_ = serise.quantile(q)
    serise = serise.apply(lambda x: (x - min_) / (max_ - min_) * (100 - min_score) + min_score)
    serise[serise >= 100] = 100
    serise[serise <= min_score] = min_score
    return serise


def col_round(df, col: list):
    """对整列进行四舍五入，默认绝对值大于1的数值保留两位小数，小于1 的保留4位"""

    def _round(x):
        if abs(x) >= 1:
            return round(x, 2)
        else:
            return round(x, 4)

    col = ensure_list(col)
    for i in col:
        df[i] = df[i].apply(lambda x: _round(x))
    return df


def fuzz_match(string: str, ss: (list, pd.Series)):
    """
    为某一字符串从某一集合中匹配相似度最高的元素

    :param string: 输入的字符串
    :param ss: 要去匹配的集合
    :return: 字符串及相似度组成的列表
    """
    from fuzzywuzzy import fuzz

    def _ratio(s, x):
        return fuzz.ratio(s, x), fuzz.partial_ratio(s, x)

    max_r, max_pr, max_s = 0, 0, None
    for s in ss:
        r, pr = _ratio(s, string)
        if r > max_r:
            max_r = r
            max_pr = pr
            max_s = s
    return max_s, max_r, max_pr


def fuzz_df(df: pd.DataFrame,
            col: str,
            target_serise: (list, pd.Series)) -> pd.DataFrame:
    """
    为DataFrame中的某一列，从某个集合中匹配相似度最高的元素

    :param df: 输入的dataframe
    :param col: 要匹配的列
    :param target_serise: 从何处匹配， list/pd.Serise
    :return:
    """
    df[[f'{col}_target',
        'normal_score',
        'partial_score']] = df.apply(lambda x: fuzz_match(x[col], target_serise),
                                     result_type='expand', axis=1)
    return df


# 地理处理
def valid_check(polygon_geom, log=True):
    """检验面的有效性"""
    from shapely.wkb import loads
    df = polygon_geom.copy()
    if len(df[df['geometry'].isna()]) > 0:
        raise ValueError('geometry中有空值，请检查')
    df['geometry'] = df['geometry'].apply(lambda x: loads(x, hex=True))
    df = gpd.GeoDataFrame(df)
    df.crs = 'epsg:4326'
    df['flag'] = df['geometry'].apply(lambda x: 1 if x.is_valid else -1)
    if len(df[df['flag'] < 0]) == 0:
        if log:
            print('Validity test passed.')
    else:
        raise ValueError('有效性检验失败，请检查并修复面')


def _loads(x, hex=True):
    from shapely.wkb import loads
    try:
        x = loads(x, hex=hex)
    except AttributeError:
        x = None
    return x


def _dumps(x, hex=True, srid=4326):
    from shapely.wkb import dumps
    try:
        if versionCompare(gpd.__version__, '0.7.2'):
            x = dumps(x, hex=hex, srid=srid)
        else:
            x = dumps(x, hex=hex)
    except AttributeError:
        x = None
    return x


def shp2csv(shpfile_name: str, encoding='utf-8'):
    """shapefile 转 csv 文件"""
    import warnings
    df = rdf(shpfile_name)
    print(df.head())
    df = gpd.GeoDataFrame(df)
    df['geometry'] = df['geometry'].apply(lambda x: _dumps(x, hex=True, srid=4326))
    df.crs = 'epsg:4326'
    save_path = fn(shpfile_name) + '.csv'
    print(df.head())
    try:
        valid_check(df)
    except ValueError:
        warnings.warn('有效性检验失败，可能影响数据上传')
    df.to_csv(save_path, encoding=encoding, index=False)


def csv2shp(filename: str):
    """csv文件 转 shapefile"""
    import fiona
    df = rdf(filename)
    df = df.rename(columns={'名称': 'name',
                            'geom': 'geometry'})
    df = gpd.GeoDataFrame(df)
    df['geometry'] = df['geometry'].apply(lambda x: _loads(x, hex=True))
    df.crs = 'epsg:4326'
    save_path = fn(filename) + '.shp'
    try:
        df.to_file(save_path)
    except fiona.errors.SchemaError:
        df.columns = [pinyin(i) for i in df.columns]
        df.to_file(save_path, encoding='utf-8')
        print('已将列名转为汉语拼音进行转换')


def geom_wkb2lnglat(df, geometry='geometry', delete=False):
    """geometry转经纬度，求中心点经纬度"""
    df = gpd.GeoDataFrame(df)
    df[geometry] = df[geometry].apply(lambda x: _loads(x, hex=True))
    df.crs = 'epsg:4326'
    df['lng'] = df.centroid.x
    df['lat'] = df.centroid.y
    if delete:
        df.drop(geometry, axis=1, inplace=True)
    else:
        df[geometry] = df[geometry].apply(lambda x: _dumps(x, hex=True, srid=4326))
    return df


def geom_wkt2wkb(df, geometry='geometry'):
    """wkb转wkt"""
    from shapely import wkb
    from shapely import wkt
    df = gpd.GeoDataFrame(df)
    df[geometry] = df[geometry].apply(lambda x: wkt.loads(x))
    df.crs = 'epsg:4326'
    df[geometry] = df[geometry].apply(lambda x: wkb.dumps(x, hex=True, srid=4326))
    return df


def point_to_geo(df, lng, lat, delt=1):
    """包含经纬度的DataFrame转GeoDataFrame"""
    from geopandas import points_from_xy
    df = gpd.GeoDataFrame(df, geometry=points_from_xy(df[lng], df[lat]))
    df.crs = 'epsg:4326'
    if delt == 1:
        del df[lng]
        del df[lat]
    return df


def point_to_geo_old(df, lng, lat, delt=1):
    """包含经纬度的DataFrame转GeoDataFrame"""
    from shapely.geometry import Point
    df['geometry'] = gpd.GeoSeries(list(zip(df[lng], df[lat]))).apply(Point)
    df = gpd.GeoDataFrame(df)
    df.crs = 'epsg:4326'
    if delt == 1:
        del df[lng]
        del df[lat]
    return df


def lnglat2geom(df, lng='lng', lat='lat', delete=False):
    """经纬度转wkb格式的geometry"""
    df = ensure_lnglat(df)
    df = point_to_geo(df, lng, lat, delt=0)
    df['geometry'] = df['geometry'].apply(lambda x: _dumps(x, hex=True, srid=4326))
    if delete:
        df.drop(['lng', 'lat'], axis=1, inplace=True)
    return df
