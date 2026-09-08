from pydantic import BaseModel


class DeviceTokenIn(BaseModel):
  device_token: str
  platform: str