"""
为了与数据库交互,我们将在crud.py中为每个模型实例化
"""

from fastcrud import FastCRUD

from models import EmailLog, User

crud_user = FastCRUD(User)
crud_email_log = FastCRUD(EmailLog)
