# capstone-project-9900f16agptea

## TEAM MEMBER
| Name | Uni Email Address (zid) | Role |
| ----------- | ----------- | -------- |
| Austin Yu  | z5017089@ad.unsw.edu.au | Product Manager |
| Siyuan Wu | z5412156@ad.unsw.edu.au  | Scrum Master |
| Chin Chai | z3405715@unsw.edu.au | Dev Member |
| Tsenguun Odgerel | z5330875@ad.unsw.edu.au | Dev Member |
| Qibai Chen | z5183891@ad.unsw.edu.au | Dev Member |
| Yuxuan Qin | z5331894@ad.unsw.edu.au | Dev Member |

## Import Team Porject Links
| Object Title | Link |
| ----------- | ----------- |
| Project Proposal |  https://unsw-my.sharepoint.com/:w:/r/personal/z5330875_ad_unsw_edu_au/Documents/COMP9900%20Project%20-%20GPTea%20-%20Anamoly%20Detection%20in%20pipeline.docx?d=w389a8504050b4fea80f4d075344bef30&csf=1&web=1&e=hlTNQH |
| System Architecture | https://drive.google.com/file/d/1XlNJDjW-G7Sxtw5psKVgmnms86LFlyNd/view?usp=sharing |
| Storyboards | https://www.figma.com/proto/64U5G1SbLWjPbCHEATFm46/WireFramer-%E2%80%93-Quick-wireframing-library-(Community)?type=design&node-id=310-4726&t=DrnskdfOUsWYrCu5-1&scaling=min-zoom&page-id=15%3A2725&starting-point-node-id=310%3A4726 |

## Configure Project
### Bash/Python command tools (for Git management)
make sure you have permission to run bash file at root
```
init_folder.sh
```
and permission to run bash file at bash folder
```
create_gitignore.sh
create_skeleton_folders.sh
```

Please edit above bash if necessary.


## Python Virtual Environment
- It is recommended that python is developed in virtual environment and recommended Python version is **Python 3.10**
- To create virtual environment, run following code at the project root folder.
```
python -m venv venv
```
- To activate the virtual environment, enter below at terminal at the root folder
```
source ./venv/bin/activate
```
- To install necessary python pacakges used, run below from time to time, as requirements.txt may get updated. You may also delete the entire venv and recreate the venv if necessary.
```
pip install -r requirements.txt
```

## Install Docker
Developers are expected to have Docker installed on their own computer.
- https://docs.docker.com/get-docker/


### Install and Run MySQL
- if you do not have MySQL at your device, or would like MySQL running at docker, run following code at terminal at root folder.
```
docker build -t comp9900-mysql ./backend_flask/mysql_db/
```
- Next, run following code and the MySQL container should run inside Docker. Docker dashboard can be used to start/stop the databse instance.
```
docker run -dit -p 3306:3306 -e MYSQL_ROOT_PASSWORD_FILE=/run/secrets/mysql-db-pass --name gptea-mysql comp9900-mysql
```
#### Create MySql Database
- run the python script below to create databases for both backend and mlflow.
```
python ./backend_flask/mysql_db/create_database.py
```
- if you need to re-create databases for both backend and mlflow, pass in an additional argument.
```
python ./backend_flask/mysql_db/create_database.py - r
```
- the old api can still be used. Check the code or consult at the team at Discord.


## Initiate MLFLOW Tracking Server
- mlflow should have been installed at the Python Virtual Environment, which is package listed at **requirements.txt**
```
mlflow server --backend-store-uri mysql+pymysql://root:gptea_admin@localhost:3306/mlflowdb --port 8080 --host 0.0.0.0 --default-artifact-root ./mlflow_tracking_server
```

## Initiate Backend Server
- following location of backend api may subject to change as it does not using multiple files for namespace.
```
python ./backend_flask/main.py
```
- if you have configured different mysql databse connection and/or password, edit the file at **backend_flask/config.py**