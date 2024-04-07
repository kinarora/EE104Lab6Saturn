# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 18:52:46 2024

@author: kinsh
"""

import pgzrun
import pygame

# Game dimensions
WIDTH = 1280
HEIGHT = 720

# Define the rectangles for various boxes
main_box = Rect(0, 0, 820, 240)
timer_box = Rect(0, 0, 240, 240)
answer_box1 = Rect(0, 0, 495, 165)
answer_box2 = Rect(0, 0, 495, 165)
answer_box3 = Rect(0, 0, 495, 165)
answer_box4 = Rect(0, 0, 495, 165)

# Move the rectangles to their positions
main_box.move_ip(50, 40)
timer_box.move_ip(990, 40)
answer_box1.move_ip(50, 358)
answer_box2.move_ip(735, 358)
answer_box3.move_ip(50, 538)
answer_box4.move_ip(735, 538)

# Group answer boxes for easier management
answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]
score = 0
time_left = 10

# Hint usage tracker
hint_shown = False
hint_message = ""

# Questions (with hints added as a new element at the end)
questions = [
    ["What is the capital of France?", "London", "Paris", "Berlin", "Tokyo", 2, "It's famous for the Eiffel Tower."],
    ["What is 5+7?", "12", "10", "14", "8", 1, "Think of a dozen."],
    ["What is the seventh month of the year?", "April", "May", "June", "July", 4, "It's named after Julius Caesar."],
    ["Which planet is closest to the Sun?", "Saturn", "Neptune", "Mercury", "Venus", 3, "It's not the hottest planet."],
    ["Where are the pyramids?", "India", "Egypt", "Morocco", "Canada", 2, "The Sphinx is also found here."],
    ["What is the largest ocean on Earth?", "Atlantic", "Indian", "Arctic", "Pacific", 4, "To the left of the US."],
    ["Who wrote 'Hamlet'?", "Charles Dickens", "William Shakespeare", "Leo Tolstoy", "Mark Twain", 2, "Romeo and Juliet."],
    ["What gas do plants breathe in?", "Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen", 2, "CO2."]
]

question = questions.pop(0)

# Drawing function
def draw():
    screen.fill("#34495e")  # Updated to a soothing dark blue-grey
    screen.draw.filled_rect(main_box, "#3498db")  # Lighter, pleasant blue for the main box
    screen.draw.filled_rect(timer_box, "#3498db")  # Same as main box for consistency
    for box in answer_boxes:
        screen.draw.filled_rect(box, "#e74c3c")  # Soft red for the answer boxes
    
    screen.draw.text(str(time_left), center=timer_box.center, color="white")
    screen.draw.text(question[0], center=main_box.center, color="white")
    if hint_shown:
        screen.draw.text(hint_message, bottomleft=(10, HEIGHT - 30), color="#f1c40f")  # Bright yellow for hints
    
    index = 1
    for box in answer_boxes:
        screen.draw.text(question[index], center=box.center, color="white")
        index += 1


# Handle game over
def game_over():
    global question, time_left, hint_shown
    message = "Game over. You got %s questions correct" % str(score)
    question = [message, "-", "-", "-", "-", 5, ""]
    time_left = 0
    hint_shown = False  # Reset hint flag
    print(message)
    pygame.quit()

# Handle correct answer
def correct_answer():
    global question, score, time_left, hint_shown
    score += 1
    hint_shown = False  # Reset hint flag for the next question
    if questions:
        question = questions.pop(0)
        time_left = 10
    else:
        print("End of questions")
        game_over()

# Mouse click handler
def on_mouse_down(pos):
    global hint_shown, hint_message
    index = 1
    for box in answer_boxes:
        if box.collidepoint(pos):
            print(f"Clicked on answer {index}")
            if index == question[5]:
                print("You got it correct!")
                correct_answer()
            else:
                if not hint_shown:
                    hint_shown = True
                    hint_message = question[6]  # Show hint
                    print("Hint: " + hint_message)
                else:
                    game_over()
            break
        index += 1

# Update time left
def update_time_left():
    global time_left
    if time_left > 0:
        time_left -= 1
    else:
        game_over()

clock.schedule_interval(update_time_left, 1.0)

# Start the game
pgzrun.go()
