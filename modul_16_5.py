from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []


class Users(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/')
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get(path='/user/{user_id}')
async def get_message(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id - 1]})
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found')


@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username',
                                                    example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> str:
    try:
        user_id = users[-1].id + 1
        user = Users(id=user_id, username=username, age=age)

    except IndexError:
        user = Users(id=1, username=username, age=age)
    users.append(user)
    return f"User {user} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int = Path(ge=1, le=250, description='Enter user_id', example=16),
                      username: str = Path(min_length=5, max_length=20, description='Enter username',
                                           example='UrbanUser'),
                      age: int = Path(ge=18, le=120, description='Enter age', example=24)) -> str:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return f"The user {user} has been updated."
    raise HTTPException(status_code=404, detail='Message not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int = Path(ge=1, le=250, description='Enter user_id', example=16)) -> str:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return f'User {user} has been deleted'
    raise HTTPException(status_code=404, detail='Message not found')

