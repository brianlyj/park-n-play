from flask import Flask, request, jsonify, Response
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
import pygame
import threading
import random
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Load the TensorFlow model
model_path = "ai/keras_model.h5"  # Update to the correct path
model = load_model(model_path)

# Load labels for predictions
label_file_path = "ai/labels.txt"  # Update to the correct path
with open(label_file_path, "r") as f:
    labels = [line.strip() for line in f]

# Preprocess image function for prediction
def preprocess_image(image, target_size=(224, 224)):
    image = load_img(image, target_size=target_size)
    image = img_to_array(image) / 255.0
    return np.expand_dims(image, axis=0)

# Route for image prediction
@app.route('/predict', methods=['POST'])
def predict():
    if not os.path.exists(model_path):
        return jsonify({"error": "Model file not found"}), 500
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Save the file temporarily
        file_path = os.path.join("ai/temp", file.filename)
        file.save(file_path)
        
        # Check if the file was saved successfully
        if not os.path.exists(file_path):
            return jsonify({"error": "Failed to save file"}), 500

        # Preprocess the image
        preprocessed_image = preprocess_image(file_path)
        predictions = model.predict(preprocessed_image)
        predicted_label = labels[np.argmax(predictions)]

        # Clean up
        os.remove(file_path)

        return jsonify({"predicted_label": predicted_label})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# # Function to update pygame window
# pygame.init()

# game1_start = True
# game1_active = False
# transition = False
# game2_start = False
# game2_active = False
# dragging = False
# tilt_button_press = None
# window_width = 390
# window_height = 844
# fps = 10

# window = pygame.display.set_mode((window_width, window_height))

# # game/game-assets
# parked_bic_game1_width, parked_bic_game1_height = 215, 181
# parked_bic_game2_width, parked_bic_game2_height = 390, 845

# bic_sprite_width, bic_sprite_height, bic_sprite_angle = 90, 194, 0

# bic_body_width, bic_body_height = 785, 611

# handlebar_width, handlebar_height = 241, 121

# handlebar_target_width, handlebar_target_height = 262, 180

# cross_button_width, cross_button_height = 326, 706

# border_width, border_height = 440, 295

# instruction_width, instruction_height = 440, 222

# arrow_width, arrow_height = 85, 85

# rotate_button_width, rotate_button_height = 299, 645

# start_text_width, start_text_height = 260, 563

# next_text_width, next_text_height = 260, 563

# upper_y_limit, lower_y_limit = 650, 250

# upper_angle_limit, lower_angle_limit = 50, -50

# transition_text_width, transition_text_height = 633, 320

# npc_width, npc_height = 1398, 689

# tilt_icon_width, tilt_icon_height = 164, 116

# npc_left_x, npc_left_y = 112, 450
# npc_right_x, npc_right_y = 257, 450
# left_forearm_height, right_forearm_height = 72, 72

# handlebar_angle = 0

# time_inside_area = 0
# threshold_time = 0.3
# time_interval = 0.01

# font_path = "roboto"
# font_size = 16
# font = pygame.font.SysFont(font_path, font_size)

# background1 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/background 1.png").convert_alpha(),(window_width, window_height))

# parked_bic1 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/anywheel parked bicycles.png").convert_alpha(),(parked_bic_game1_width, parked_bic_game1_height))
# mask_parked_bic1 = pygame.mask.from_surface(parked_bic1)
# parked_bic1_rect = parked_bic1.get_rect(center=(105, 395))

# parked_bic2 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/anywheel parked bicycles.png").convert_alpha(),(parked_bic_game1_width, parked_bic_game1_height))
# mask_parked_bic2 = pygame.mask.from_surface(parked_bic2)
# parked_bic2_rect = parked_bic2.get_rect(center=(105, 450))

# parked_bic3 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/anywheel parked bicycles.png").convert_alpha(),(parked_bic_game1_width, parked_bic_game1_height))
# mask_parked_bic3 = pygame.mask.from_surface(parked_bic3)
# parked_bic3_rect = parked_bic3.get_rect(center=(105, 505))

# parked_bic4 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/anywheel parked bicycles.png").convert_alpha(),(parked_bic_game1_width, parked_bic_game1_height))
# mask_parked_bic4 = pygame.mask.from_surface(parked_bic4)
# parked_bic4_rect = parked_bic4.get_rect(center=(105, 560))

# bic_sprite = pygame.transform.smoothscale(pygame.image.load("game/game-assets/anywheel sprite.png").convert_alpha(),(bic_sprite_width, bic_sprite_height))
# rotated_bic_sprite = pygame.transform.rotate(bic_sprite, bic_sprite_angle)
# mask_rotated_bic_sprite = pygame.mask.from_surface(rotated_bic_sprite)
# rotated_bic_sprite_rect = rotated_bic_sprite.get_rect(center=(263, 620))

# cross_button = pygame.transform.smoothscale(pygame.image.load("game/game-assets/cross button.png").convert_alpha(),(cross_button_width, cross_button_height))
# cross_button_rect = cross_button.get_rect(center = (330, 60))
# cross_button_area = pygame.Rect(306, 20, 66, 63)

# border = pygame.transform.smoothscale(pygame.image.load("game/game-assets/blue border.png").convert_alpha(),(border_width, border_height))
# border_rect = border.get_rect()
# border_rect.center = (105,330)

# cw_rotate_button = pygame.transform.smoothscale(pygame.image.load("game/game-assets/white rotate button.png").convert_alpha(),(rotate_button_width, rotate_button_height))
# cw_rotate_button_rect = cw_rotate_button.get_rect(center = (308,767))
# cw_rotate_button_area = pygame.Rect(268, 690, 100, 100)

# acw_rotate_button = pygame.transform.smoothscale(pygame.image.load("game/game-assets/white rotate button.png").convert_alpha(),(rotate_button_width, rotate_button_height))
# acw_rotate_button_rect = acw_rotate_button.get_rect(center = (59,767))
# acw_rotate_button_area = pygame.Rect(22, 690, 100, 100)

# acw = pygame.transform.smoothscale(pygame.image.load("game/game-assets/acw.png").convert_alpha(), (arrow_width, arrow_height))
# acw_rect = acw.get_rect(center=(70, 740))

# cw = pygame.transform.smoothscale(pygame.image.load("game/game-assets/cw.png").convert_alpha(), (arrow_width, arrow_height))
# cw_rect = cw.get_rect(center=(320, 740))

# destination_text = font.render("DESTINATION", 1, "#2bceff")

# instructions1 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/instructions1.png").convert_alpha(),(instruction_width, instruction_height))
# instructions1_rect = instructions1.get_rect(center = (195, 160))

# transition_text = pygame.transform.smoothscale(pygame.image.load("game/game-assets/transition text.png").convert_alpha(),(transition_text_width, transition_text_height))
# transition_text_rect = transition_text.get_rect(center = (182, 500))

# winning_area = pygame.Rect(97, 275, 25, 75)

# start_text = pygame.transform.smoothscale(pygame.image.load("game/game-assets/start.png").convert_alpha(),(start_text_width, start_text_height))
# start_text_rect = start_text.get_rect(center = (185, 700))
# start_text_area = pygame.Rect(80, 560, 224, 150)

# next_text = pygame.transform.smoothscale(pygame.image.load("game/game-assets/next.png").convert_alpha(),(next_text_width, next_text_height))
# next_text_rect = next_text.get_rect(center = (195, 700))
# next_text_area = pygame.Rect(90, 560, 224, 150)

# background2 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/game 2 background.png").convert_alpha(),(window_width, window_height))

# parked_bic5 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/parked bic game 2.png").convert_alpha(),(parked_bic_game2_width, parked_bic_game2_height))
# parked_bic5_rect = parked_bic5.get_rect(center = (0, 505))

# parked_bic6 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/parked bic game 2.png").convert_alpha(),(parked_bic_game2_width, parked_bic_game2_height))
# parked_bic6_rect = parked_bic6.get_rect(center = (390, 505))

# bic_body = pygame.transform.smoothscale(pygame.image.load("game/game-assets/bic body game 2.png").convert_alpha(),(bic_body_width, bic_body_height))
# bic_body_rect = bic_body.get_rect(center = (160, 497))

# original_handlebar = pygame.transform.smoothscale(pygame.image.load("game/game-assets/handlebar.png").convert_alpha(),(handlebar_width, handlebar_height))
# handlebar = pygame.transform.rotate(original_handlebar, handlebar_angle)
# handlebar_rect = handlebar.get_rect(center = (195, 385))

# npc_left_forearm = pygame.Rect(npc_left_x , (470 - left_forearm_height), 24, left_forearm_height)
# npc_right_forearm = pygame.Rect(npc_right_x, (470 - right_forearm_height), 24, right_forearm_height)

# handlebar_target_position = pygame.transform.smoothscale(pygame.image.load("game/game-assets/target position.png").convert_alpha(),(handlebar_target_width, handlebar_target_height))
# handlebar_target_position = pygame.transform.rotate(handlebar_target_position, 30)
# handlebar_target_position_rect = handlebar_target_position.get_rect(center = (195, 385))

# cw_tilt_icon = pygame.transform.smoothscale(pygame.image.load("game/game-assets/cw tilt icon.png").convert_alpha(),(tilt_icon_width, tilt_icon_height))
# cw_tilt_icon_rect = cw_tilt_icon.get_rect(center = (321,741))
# cw_tilt_icon_area = pygame.Rect(270, 688, 100, 100)

# acw_tilt_icon = pygame.transform.smoothscale(pygame.image.load("game/game-assets/acw tilt icon.png").convert_alpha(),(tilt_icon_width, tilt_icon_height))
# acw_tilt_icon_rect = acw_tilt_icon.get_rect(center = (70,741))
# acw_tilt_icon_area = pygame.Rect(20, 688, 100, 100)

# instructions2 = pygame.transform.smoothscale(pygame.image.load("game/game-assets/instructions2.png").convert_alpha(),(495, 270))
# instructions2_rect = instructions2.get_rect(center = (217, 180))

# npc = pygame.transform.smoothscale(pygame.image.load("game/game-assets/npc.png").convert_alpha(),(npc_width, npc_height))
# npc_rect = npc.get_rect(center = (510, 490))

# accuracy_text = pygame.transform.smoothscale(pygame.image.load("game/game-assets/accuracy text.png").convert_alpha(),(325, 703))
# accuracy_text_rect = accuracy_text.get_rect(center = (195, 620))

# parking_symbol = pygame.transform.smoothscale(pygame.image.load("game/game-assets/parking symbol.png").convert_alpha(),(170, 170))
# parking_symbol_rect = parking_symbol.get_rect(center = (195, 580))
# parking_symbol_area = pygame.Rect(110, 500, 170, 170)

# well_done_text = pygame.transform.smoothscale(pygame.image.load("game/game-assets/well done.png").convert_alpha(),(550, 248))
# well_done_rect = well_done_text.get_rect(center = (195, 200))

# hmm_text = pygame.transform.smoothscale(pygame.image.load("game/game-assets/hmmm text.png").convert_alpha(),(715, 323))
# hmm_text_rect = hmm_text.get_rect(center = (205, 200))

# retry = pygame.transform.smoothscale(pygame.image.load("game/game-assets/retry.png").convert_alpha(),(200,433))
# retry_rect = retry.get_rect(center = (187, 780))
# retry_area = pygame.Rect(110, 675, 170, 115)

# exit_text = pygame.transform.smoothscale(pygame.image.load("game/game-assets/exit.png").convert_alpha(),(200,433))
# exit_text_rect = exit_text.get_rect(center = (187, 780))
# exit_area = pygame.Rect(110, 675, 170, 115)

# clock = pygame.time.Clock()

# def load_start_screen_for_game1():
#     window.blit(background1, (0, 0))
#     window.blit(parked_bic1, parked_bic1_rect)
#     window.blit(parked_bic2, parked_bic2_rect)
#     window.blit(parked_bic3, parked_bic3_rect)
#     window.blit(parked_bic4, parked_bic4_rect)
#     window.blit(start_text, start_text_rect)
#     window.blit(cross_button, cross_button_rect)
    


# def load_game1_assets():
#     global winning_area
#     window.blit(background1, (0, 0))
#     window.blit(parked_bic1, parked_bic1_rect)
#     window.blit(parked_bic2, parked_bic2_rect)
#     window.blit(parked_bic3, parked_bic3_rect)
#     window.blit(parked_bic4, parked_bic4_rect)
#     window.blit(cross_button, cross_button_rect)
#     window.blit(border, border_rect)
#     window.blit(destination_text, (58, 310))
#     window.blit(instructions1, instructions1_rect)
#     window.blit(cw_rotate_button, cw_rotate_button_rect)
#     window.blit(acw_rotate_button, acw_rotate_button_rect)
#     window.blit(acw, acw_rect)
#     window.blit(cw, cw_rect)
#     window.blit(rotated_bic_sprite, rotated_bic_sprite_rect)

# def update_pos(mouse_pos):
#     global rotated_bic_sprite_rect
#     rotated_bic_sprite_rect.center = mouse_pos

# def check_colour_collision(mask_rotated_bic_sprite, rotated_bic_sprite_rect, background1, target_colour):
#     overlap_rect = rotated_bic_sprite_rect.clip(background1.get_rect())
#     for x in range(overlap_rect.left, overlap_rect.right):
#         for y in range(overlap_rect.top, overlap_rect.bottom):
#             rel_x = x - rotated_bic_sprite_rect.left
#             rel_y = y - rotated_bic_sprite_rect.top
#             bg_x = x
#             bg_y = y
#             if mask_rotated_bic_sprite.get_at((rel_x, rel_y)) > 0:
#                 if background1.get_at((bg_x, bg_y))[:3] == target_colour[:3]:
#                     return True
#     return False

# def draw_outline(thingy):
#     pygame.draw.rect(window, "red", thingy, 2)
#     pygame.display.flip()

# def draw_mask_outline(thingy, thingy_rect):
#     border_points = thingy.outline()
#     border_points = [(x + thingy_rect.x, y + thingy_rect.y) for x, y in border_points]
#     pygame.draw.lines(window, "red", True, border_points, 2)

# def draw_point(place):
#     pygame.draw.circle(window, "orange", place, 5)

# def get_touch_pos(event):
#     x, y = event.pos
#     return x, y

# def turn_cw():
#     global bic_sprite_angle, rotated_bic_sprite_rect, rotated_bic_sprite, mask_rotated_bic_sprite
#     bic_sprite_angle -= 90
#     rotated_bic_sprite = pygame.transform.rotate(bic_sprite, bic_sprite_angle)
#     rotated_bic_sprite_rect = rotated_bic_sprite.get_rect(center=rotated_bic_sprite_rect.center)
#     mask_rotated_bic_sprite = pygame.mask.from_surface(rotated_bic_sprite)

# def turn_acw():
#     global bic_sprite_angle, rotated_bic_sprite_rect, rotated_bic_sprite, mask_rotated_bic_sprite
#     bic_sprite_angle += 90
#     rotated_bic_sprite = pygame.transform.rotate(bic_sprite, bic_sprite_angle)
#     rotated_bic_sprite_rect = rotated_bic_sprite.get_rect(center=rotated_bic_sprite_rect.center)
#     mask_rotated_bic_sprite = pygame.mask.from_surface(rotated_bic_sprite)

# def game1():
#     global game1_active, transition, time_inside_area, bic_sprite_angle, rotated_bic_sprite_rect, mask_rotated_bic_sprite, rotated_bic_sprite, dragging
#     previous_pos = rotated_bic_sprite_rect.center  # Initialize previous position

#     while game1_active:
#         for event in pygame.event.get():
#             # Check winning condition
#             if winning_area.collidepoint(rotated_bic_sprite_rect.center) and (bic_sprite_angle == 90 or (bic_sprite_angle - 90) % 360 == 0):
#                 time_inside_area += 1 / fps
#                 if time_inside_area >= threshold_time:
#                     final_x, final_y = rotated_bic_sprite_rect.centerx, rotated_bic_sprite_rect.centery
#                     game1_active = False
#                     transition = True
#                     return final_x, final_y

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 touch_pos = get_touch_pos(event)
#                 if cross_button_area.collidepoint(touch_pos):
#                     pygame.quit()
#                     sys.exit()
#                 elif cw_rect.collidepoint(touch_pos):
#                     turn_cw()
#                 elif acw_rect.collidepoint(touch_pos):
#                     turn_acw()
#                 elif rotated_bic_sprite_rect.collidepoint(touch_pos):
#                     dragging = True
#                     previous_pos = rotated_bic_sprite_rect.center  # Save initial position for dragging

#             if event.type == pygame.MOUSEBUTTONUP:
#                 dragging = False

#             if event.type == pygame.MOUSEMOTION and dragging:
#                 # Save current position
#                 x, y = get_touch_pos(event)

#                 if lower_y_limit < y < upper_y_limit:
#                     # Tentatively update position for collision check
#                     rotated_bic_sprite_rect.center = (x, y)

#                     # Calculate offsets for masks
#                     offset1 = (rotated_bic_sprite_rect.x - parked_bic1_rect.x, rotated_bic_sprite_rect.y - parked_bic1_rect.y)
#                     offset2 = (rotated_bic_sprite_rect.x - parked_bic2_rect.x, rotated_bic_sprite_rect.y - parked_bic2_rect.y)
#                     offset3 = (rotated_bic_sprite_rect.x - parked_bic3_rect.x, rotated_bic_sprite_rect.y - parked_bic3_rect.y)
#                     offset4 = (rotated_bic_sprite_rect.x - parked_bic4_rect.x, rotated_bic_sprite_rect.y - parked_bic4_rect.y)

#                     # Check for collisions
#                     if (
#                         mask_parked_bic1.overlap(mask_rotated_bic_sprite, offset1) or
#                         mask_parked_bic2.overlap(mask_rotated_bic_sprite, offset2) or
#                         mask_parked_bic3.overlap(mask_rotated_bic_sprite, offset3) or
#                         mask_parked_bic4.overlap(mask_rotated_bic_sprite, offset4) or
#                         check_colour_collision(mask_rotated_bic_sprite, rotated_bic_sprite_rect, background1, (87, 135, 2))
#                     ):
#                         # Collision detected, revert to previous valid position
#                         rotated_bic_sprite_rect.center = previous_pos
#                     else:
#                         # No collision, update previous position
#                         previous_pos = rotated_bic_sprite_rect.center

#         load_game1_assets()

#         pygame.display.flip()
#         clock.tick(fps)

# def check_for_start_game1():
#     global game1_start, game1_active
#     load_start_screen_for_game1()
#     for event in pygame.event.get():
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             touch_pos = get_touch_pos(event)
#             if cross_button_area.collidepoint(touch_pos):
#                 pygame.quit()
#                 sys.exit()
#             elif start_text_area.collidepoint(touch_pos):
#                 game1_start = False
#                 game1_active = True

#     pygame.display.flip()
#     clock.tick(fps)

# def load_transition_screen():
#     window.blit(background1, (0, 0))
#     window.blit(parked_bic1, parked_bic1_rect)
#     window.blit(parked_bic2, parked_bic2_rect)
#     window.blit(parked_bic3, parked_bic3_rect)
#     window.blit(parked_bic4, parked_bic4_rect)
#     window.blit(cross_button, cross_button_rect)
#     window.blit(border, border_rect)
#     window.blit(destination_text, (58, 310))
#     window.blit(next_text, next_text_rect)
#     window.blit(transition_text, transition_text_rect)

# def transition_phase(coord_of_sprite):
#     global transition, game2_start
#     load_transition_screen()
#     rotated_bic_sprite_rect.center = coord_of_sprite
#     window.blit(rotated_bic_sprite, rotated_bic_sprite_rect)
#     for event in pygame.event.get():
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             touch_pos = get_touch_pos(event)
#             if cross_button_area.collidepoint(touch_pos):
#                 pygame.quit()
#                 sys.exit()
#             elif next_text_area.collidepoint(touch_pos):
#                 transition = False
#                 game2_start = True


#         pygame.display.flip()
#         clock.tick(fps)

# def load_start_screen_for_game2():
#     window.blit(background2, (0,0))
#     window.blit(parked_bic5, parked_bic5_rect)
#     window.blit(parked_bic6, parked_bic6_rect)
#     window.blit(bic_body, bic_body_rect)
#     window.blit(cross_button, cross_button_rect)
#     window.blit(start_text, start_text_rect)
#     pygame.draw.rect(window, "#f9df8b", npc_left_forearm, 0)
#     pygame.draw.rect(window, "#f9df8b", npc_right_forearm, 0)
#     pygame.draw.rect(window, "black", npc_left_forearm, 1)
#     pygame.draw.rect(window, "black", npc_right_forearm, 1)
#     window.blit(npc, npc_rect)
#     window.blit(handlebar, handlebar_rect)

# def check_for_start_game2():
#     global game2_start, game2_active
#     load_start_screen_for_game2()
#     for event in pygame.event.get():
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             touch_pos = get_touch_pos(event)
#             if cross_button_area.collidepoint(touch_pos):
#                 pygame.quit()
#                 sys.exit()
#             elif start_text_area.collidepoint(touch_pos):
#                 game2_start = False
#                 game2_active = True

#     pygame.display.flip()
#     clock.tick(fps)

# def load_game2_assets():
#     window.blit(background2, (0, 0))
#     window.blit(parked_bic5, parked_bic5_rect)
#     window.blit(parked_bic6, parked_bic6_rect)
#     window.blit(bic_body, bic_body_rect)
#     window.blit(handlebar_target_position, handlebar_target_position_rect)
#     window.blit(cross_button, cross_button_rect)
#     pygame.draw.rect(window, "#f9df8b", npc_left_forearm, 0)
#     pygame.draw.rect(window, "#f9df8b", npc_right_forearm, 0)
#     pygame.draw.rect(window, "black", npc_left_forearm, 1)
#     pygame.draw.rect(window, "black", npc_right_forearm, 1)
#     pygame.draw.rect(window, "#004D40", (-5, 470, 400, 390), 0, 20)
#     window.blit(instructions2, instructions2_rect)
#     window.blit(cw_rotate_button, cw_rotate_button_rect)
#     window.blit(acw_rotate_button, acw_rotate_button_rect)
#     window.blit(cw_tilt_icon, cw_tilt_icon_rect)
#     window.blit(acw_tilt_icon, acw_tilt_icon_rect)
#     window.blit(handlebar, handlebar_rect)
#     pygame.draw.rect(window, "white", (107, 493, 175, 175), 0, 20)
#     window.blit(parking_symbol, parking_symbol_rect)

# def handlebar_rotate_acw():
#     global handlebar_angle, handlebar, handlebar_rect, left_forearm_height, right_forearm_height, npc_left_x, npc_right_x
#     handlebar_angle += 0.5
#     if handlebar_angle > 0:
#         npc_left_x += 0.33
#         left_forearm_height -= 0.42
#         npc_right_x -= 0.15
#         right_forearm_height += 0.70
#     elif handlebar_angle < 0:
#         npc_left_x -= 0.16
#         left_forearm_height -= 0.70
#         npc_right_x += 0.37
#         right_forearm_height += 0.42

#     npc_left_forearm.x = npc_left_x
#     npc_right_forearm.x = npc_right_x
#     npc_left_forearm.height = left_forearm_height
#     npc_right_forearm.height = right_forearm_height
#     npc_left_forearm.y = 470 - left_forearm_height
#     npc_right_forearm.y = 470 - right_forearm_height

#     handlebar = pygame.transform.rotate(original_handlebar, handlebar_angle)
#     handlebar_rect = handlebar.get_rect(center=(195, 385))


# def handlebar_rotate_cw():
#     global handlebar_angle, handlebar, handlebar_rect, npc_left_x, left_forearm_height, npc_right_x, right_forearm_height
#     handlebar_angle -= 0.5
#     if 0 < handlebar_angle:
#         npc_left_x -= 0.33
#         left_forearm_height += 0.42
#         npc_right_x += 0.15
#         right_forearm_height -= 0.70
#     elif handlebar_angle < 0:
#         npc_left_x += 0.16
#         left_forearm_height += 0.70
#         npc_right_x -= 0.37
#         right_forearm_height -= 0.42

#     npc_left_forearm.x = npc_left_x
#     npc_right_forearm.x = npc_right_x
#     npc_left_forearm.height = left_forearm_height
#     npc_right_forearm.height = right_forearm_height
#     npc_left_forearm.y = 470 - left_forearm_height
#     npc_right_forearm.y = 470 - right_forearm_height

#     handlebar = pygame.transform.rotate(original_handlebar, handlebar_angle)
#     handlebar_rect = handlebar.get_rect(center=(195, 385))

# def calculate_accuracy():
#     global handlebar_angle

#     font = pygame.font.SysFont("Roboto", 75, True)
#     if handlebar_angle < 30:
#         accuracy = round((handlebar_angle + 30) / 60 * 100)
#     elif handlebar_angle > 30:
#         accuracy = 100 - round((handlebar_angle - 30) / 60 * 100)
#     else:
#         accuracy = 100

#     if 0 <= accuracy < 50:
#         colour = "red"
#     elif 50 <= accuracy < 75:
#         colour = "orange"
#     elif 75 <= accuracy < 90:
#         colour = "yellow"
#     elif 90 <= accuracy < 99:
#         colour = "#D0FE1D"
#     else:
#         colour = "green"

#     accuracy_percentage = font.render("{}%".format(accuracy), True, colour)
#     accuracy_percentage_rect = accuracy_percentage.get_rect(center = (200, 630))
#     return accuracy_percentage, accuracy_percentage_rect, accuracy

# def load_game2_end(accuracy_percentage, accuracy_percentage_rect):
#     global font
#     window.blit(background2, (0, 0))
#     window.blit(parked_bic5, parked_bic5_rect)
#     window.blit(parked_bic6, parked_bic6_rect)
#     window.blit(bic_body, bic_body_rect)
#     window.blit(handlebar_target_position, handlebar_target_position_rect)
#     window.blit(cross_button, cross_button_rect)
#     pygame.draw.rect(window, "#f9df8b", npc_left_forearm, 0)
#     pygame.draw.rect(window, "#f9df8b", npc_right_forearm, 0)
#     pygame.draw.rect(window, "black", npc_left_forearm, 1)
#     pygame.draw.rect(window, "black", npc_right_forearm, 1)
#     pygame.draw.rect(window, "#004D40", (-5, 470, 400, 390), 0, 20)
#     window.blit(accuracy_text, accuracy_text_rect)
#     window.blit(accuracy_percentage, accuracy_percentage_rect)
#     window.blit(well_done_text, well_done_rect)
#     window.blit(exit_text, exit_text_rect)
#     window.blit(handlebar, handlebar_rect)
#     draw_outline(exit_area)


# def load_game2_retry(accuracy_percentage, accuracy_percentage_rect):
#     global font
#     window.blit(background2, (0, 0))
#     window.blit(parked_bic5, parked_bic5_rect)
#     window.blit(parked_bic6, parked_bic6_rect)
#     window.blit(bic_body, bic_body_rect)
#     window.blit(handlebar_target_position, handlebar_target_position_rect)
#     window.blit(cross_button, cross_button_rect)
#     pygame.draw.rect(window, "#f9df8b", npc_left_forearm, 0)
#     pygame.draw.rect(window, "#f9df8b", npc_right_forearm, 0)
#     pygame.draw.rect(window, "black", npc_left_forearm, 1)
#     pygame.draw.rect(window, "black", npc_right_forearm, 1)
#     pygame.draw.rect(window, "#004D40", (-5, 470, 400, 390), 0, 20)
#     window.blit(accuracy_text, accuracy_text_rect)
#     window.blit(accuracy_percentage, accuracy_percentage_rect)
#     window.blit(hmm_text, hmm_text_rect)
#     window.blit(retry, retry_rect)
#     window.blit(handlebar, handlebar_rect)
#     draw_outline(retry_area)


# def game2():
#     global tilt_button_press, handlebar_angle, time_inside_area, game2_active
#     while game2_active:
#         load_game2_assets()
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 touch_pos = get_touch_pos(event)
#                 if cross_button_area.collidepoint(touch_pos):
#                     pygame.quit()
#                     sys.exit()
#                 if parking_symbol_area.collidepoint(touch_pos) and handlebar_angle > -30:
#                     game2_active = False
#                     print("gay")
#                 elif acw_tilt_icon_area.collidepoint(touch_pos):
#                     tilt_button_press = "ACW"
#                 elif cw_tilt_icon_area.collidepoint(touch_pos):
#                     tilt_button_press = "CW"
#             elif event.type == pygame.MOUSEBUTTONUP:
#                 tilt_button_press = None

#         if tilt_button_press == "ACW" and handlebar_angle < upper_angle_limit:
#             handlebar_rotate_acw()
#         elif tilt_button_press == "CW" and lower_angle_limit < handlebar_angle:
#             handlebar_rotate_cw()

#         pygame.display.flip()
#         clock.tick(fps)

#     else:
#         while not game2_active:
#             accuracy_percentage, accuracy_percentage_rect, accuracy = calculate_accuracy()
#             if accuracy >= 90:
#                 load_game2_end(accuracy_percentage, accuracy_percentage_rect)
#                 for event in pygame.event.get():
#                     if event.type == pygame.MOUSEBUTTONDOWN:
#                         touch_pos = get_touch_pos(event)
#                         if cross_button_area.collidepoint(touch_pos):
#                             pygame.quit()
#                             sys.exit()
#                         elif exit_area.collidepoint(touch_pos):
#                             pygame.quit()
#                             sys.exit()
#             else:
#                 load_game2_retry(accuracy_percentage, accuracy_percentage_rect)
#                 for event in pygame.event.get():
#                     if event.type == pygame.MOUSEBUTTONDOWN:
#                         touch_pos = get_touch_pos(event)
#                         if cross_button_area.collidepoint(touch_pos):
#                             pygame.quit()
#                             sys.exit()
#                         elif retry_area.collidepoint(touch_pos):
#                             game2_active = True


#         pygame.display.flip()
#         clock.tick(fps)


# def main():
#     while True:
#         if game1_start and not game1_active:
#             check_for_start_game1()
#         elif not game1_start and game1_active:
#             coord_of_sprite = game1()
#         elif not game1_active and transition:
#             transition_phase(coord_of_sprite)
#         elif not transition and game2_start:
#             check_for_start_game2()
#         elif not game2_start and game2_active:
#             game2()

# main()

# # Function to capture pygame screen and stream as MJPEG
# def generate_frames():
#     while True:
#         # Capture pygame screen
#         pygame_surface = pygame.surfarray.array3d(pygame.display.get_surface())
#         pygame_surface = pygame_surface.swapaxes(0, 1)  # Correct axis for OpenCV

#         # Convert to OpenCV image
#         frame = cv2.cvtColor(pygame_surface, cv2.COLOR_RGB2BGR)

#         # Encode as JPEG
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         # Yield frame
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# # Route to stream the pygame output
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # Start the Flask app with threading for Pygame
# if __name__ == '__main__':
#     # Run pygame in a separate thread
#     threading.Thread(target=main(), daemon=True).start()

#     # Start Flask server
#     app.run(debug=True, host='0.0.0.0')

# Initialize Pygame
pygame.init()
width, height = 390, 844
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Stream Example")

# Function to update pygame window
def pygame_game():
    clock = pygame.time.Clock()
    running = True
    x, y = 50, 50  # Initial position of the red square
    speed = 15  # Movement speed

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Randomly update the position of the red square
        x += random.randint(-speed, speed)
        y += random.randint(-speed, speed)

        # Keep the square within bounds of the screen
        x = max(0, min(width - 100, x))
        y = max(0, min(height - 100, y))

        screen.fill((0, 0, 255))  # Blue background
        pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 100))  # Red square
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Function to capture pygame screen and stream as MJPEG
def generate_frames():
    while True:
        # Capture pygame screen
        pygame_surface = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame_surface = pygame_surface.swapaxes(0, 1)  # Correct axis for OpenCV

        # Convert to OpenCV image
        frame = cv2.cvtColor(pygame_surface, cv2.COLOR_RGB2BGR)

        # Encode as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to stream the pygame output
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Start the Flask app with threading for Pygame
if __name__ == '__main__':
    # Run pygame in a separate thread
    threading.Thread(target=pygame_game, daemon=True).start()

    # Start Flask server
    app.run(debug=True, host='0.0.0.0')