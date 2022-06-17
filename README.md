Laboratorio 3: Criptografia y seguridad en redes
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

## Comparativas entre algorimos[^2]
- En la siguientes tablas se puede observar el rendimiento de este algoritmo de Hash y el de otros.

### Comparativa con un string
- Para realizar esta comparativa, se utilizo el string `ColoColoLoMasGrande`.[^bignote]

|            | **LARGO** | **BASE** | **ENTROPIA** | **RENDIMIENTO (MS)** |
|------------|-----------|----------|--------------|----------------------|
| **MD5**    | 32        | 14       | 122          | 25                   |
| **SHA1**   | 40        | 14       | 153          | 23                   |
| **SHA256** | 64        | 16       | 256          | 9                    |
| **HASHJG** | 60        | 34       | 306          | 0.8                  |

### Comparativa con un archivo
- Para realizar esta comparativa, se utilizo el archivo [HimnoColoColo](HimnoColoColo.txt).

|            | **LARGO** | **BASE** | **ENTROPIA** | **RENDIMIENTO (MS)** |
|------------|-----------|----------|--------------|----------------------|
| **MD5**    | 32        | 14       | 122          | 5                    |
| **SHA1**   | 40        | 16       | 160          | 11                   |
| **SHA256** | 64        | 16       | 256          | 6                    |
| **HASHJG** | 60        | 36       | 311          | 23                   |


[^1]: Se requiere instalar la libreria de [Base58](https://pypi.org/project/base58/).
[^2]: Para estas comparativas, se utilizo:

    SO  : Windows 10 v21H2.
    
    CPU : Intel(R) Core(TM) i5-3570S CPU @ 3.10GHz   3.10 GHz.
    
    RAM : 8,00 GB.
    
    Sistema operativo de 64 bits, procesador x64.
    
    Todo se ejecuto mediante la consola de WSL.
