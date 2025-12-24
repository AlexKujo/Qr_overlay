from PIL import Image
import io
from qr_generator import QRCodeGenerator, QRCodeOverlayer
from schemas import QRRequest
import state

def generate_qr_url(chat_id: int, user_id: int) -> str:
    return f"{state.BASE_URL}/invite?chat_id={chat_id}&user_id={user_id}"


def create_qr_code(qr_data: str, size: int) -> Image.Image:
    generator = QRCodeGenerator(size=size)
    return generator.create(qr_data)


def overlay_qr_on_image(
    base_image: Image.Image,
    qr_code: Image.Image,
    x: int,
    y: int,
    size: int
) -> Image.Image:

    overlayer = QRCodeOverlayer()
    return overlayer.overlay(
        base_image=base_image,
        qr_code=qr_code,
        x=x,
        y=y,
        size=size,
    )


def image_to_bytes(image: Image.Image) -> bytes:
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output.read()


def process_qr_overlay(base_image: Image.Image, request: QRRequest) -> bytes:
    # region docstring
    """
    Обрабатывает наложение QR-кода на изображение

    Args:
        base_image: Базовое изображение
        request: Модель запроса с данными

    Returns:
        Байты обработанного изображения в формате PNG
    """
    # endregion

    qr_data = generate_qr_url(request.chat_id, request.user_id)
    print("QR DATA =", repr(qr_data))
    qr_code = create_qr_code(qr_data, request.qr_size)
    result_image = overlay_qr_on_image(
        base_image=base_image,
        qr_code=qr_code,
        x=request.qr_x,
        y=request.qr_y,
        size=request.qr_size
    )
    return image_to_bytes(result_image)
