import cv2

def capture_image():
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)  # Usar el índice 0 para la cámara USB

    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    # Capturar una imagen
    ret, frame = cap.read()

    # Verificar si la captura fue exitosa
    if not ret:
        print("Error al capturar la imagen")
        return

    # Guardar la imagen en un archivo
    cv2.imwrite("funciona.jpg", frame)

    # Liberar la cámara
    cap.release()

    print("Imagen capturada correctamente")

# Llamar a la función para capturar la imagen
capture_image()
