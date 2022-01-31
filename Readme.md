# CloudWiry_Hackathon

## About the Project
  This blob storage is built completely in python using FastAPI. It allows users to upload create new credentials and login to the system. User authentication is done through **JWT Tokens**. So the next time when they login to the system, the user will have to provide the JWT Token.

  Next, the user will have some basic features like   
* upload new file
* fetch all the files accessible to the user
* Update user details
* upload another file for the same user
* delete a particular user
----------------------------------------------------------------
* download a file accessible to the user
* rename an already existing file, again accessible to the user
* delete a file which is owned by a user
* share a file to another user (new user won't be the owner of the shared file)


## Live Demonstartion of the Project

  LIVE Demonstration: https://youtu.be/whAY6jsKJIk

## Installation

1. Clone repo on your local system

```bash
git clone https://github.com/MishraLokesh/CloudWiry_Hackathon.git
```
2. Open a terminal on your localhost and install the dependencies

```bash
pip install -r /path/to/requirements.txt
```
3. Setup a database in your system with the name of blob and import database from the file provided

4. In the backend directory, start the uvicorn

```bash
uvicorn index:app --reload
```

5. Open [localhost:8000/docs](localhost:8000/docs) to open the FastAPI docs and access all features of the API 

```bash
curl http://localhost:8000
```
You're good to go! 

## Connect with the Collaborators
1. Lokesh Mishra - [LinkedIN](https://www.linkedin.com/in/lokesh-mishra-0807/) || [GitHub](https://github.com/MishraLokesh) || [Instagram](https://www.instagram.com/lokesh.mishra__/)


## License
Distributed under the [MIT](https://choosealicense.com/licenses/mit/) license.



