# ai-todo-py

This repo is a demo of a sample TODO app built via Python(using Flask + Mongodb)


## Initilize MongoDB

Start mongo docker container
```bash
# Create host data volume
mkdir -p /root/mongo/db
 
docker run --rm --name mongodb -p 27017:27017 \
-v=/root/mongo/db:/data/db \
-d mongo
```

Create user and collection.
```bash
docker exec -it mongodb mongo

> use todolist
switched to db todolist
> db.createUser({user: "todo", pwd: "todo", roles:[{role: "readWrite", db: "todolist"}]})
Successfully added user: {
        "user" : "todo",
        "roles" : [
                {
                        "role" : "readWrite",
                        "db" : "todolist"
                }
        ]
}
> db.createCollection("todo", {capped: false})
{ "ok" : 1 }
> exit
bye
```

## Run the app locally:

1. Build backend
```bash
docker build -t my-taskapi .

docker run --rm -d -p 8080:8080 --name taskapi  --link mongodb:db my-taskapi
```

2. Build frontend
```bash
docker build -t my-todo .

docker run --rm -d -p 8081:8081 --name todo  --link taskapi:api my-todo
```

3. Access 'localhost:8081'


## Run the app in kubernetes (local cluster):

- Use kubectl
```bash
kubectl apply -f manifests/mongo-pv.yaml
kubectl apply -f manifests/mongodb.yaml
kubectl apply -f manifests/backend.yaml
kubectl apply -f manifests/frontend.yaml
```

- Use skaffold
```bash
# run in local-cluster
skaffold config set --global local-cluster true
skaffold run
```