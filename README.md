# Project name: ${\color{green}Project \space name}$

### 1. Introduction:
This is a social website project running as Instagram, however, it will have some features that Instagram hasn't supported currently such as download images/video.

### 2. Features:
| No | Feature name |<div style="width:425px">Details</div>| API|
|:---:|:---:|---|---|
| 1 | Create new post | a. Contents (text) <br> b. Media (Image/Video/Music) <br> c. Files <br> d. Links | `POST`|
| 2 | Edit post | a. Allow edit contents <br> b. Add/change people | `PUT` |
| 3 | Reaction | Like/Dislike | `POST`
| 4 | Comment | a. Tag friends <br> b. Edit comment | `PUT`|
| 5 | Delete | a. Posts <br> b. Comments | `DELETE` |
| 6 | Download | Allow download image, video
| 7 | Search/filter | a. Contents <br> b. Friends' name <br> c. Tags | `GET` |
| 8 | List posts | a. Show detail & .... <br> b. Total likes | `GET` |
| 9 | Add friend | Follow/ Unfollow
| 10 | Profiles | a. Edit infor <br> b. Upload avatar <br> c. Show profile| `POST`|
| 11| Settings | a. Block accounts <br> b. Languages |`PUT`|
| 12| Authentication and permission | a. Create new account <br> b. Check authentication <br> c. Verify OTP | 


---
### 3. Sources
#### Build containers by Docker compose:
Check docker-compose.yml 
> cmd: docker compose up --build -d  

#### Migrate database 
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




