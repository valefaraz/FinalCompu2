class Parceo():
     def parcear(dato):
        try:
            encabezado = dato.decode().splitlines()[0]
            pedido = encabezado.split()
        except:
            pass

        return(pedido)
        
