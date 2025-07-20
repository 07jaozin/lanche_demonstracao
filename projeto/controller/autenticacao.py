from flask import session

class Autenticacao():

    @staticmethod
    def verificacao(senha):
        if senha == 'usuarioadm':
            session['adm'] = True

            return True
        else:
            return False