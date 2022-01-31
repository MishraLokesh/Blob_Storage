# CloudWiry_Hackathon

## Instructions followed while building the project
  * All rules were kept in mind while making the project
  * No third party service was used for implementing the blob storage
  * The source code is totally unique and not copied from anywhere


## All checkpoints mentioned in the document are successfully implemented
  * Checkpoint A - User authentication and session management [done]   
    User is authenticated and session management is done using JWT tokens

  * Checkpoint B - Implementation of the blob storage server [done]   
    Blob storage is done locally on the system using mySQL database

  * Checkpoint C - Client application (CLI/ web based) for file upload, download, rename and delete [done]   
    The FastAPI docs provides a beautiful frontend in /docs to access the core functionalities of the API. For now, file to be uploaded should be kept in the File_Upload folder and on inserting to the DB, it will be inserted in the form of a longblob

  * Checkpoint D - User based access control on who can access the files [done]   
    User access is controlled by another table in the DB, which connects all the users with user_id to the files they have access to using file_id, and is_owner is used to detect who is the actual owner of the file and who has access to file since it was shared. (is_owner = 1 -> user is the actual owner  is_owner = 0 -> user got access to the file after someone shared the file)

  * Checkpoint E - Deploy the application [done]   
    The application was deployed successfully on **Deta** using the fastAPI docs. The deployed link is not working right now as the mySQL database is not present on the server where it is deployed. But the application is working totally fine on the local system.

  * Checkpoint F (optional - bonus points) - File compression [done]   
    File compression was also implemented using **zlib** library in python. The file uploaded by the user is converted to a blob, which is compressed before storing in the database. Once retrieved, the blob is first decompressed and then converted into a actual file.
  ----------------------------------------------------------------
## Other features implemented
  *  A high-level diagram is also uploaded in the github repository
  *  As mentioned, to make the application more scalable, it is completely **dockerized** and all the separate images including **mySQL, python 3.9**. A composite image is made and uploaded in the github repository
  *  The password entered in the database is encrypted using Bcrypt algorithm and also decrypted while verifying it at the time of user login. This ensures user's privacy.
  * The API completely follews REST principles.
  * Files to be uploaded are picked from the File_Upload directory and files downloaded are stored in the File_Download directory


## Live Demonstartion of the Project

  LIVE Demonstration: https://youtu.be/whAY6jsKJIk


## Connect with the Collaborators
1. Lokesh Mishra - [LinkedIN](https://www.linkedin.com/in/lokesh-mishra-0807/) || [GitHub](https://github.com/MishraLokesh) || [Instagram](https://www.instagram.com/lokesh.mishra__/)


## License
Distributed under the [MIT](https://choosealicense.com/licenses/mit/) license.



