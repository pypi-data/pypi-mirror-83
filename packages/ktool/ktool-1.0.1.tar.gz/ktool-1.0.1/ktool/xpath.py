import lxml.etree as le

# 返回唯一的xpath结果
def xpath_one(contentx, path, default=None):
    if type(contentx) == str or type(contentx) == bytes:
        contentx = le.HTML(contentx)
    rets = contentx.xpath(path)
    return rets[0] if rets else default


# 返回多个xpath的结果
def xpath_all(contentx, path,strip=False):
    if type(contentx) == str or type(contentx) == bytes:
        contentx = le.HTML(contentx)
    rets = contentx.xpath(path)
    if strip:
        ret_strips = []
        for ret in rets:
            ret_strips.append(ret.strip())
        return ret_strips
    else:
        return rets

# 合并的得到的结果
def xpath_union(contentx, path, sep='', strip=True,default=None):
    if type(contentx) == str or type(contentx) == bytes:
        contentx = le.HTML(contentx)
    rets = xpath_all(contentx=contentx,path=path,strip=strip)
    if rets:
        return sep.join(rets)
    else:
        return default



