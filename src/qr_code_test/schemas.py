from pydantic import BaseModel


class QRRequest(BaseModel):
    qr_x: int
    qr_y: int
    qr_size: int
    image_width: int
    image_height: int
    reasoning: str
    chat_id: int
    user_id: int

    class Config:
        extra = "ignore"