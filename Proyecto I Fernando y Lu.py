from machine import Pin, PWM, ADC
import utime
import sys
from time import sleep

#Estructura de Movimiento:

#Pines Motor A:
ena=Pin(16, Pin.OUT)
in1=Pin(17, Pin.OUT)
in2=Pin(18,Pin.OUT)

#Pines Motor B:
in3=Pin(19,Pin.OUT)
in4=Pin(20,Pin.OUT)
enb=Pin(21,Pin.OUT)

#Pines pwm:
pwm_pinA = PWM(Pin(16))
pwm_pinB = PWM(Pin(19))

pwm_pinA.freq(1000)
pwm_pinB.freq(1000)

#Función que detiene los motores de la maqueta
def detener():
    ena.value(0)
    enb.value(0)
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)

#Función que avanza o retrocede el auto a cierta potencia
def pwm(num1):
    if num1 == 0:
        ena.value(0)
        enb.value(0)
    elif num1 == 1:
        ena.value(1)
        enb.value(1)
        pwm_pinA.duty_u16(32768)
        in1.value(0)
        in2.value(1)
        utime.sleep(2)
        detener()
    elif num1 == 2:
        ena.value(1)
        enb.value(1)
        pwm_pinA.duty_u16(40960)
        in1.value(0)
        in2.value(1)
        utime.sleep(2)
        detener()
    elif num1 == 3:
        ena.value(1)
        enb.value(1)
        pwm_pinA.duty_u16(49152)
        in1.value(0)
        in2.value(1)
        utime.sleep(2)
        detener()
    elif num1 == 4:
        ena.value(1)
        enb.value(1)
        pwm_pinA.duty_u16(65535)
        in1.value(0)
        in2.value(1)
        utime.sleep(2)
        detener()
    elif num1 == -1:
        ena.value(1)
        enb.value(1)
        pwm_pinA.duty_u16(32768)
        in1.value(1)
        in2.value(0)
        utime.sleep(2)
        detener()
    elif num1 == -2:
        ena.value(1)
        enb.value(1)
        pwm_pinA.duty_u16(40960)
        in1.value(1)
        in2.value(0)
        utime.sleep(2)
        detener()
    elif num1 == -3:
        ena.value(1)
        enb.value(1)
        pwm_pinA.duty_u16(49152)
        in1.value(1)
        in2.value(0)
        utime.sleep(2)
        detener()
    elif num1 == -4:
        ena.value(1)
        enb.value(1)
        pwm_pinA.duty_u16(65535)
        in1.value(1)
        in2.value(0)
        utime.sleep(2)
        detener()
    else:
        print("Valor Incorrecto")

#Función que controla el la dirección del auto (giro izquierda, giro derecha, avanzar, retroceder)
def dir(num2):
    ena.value(1)
    enb.value(1)
    if num2 == 0:
        in1.value(0)
        in2.value(1)
        utime.sleep(1.5)
        detener()
    elif num2 == -1:
        in3.value(1)
        in4.value(0)
        utime.sleep(0.75)
    elif num2 == 1:
        in3.value(0)
        in4.value(1)
        utime.sleep(0.75)
    elif num2 == 2:
        in1.value(1)
        in2.value(0)
        utime.sleep(1.5)
        detener()
    else:
        print("Valor Incorrecto")

#Estructura de luces:

#Pines Input del Registro de Corrimiento
clk = Pin(14, Pin.OUT, value=0)
data = Pin(15, Pin.OUT, value=0)

data.value(0)
clk.value(0)

#Función que actualiza los valores del Registro de Corrimiento para controlar las luces
def actualizar_luces(Lb, Lf, Ll, Lr):
    #Lista que contiene los valores binarios para controlar las luces
    luces = [Lr, Ll, Lf, Lf, Lb, Lb]
    #Ciclo iterativo que actualiza los valores dentro del Registro de Corrimiento
    for estado in luces:
        
        data.value(estado)

        clk.value(1)
        utime.sleep_us(10)

        clk.value(0)
        utime.sleep_us(10)

#Función que enciende y apaga las luces traseras
def lb(num3):
    if num3 == 0:
        actualizar_luces(0,0,0,0)
    elif num3 == 1:
        actualizar_luces(1,0,0,0)
    else:
        print("Valor Incorrecto")

#Función que enciende y paga las luces frontales
def lf(num4):
    if num4 == 0:
        actualizar_luces(0,0,0,0)
    elif num4 == 1:
        actualizar_luces(0,1,0,0)
    else:
        print("Valor Incorrecto")

#Función que enciende y apaga la luz direccional izquierda
def ll(num5):
    if num5 == 0:
        actualizar_luces(0,0,0,0)
    elif num5 == 1:
        actualizar_luces(0,0,1,0)
    else:
        print("Valor Incorrecto")

#Función que enciende y apaga la luz direccional derecha
def lr(num6):
    if num6 == 0:
        actualizar_luces(0,0,0,0)
    elif num6 == 1:
        actualizar_luces(0,0,0,1)
    else:
        print("Valor Incorrecto")

#Estructura Control de luces con la fotoresistencia

#Pin que recopila los valores obtenidos de la fotoresistencia
Ldr = ADC(Pin(27))

#Función que enciende o apaga las luces según la luminosidad del entorno y si el modo está activado
def ldr(num7):
    luminosidad = Ldr.read_u16()
    if num7 == 0:
        actualizar_luces(0, 0, 0, 0)
    elif num7 == 1:
        if luminosidad<1:
            actualizar_luces(1, 1, 0, 0)
        elif luminosidad>=1:
            actualizar_luces(0, 0, 0, 0)
        else:
            detener()
            actualizar_luces(0, 0, 0, 0)
            print("Error")
    else:
        print("Valor Incorrecto")

#Estructura Comandos para Instrucciones de Patrón:

#Función que mueve el auto con una trayectoria que forma un círculo
def Circle():
    ena.value(1)
    enb.value(1)
    in4.value(1)
    utime.sleep(0.75)
    in2.value(1)
    utime.sleep(3)
    detener()

#Función que mueve el auto con una trayectoria que forma el símbolo de infinito
def Infinite():
    ena.value(1)
    enb.value(1)
    in3.value(1)
    utime.sleep(0.75)
    in2.value(1)
    utime.sleep(3)
    in3.value(0)
    utime.sleep(0.5)
    in4.value(1)
    utime.sleep(2.5)
    detener()

#Función que mueve el auto con una trayectoria que forma un patrón en ZigZag  
def ZigZag():
    ena.value(1)
    enb.value(1)
    in3.value(1)
    in2.value(1)
    utime.sleep(0.025)
    in3.value(0)
    utime.sleep(1.5)
    in4.value(1)
    utime.sleep(0.5)
    in4.value(0)
    utime.sleep(1.5)
    in3.value(1)
    utime.sleep(0.5)
    in3.value(0)
    utime.sleep(1.5)
    in4.value(1)
    utime.sleep(0.5)
    in4.value(0)
    detener()
    
