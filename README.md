# Ransomware
Simple and effective ransomware application

## Features
* Strong AES Encryption
* Safe server-payload communication
* Payload's data tracking and restoration options
* Supports several options of tracking target files including full paths, root folders and using extensions or strict filenames
* Supports target's machine (terminal or graphic) UI for messaging and files recovery
* Payload compilation for more convenient portable option
* Easy graphic payload geneartor
* Custom victim message and ransom details

## Payload
The payload runs on the target's machine and responsible for several tasks:
* Establish connection with the server and register its data
* Locate target files on local machine's file system
* Encrypt the files and update the server about the process
* Run the defined user interface and notify the target machine's users about the attack
* Provide target files decryption and restoration interface
### Generator
Run ``plgenerator.py`` to load the payload generator window, where the payload's data is defined:
* Server's ip and port addresses
* Rasnom time in hours and json file containing the target files (see taregts files section)
* Payment data (optional- in case paymant is requiered) such as amount, payment details (such as crypto address) and contact details.
* User interface- console/terminal (text) or graphic (os window)
* Payload's filename (used for disguise) and ID number.
There are two options for generation: simple generation (.py file) or compilation (executable file) which is more portable.
#### Target files
The target files for encryption are defined in seperate file in JOSN format.
```json
{
  "files": {
  }
}
```
There are two sections:

Files per full path which could save expensive search time:
```json
{
  "files": {
    "fullPath": [
        "C:\Users\User\Documents\file1.txt"
      ]
  }
}
```
Files per root folder, which may include filenames or extensions:
```json
{
  "files": {
    "fullPath": [
      "C:\Users\User\Documents\file1.txt"
    ],
    "roots": [
      {
        "paths": ["C:/Users/User/Documents", "C:/Users/User/videos"],
        "files": [
          "accounts",
          "trip"
        ],
        "extensions": [
          ".py",
          ".exe",
          ".mp4",
          ".doc"
        ]
      }
    ]
  }
}
```
### Recovery
The files can be restored by inserting the cipher key and decrypting them throught the user inetrface once the attack is completed.
### Safety option
As the program was written for educaiotnal purpose soley it does not remove the encryption key from the victim's machine and provide a recovery option by revealing the key by a click of a button.
## Server
The server is used for payload registeriaiton, activation and storing their data and operation status. The payloads inform the server about the target files that were located and update their encryption status, send a copy of the generated cipher key and notify when an attacked is executed. The data can be extarcted any time and restored to the payloads when their activity is halted.

The server runs on the terminal and supports the following commands:
```console
Prints all registered payload
>>> all
Prints single payload where id is the desired payload's id
>>> pl id 
Quites server
>>> q
```



