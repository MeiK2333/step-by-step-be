import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/groups")
def group_list():
    resp = requests.get("https://stepbystep.sdutacm.cn/API/GetOrgList")
    data = []
    for item in resp.json()["list"]:
        data.append({"id": item["id"], "code": item["shortName"], "name": item["name"]})
    return data


@app.get("/group/{group_id}/set")
def group_set(group_id: int):
    resp = requests.get(
        f"https://stepbystep.sdutacm.cn/API/GetStepList?orgId={group_id}"
    )
    data = []
    for item in resp.json()["list"]:
        data.append(
            {
                "id": item["id"],
                "source": item["source"],
                "name": item["title"],
                "problem": item["problemCount"],
                "person": item["userCount"],
            }
        )
    return data


@app.get("/group/{group_id}")
def group(group_id: int):
    resp = requests.get("https://stepbystep.sdutacm.cn/API/GetOrgList")
    for item in resp.json()["list"]:
        if item["id"] == group_id:
            return item
    return {}


@app.get("/set/{set_id}/problems")
def set_problems(set_id: int):
    resp = requests.get(f"https://stepbystep.sdutacm.cn/API/GetStep?stepId={set_id}")
    return resp.json()["problemList"]


@app.get("/set/{set_id}")
def set_detail(set_id: int):
    resp = requests.get(
        f"https://stepbystep.sdutacm.cn/API/GetStep?stepId={set_id}"
    ).json()
    for item in resp["userList"]:
        item["id"] = item["userId"]
        item.pop("userId")
        item.pop("class")
        item.pop("count")
    data = {
        "problems": resp["problemList"],
        "persons": resp["userList"],
        "name": resp["title"],
    }
    prob_set = set()
    for problem in data['problems']:
        prob_set.add(problem['problem'])
    for person in data["persons"]:
        username = person.pop("userName")
        solutions = {}
        for key, value in resp["data"][username].items():
            if key not in prob_set:
                continue
            solutions[key] = {"result": "Accepted", "date": value}
        person["solutions"] = solutions
    return data
