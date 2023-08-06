import logging.config


def get_logger(log_filepath,maxBytes,backupCount,sh_level,fh_level):
    standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                      '[%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字
    simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
    id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

    # 定义日志输出格式 结束
    logfile_path_staff = log_filepath

    # log配置字典
    # LOGGING_DIC第一层的所有的键不能改变
    LOGGING_DIC = {
        'version': 1,  # 版本号
        'disable_existing_loggers': False,  # 固定写法
        'formatters': {
            'standard': {
                'format': standard_format
            },
            'simple': {
                'format': simple_format
            },
        },
        'filters': {},
        'handlers': {
            # 打印到终端的日志
            'sh': {
                'level': sh_level,
                'class': 'logging.StreamHandler',  # 打印到屏幕
                'formatter': 'simple'
            },
            # 打印到文件的日志,收集info及以上的日志
            'fh': {
                'level': fh_level,
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                'formatter': 'standard',
                'filename': logfile_path_staff,  # 日志文件
                'maxBytes': maxBytes,  # 日志大小 300字节
                'backupCount': backupCount,  # 轮转文件的个数
                'encoding': 'utf-8',  # 日志文件的编码
            },
        },
        'loggers': {
            # logging.getLogger(__name__)拿到的logger配置
            '': {
                'handlers': ['sh', 'fh'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                'level': sh_level,
                'propagate': True,  # 向上（更高level的logger）传递
            },
        },
    }

    logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置 通过字典方式去配置这个日志
    logger = logging.getLogger()  # 生成一个log实例  这里可以有参数 传给task_id
    return logger