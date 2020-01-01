__author__ = 'chenyiqun'

import pygame
import sys
from car_drive import CarDrive

def keyControl():
    pygame.init()
    pygame.display.set_caption("Auto Car")

    car = CarDrive()

    #生成控制窗口
    screen = pygame.display.set_mode((480,480),0,32) 

    while True:
        for event in pygame.event.get():
            
            #按键按下时
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_a:
                    car.left()
                elif event.key == pygame.K_d:
                    car.right()
                elif event.key == pygame.K_w:
                    car.forward()
                elif event.key == pygame.K_s:
                    car.backward()
                elif event.key == pygame.K_q:
                    sys.exit()
                    
            #按键松开时
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    car.stop()
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    car.middle()


if __name__ == '__main__':
    keyControl()
