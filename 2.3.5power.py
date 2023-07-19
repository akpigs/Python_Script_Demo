import os
import concurrent.futures
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import win32com.client

# 生成随机的AES密钥
def generate_aes_key():
    return os.urandom(32)

# 生成随机的salt
def generate_salt():
    return os.urandom(16)

# 生成随机的IV（初始化向量）
def generate_iv():
    return os.urandom(16)

# 生成随机的RSA密钥对
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# 使用AES加密文件内容
def encrypt_file(file_path, key, iv):
    with open(file_path, 'rb') as file:
        file_data = file.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(file_data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_data

# 使用RSA加密AES密钥
def encrypt_aes_key(aes_key, public_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

# 加密单个文件
def process_file(file_path, aes_key, iv, encrypted_directory_path):
    encrypted_data = encrypt_file(file_path, aes_key, iv)
    encrypted_file_path = os.path.join(encrypted_directory_path, os.path.relpath(file_path, encrypted_directory_path) + '.encrypted')
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    os.remove(file_path)  # 删除原文件

# 加密指定路径下的所有文件
def encrypt_files_in_directory(directory_path):
    # 生成AES密钥、salt、IV和RSA密钥对
    aes_key = generate_aes_key()
    salt = generate_salt()
    iv = generate_iv()
    private_key, public_key = generate_rsa_key_pair()

    # 获取上级目录路径
    parent_directory_path = os.path.dirname(directory_path)
    if parent_directory_path == '':
        # 如果上级目录为空，说明当前目录是根目录，将文件保存在被加密文件内
        encrypted_directory_path = directory_path
    else:
        # 否则，保存在上级目录
        encrypted_directory_path = parent_directory_path

    # 将AES密钥加密并保存到文件
    encrypted_aes_key = encrypt_aes_key(aes_key, public_key)
    with open(os.path.join(encrypted_directory_path, 'encrypted_aes_key.txt'), 'wb') as file:
        file.write(encrypted_aes_key)

    # 使用多线程加密文件
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                executor.submit(process_file, file_path, aes_key, iv, encrypted_directory_path)

    # 保存密钥、salt和IV等敏感信息到data.txt文件中
    with open(os.path.join(encrypted_directory_path, 'data.txt'), 'w') as data_file:
        data_file.write('AES Key: {}\n'.format(aes_key.hex()))
        data_file.write('Salt: {}\n'.format(salt.hex()))
        data_file.write('IV: {}\n'.format(iv.hex()))
        data_file.write('Private Key: {}\n'.format(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()))

    # 弹出 Windows 弹框
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.Popup('File encryption complete!', 0, 'encrypted', 64)

# 获取未加密的文件列表
def get_remaining_files(directory_path, encrypted_directory_path):
    remaining_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypted_file_path = os.path.join(encrypted_directory_path, os.path.relpath(file_path, directory_path) + '.encrypted')
            if not os.path.exists(encrypted_file_path):
                remaining_files.append(file_path)
    return remaining_files


if __name__ == "__main__":
    print("如加密失败，请检查是否安装python或使用管理员权限运行该程序！！")
    # 用户输入加密路径
    directory_path = input("Enter the path encryption：")
    # 验证输入的路径是否存在
    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
    else:
        # 加密指定路径下的所有文件
        encrypt_files_in_directory(directory_path)

        # 弹出 Windows 弹框
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.Popup('File encryption complete!', 0, 'encrypted', 64)

# import os
# import concurrent.futures
# from cryptography.hazmat.primitives import hashes, padding
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.backends import default_backend
# import win32com.client
#
# # 生成随机的AES密钥
# def generate_aes_key():
#     return os.urandom(32)
#
# # 生成随机的salt
# def generate_salt():
#     return os.urandom(16)
#
# # 生成随机的IV（初始化向量）
# def generate_iv():
#     return os.urandom(16)
#
# # 生成随机的RSA密钥对
# def generate_rsa_key_pair():
#     private_key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048,
#         backend=default_backend()
#     )
#     public_key = private_key.public_key()
#     return private_key, public_key
#
# # 使用AES加密文件内容
# def encrypt_file(file_path, key, iv):
#     with open(file_path, 'rb') as file:
#         file_data = file.read()
#
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     encryptor = cipher.encryptor()
#
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_data = padder.update(file_data) + padder.finalize()
#
#     encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
#
#     return encrypted_data
#
# # 使用RSA加密AES密钥
# def encrypt_aes_key(aes_key, public_key):
#     encrypted_key = public_key.encrypt(
#         aes_key,
#         asymmetric_padding.OAEP(
#             mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#     return encrypted_key
#
# # 加密单个文件
# def process_file(file_path, aes_key, iv, encrypted_directory_path):
#     encrypted_data = encrypt_file(file_path, aes_key, iv)
#     encrypted_file_path = os.path.join(encrypted_directory_path, os.path.relpath(file_path, encrypted_directory_path) + '.encrypted')
#     with open(encrypted_file_path, 'wb') as encrypted_file:
#         encrypted_file.write(encrypted_data)
#     os.remove(file_path)  # 删除原文件
#
# # 加密指定路径下的所有文件
# def encrypt_files_in_directory(directory_path):
#     # 生成AES密钥、salt、IV和RSA密钥对
#     aes_key = generate_aes_key()
#     salt = generate_salt()
#     iv = generate_iv()
#     private_key, public_key = generate_rsa_key_pair()
#
#     # 获取上级目录路径
#     parent_directory_path = os.path.dirname(directory_path)
#     if parent_directory_path == '':
#         # 如果上级目录为空，说明当前目录是根目录，将文件保存在被加密文件内
#         encrypted_directory_path = directory_path
#     else:
#         # 否则，保存在上级目录
#         encrypted_directory_path = parent_directory_path
#
#     # 将AES密钥加密并保存到文件
#     encrypted_aes_key = encrypt_aes_key(aes_key, public_key)
#     with open(os.path.join(encrypted_directory_path, 'encrypted_aes_key.txt'), 'wb') as file:
#         file.write(encrypted_aes_key)
#
#     # 使用多线程加密文件
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         for root, dirs, files in os.walk(directory_path):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 executor.submit(process_file, file_path, aes_key, iv, encrypted_directory_path)
#
#     # 保存密钥、salt和IV等敏感信息到data.txt文件中
#     with open(os.path.join(encrypted_directory_path, 'data.txt'), 'w') as data_file:
#         data_file.write('AES Key: {}\n'.format(aes_key.hex()))
#         data_file.write('Salt: {}\n'.format(salt.hex()))
#         data_file.write('IV: {}\n'.format(iv.hex()))
#         data_file.write('Private Key: {}\n'.format(private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.PKCS8,
#             encryption_algorithm=serialization.NoEncryption()
#         ).decode()))
#
#     # 检查是否还有未加密的文件，如果有则继续加密
#     remaining_files = get_remaining_files(directory_path, encrypted_directory_path)
#     while remaining_files:
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             for file_path in remaining_files:
#                 executor.submit(process_file, file_path, aes_key, iv, encrypted_directory_path)
#         remaining_files = get_remaining_files(directory_path, encrypted_directory_path)
#
#     # 检查是否所有文件都已加密
#     remaining_files = get_remaining_files(directory_path, encrypted_directory_path)
#     if not remaining_files:
#         # 弹出 Windows 弹框
#         shell = win32com.client.Dispatch("WScript.Shell")
#         shell.Popup('文件加密完成', 0, '加密成功', 64)
#
# # 获取未加密的文件列表
# def get_remaining_files(directory_path, encrypted_directory_path):
#     remaining_files = []
#     for root, dirs, files in os.walk(directory_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             encrypted_file_path = os.path.join(encrypted_directory_path, os.path.relpath(file_path, directory_path) + '.encrypted')
#             if not os.path.exists(encrypted_file_path):
#                 remaining_files.append(file_path)
#     return remaining_files
#
# # 用户输入加密路径
# directory_path = input("请输入要加密的目录路径：")
# # 验证输入的路径是否存在
# if not os.path.isdir(directory_path):
#     print("无效的目录路径。")
# else:
#     # 加密指定路径下的所有文件
#     encrypt_files_in_directory(directory_path)