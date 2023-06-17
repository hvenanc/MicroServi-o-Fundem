from infra.configs.connection import DBConnectionHandler
from infra.entities.usuario_pf import Usuario_pf


class Usuario_pfRepository:

    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Usuario_pf).all()
            return data

    def insert(self, id, nome, data_nasc, email, telefone):
        with DBConnectionHandler() as db:
            data = Usuario_pf(id=id, nome=nome.upper(), data_nasc=data_nasc, email=email, telefone=telefone)
            db.session.add(data)
            db.session.commit()
