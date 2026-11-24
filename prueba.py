import machine
import time
from machine import Pin, PWM, ADC
import utime
import sys
from time import sleep
import socket


#Estructura de Movimiento:

#Pines Motor A:

in1=Pin(17, Pin.OUT)
in2=Pin(18,Pin.OUT)

#Pines Motor B:
in3=Pin(20,Pin.OUT)
in4=Pin(21,Pin.OUT)


#Entrada de circuito decrementador
entradaA=Pin(2,Pin.OUT)
entradaB=Pin(3,Pin.OUT)
entradaC=Pin(4,Pin.OUT)
salidaX=Pin(6,Pin.IN)
salidaY=Pin(7,Pin.IN)
salidaZ=Pin(8,Pin.IN)

#Pines pwm:

pwm_pinA = PWM(Pin(16))
pwm_pinB = PWM(Pin(19))

pwm_pinA.freq(1000)
pwm_pinB.freq(1000)

#Ldr
Ldr = ADC(Pin(27))

def decrementadormanual(A,B,C):
    if (A==0 or A==1) and (B==0 or B==1) and (C==0 or C==1):
        entradaA.value(A)
        entradaB.value(B)
        entradaC.value(C)
        X = salidaX.value()
        Y=salidaY.value()
        Z=salidaZ.value()
        actualizar_luces(Z,X,Y,Y)
    else:
        return "error"

def decrementadorldr(num8):
    luces_entorno=Ldr.read_u16()
    while num8==1:
        luces_entorno=Ldr.read_u16()
        if luces_entorno>=0 and luces_entorno<8192:
            decrementadormanual(0, 0, 0)
            print(luces_entorno)
        elif luces_entorno>=8192 and luces_entorno<16384:
            decrementadormanual(0, 0, 1)
            print(luces_entorno)
        elif luces_entorno>=16384 and luces_entorno<24576:
            decrementadormanual(0, 1, 0)
            print(luces_entorno)
        elif luces_entorno>=24576 and luces_entorno<32768:
            decrementadormanual(0, 1, 1)
            print(luces_entorno)
        elif luces_entorno>=32768 and luces_entorno<40960:
            decrementadormanual(1, 0, 0)
            print(luces_entorno)
        elif luces_entorno>=40960 and luces_entorno<49152:
            decrementadormanual(1, 0, 1)
            print(luces_entorno)
        elif luces_entorno>=49152 and luces_entorno<57344:
            decrementadormanual(1, 1, 0)
            print(luces_entorno)
        elif luces_entorno>=57344 and luces_entorno<=65535:
            decrementadormanual(1, 1, 1)
            print(luces_entorno)
    
    if num8==0:
        actualizar_luces(0, 0, 0, 0)
        
    
    num=num/7
    

#Función que detiene los motores de la maqueta
def detener():
    pwm_pinA.duty_u16(0)
    pwm_pinB.duty_u16(0)
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)

#Función que avanza o retrocede el auto a cierta potencia
def pwm(num1):
    if num1 == 0:
        pwm_pinA.duty_u16(0)
        pwm_pinB.duty_u16(0)

    elif num1 == 1:
        pwm_pinA.duty_u16(32768)
        pwm_pinB.duty_u16(65535)
        in1.value(0)
        in2.value(1)
        utime.sleep(2)
        detener()

    elif num1 == 2:
        pwm_pinA.duty_u16(40960)
        pwm_pinB.duty_u16(65535)
        in1.value(0)
        in2.value(1)
        utime.sleep(2)
        detener()

    elif num1 == 3:
        pwm_pinA.duty_u16(49152)
        pwm_pinB.duty_u16(65535)
        in1.value(0)
        in2.value(1)
        utime.sleep(2)
        detener()

    elif num1 == 4:
        pwm_pinA.duty_u16(65534)
        pwm_pinB.duty_u16(65535)
        in1.value(0)
        in2.value(1)
        utime.sleep(2)
        detener()

    elif num1 == -1:
        pwm_pinA.duty_u16(32768)
        pwm_pinB.duty_u16(65535)
        in1.value(1)
        in2.value(0)
        utime.sleep(2)
        detener()

    elif num1 == -2:
        pwm_pinA.duty_u16(40960)
        pwm_pinB.duty_u16(65535)
        in1.value(1)
        in2.value(0)
        utime.sleep(2)
        detener()

    elif num1 == -3:
        pwm_pinA.duty_u16(49152)
        pwm_pinB.duty_u16(65535)
        in1.value(1)
        in2.value(0)
        utime.sleep(2)
        detener()

    elif num1 == -4:
        pwm_pinA.duty_u16(65535)
        pwm_pinB.duty_u16(65535)
        in1.value(1)
        in2.value(0)
        utime.sleep(2)
        detener()

    else:
        print("Valor Incorrecto")

#Función que controla el la dirección del auto (giro izquierda, giro derecha, avanzar, retroceder)
def dir(num2):
    detener()
    pwm_pinA.duty_u16(32768)
    pwm_pinB.duty_u16(65535)

    if num2 == 0:
        in1.value(0)
        in2.value(1)
       
        
    elif num2 == -1:
        in3.value(0)
        in4.value(1)

        
    elif num2 == 1:
        in3.value(1)
        in4.value(0)

        
    elif num2 == 2:
        in1.value(1)
        in2.value(0)

        
    else:
        print("Valor Incorrecto")
        detener()
        
    utime.sleep(2)
    detener()

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


#Función que enciende o apaga las luces según la luminosidad del entorno y si el modo está activado
def ldr(num7):


    while num7==1:
        luminosidad = Ldr.read_u16()
        if luminosidad<35000:
            actualizar_luces(1, 1, 0, 0)

        elif luminosidad>=35000:
            actualizar_luces(0, 0, 0, 0)

        else:
            detener()
            actualizar_luces(0, 0, 0, 0)
            print("Error")
    if num7 == 0:
        actualizar_luces(0, 0, 0, 0)
    else:
        print("Valor Incorrecto")

#Estructura Comandos para Instrucciones de Patrón:

#Función que mueve el auto con una trayectoria que forma un círculo
def Circle():
    pwm_pinA.duty_u16(65535)
    pwm_pinB.duty_u16(65535)
    in4.value(1)
    utime.sleep(0.75)
    in2.value(1)
    utime.sleep(3)
    detener()

#Función que mueve el auto con una trayectoria que forma el símbolo de infinito
def Infinite():
    pwm_pinA.duty_u16(65535)
    pwm_pinB.duty_u16(65535)
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
    pwm_pinA.duty_u16(65535)
    pwm_pinB.duty_u16(65535)
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
    
EntradaA=machine.Pin(2,machine.Pin.OUT)
EntradaB=machine.Pin(3,machine.Pin.OUT)
EntradaC=machine.Pin(4,machine.Pin.OUT)
 
Resultado1=machine.Pin(6,machine.Pin.IN,machine.Pin.PULL_DOWN)
Resultado2=machine.Pin(7,machine.Pin.IN,machine.Pin.PULL_DOWN)
Resultado3=machine.Pin(8,machine.Pin.IN,machine.Pin.PULL_DOWN)
 
EntradaA.value(1)
EntradaB.value(1)
EntradaC.value(0)
 
 
