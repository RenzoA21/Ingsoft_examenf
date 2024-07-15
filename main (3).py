from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

class CuentaUsuario:
    def __init__(self, numero, saldo, numeros_contacto):
        self.numero = numero
        self.saldo = saldo
        self.numeros_contacto = numeros_contacto
        self.operaciones = []

    def historialOperaciones(self):
        return self.operaciones

    def transferir(self, destino, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            destino.saldo += valor
            operacion = Operacion(self, destino, valor, datetime.now())
            self.operaciones.append(operacion)
            destino.operaciones.append(operacion)
            return True
        return False

class Operacion:
    def __init__(self, origen, destino, valor, fecha):
        self.origen = origen
        self.destino = destino
        self.valor = valor
        self.fecha = fecha

BD = {
    "21345": CuentaUsuario("21345", 200, ["123", "456"]),
    "123": CuentaUsuario("123", 400, ["456"]),
    "456": CuentaUsuario("456", 300, ["21345"])
}

@app.route('/billetera/contactos')
def contactos():
    numero = request.args.get('minumero')
    cuenta = BD.get(numero)
    if cuenta:
        contactos = {contacto: BD[contacto].numero for contacto in cuenta.numeros_contacto}
        return jsonify(contactos)
    return "Cuenta no encontrada", 404

@app.route('/billetera/pagar')
def pagar():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = float(request.args.get('valor'))
    cuenta_origen = BD.get(minumero)
    cuenta_destino = BD.get(numerodestino)
    if cuenta_origen and cuenta_destino:
        if cuenta_destino.numero in cuenta_origen.numeros_contacto:
            if cuenta_origen.transferir(cuenta_destino, valor):
                return f"Realizado en {datetime.now().strftime('%d/%m/%Y')}."
            return "Saldo insuficiente", 400
        return "Destino no es contacto", 400
    return "Cuenta no encontrada", 404

@app.route('/billetera/historial')
def historial():
    numero = request.args.get('minumero')
    cuenta = BD.get(numero)
    if cuenta:
        operaciones = [
            {
                "origen": operacion.origen.numero,
                "destino": operacion.destino.numero,
                "valor": operacion.valor,
                "fecha": operacion.fecha.strftime('%d/%m/%Y')
            } for operacion in cuenta.historialOperaciones()
        ]
        return jsonify({
            "saldo": cuenta.saldo,
            "operaciones": operaciones
        })
    return "Cuenta no encontrada", 404

if __name__ == '__main__':
    app.run(debug=True)
