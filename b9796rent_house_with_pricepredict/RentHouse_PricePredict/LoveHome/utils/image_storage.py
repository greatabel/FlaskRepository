# -*- coding:utf-8 -*-
__author__ = 'xiaoguo'

import qiniu

access_key = "HeZNmLfeU5htH64ZK2YHBlXmOmXrAzKO-PeJMlZp"
secret_key = "QAmgQNB6TTjAvdCXFIR_H22UmKrO5OEQvc5PKtaR"
bucket_name = 'ihome'

'''上传图片到七牛云的方法'''
def upload_image(data):
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket_name)
    ret, info = qiniu.put_data(token, None, data)

    if info.status_code == 200:     # 上传成功返回图片对应的 key
        return ret.get('key')
    else:                           # 上传失败，抛出异常
        raise Exception('上传图片失败')


# if __name__ == '__main__':
#     file_name = raw_input('请输入图片地址：')
#     with open(file_name, 'rb') as f:
#         upload_image(f.read())
