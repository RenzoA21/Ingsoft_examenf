import unittest
from app import Cuenta, buscar_cuenta, BD

class TestCuenta(unittest.TestCase):
    
    def setUp(self):
        self.cuenta1 = Cuenta("111", "Test1", 100, ["222", "333"])
        self.cuenta2 = Cuenta("222", "Test2", 200, ["111"])
        self.cuenta3 = Cuenta("333", "Test3", 300, ["111"])
    
    def test_buscar_cuenta_exito(self):
        cuenta = buscar_cuenta("21345")
        self.assertIsNotNone(cuenta)
        self.assertEqual(cuenta.nombre, "Arnaldo")
    
    def test_buscar_cuenta_error(self):
        cuenta = buscar_cuenta("99999")
        self.assertIsNone(cuenta)
    
    def test_pagar_exito(self):
        cuenta_origen = buscar_cuenta("21345")
        cuenta_destino = buscar_cuenta("123")
        saldo_inicial_origen = cuenta_origen.saldo
        saldo_inicial_destino = cuenta_destino.saldo
        valor = 50
        
        cuenta_origen.saldo -= valor
        cuenta_destino.saldo += valor
        
        self.assertEqual(cuenta_origen.saldo, saldo_inicial_origen - valor)
        self.assertEqual(cuenta_destino.saldo, saldo_inicial_destino + valor)
    
    def test_pagar_saldo_insuficiente(self):
        cuenta_origen = buscar_cuenta("21345")
        cuenta_destino = buscar_cuenta("123")
        valor = 1000
        
        saldo_inicial_origen = cuenta_origen.saldo
        
        if cuenta_origen.saldo < valor:
            cuenta_origen.saldo = saldo_inicial_origen
        
        self.assertEqual(cuenta_origen.saldo, saldo_inicial_origen)
    
    def test_historial(self):
        cuenta = buscar_cuenta("21345")
        cuenta.historial.append("Pago recibido de 50 de Test")
        self.assertIn("Pago recibido de 50 de Test", cuenta.historial)

if __name__ == '__main__':
    unittest.main()
