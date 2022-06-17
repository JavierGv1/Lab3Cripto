import base58
import time
import math

"""Funcion que transforma de Hexadecimal a Base58"""
def HexToB58(HexString):
  """
  Si el largo de HexString es impar, se le agrega el primer carater
  ya que de ser impar, existe un numero en Hexadecimal que le falta un
  caracter, por lo que al momento de realizar la conversion, esta fallaria.
  """
  if len(HexString)%2!=0:
    HexString=HexString+HexString[1]
  
  """Se realiza la conversion de Hex a Base58"""
  bytes_str = bytes.fromhex(HexString)
  base58_str = base58.b58encode_check(bytes_str)

  return base58_str.decode('UTF-8')

"""Funcion que realiza el Hash"""
def Hashing(text):
  print("Hashing...")
  """Se transforma de ASCII a Hex para realizar el XOR"""
  KeyHex = text.encode().hex()
  DigKey = list(KeyHex)

  """
  Se le agrega el primere carater, para posteriormente realizar XOR
  con el resultado del XOR de los caracteres anteriores.
  El resultado del XOR es de forma '0XAB'
  """
  Xor=[]
  Xor.append(int(DigKey[0]+DigKey[1],16)^int(DigKey[2]+DigKey[3],16))

  for i in range(4,len(DigKey)-1,2):
    Xor.append(Xor[len(Xor)-1]^int(DigKey[i]+DigKey[i+1],16))

  TextHex=""

  """
  Se transforma el resultado Hex de string a numero, osea
  pasa de '0XAB' a 'AB'. Además que se transforma de lista a string.
  """

  for i in Xor:
    Hex = hex(i)
    Hex=Hex.split('x')
    TextHex+=(Hex[1])

  """Se realiza la conversión de Hex a Base58"""
  Hash = HexToB58(TextHex)
  
  """Se recorta el Hash con el fin que este sea de 60 caracteres."""  
  Hash=Hash[:60]

  return Hash
  
"""Funcion que Extiende un String"""
def Extend(text):
  print("Extendiendo...")
  """
  En caso de ser menor que 55 caracteres, ya que en con esta 
  cantidad de caracteres, el Hash posee un largo entre 60 
  y 65 caracteres. 
  Para extender este string, se agrega el mismo string pero de manera
  invertida, alternando cada vez que se termine de recorrer el string.
  En caso que sea mayor, todavia no se encuentra implementado.
  """
  if len(text)<=55:
    i=0
    rev=0
    while len(text)<=55:
      if i%55==0:
        if rev==0:
          rev=-1
        else:
          rev=0
      text = text+text[i%55::rev]
      i+=1

  return text

"""Funcion que Comprime un String"""
def Compress(text):
  print("Comprimiendo...")
  """
  Se transforma el string ingresado a Hex con el fin de
  poder realizar un XOR entre sus caracteres.
  """
  KeyHex = text.encode().hex()
  DigKey = list(KeyHex)

  Comp=[]
  """
  Se transforma a lista de caracteres anteriores a una 
  lista de numeros en Hex.
  """
  for i in range(4,len(DigKey)-1,2):
    Comp.append(DigKey[i]+DigKey[i+1])
  
  """
  Mientras el largo sea mayor a 55 caracteres, se realiza
  el XOR entre sus primeros carateres. Estos son eliminados de la lista
  y el resutaldo del XOR es agregado el final.
  En caso que el resultado del XOR sea mayor a 2 digitos,
  este se recorta a los 2 primeros.
  """
  while(len(Comp)>55):
    Hex1 = str(Comp.pop(0))
    Hex2 = str(Comp.pop(0))

    Xor = str(int(Hex1,16)^int(Hex2,16))

    if len(Xor)>2:
      Xor = Xor[2:]

    Comp.append(int(Xor,16))
  """
  Se transforma los resultados de los XOR a string,
  para posterirmente transformarlo a Base58.
  """
  Text = ""

  for i in Comp:
    try:
      Hex = hex(i)
    except TypeError:
      Hex = hex(int(i,16))

    Hex=Hex.split('x')
    Text+=(Hex[1])

  Text = HexToB58(Text)

  return Text[:60]

print("-----------------------------------------------------")

while(True):

  print("Ingrese la opción que desea ejecutar: ")
  print("1 - Hash a un texto")
  print("2 - Hash a un archivo")
  print("3 - Hash a un archivo linea por linea")
  print("4 - Entropia de un texto")
  print("0 - Finalizar programa")

  op = int(input("Opción "))

  print("-----------------------------------------------------")

  if(op==0):
    print("Adios")
    print("-----------------------------------------------------")
    break

  #Si la opcion es igual a 1, entonces se necesita Hashear un string
  elif op==1:
    text = input("Ingrese el texto: ")
    StarTime=time.time()

    """
    Se verifica la longitud del string ingresado,
    para extenderlo o acortarlo.
    """
    if len(text)<55:
      text = Extend(text)
    elif len(text)>55:
      text = Compress(text)

    """Se le realiza el Hash al string ingresado."""
    
    Hash=Hashing(text)
    ExecutionTime=time.time() - StarTime

    print("-----------------------------------------------------")
    print("Hash: ",Hash)
    print("-----------------------------------------------------")
    print("Tiempo de ejecucion: ",ExecutionTime,"s")
    print("-----------------------------------------------------")

  #Si la opcion es igual a 2, entonces se necesita Hashear un archivo
  elif op==2:
    Path = input("Ingrese la ruta del archivo: ")
    StarTime=time.time()

    """
    Para Hashear al archivo, se leeran cada 100 bytes
    con el fin de optimizar la memoria.
    """
    BUF_SIZE = 1024
    Hash=""

    """Se lee el archivo"""
    with open(Path,'rb') as f:
      while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        else:
          """
          En 'data' se encuentra el archivo en bytes.
          Esto se transforma a base58 para su mejor manipulacion.
          Posteriormente se realiza el Hash.
          """
          data = str(base58.b58encode_check(data))
          Hash += Hashing(data)

    Hash = Compress(Hash)

    """
    Se comprime el Hash resultante con el finde que el resultado
    sea de 60 caracteres.
    """
    ExecutionTime=time.time() - StarTime

    print("-----------------------------------------------------")
    print("Hash: ",Hash)
    print("-----------------------------------------------------")
    print("Tiempo de ejecucion: ",ExecutionTime,"s")
    print("-----------------------------------------------------")
  
  #Si la opcion es igual a 3, entonces se necesita Hashear un archivo linea por linea  
  elif op==3:
    Path = input("Ingrese la ruta del archivo: ")
    Rows = int(input("Ingrese la cantidad de iteraciones: "))

    """
    Para Hashear al archivo, se leeran cada linea.
    """
    Hash=""
    count=0
    """Se lee el archivo"""
    with open(Path) as file:
      for line in file:
          if count==Rows:
            break
          line=line[:-1]
          LineTime=time.time()
          """
          Se verifica la longitud del string ingresado,
          para extenderlo o acortarlo.
          """
          if len(line)<55:
            Text = Extend(line)
          elif len(line)>55:
            Text = Compress(line)

          """Se le realiza el Hash al string ingresado."""
          
          Hash=Hashing(Text)
          ExecutionTime=time.time() - LineTime
          print("-----------------------------------------------------")
          print("Linea: ",line)
          print("-----------------------------------------------------")
          print("Hash: ",Hash)
          print("-----------------------------------------------------")
          print("Tiempo de ejecucion: ",ExecutionTime,"s")
          print("-----------------------------------------------------")
          count+=1
  
  #Si la opcion es igual a 4, se busca calcular la entropia de un string
  elif op==4:
    text = input("Ingrese el texto: ")

    """Se lista el texto ingresado, eliminando los elementos repetidos."""
    BaseText = list(dict.fromkeys(text))

    """Se obtiene el largo, la base y se calcula la entropia del string."""
    Len = len(text)
    Base = len(BaseText)
    H = math.ceil(Len*math.log2(Base))

    print("-----------------------------------------------------")
    print("Base: ",Base)
    print("Largo: ",Len)
    print("Entropia: ",H)
    print("-----------------------------------------------------")

  else:
    print("Opcion incorrecta.")
    print("-----------------------------------------------------")