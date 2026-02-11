from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query
from app.models.users import UserModel
from app.schemas.users import UserCreateRequest, UserFilterParams, UserUpdateRequest

app = FastAPI()

UserModel.create_dummy()  # API 테스트를 위한 더미를 생성하는 메서드 입니다.


@app.post("/users")
async def create_user(data: UserCreateRequest):
    user = UserModel.create(**data.model_dump())
    return {"id": user.id}  # {"id": 11} 형태의 JSON 응답


@app.get("/users")
async def get_all_users():
    # UserModel의 all() 메서드로 데이터 가져오기
    users = UserModel.all()

    # 유저가 없는 경우 404 에러 반환
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@app.get("/users/{user_id}")
async def get_user(
    # 조건 1. Path 객체를 활용하여 user_id가 양수(gt=0)인지 검증
    user_id: Annotated[int, Path(gt=0)]
):
    # 검증된 user_id를 통해 UserModel 객체 가져오기
    user = UserModel.get(id=user_id)
    # 유저 객체가 없을 경우 404 에러 반환
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/users/{user_id}")
async def update_user(
    # Path 객체를 활용하여 user_id가 양수(gt=0)인지 검증
    user_id: Annotated[int, Path(gt=0)],
    # Pydantic 모델을 활용하여 데이터 유효성 검증
    data: UserUpdateRequest,
):
    # user_id를 이용해 UserModel 객체 가져오기
    user = UserModel.get(id=user_id)

    # 유저 객체가 없을 경우 404 에러 반환
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Request Body로 받은 데이터가 있을 경우에만 유저 정보 업데이트
    # model_dump(exclude_unset=True)를 쓰면 클라이언트가 보낸 값만 추출됩니다.
    user.update(**data.model_dump(exclude_unset=True))
    return user


@app.get("/users/search")
async def search_users(
    # Pydantic 모델을 활용하여 쿼리 매개변수 유효성 검증
    params: Annotated[UserFilterParams, Query()]
):
    # 전달받은 매개변수 중 값이 있는 것만 필터링 조건으로 추출
    filter_kwargs = params.model_dump(exclude_none=True)

    # UserModel.filter를 이용해 정보와 일치하는 유저 객체들을 가져옴
    users = UserModel.filter(**filter_kwargs)

    # 검색결과가 없을 경우 404 에러 반환
    if not users:
        raise HTTPException(status_code=404, detail="해당 조건의 유저가 없습니다.")
    return users


@app.delete("/users/{user_id}")
async def delete_user(
    # Path 객체를 활용하여 user_id가 양수(gt=0)인지 검증
    user_id: Annotated[int, Path(gt=0)]
):
    # 경로 매개변수로 넘겨받은 user_id를 이용해 UserModel 객체 가져오기
    user = UserModel.get(id=user_id)

    # user_id에 해당하는 유저 객체가 없을 경우 404 에러 반환
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # 유저 모델의 delete 메서드를 이용하여 유저 객체 삭제
    user.delete()
    return {"detail": f"User: {user_id}, Successfully Deleted."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
