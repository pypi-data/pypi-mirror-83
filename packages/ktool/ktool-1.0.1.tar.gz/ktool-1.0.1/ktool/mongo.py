import pymongo
print(pymongo.__version__)
import warnings
import traceback

def get_datas(db_name,c_name,client:pymongo.MongoClient=None):
    use_close = False
    if not client:
        client = pymongo.MongoClient()
        use_close = True

    datas = []
    try:
        for data in client.get_database(db_name).get_collection(c_name).find({},{'_id':0}):
            datas.append(data)
    except:
        warnings.warn('空集合')
        print(traceback.format_exc())
    if use_close:
        client.close()
    return datas


def save_datas(datas,db_name,c_name,client:pymongo.MongoClient=None):
    try:
        use_close = False
        if not client:
            client = pymongo.MongoClient()
            use_close = True

        c = client.get_database(db_name).get_collection(c_name)
        c.insert_many(datas)
        if use_close:
            client.close()
        return True
    except:
        print(traceback.format_exc())
        return False


