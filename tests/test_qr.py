from PIL import Image

from src.qr_code_test.qr_generator import QRCodeGenerator, QRCodeOverlayer

if __name__ == "__main__":
    # 1. Генератор QR
    generator = QRCodeGenerator(size=100, fill_color="black", back_color="white")

    # 2. Overlay
    overlayer = QRCodeOverlayer()

    # 3. Создаём QR
    qr = generator.create("https://dtf.ru/")

    # 4. Загружаем базовое изображение
    base_image = Image.open("input.jpg").convert("RGB")

    # 5. Накладываем QR
    result_img = overlayer.overlay(
        base_image=base_image, qr_code=qr, x=50, y=50, size=100)

    # 6. Сохраняем результат
    result_img.save("test_img.png")
    print("Image with QR saved as test_img.png")
