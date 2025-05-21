from PIL import Image

def aplicar_filtro_bn(ruta_entrada, ruta_salida):
    """Convierte una imagen a blanco y negro."""
    imagen = Image.open(ruta_entrada).convert("L")  # Convertimos a escala de grises
    imagen.save(ruta_salida)
    print(f"Imagen blanco y negro guardada en {ruta_salida}")

def aplicar_filtro_sepia(ruta_entrada, ruta_salida):
    """Aplica un filtro sepia a la imagen."""
    imagen = Image.open(ruta_entrada)
    pixeles = imagen.load()

    for y in range(imagen.height):
        for x in range(imagen.width):
            r, g, b = imagen.getpixel((x, y))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            # Aseguramos que los valores estén en el rango [0, 255]
            sepia = (
                min(255, tr),
                min(255, tg),
                min(255, tb)
            )

            pixeles[x, y] = sepia

    imagen.save(ruta_salida)
    print(f"Imagen sepia guardada en {ruta_salida}")

aplicar_filtro_bn("cbum normal.jfif", "cbum bn.jfif")
aplicar_filtro_sepia("cbum normal.jfif", "cbum sepia.jfif")
