from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

""" 注册用户 """
username = input('请输入用户名')
password = input('请输入密码')
password_hash = generate_password_hash(password, method='sha256')
print(password_hash)