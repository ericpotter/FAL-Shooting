# Fake Aim Lab Shooting

The main purpose is to make it look like Aim Lab, but instead of using a mouse, you use your fingers as a mouse to shoot. There are three modes and three difficulty levels. There are different scores according to different modes and difficulty levels. The end screen will also show your current score and ranking.

## Pre Install
Before starting, Please check your computer has these environments and all the Python package
1. [Anaconda](###Anaconda)
2. [Keras](###Keras)
3. [OpenCV](###OpenCV)
4. [Tensorflow](###Tensorflow)
5. [Pygame](###Pygame)
6. [Mediapipe](###Mediapipe)


### Anaconda
1. Please go to the Anaconda website to download the software first
https://www.anaconda.com/download/
![anaconda](https://blog-cavedu.sgp1.digitaloceanspaces.com/wp-content/uploads/2018/09/00-0_2020-768x469.jpg)
2. After finishing downloading, open the Anaconda prompt on your computer
![anaconda prompt](https://blog-cavedu.sgp1.digitaloceanspaces.com/wp-content/uploads/2018/09/p11-768x257.png)
3. Create an Anaconda environment (type the following code in your prompt)
```cmd=
conda create --name testAI python=3.7 anaconda
```
4. Activate the environment
```cmd=
conda activate testAI
```
### Keras
5. Install Keras
```cmd=
conda install keras
```
### OpenCV
6. Install OpenCV
```cmd=
conda install opencv
```
### Tensorflow
7. Install Tensorflow
```cmd=
pip install tensorflow
```
8. Install Tensorflow Lite
```cmd=
pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-win_amd64.whl
```
### Pygame
9. Install Pygame
```cmd=
pip install pygame
```
### Mediapipe
10. Install Mediapipe
```cmd=
pip install mediapipe
```

## Game Start
Before running the file, please make sure all the files are on the same disk as the Anaconda environment in
1. Activate the Anaconda environment
```cmd=
conda activate testAI
```
2. Run the Game_Screen file
```cmd=
python Game_Screen.py
```
3. Start Playing!!

## Game Mode
### Random Shooting
One ball will move to a random position per time which can be adjusted in the settings
### Random and Decreasing
One ball will still move randomly but will decrease in size when every time you shoot
### Multiple Shooting
Up to six balls will show on the screen. Each time you shoot, you will add another ball on the screen. One random ball will randomly change its position.
## Game Rule
### Main Rule
1. Time Set: 30 seconds
2. Each Ball's Score: 
    * Easy: 15 points
    * Normal: 20 points
    * Hard: 30 points

In Multiple Shooting mode, this mode is comparatively easier, the base score will be five points less for each difficulty level, which is 10, 15 and 25 respectively
