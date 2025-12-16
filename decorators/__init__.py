from functools import wraps
from flask_login import current_user, login_required
from flask import abort

def admin_required(f):
    @wraps(f)
    @login_required # Garante que o usuário está logado, se não redireciona pra login
    def wrapper(*args, **kwargs): #Sei o que é isso de *args e **kwargs não, mas vi que é normal usar isso e tô usando
        if not current_user.is_admin():
             abort(403) #Erro na tela para o usuário ficar esperto e não tentar invadir o site na url.
        return f(*args, **kwargs)
    return wrapper