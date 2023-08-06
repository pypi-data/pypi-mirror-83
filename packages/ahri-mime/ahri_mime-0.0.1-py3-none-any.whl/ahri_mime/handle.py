from .MIME import EXT_TO_TYPE, TYPE_TO_EXT


def get_ext(type, default='', dot=True):
    """
    :ext: 类型, 比如 application/json | Type, such as application/json
    :default: 未找到时返回的值, 默认空字符串 | The value returned when not found. The default is an empty string
    :dot: 扩展名前是否有点 '.', 默认 True | Whether there is a dot "." before the extension. The default is true
    :return: 类型对应的扩展名 | 类型对应的扩展名
    """
    if type in TYPE_TO_EXT.keys():
        try:
            default = TYPE_TO_EXT[type][0]
        except Exception as ex:
            raise Exception('Type Not Found. ' + str(ex))
    return default if dot else default.lstrip('.')


def get_exts(type, default=[], dot=True):
    """
    :ext: 类型, 比如 application/json | Type, such as application/json
    :default: 未找到时返回的值, 默认空列表 | The value returned when not found. The default empty list
    :dot: 扩展名前是否有点 '.', 默认 True | Whether there is a dot "." before the extension. The default is true
    :return: 类型对应扩展名的列表 | List of extensions corresponding to the type
    """
    if type in TYPE_TO_EXT.keys():
        default = TYPE_TO_EXT[type]
    return default if dot else [i.lstrip('.') for i in default]


def get_type(ext, default='', dot=True):
    """
    :ext: 扩展名, 比如 .json | Extension, such as .json
    :default: 未找到时返回的值, 默认空字符串 | The value returned when not found. The default is an empty string
    :dot: 扩展名前是否有点 '.', 默认 True | Whether there is a dot "." before the extension. The default is true
    :return: 扩展名对应的类型 | The type of the extension
    """
    ext = ext if dot else '.' + ext
    if ext in EXT_TO_TYPE.keys():
        try:
            default = EXT_TO_TYPE[ext][0]
        except Exception as ex:
            raise Exception('Ext Not Found. ' + str(ex))
    return default


def get_types(ext, default=[], dot=True):
    """
    :ext: 扩展名 | Extension, such as .json
    :default: 未找到时返回的值, 默认空列表 | The value returned when not found. The default empty list
    :dot: 扩展名前是否有点 '.', 默认 True | Whether there is a dot "." before the extension. The default is true
    :return: 扩展名对应类型的列表 | List of types corresponding to the extension
    """
    ext = ext if dot else '.' + ext
    if ext in EXT_TO_TYPE.keys():
        default = EXT_TO_TYPE[ext]
    return default
