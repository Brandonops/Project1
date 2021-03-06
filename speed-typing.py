import pygame
from pygame.locals import *
import sys
import time
import random

class Game:
    def __init__(self):
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.input_text = ""
        self.word = ""
        self.time_start = 0
        self.total_time = 0
        self.accuracy = "0%"
        self.results = "Time:0 Accuracy:0 %wpm:0 "
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 61, 61)
        self.TEXT_C = (255, 61, 61)
        self.RESULT_C = (255, 61, 61)


        pygame.init()
        #self.open_img = pygame.image.load("type-speed-open.png")
        #self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))
        
        
        self.bg = pygame.image.load("background.jpg")
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Typing Speed test")

        #applying text to the screen
    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font("myfont.ttf", fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center = (self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

        #getting random sentences pulled from text file
    def get_sentence(self):
        f = open("sentences.txt", "r").read()
        sentences = f.split("\n")
        sentence = random.choice(sentences)
        #self.draw_text(self.screen, sentence, (self.h - 301), 35, (19, 16, 16))
        self.draw_text(self.screen, sentence, (self.h - 299), 30, self.TEXT_C)
        return sentence

        #showing results/score
    def show_results(self, screen):
        if(not self.end):
            #calculate time
            self.total_time = time.time() - self.time_start
            self.total_time = round(self.total_time, 2)

            #calculate accuracy
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.word) * 100

            #calculate words per minute
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True
            #print(self.total_time)

            self.results = "Time: " + str(self.total_time) + " secs    Accruacy: " + str(round(self.accuracy)) + "%" + "    Wpm: " + str(round(self.wpm))

            #draw icon image
            self.time_img = pygame.image.load("icon.png")
            self.time_img = pygame.transform.scale(self.time_img, (75,75))
            screen.blit(self.time_img, (self.w/2 - 38, self.h-105))
            self.draw_text(self.screen,"Reset", (self.h - 70), 20, (255, 61, 61))

            print(self.results)
            pygame.display.update()

    #main method
    def run(self):
        self.reset_game()

        self.running = True
        while(self.running):
            Clock = pygame.time.Clock()
            self.screen.fill((198, 96, 48), (50,250,650,50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50,250,650,50), 2)
                        
            #updating the test of the user input
            self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    #position of the input box
                    if(x >= 50 and x<= 650 and y >= 250 and y <=300):
                        self.active = True
                        self.input_text = ""
                        self.time_start = time.time()

                    #position of the reset button
                    if(x >= 310 and x <= 510 and y >= 390 and self.end):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        #printing results to screen 
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            #print(self.results)
                            self.draw_text(self.screen, self.results, 350, 23, self.RESULT_C)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            pygame.display.update()

        Clock.tick(60)


    def reset_game(self):
        self.screen.blit(self.bg, (0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, 45, 80, (19, 16, 16))
        self.draw_text(self.screen, msg, 50, 80, self.HEAD_C)
        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False
        self.active = False

        self.input_text = ""
        self.word = ""
        self.time_start = 0 
        self.wpm = 0
        

        self.word = self.get_sentence()
        if (not self.word): 
            
            self.reset_game()

            # #applying heading to the screen
            # self.screen.fill((0, 0, 0))
            # self.screen.blit(self.bg, (0,0))
            # pygame.display.update()
            # msg = "Typing Speed Test!"
            # self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)

            # #applying the rectangle for the input box
            # pygame.draw.rect(self.screen, (255, 42, 42), (50,250,650,50), 2)


            # #applying the sentence 
            # self.draw_text(self.screen, self.get_sentence(), (self.h - 300), 26, (201, 42, 255))
            # print(self.get_sentence)
            # pygame.display.update()
            



Game().run()

