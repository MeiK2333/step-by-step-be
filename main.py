from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from logger import module_logger
from models.bind_user import BindUser
from models.db import get_db
from models.solution import Solution
from models.user import User
from schemas.exception import SBSException, exception_handler
from views.admin import router as admin_router
from views.auth import router as auth_router
from views.groups import router as groups_router
from views.steps import router as steps_router

module_logger("uvicorn")
logger = module_logger("stepbystep")

app = FastAPI()

app.add_exception_handler(SBSException, exception_handler)
app.include_router(groups_router)
app.include_router(steps_router)
app.include_router(admin_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/events")
def get_events(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if user is None:
        raise SBSException(errmsg="user not found")
    bind_users = db.query(BindUser.id).filter_by(user=user)
    query = (
        db.query(
            func.count(Solution.id).label("count"),
            func.strftime("%Y-%m-%d", Solution.submitted_at).label("date"),
        )
        .filter(Solution.bind_user_id.in_(bind_users))
        .group_by(func.strftime("%Y-%m-%d", Solution.submitted_at))
    )
    res = query.all()
    return res


@app.get("/solutions")
def get_solutions(limit: int = 20, username: str = None, db: Session = Depends(get_db)):
    if limit > 1000:
        limit = 1000
    resp = []
    query = db.query(Solution)
    if username is not None:
        user = db.query(User).filter_by(username=username).first()
        bind_users = db.query(BindUser.id).filter_by(user=user)
        query = query.filter(Solution.bind_user_id.in_(bind_users))
    solutions = query.order_by(Solution.submitted_at.desc()).limit(limit).all()
    for solution in solutions:
        solution: Solution
        resp.append(
            {
                "result": solution.result.name,
                "time_used": solution.time_used,
                "memory_used": solution.memory_used,
                "username": solution.bind_user.user.username,
                "nickname": solution.nickname,
                "code_len": solution.code_len,
                "submitted_at": solution.submitted_at.strftime("%Y-%m-%d %H:%M:%S"),
                "language": solution.language.name,
                "problem_id": solution.problem.problem_id,
                "title": solution.problem.title,
                "source": solution.problem.source.name,
                "link": solution.problem.link,
            }
        )
    return resp
