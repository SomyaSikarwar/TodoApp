from fastapi import FastAPI, Depends ,HTTPException
import models  #importing models file which contains schema of the database
from auth import get_current_user
from database import engine,SessionLocal  # imported from database
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional



app = FastAPI()
models.Base.metadata.create_all(bind=engine)

#WE USED TRY AND FINALLY BLOCK BECAUSE NO MATTER WHAT WE HAVE TO CLOSE THE DATABASE AFTER USE
def get_db():   # getting the database
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title :str
    description : Optional[str]
    priority : int = Field(lt = 6 ,gt=0 ,default="Priority must be between 1-5")
    status : bool


@app.get("/")
async def create_database(db: Session = Depends(get_db)):
    return db.query(models.Todos).all() #WAY TO WRITE QUERY IN OUR FILE

@app.get("/todos/user")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db : Session = Depends(get_db) ):
    if user is None:
        raise HTTPException(status_code=404 , detail="User not found")
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()



#finding a todo by primary key
@app.get('/todo/{todo_id}')
async def find(todo_id : int,user : dict= Depends(get_current_user) ,db : Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=404 , detail="User not found")

    todo_model = db.query(models.Todos)\
                .filter(models.Todos.id == todo_id)\
                .filter(models.Todos.owner_id == user.get("id"))\
                .first()
    if todo_model is not None:
         return todo_model
    raise HTTPException(status_code=301 , detail="Todo not found")

@app.post("/")
async def create_todo(todo : Todo ,user : dict= Depends(get_current_user),db : Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=404 , detail="User not found")

    todo_model = models.Todos()
    todo_model.tiile = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.status = todo.status
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    #returning the user that creation is done
    return {
        "Satus" : 201,
        "Transaction" : "Successful"
    }

@app.put("/{todo_id)")
async def Update_todo(todo_id : int ,todo: Todo  ,user : dict= Depends(get_current_user),  db : Session = Depends(get_db)):
    todo_model = db.query(models.Todos)\
    .filter(models.Todos.id == todo_id)\
    .filter(models.Todos.owner_id == user.get("id"))\
    .first()


    if todo_model is None:
        raise HTTPException(status_code=202 , detail="todo model not found")

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.status = todo.status

    db.add(todo_model)
    db.commit()

    return {
        "Satus": 201,
        "Transaction": "Successful"
    }

@app.delete("/{todo_id}")
async def delete_todo(todo_id : int ,user : dict= Depends(get_current_user),db : Session = Depends(get_db)):
    #validate that the todo id exists
    todo_model =  db.query(models.Todos)\
    .filter(models.Todos.id == todo_id)\
    .filter(models.Todos.owner_id == user.get("id"))\
    .first()

    if todo_model is None:
        raise HTTPException(status_code=201 , detail="todo not found")

    db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .delete()

    db.commit()

    return {
        "Satus": 201,
        "Transaction": "Successful"
    }