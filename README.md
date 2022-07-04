## Running Application from a Docker Container (Preferred Option)
1. Open command-line interface (search **cmd** in windows or **terminal** in mac)
2. Type ```docker run -it dsandoval571/geo_data``` and press **ENTER**
3. After docker container has downloaded and is running, type ```python app.py``` and press **ENTER**
4. type ```exit``` and press **ENTER** to exit the container AFTER quitting the console application


## Building Docker Container Locally then Running from Local Image
1. Open command-line interface (search **cmd** in windows or **terminal** in mac)
2. cd into **src** folder
3. Run ```docker build -t ds_geo_data:latest .```
4. Run ```docker run -it ds_geo_data```
5. Once docker container is up and runninng, run ```python app.py```


## Running Application on Local Machine
**Note: This assumes you have the dependencies to run the application. It is HIGHLY RECOMMENDED to run this application in a Docker container.**
1. Open command-line interface (search **cmd** in windows or **terminal** in mac)
2. Navigate to **src** folder
3. Run ```python app.py```
