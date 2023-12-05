from binding.python.xdbSearcher import XdbSearcher
import timeit


def searchWithFile():
    # 1. 创建查询对象
    dbPath = "./data/ip2region.xdb"
    searcher = XdbSearcher(dbfile=dbPath)

    # 2. 执行查询
    ip = "175.13.226.104"
    region_str = searcher.searchByIPStr(ip)
    print(region_str)

    # 3. 关闭searcher
    searcher.close()


if __name__ == '__main__':
    elapsed_time = timeit.timeit(searchWithFile, number=1000)  # 重复执行 1000 次
    formatted_time = '{:.15f}'.format(elapsed_time / 1000)  # 格式化运行时间
    print(f"平均运行时间: {formatted_time} 秒")