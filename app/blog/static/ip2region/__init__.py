from .binding.python.xdbSearcher import XdbSearcher
import os


def search_with_file(ip):
    module_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(module_path, "./data/ip2region.xdb")
    searcher = XdbSearcher(dbfile=db_path)
    region_str = searcher.searchByIPStr(ip)
    searcher.close()
    return region_str
