import pygame
from random import randint
from maze_settings import *
from player import Player
from Tile import Wall
from way import Way
from trap import Spike,Laser
from goal import Goal
from score import Score
from game import Game
from Music import *
from Icons import Icons
from pygame.sprite import spritecollideany
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

class world:
        def __init__(self,world_data,screen):              
                self.screen = screen
                self.world_data = world_data
                self._setup_world(world_data)
                self.game = Game(self.screen)

                

                self.scoreall = False
                self.finished = False
                self.player_face = 'right'

                self.pause_flag = False
                GameMusic.Background()
                #pygame.mouse.set_visible(False)


        def _setup_world(self,layout):
                self.tiles = pygame.sprite.Group()
                #self.player = pygame.sprite.GroupSingle()
                self.player = pygame.sprite.Group()
                self.way = pygame.sprite.Group()
                self.finishflag = pygame.sprite.Group()

                self.SpikeTraps = pygame.sprite.Group()
                self.LaserTraps = pygame.sprite.Group()

                self.goal = pygame.sprite.Group()
                self.score = pygame.sprite.Group()
                
                self.all_sprite = CameraGroup()
                
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
                """
                for i in range(len(self.world_data)):
                        for j in range(len(self.world_data[i])):  
                        """
                for i, row in enumerate(self.world_data):
                        for j, value in enumerate(row):                           
                                x,y = j *Tile_size, i * Tile_size
                                
                                #if self.world_data[i][j] == 2:  

                                way_sprite = Way((x, y), Tile_size)
                                self.way.add(way_sprite)
                                self.all_sprite.add(way_sprite) 

                                if value == 2:                  
                                        self.player_start_cord_x,  self.player_start_cord_y = x, y                                        
                                elif value == 1:                                      
                                        tile = Wall((x, y), Tile_size)
                                        self.tiles.add(tile)
                                        self.all_sprite.add(tile)
                                elif value == 41:
                                        self.SpikeTrap = Spike((x, y), Tile_size)                                     
                                        self.SpikeTraps.add(self.SpikeTrap)
                                        self.all_sprite.add(self.SpikeTrap)
                                elif value == 42:
                                        self.LaserTrap = Laser((x, y), Tile_size)                                     
                                        self.LaserTraps.add(self.LaserTrap)
                                        self.all_sprite.add(self.LaserTrap)
                                elif value == 5:
                                        goal = Goal((x, y), Tile_size)
                                        self.goal.add(goal) 
                                        self.all_sprite.add(goal) 
                                elif value == 6:
                                        score_sprite = Score((x, y), Tile_size)
                                        self.score.add(score_sprite)
                                        self.all_sprite.add(score_sprite)  

                                elif value == 10:
                                        finish_sprite = Icons((x, y), Tile_size)
                                        self.finishflag.add(finish_sprite)
                                        self.all_sprite.add(finish_sprite) 

                player_sprite = Player((self.player_start_cord_x, self.player_start_cord_y))
                self.player.add(player_sprite)
                self.all_sprite.add(player_sprite)
                                


        def draw_tile(self):
                
                center_y = Height // 2 - len(self.world_data) / 2 * Tile_size
                center_x = Width // 2 - len(self.world_data) / 2 * Tile_size
                xy = CameraGroup()
                
                #x = xy.offset.x
                #y = xy.offset.y 
                for i in range(len(self.world_data)):
                        for j in range(len(self.world_data[i])):
                                #if self.world_data[i][j] == 0 or self.world_data[i][j] == 2 or self.world_data[i][j] == 5 or self.world_data[i][j] == 6:
                                        #pygame.draw.rect(self.screen, color_way,(j * Tile_size + self.way_x, i * Tile_size +y, Tile_size, Tile_size))
                                #elif self.world_data[i][j] == 3:
                                        #pygame.draw.rect(self.screen, color_bonus, (j * Tile_size + self.way_x, i * Tile_size + y, Tile_size, Tile_size))
                                #if self.world_data[i][j] == 3:
                                        #pygame.draw.rect(self.screen, color_bonus, (j * Tile_size + self.way_x, i * Tile_size + y, Tile_size, Tile_size))
                                if self.world_data[i][j] != 1 and self.world_data[i][j] != 9: # !=1
                                        #pygame.draw.rect(self.screen, color_way,(j * Tile_size - x, i * Tile_size -y, Tile_size, Tile_size))
                                        xy.custom_draw()
                
        # take goal
        def _handle_collision(self):
                # Получаем список всех спрайтов в группе self.player
                player_sprites = self.player.sprites()

                # Проверяем коллизии для каждого спрайта игрока
                for player in player_sprites:
                        collided_goal = spritecollideany(player, self.goal)
                        if collided_goal is not None:
                                collided_goal.kill()

                                # Инициализируем collided_score заранее
                        collided_score = None
                        if self.score:
                                collided_score = spritecollideany(player, self.score)

                        if collided_score is not None:
                                collided_score.kill()
                                self.Scorespawn -= 1
                                if self.Scorespawn == 0:
                                        self.scoreall = True

                        collided_finishflag = None
                        if self.finishflag:
                                collided_finishflag = spritecollideany(player, self.finishflag)
                        if collided_finishflag is not None:
                                self.finished = True

                        for Spiketrap in self.SpikeTraps.sprites():
                                if spritecollideany(player, self.SpikeTraps) and Spiketrap.status == 'activated':
                                        player.rect.x = self.player_start_cord_x
                                        player.rect.y = self.player_start_cord_y
                                        player.life -= 1
                        for LaserTrap in self.LaserTraps.sprites():
                                if spritecollideany(player, self.LaserTraps) and LaserTrap.status == 'activated':
                                        player.rect.x = self.player_start_cord_x
                                        player.rect.y = self.player_start_cord_y
                                        player.life -= 1


        




        
        # prevents player to pass through objects horizontall
        def _horizontal_movement_collision(self):
                # Итерируем по всем спрайтам игрока в группе
                for player in self.player.sprites():
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
                for player in self.player.sprites():
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
                if value:
                        # Если группа не пуста, то получаем первый спрайт из группы
                        player = self.player.sprites()[0] if self.player else None
                        if player:
                                player.speed = 0
                else:
                        # Если группа не пуста, то получаем первый спрайт из группы
                        player = self.player.sprites()[0] if self.player else None
                        if player:
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
                mouse_click = pygame.mouse.get_pressed()

                if mouse_click[0]:  # Проверка левой кнопки мыши (нажата ли она)
                        if Continue_rect.collidepoint(mouse_pos):
                                self.set_Pause_Flag(False)

                        elif Back_rect.collidepoint(mouse_pos):
                                from Levels import show_level_menu
                                show_level_menu()

                Continue_collide = Continue_rect.collidepoint(mouse_pos)
                Back_collide = Back_rect.collidepoint(mouse_pos)

                Continue_color = Color_Purple if Continue_collide else Color_Yellow
                Back_color = Color_Purple if Back_collide else Color_Yellow

                # Redraw with updated colors
                pygame.draw.rect(screen, (255, 255, 30), (Width // 2 - 140, Height // 2 - 120, 300, 200), 5, 34)

                Continue_text = font.render("Continue", True, Continue_color)
                screen.blit(Continue_text, Continue_rect)

                Back_text = font.render("Exit", True, Back_color)
                screen.blit(Back_text, Back_rect)

        # updating the game world from all changes committed
        def update(self, screen, player_event):
                # for draw tile
                #self.draw_tile()

                # for trap
                #if (self.trap_visible):    
                        #self.traps.remove(self.trap)                    
                       #self.traps.draw(screen)
                        
                self.SpikeTraps.update()
                self.LaserTraps.update()


                self.all_sprite.custom_draw(self.player)
                
                # for tile
                #self.tiles.draw(screen)                
                
                # for way
                #self.way.draw(self.screen)               

                # for goal
                #self.goal.draw(screen)

                #for score
                #self.score.draw(screen)
                
                
                # for collsion
                self._handle_collision()

                             
                self.player.update(player_event, self.player_face)
                #self.player.draw(screen)

                self._horizontal_movement_collision()
                self._vertical_movement_collision()

                # отображение хп и проверка конца игры
                if self.player.sprites():
                        self.game.show_life(self.player)
                        self.game.game_state(self.player.sprites()[0], self.scoreall, self.finished)
                        
                
                

                if self.pause_flag:
                        self.GamePause(screen)
       
                clock.tick(fps)
                
                text_fps = font.render(str(int(clock.get_fps())),1,(255,255,255))
                screen.blit(text_fps,(10,100))

class CameraGroup(pygame.sprite.Group):
        def __init__(self):
                super().__init__()
                self.displya_surface = pygame.display.get_surface()
                self.offset = pygame.math.Vector2()

        def custom_draw(self,player_group):
                if player_group:
                        player = player_group.sprites()[0]
                        self.offset.x = player.rect.centerx - Width / 2
                        self.offset.y = player.rect.centery - Height / 2
                        for sprite in self:
                                offset_rect = sprite.rect.copy()
                                offset_rect.center -= self.offset
                                self.displya_surface.blit(sprite.image, offset_rect)