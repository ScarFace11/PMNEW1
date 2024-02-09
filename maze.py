import pygame
from random import randint
from maze_settings import *
from player import Player
from Tile import Tile
#from way import Way
from trap import Trap
from goal import Goal
from score import Score
from game import Game
from Music import *

from pygame.sprite import spritecollideany
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
class world:
        def __init__(self,world_data,screen):              
                self.screen = screen
                self.world_data = world_data
                self._setup_world(world_data)
                self.game = Game(self.screen)
                self.world_shift = 0
                self.world_shift_y = 0

                self.way_x = Width // 2 - len(self.world_data[0]) / 2 * Tile_size
                self.way_y = Height // 2 - len(self.world_data[0]) / 2 * Tile_size            

                self.trap_visible = True
                self.last_sprite_change_time = pygame.time.get_ticks()

                self.scoreall = False
                self.player_face = 'right'

                self.pause_flag = False
                #Background()
                #pygame.mouse.set_visible(False)
        
        def findplayercoord(self):
                for i in range(len(self.world_data)):
                        for j in range(len(self.world_data[i])):  
                                if (self.world_data[i][j] == 2):
                                        player_x = i * Tile_size
                                        player_y = j * Tile_size
                                        #print(f"x = {player_x} y = {player_y}")
                return player_x, player_y
        
        def _setup_world(self,layout):
                player_x,player_y = self.findplayercoord()
                self.tiles = pygame.sprite.Group()
                self.player = pygame.sprite.GroupSingle()
                self.way = pygame.sprite.Group()
                self.traps = pygame.sprite.Group()
                self.goal = pygame.sprite.Group()
                self.score = pygame.sprite.Group()
                
                center_x = Width // 2 - len(self.world_data[0]) / 2 * Tile_size 
                #center_x = Width // 2 - player_x
                center_y = Height // 2 - len(self.world_data) / 2 * Tile_size
                #center_y = Height // 2 - player_y
                
                #print(f"x = {center_x} y = {center_y}")
                
                #               РАЗОБРАТЬСЯ

                
                # Генерация монеток
                moneyflag = True
                totalmoney = 5
                if totalmoney != 0 and moneyflag:
                        
                        coins = [(randint(1, len(self.world_data[0])-1), randint(1, len(self.world_data)-1))
                                for _ in range(totalmoney)]
                        
                        for coin in coins:
                                
                                random_x, random_y = coin
                                while self.world_data[random_y][random_x] != 0:
                                        random_x, random_y = (randint(1, len(self.world_data[0])-1),
                                                        randint(1, len(self.world_data)-1))
                                self.world_data[random_y][random_x] = 5
                        moneyflag = False
                # Распределение очков
                scoreflag = True
                if scoreflag:
                        score_positions = [(i, j) for i in range(len(self.world_data)-1)
                                for j in range(len(self.world_data[i])-1)
                                if self.world_data[i][j] == 0]
                        
                for pos in score_positions:
                        self.world_data[pos[0]][pos[1]] = 6
                self.Scorespawn = len(score_positions)
                scoreflag = False
                
                for i in range(len(self.world_data)):
                        for j in range(len(self.world_data[i])):                             
                                x,y = j *Tile_size + center_x, i * Tile_size + center_y
                                if self.world_data[i][j] == 2:                                        
                                        player_sprite = Player((x, y))
                                        self.player.add(player_sprite)
                                        self.player_start_cord_x,  self.player_start_cord_y = x, y                                        
                                elif self.world_data[i][j] == 1:                                      
                                        tile = Tile((x, y), Tile_size)
                                        self.tiles.add(tile)
                                elif self.world_data[i][j] == 4:
                                        tile = Trap((x, y-5), Tile_size)
                                        self.traps.add(tile)
                                elif self.world_data[i][j] == 5:
                                        goal = Goal((x, y), Tile_size)
                                        self.goal.add(goal) 
                                if self.world_data[i][j] == 6:
                                        score_sprite = Score((x, y), Tile_size)
                                        self.score.add(score_sprite)       
                                        
                                #if self.world_data[i][j] == 0 or self.world_data[i][j] == 2:
                                        #pygame.draw.rect(self.screen, color_way,(j * Tile_size, i * Tile_size, Tile_size, Tile_size))
                                        #way_sprite = Way((x, y), Tile_size)
                                        #self.way.add(way_sprite)


        def draw_tile(self, x_shift, y_shift):
                
                center_y = Height // 2 - len(self.world_data) / 2 * Tile_size
                y = center_y
                self.way_x += x_shift
                self.way_y += y_shift
                for i in range(len(self.world_data)):
                        for j in range(len(self.world_data[i])):
                                #if self.world_data[i][j] == 0 or self.world_data[i][j] == 2 or self.world_data[i][j] == 5 or self.world_data[i][j] == 6:
                                        #pygame.draw.rect(self.screen, color_way,(j * Tile_size + self.way_x, i * Tile_size +y, Tile_size, Tile_size))
                                #elif self.world_data[i][j] == 3:
                                        #pygame.draw.rect(self.screen, color_bonus, (j * Tile_size + self.way_x, i * Tile_size + y, Tile_size, Tile_size))
                                #if self.world_data[i][j] == 3:
                                        #pygame.draw.rect(self.screen, color_bonus, (j * Tile_size + self.way_x, i * Tile_size + y, Tile_size, Tile_size))
                                if self.world_data[i][j] != 1 and self.world_data[i][j] != 9: # !=1
                                        pygame.draw.rect(self.screen, color_way,(j * Tile_size + self.way_x, i * Tile_size +y, Tile_size, Tile_size))
                

        # движение камеры по x
        def _scroll_x(self):

                player = self.player.sprite
                player_x = player.rect.centerx
                direction_x = player.direction.x

                direction_y = player.direction.y
                
                if  player_x < Width // 3 and direction_x < 0:
                        player.speed = 0
                        self.world_shift = Tile_size / 10.0
                elif player_x > Width - (Width // 3) and direction_x > 0:
                        player.speed = 0
                        self.world_shift = -(Tile_size / 10.0)                    
                else:
                        self.world_shift = 0
                        player.speed = Tile_size / 10.0

                if self.player_face == "up" or self.player_face == "down":#if direction_y != 0:
                        self.world_shift = 0
                        player.speed = Tile_size / 10.0
                        
                
                """
                elif player_y < Height // 3 - 50 and direction_y < 0 and direction_x == 0:
                        self.world_shift_y = 5
                        player.speed = 0
                elif player_y > Height - (Height // 3)+50 and direction_y > 0 and direction_x == 0:
                        self.world_shift_y = -5
                        player.speed = 0
                        """
                

                #Слежка за игроком
                """
                if player_x < Width - (Width // 2) and direction_x < 0 and direction_y == 0:
                        self.world_shift = 5
                        player.speed = 0
                elif player_x > Width - (Width // 2) and direction_x > 0 and direction_y == 0:
                        self.world_shift = -5
                        player.speed = 0
                """
        
        # движение камеы по y
        def _scroll_y(self):

                player = self.player.sprite
                #player_y = player.rect.centery-5
                player_y = player.rect.centery
                direction_y = player.direction.y
                # Если выше положенного
                if player_y < Height // 3 and direction_y < 0: 
                        self.world_shift_y = 5
                        player.speed = 0
                # Если ниже положенного
                
                elif player_y > Height - (Height // 3) and direction_y > 0:
                        self.world_shift_y = -5
                        player.speed = 0
                #elif player_y >= Height // 2+100 and direction_y < 0:
                        #self.world_shift_y = 5
                        #player.speed = 0
                
                #elif player_y <= Height - (Height // 2)-100 and direction_y > 0:
                        #self.world_shift_y = -5
                        #player.speed = 0
                else:
                        self.world_shift_y = 0
                        player.speed = Tile_size / 10.0
        # take goal
        def _handle_collision(self):
                player = self.player.sprite

                collided_goal = spritecollideany(player, self.goal)
                if collided_goal is not None:
                        collided_goal.kill()
                #pygame.sprite.spritecollide(player, self.goal, True)
                
                #if pygame.sprite.spritecollide(player, self.score, True):
                collided_score = spritecollideany(player, self.score)
                if collided_score is not None:
                        collided_score.kill()
                #if spritecollideany(player, self.score):
                        
                        self.Scorespawn-=1
                        if (self.Scorespawn == 0):
                                self.scoreall = True
                #if pygame.sprite.spritecollide(player, self.traps, False) and self.trap_visible == True:
                if spritecollideany(player, self.traps) and self.trap_visible == True:
                        player.rect.x = self.player_start_cord_x
                        player.rect.y = self.player_start_cord_y
                        player.life -= 1

        def traptime(self):
                current_time = pygame.time.get_ticks()   
                if current_time - self.last_sprite_change_time >= 5000:
                        # Если прошло 5 секунд, меняем видимость спрайта
                        self.last_sprite_change_time = current_time
                        self.trap_visible = not self.trap_visible
        
        # prevents player to pass through objects horizontall
        def _horizontal_movement_collision(self):
                player = self.player.sprite
                player.rect.x += player.direction.x * player.speed

                collided = False 

                for sprite in self.tiles.sprites():
                        if sprite.rect.colliderect(player.rect):
                                collided = True 

                                if player.direction.x < 0:  # Движение влево
                                        player.rect.left = sprite.rect.right
                                        player.direction.x = 0
                                        self.world_shift_x = 0
                                        self.world_shift_y = 0
                                        self.current_x = player.rect.left
                                elif player.direction.x > 0:  # Движение вправо
                                        player.rect.right = sprite.rect.left
                                        player.direction.x = 0
                                        self.world_shift_x = 0
                                        self.world_shift_y = 0
                                        self.current_x = player.rect.right

                # Если нет столкновений, определяем направление игрока
                if not collided:
                        for sprite in self.tiles.sprites():
                                if player.rect.left != sprite.rect.right and player.direction.x < 0:
                                        self.player_face = 'left'
                                        break  # Прерываем цикл, если направление найдено
                                elif player.rect.right != sprite.rect.left and player.direction.x > 0:
                                        self.player_face = 'right'
                                        break  # Прерываем цикл, если направление найдено


                
        # prevents player to pass through objects vertically
        def _vertical_movement_collision(self):
                player = self.player.sprite
                player.rect.y += player.direction.y * player.speed

                collided = False 

                for sprite in self.tiles.sprites():
                        if sprite.rect.colliderect(player.rect):
                                collided = True 

                                if player.direction.y > 0:  # Движение вниз
                                        player.rect.bottom = sprite.rect.top
                                        player.direction.y = 0
                                        self.world_shift_x = 0
                                        self.world_shift_y = 0
                                        player.on_ground = True
                                elif player.direction.y < 0:  # Движение вверх
                                        player.rect.top = sprite.rect.bottom
                                        player.direction.y = 0
                                        self.world_shift_x = 0
                                        self.world_shift_y = 0
                                        player.on_ceiling = True

                # Если нет столкновений, определяем направление игрока
                if not collided:
                        for sprite in self.tiles.sprites():
                                if player.rect.bottom <= sprite.rect.top and player.direction.y > 0:
                                        self.player_face = 'down'
                                        break  # Прерываем цикл, если направление найдено
                                elif player.rect.top >= sprite.rect.bottom and player.direction.y < 0:
                                        self.player_face = 'up'
                                        break  # Прерываем цикл, если направление найдено
        """ запомнить
        def _movement_collision(self):
                player = self.player.sprite
                if player.direction.y != 0: is_vertical = True
                else: is_vertical = False
                
                if is_vertical:
                        player.rect.y += player.direction.y * player.speed
                else:
                        player.rect.x += player.direction.x * player.speed

                collided = False  # Флаг для отслеживания столкновений

                for sprite in self.tiles.sprites():
                        if sprite.rect.colliderect(player.rect):
                                collided = True  # Если есть столкновение, устанавливаем флаг в True

                                if is_vertical:  # Проверка столкновений по вертикали
                                        if player.direction.y > 0:  # Движение вниз
                                                player.rect.bottom = sprite.rect.top
                                                player.direction.y = 0
                                        elif player.direction.y < 0:  # Движение вверх
                                                player.rect.top = sprite.rect.bottom
                                                player.direction.y = 0
                                else:  # Проверка столкновений по горизонтали
                                        if player.direction.x < 0:  # Движение влево
                                                player.rect.left = sprite.rect.right
                                                player.direction.x = 0
                                        elif player.direction.x > 0:  # Движение вправо
                                                player.rect.right = sprite.rect.left
                                                player.direction.x = 0
                                                self.world_shift_x = 0
                                                self.world_shift_y = 0

                # Если нет столкновений, определяем направление игрока
                if not collided:
                        for sprite in self.tiles.sprites():
                                if is_vertical:
                                        if player.rect.bottom <= sprite.rect.top and player.direction.y > 0:
                                                self.player_face = 'down'
                                                break
                                        elif player.rect.top > sprite.rect.bottom and player.direction.y < 0:
                                                self.player_face = 'up'
                                                break
                                else:
                                        if player.rect.left != sprite.rect.right and player.direction.x < 0:
                                                self.player_face = 'left'
                                                break
                                        elif player.rect.right != sprite.rect.left and player.direction.x > 0:
                                                self.player_face = 'right'
                                                break
        """        
        def set_Pause_Flag(self, value):
                self.pause_flag = value
                player = self.player.sprite
                
                if value == True:
                        player.speed = 0
                else:
                        player.speed = Tile_size / 10.0
                        print("continue")


        def GamePause(self, screen):
                
                Continue_color = Color_Yellow
                Back_color = Color_Yellow

                s = pygame.Surface((Width // 2 - 140, Height // 2 - 120), pygame.SRCALPHA)
                pygame.draw.rect(s, (128, 128, 128, 128), (0, 0, 300, 200), 0, 34)
                screen.blit(s, (Width // 2 - 140, Height // 2 - 120))

                pygame.draw.rect(screen, (255, 255, 30), (Width // 2 - 140, Height // 2 - 120, 300, 200), 5, 34)

                Continue_text = font.render("Continue", True, Continue_color)
                Continue_rect = Continue_text.get_rect(center=(Width // 2, Height // 2 - 80))
                screen.blit(Continue_text, Continue_rect)

                Back_text = font.render("Exit", True, Back_color)
                Back_rect = Back_text.get_rect(center=(Width // 2, Height // 2))
                screen.blit(Back_text, Back_rect)

                mouse_pos = pygame.mouse.get_pos()

                for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                if Continue_rect.collidepoint(mouse_pos):
                                        self.set_Pause_Flag(False)
                                        #self.pause_flag = False
                                        
                                       

                                elif Back_rect.collidepoint(mouse_pos):
                                        print("exit")
                                        from Levels import show_level_menu
                                        show_level_menu()

                Continue_collide = Continue_rect.collidepoint(mouse_pos)
                Back_collide = Back_rect.collidepoint(mouse_pos)

                Continue_color = Color_Yellow if Continue_collide else Color_Purple
                Back_color = Color_Yellow if Back_collide else Color_Purple

                # Redraw with updated colors
                pygame.draw.rect(screen, (255, 255, 30), (Width // 2 - 140, Height // 2 - 120, 300, 200), 5, 34)

                Continue_text = font.render("Continue", True, Continue_color)
                screen.blit(Continue_text, Continue_rect)

                Back_text = font.render("Exit", True, Back_color)
                screen.blit(Back_text, Back_rect)

        # updating the game world from all changes committed
        def update(self, screen, player_event):
                
                # for tile
                self.tiles.update(self.world_shift,self.world_shift_y)
                self.tiles.draw(screen)
                
                # for way
                self.way.update(self.world_shift, self.world_shift_y)
                self.way.draw(self.screen)

                # for draw tile
                self.draw_tile(self.world_shift, self.world_shift_y)
                # for goal
                self.goal.update(self.world_shift, self.world_shift_y)
                self.goal.draw(screen)
                #for score
                self.score.update(self.world_shift, self.world_shift_y)
                self.score.draw(screen)
                # for trap
                if (self.trap_visible):                        
                        self.traps.draw(screen)
                        
                self.traptime()
                self.traps.update(self.world_shift,self.world_shift_y)
                # for collsion
                self._handle_collision()

                
                
                self.player.update(player_event, self.player_face)
                self.player.draw(screen)

                self._horizontal_movement_collision()
                self._vertical_movement_collision()

                #Альфа версия
                #self._scroll_x()
                #self._scroll_y()

                self.game.show_life(self.player.sprite)
                self.game.game_state(self.player.sprite, self.scoreall)
                if self.pause_flag:
                        self.GamePause(screen)
       
                #clock.tick(fps)
                
                #text_fps = font.render(str(int(clock.get_fps())),1,(255,255,255))
                #screen.blit(text_fps,(10,100))
