from database import db

class Consultas(db.Model):
    __tablename__="consultas"
    id_consultas = db.Column(db.Integer, primary_key = True)
    paciente = db.Column(db.String(100))
    data_consulta = db.Column(db.Date)
    medico = db.Column(db.String(100))

    def __init__(self, paciente, data_consulta, medico):
        self.paciente = paciente
        self.data_consulta = data_consulta
        self.medico = medico

    def __repr__(self):
        return "<Paciente da Consulta: {}>".format(self.paciente)
    