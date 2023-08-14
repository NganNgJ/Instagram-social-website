# Project name: ${\color{blue}Project \space name}$

###1. Introduction:


###2. Features:
| No | Feature name |<div style="width:425px">Details</div>| API|
|:---:|:---:|---|---|
| 1 | Create new post | a. Contents (text) <br> b. Media (Image/Video/Music) <br> c. Files <br> d. Links | `POST`|
| 2 | Edit post | a. Allow edit contents <br> b. Add/change people | `PUT` |
| 3 | Reaction | Like/Dislike | `POST`
| 4 | Comment | a. Tag friends <br> b. Edit comment | `PUT`|
| 5 | Delete | a. Posts <br> b. Comments | `DELETE` |
| 6 | Search/filter | a. Contents <br> b. Friends' name <br> c. Tags | `GET` |
| 7 | List posts | a. Show detail? <br> b. Total likes | `GET` |
| 8 | Add friend | Follow/ Unfollow
| 9 | Profiles | a. Edit infor <br> b. Upload avatar <br> c. Show profile| `POST`|
| 10| Settings | a. Block accounts <br> b. Languages | `PUT`|
| 11| Authentication and permission | a. Create new account <br> b. Check authentication <br> c. Verify OTP | 


---
## Sources
### 1. Dockers steps:
    a. Create a network 
        > docker network create social_network
    b. Build mySQL container (create .env file)
        > docker run -d --name social-mysql -p 3309:3306 -v "D:/Sources/social-api-2/data:/var/lib/mysql" --network social_network --env-file .env  mysql:5.7.13 --default-authentication-plugin=mysql_native_password
    c. Create Django project 
        > docker run -it --rm -v "D:/Sources/social-api-2/src:/app" --network social_network python:3.7.1 bash -c "pip install django && django-admin startproject socialweb && mv socialweb/* /app/ && rmdir socialweb"
    d. Build an Image 
        > docker build -t socialweb .
    e. Create server
        > docker run -it -p 8000:8000 --name social-web -v "D:/Sources/social-api-2/src:/app" --network social_network socialweb
### 2. Migrate database 
1. Execute to container application 
    > *docker exec -it social-web /bin/bash*

2. Run migrate in order to all default dbs's Django  (one time)
    > *python manage.py migrate*

3. Get the last Django (ignore 'sessions')
    > *SELECT * FROM <database_name>.django_migrations order by applied desc;*

4. Run makemigrations (make sure to have all Models) & add the last Django (3) into 'dependencies' 
    > - *python manage.py makemigrations*
    > - *Add dependencies = [('auth', '<last_django>'),]*

5. Change new migrations (if any)

6. Run Migrate to update any new changes from Models (from migrations files at step 4)
    > *python manage.py migrate*


# Coi log: mình sẽ coi theo tail log, tức là coi ở cuối file log của docker, và thêm -f (--follow) để khi có log mới thì nó cũng sẽ append thêm luôn
ví dụ log có tail nhưng ko có -f: sau khi chạy lệnh nó sẽ thoát khỏi file log luôn, tức là chỉ hiện tail 100 dòng cuối file
còn nếu có -f: nó sẽ giữ luôn trạng thái log, khi có lệnh gì hay log mới nó sẽ hiện lên luôn, đó Ngân chạy source web là hiểu :D 

docker logs -f --tail 100 social-mysql # xem log 100 dòng cuối cùng và follow khi có dòng mới dc thêm vào log

