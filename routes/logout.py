from flask import redirect, url_for, session

def logout():
    session.pop("user", None)
    session.pop("is_admin", None)
    
    return redirect(url_for("login"))
