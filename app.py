from flask import Flask, request, jsonify

app = Flask(__name__)

class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.historial = []

# Inicializar cuentas
BD = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]

def buscar_cuenta(numero):
    for cuenta in BD:
        if cuenta.numero == numero:
            return cuenta
    return None

@app.route('/billetera/contactos', methods=['GET'])
def obtener_contactos():
    minumero = request.args.get('minumero')
    cuenta = buscar_cuenta(minumero)
    if cuenta:
        contactos = {contacto: buscar_cuenta(contacto).nombre for contacto in cuenta.contactos}
        return jsonify(contactos)
    return jsonify({"error": "Cuenta no encontrada"}), 404

@app.route('/billetera/pagar', methods=['POST'])
def pagar():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = float(request.args.get('valor'))

    cuenta_origen = buscar_cuenta(minumero)
    cuenta_destino = buscar_cuenta(numerodestino)

    if cuenta_origen and cuenta_destino:
        if cuenta_origen.saldo >= valor:
            cuenta_origen.saldo -= valor
            cuenta_destino.saldo += valor
            cuenta_origen.historial.append(f"Pago realizado de {valor} a {cuenta_destino.nombre}")
            cuenta_destino.historial.append(f"Pago recibido de {valor} de {cuenta_origen.nombre}")
            return jsonify({"message": "Pago realizado con éxito"})
        return jsonify({"error": "Saldo insuficiente"}), 400
    return jsonify({"error": "Cuenta no encontrada"}), 404

@app.route('/billetera/historial', methods=['GET'])
def obtener_historial():
    minumero = request.args.get('minumero')
    cuenta = buscar_cuenta(minumero)
    if cuenta:
        historial = {
            "saldo": cuenta.saldo,
            "operaciones": cuenta.historial
        }
        return jsonify(historial)
    return jsonify({"error": "Cuenta no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
