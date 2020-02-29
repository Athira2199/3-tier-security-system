# 3-tier-security-system
###ADMIN
```
An admin can add users to the system.
Whenever an admin adds a user a folder will be automatically created for the user and the
images reuired for training can be added to it.
```
###USERS
```
This system authenticates each of its users using three stages.

   1.Stage 1 beign the login stage
   2.Stage 2 the otp stage
   3.Stage 3 the face recognition stage
```
```
STAGE 1
------------------
In this stage each user has to input his/her credentials which refers to his/her username and password.

STAGE 2
------------------
Once the user has successfully passed the first stage he/she will receive an otp in his/her registered mail id.
He/she is required to add this otp in the otp field to pass this stage.

STAGE 3
------------------
Once the user has successfully passed the second stage the face recognition part starts running automatically.
It then checks if the logged in user and recognized face are same.If yes then it will grant access.
```
