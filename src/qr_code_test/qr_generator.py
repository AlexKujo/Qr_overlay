import qrcode
from PIL import Image
from dataclasses import dataclass


@dataclass
class QRCodeGenerator:
    size: int = 100
    fill_color: str = "black"
    back_color: str = "white"

    def create(self, data: str) -> Image.Image:
        qr = qrcode.QRCode(version=1, border=2)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color).convert("RGB")
        img = img.resize((self.size, self.size), Image.Resampling.NEAREST)
        return img


@dataclass
class QRCodeOverlayer:

    def overlay(
        self,
        base_image: Image.Image,
        qr_code: Image.Image,
        x: int,
        y: int,
        size: int,
    ) -> Image.Image:
        # region docstring
        """
        Накладывает QR-код на изображение

        Args:
            base_image: Базовое изображение
            qr_code: QR-код для наложения
            x: X координата позиции
            y: Y координата позиции
            size: размер

        Returns:
            Изображение с наложенным QR-кодом
        """
        # endregion

        result = base_image.copy()

        qr_resized = qr_code.resize((size, size), Image.Resampling.NEAREST)

        # if self.use_background:
        #     draw = ImageDraw.Draw(result)
        #     draw.rectangle([x, y, x + size, y + size], fill="white")

        result.paste(qr_resized, (x, y))
        return result
