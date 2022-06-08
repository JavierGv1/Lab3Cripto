Laboratiorio 3: Criptografia y seguridad en redes
===============
- En este laboratorio, se solicita la creacion de un de un algoritmo Hash. Este algoritmo debe ser funcional, mediante el ingreso de texto y/o un archivo. A su vez, el Hash resultante, pooser un largo fijo que sea independiente al largo del texto de entrada.
- Para ello, se implemento el siguiente Algoritomo: [Algoritmo](Hash.py).

## Descripción del algoritmo
- La idea principal del algoritmo a implementar es la realizacion de un **Xor** entre los primeros caracteres del texto, para posteriormente continuar realizando esta operacion, pero entre el resultado anterior y el nuevo caracter.
- Cabe recalcar, que para ello se realiza una transformación de ASCII a Hex y el resultado de esto se encuentra en una listade la forma: **'a','b'**.
```py
  Xor=[]
  Xor.append(int(DigKey[0]+DigKey[1],16)^int(DigKey[2]+DigKey[3],16))

  for i in range(4,len(DigKey)-1,2):
    Xor.append(Xor[len(Xor)-1]^int(DigKey[i]+DigKey[i+1],16))
```
- Posteriormente, transformar el resultado a Base58[^1].
```py
  bytes_str = bytes.fromhex(HexString)
  base58_str = base58.b58encode_check(bytes_str)
```
- En cuanto al largo resultante del Hash:
  - En caso que se tenga un texto que sea menor al 55 caracteres, se extiende cada 5 caracteres con la inversa de este texto.
  - Y en caso que este sea mayor a 55 caracteres, este se comprime mediante en **Xor** entre sus caracteres.
- Este largo se debe a que al momento de transformar el Hex a Base58, este posee un largo dinamico entre 60 y 65 caracteres. Para retornar un largo fijo de 60 caracteres, se realiza un recorte al resultado del algoritmo.
[^1]: Se requiere instalar la libreria de [Base58](https://pypi.org/project/base58/).
