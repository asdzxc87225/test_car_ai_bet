class DataCenterError(Exception):
    """資料中心基礎錯誤類別"""
    pass

class DataLoadError(DataCenterError):
    """讀取資料時發生錯誤"""
    pass

class DataFormatError(DataCenterError):
    """資料格式錯誤"""
    pass

