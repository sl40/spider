from config import config


def get_image_full_url(image, image_format=True):
    """获取完整的图片URL
    :param image:
    :param image_format:
    :return:
    """
    full_url = image
    if not image.startswith('http'):
        full_url = config.get('qiniu', 'image_cdn') + image
    if image_format:
        return full_url + config.get('qiniu', 'image_format')
    return full_url
