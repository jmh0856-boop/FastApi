from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Gender(str, Enum):
    male = "male"
    female = "female"


class UserCreateRequest(BaseModel):
    username: str
    age: int
    gender: Gender


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    age: Optional[int] = None


class UserFilterParams(BaseModel):
    # 추가 매개변수 전달 시 에러를 반환하도록 설정 (조건 2)
    model_config = ConfigDict(extra="forbid")

    # 쿼리 매개변수 정의 및 유효성 검증
    username: Optional[str] = None
    age: Optional[int] = Field(None, gt=0)  # 0보다 큰 값만 허용 (조건 1-a)
    gender: Optional[str] = None
