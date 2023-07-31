import os
import imghdr

def correct_image_extensions(directory):
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 获取文件的完整路径
        filepath = os.path.join(directory, filename)
        # 使用imghdr确定图片的格式
        format = imghdr.what(filepath)
        # 如果文件是图片
        if format:
            # 获取文件的名字和后缀名
            base, ext = os.path.splitext(filepath)
            # 如果后缀名不正确，修改它
            if ext[1:].lower() != format.lower():
                new_filepath = base + '.' + format
                os.rename(filepath, new_filepath)
                print(f'Renamed {filepath} to {new_filepath}')

# 调用函数，传入你要处理的目录路径
correct_image_extensions('stickers')

