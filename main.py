# from firebase import firebase
#
# firebase=firebase.FirebaseApplication("https://buspass-b03-default-rtdb.firebaseio.com/",None)
#
# data={
#     'name':"Yaswanth",
#     'ID':18891445,
#     'stop':'UPL'
# }
# # for uploading the data
# # result=firebase.post('https://testfirebase-8866b-default-rtdb.firebaseio.com/studentext',data)
# # print(result)
#
# # for geting the data
# result=firebase.get('https://buspass-b03-default-rtdb.firebaseio.com/student',"")
# print(list(result.values())[-1])

#
# from cryptography.fernet import Fernet
# #key = Fernet.generate_key()
# data_all = pd.read_excel('test_data.xlsx')
# key=b'w0aM-ojBoT0UwcuunRym0mjD-B7nfWtQh3K85fIcdP8='
# fernet = Fernet(key)
# def encrypt(n):
#     return fernet.encrypt(n.encode())
#
#
# def decrypt(n):
#      return fernet.decrypt(n).decode()
#
# # for i in list(data_all['id']):
# #     print(encrypt(i))
# print("----------------------------------------------------------------")
# x=b'gAAAAABimbSbqUO0ypv3N9TfWVYugS1ZeBMJjg4py--6UppTlC52XjGjJRhIOr6KHxcd7q_kIdBI21R05DlvcttrrWeOw4jsXg=='
# # print(encrypt(x))
# print(decrypt(x))


# import pandas as pd
# import pyqrcode
# data_all = pd.read_excel('test_data.xlsx')
#
# # print(data_all['en_id'])
# x=0
# for i in list(data_all['id']):
#     url = pyqrcode.create(i)
#     x+=1
# # Create and save the png file naming "myqr.png"
#     url.png('scan/"{}.png'.format(x), scale=8)
#     if x>10: break

print(3 or 5)