from PIL import Image, ImageOps, ImageFilter

def aplicar_filtro_bn(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada).convert("L") 
    imagen.save(ruta_salida)
    print(f"Imagen blanco y negro guardada en {ruta_salida}")

def aplicar_filtro_sepia(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    pixeles = imagen.load()

    for y in range(imagen.height):
        for x in range(imagen.width):
            r, g, b = imagen.getpixel((x, y))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            sepia = (
                min(255, tr),
                min(255, tg),
                min(255, tb)
            )

            pixeles[x, y] = sepia

    imagen.save(ruta_salida)
    print(f"Imagen sepia guardada en {ruta_salida}")

def aplicar_filtro_negativo(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    imagen_negativa = ImageOps.invert(imagen.convert("RGB"))
    imagen_negativa.save(ruta_salida)
    print(f"Imagen negativa guardada en {ruta_salida}")
    
def aplicar_filtro_desenfoque(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    imagen_desenfocada = imagen.filter(ImageFilter.BLUR)
    imagen_desenfocada.save(ruta_salida)
    print(f"Imagen desenfocada guardada en {ruta_salida}")
      
def aplicar_filtro_bordes(ruta_entrada, ruta_salida):
    imagen = Image.open(ruta_entrada)
    imagen_bordes = imagen.filter(ImageFilter.FIND_EDGES)
    imagen_bordes.save(ruta_salida)
    print(f"Imagen con bordes guardada en {ruta_salida}")

def aplicar_filtro_grises_ajustable(ruta_entrada, ruta_salida, intensidad=0.5):
    imagen = Image.open(ruta_entrada)
    imagen_gris = imagen.convert("L")
    imagen_final = Image.blend(imagen.convert("RGB"), imagen_gris.convert("RGB"), intensidad)
    imagen_final.save(ruta_salida)
    print(f"Imagen en escala de grises ajustada guardada en {ruta_salida}")

def aplicar_filtro_pixelado(ruta_entrada, ruta_salida, pixel_size=10):
    imagen = Image.open(ruta_entrada)
    imagen_pequeña = imagen.resize(
        (imagen.width // pixel_size, imagen.height // pixel_size), Image.NEAREST
    )
    imagen_pixelada = imagen_pequeña.resize(imagen.size, Image.NEAREST)
    imagen_pixelada.save(ruta_salida)
    print(f"Imagen pixelada guardada en {ruta_salida}")

aplicar_filtro_bn("cbum normal.jfif", "cbum bn.jfif")
aplicar_filtro_sepia("cbum normal.jfif", "cbum sepia.jfif")
aplicar_filtro_negativo("cbum normal.jfif", "cbum negativo.jfif")
aplicar_filtro_desenfoque("cbum normal.jfif", "cbum desenfoque.jfif")
aplicar_filtro_bordes("cbum normal.jfif", "cbum bordes.jfif")
aplicar_filtro_grises_ajustable("cbum normal.jfif", "cbum grises ajustable.jfif", intensidad=0.7)
aplicar_filtro_pixelado("cbum normal.jfif", "cbum pixelado.jfif", pixel_size=10)