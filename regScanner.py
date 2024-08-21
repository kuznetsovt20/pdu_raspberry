from pyModbusTCP.client import ModbusClient
import time



c = ModbusClient(host='192.168.1.254', port=502, unit_id=1, auto_open=True, debug=False, timeout=1)
c2 = ModbusClient(host='192.168.1.250', port=502, unit_id=1, auto_open=True, debug=False, timeout=1)
regNum = 0
run1, run2, compare = True, False, False
registerNum, registerValue1, registerValue2 = [], [], []

while run1:
    data = c.read_holding_registers(regNum, 1)
    if data != None:
        print('register = ' + str(regNum) + '           value = ' + str(data[0]))
        registerValue1.append(data[0])
    else:
        print('register = ' + str(regNum) + '           value = no data')
        registerValue1.append(0)
    regNum = regNum+1
    if regNum == 65536:
        run1 = False
        run2 = True
        regNum = 0
        print ('Change ip to 192.168.1.250')
        time.sleep(60)


while run2:
    data = c2.read_holding_registers(regNum, 1 )
    if data is not None:
        print('register = ' + str(regNum) + '           value = ' + str(data[0]))
        registerValue2.append(data[0])
    else:
        print('register = ' + str(regNum) + '           value = no data')
        registerValue2.append(0)
    regNum = regNum+1
    if regNum == 65536:
        run2 = False
        compare = True
        regNum = 0

while compare:
    if registerValue1[regNum] != registerValue2[regNum]:
        print('Difference in values: register = ' + str(regNum) + '  value #1 = ' + str(registerValue1[regNum]) + ' value #2 = ' + str(registerValue2[regNum]))
    regNum = regNum+1
    if regNum == 65536:
        quit