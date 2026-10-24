"""Deterministic 120 Hz platform physics, independent of rendering and input APIs."""
from dataclasses import dataclass
import math
import pygame as pg
from .levels import level_data
from .combat import Enemy, Boss, Projectile

STEP = 1 / 120
GRAVITY = 1900
JUMP = -660
RUN = 310


def approach(value, target, amount):
    return min(value + amount, target) if value < target else max(value - amount, target)


@dataclass
class Controls:
    axis: float = 0
    jump: bool = False
    held: bool = False
    dash: bool = False
    attack: bool = False
    drop: bool = False


class Platform:
    def __init__(self, spec):
        self.rect = pg.FRect(spec['x'], spec['y'], spec['w'], spec['h'])
        self.origin = self.rect.x
        self.moving = spec['moving']
        self.oneway = spec.get('oneway',self.moving)
        self.amplitude = spec.get('amplitude', 0)
        self.speed = spec.get('speed', 0)
        self.dx = 0

    def update(self, time):
        old = self.rect.x
        if self.moving:
            self.rect.x = self.origin + math.sin(time * self.speed) * self.amplitude
        self.dx = self.rect.x - old


class Player:
    def __init__(self, pos):
        self.rect = pg.FRect(*pos, 28, 64)
        self.vx = self.vy = 0.
        self.facing = 1
        self.grounded = False
        self.support = None
        self.coyote = self.buffer = 0.
        self.dash_time = self.cooldown = 0.
        self.dash_ready = True
        self.invincible = 0.
        self.hurt_time = 0.
        self.hp = 3
        self.max_hp=3
        self.upgrades=set()
        self.air_jump=True
        self.shield=0
        self.shot_cooldown=0.
        self.anim = 0.
        self.trail = []
        self.drop_time=0.

    def configure(self,upgrades,heal=False):
        self.upgrades=set(upgrades)
        self.max_hp=3+('vitality' in self.upgrades)+('vitality2' in self.upgrades)
        self.hp=self.max_hp if heal else min(self.max_hp,self.hp)
        if 'shield' in self.upgrades and heal:
            self.shield=1

    def update(self, dt, controls, world):
        events = []
        self.drop_time=max(0,self.drop_time-dt)
        if controls.drop and self.grounded and self.support and self.support.oneway:
            self.drop_time=.22
            self.rect.y+=3
            self.grounded=False
            self.coyote=self.buffer=0
            self.vy=max(45,self.vy)
        self.invincible = max(0, self.invincible - dt)
        self.hurt_time = max(0, self.hurt_time - dt)
        self.cooldown = max(0, self.cooldown - dt)
        self.shot_cooldown=max(0,self.shot_cooldown-dt)
        self.coyote = .115 if self.grounded else max(0, self.coyote - dt)
        self.buffer = .14 if controls.jump and not self.drop_time else max(0, self.buffer - dt)
        if self.support and self.grounded:
            self.rect.x += self.support.dx
        if abs(controls.axis) > .1:
            self.facing = 1 if controls.axis > 0 else -1
        if controls.dash and self.dash_ready and self.cooldown <= 0:
            self.dash_time = .20 if 'dash' in self.upgrades else .16
            self.cooldown = .28 if 'dash' in self.upgrades else .46
            self.dash_ready = False
            self.vy = 0
            events.append('dash')
        dashing = self.dash_time > 0
        if dashing:
            self.dash_time = max(0, self.dash_time - dt)
            self.vx = self.facing * 820
            self.vy = 0
        else:
            accel = 2400 if self.grounded else 1650
            if 'boots' in self.upgrades and not self.grounded:
                accel=2100
            if self.hurt_time<=0:
                self.vx = approach(self.vx, controls.axis * (355 if 'boots' in self.upgrades else RUN), accel * dt)
            if self.buffer > 0 and self.coyote > 0:
                self.vy = JUMP
                self.buffer = self.coyote = 0
                self.grounded = False
                events.append('jump')
            elif controls.jump and 'double_jump' in self.upgrades and self.air_jump and not self.grounded:
                self.vy=JUMP*.93
                self.air_jump=False
                self.buffer=0
                events.append('jump')
            if not controls.held and self.vy < -250:
                self.vy = approach(self.vy, -250, 4200 * dt)
            self.vy = min(950, self.vy + GRAVITY * dt)
        # Axis-separated collisions; float positions avoid low-speed quantisation.
        self.rect.x += self.vx * dt
        for p in world.platforms:
            if p.oneway:  # Branch galleries and ferries can be entered from below.
                continue
            if self.rect.colliderect(p.rect):
                if self.vx > 0:
                    self.rect.right = p.rect.left
                elif self.vx < 0:
                    self.rect.left = p.rect.right
                self.vx = 0
                self.dash_time = 0
        self.rect.x = max(0, min(world.width - self.rect.w, self.rect.x))
        old_bottom = self.rect.bottom
        self.rect.y += self.vy * dt
        self.grounded = False
        self.support = None
        for p in world.platforms:
            if p.oneway and self.drop_time>0:
                continue
            if self.rect.colliderect(p.rect):
                if self.vy >= 0 and old_bottom <= p.rect.top + 1:
                    self.rect.bottom = p.rect.top
                    self.vy = 0
                    self.grounded = True
                    self.support = p
                    self.dash_ready = True
                    self.air_jump=True
                elif self.vy < 0 and not p.oneway:
                    self.rect.top = p.rect.bottom
                    self.vy = 0
        self.anim += dt * (abs(self.vx) / 65 if self.grounded else 1)
        return events


class World:
    def __init__(self, index,stage=0,upgrades=None,answered=None,difficulty=0):
        self.index = index
        self.stage=stage
        self.difficulty=max(0,min(2,difficulty))
        self.level_id=index*3+stage
        self.upgrades=set(upgrades or ())
        self.answered=set(answered or ())
        self.data = level_data(index,stage)
        self.checkpoint_ids=self.selected_checkpoints(self.difficulty)
        self.width = self.data['width']
        self.platforms = [Platform(p) for p in self.data['platforms']]
        self.player = Player(self.data['spawn'])
        self.player.configure(self.upgrades,True)
        self.enemies = [Enemy(s, index,self.difficulty) for s in self.data['enemies']]
        self.hazards = [pg.FRect(s) for s in self.data['hazards']]
        self.shards = set()
        self.echoes = set()
        self.checkpoint = -1
        self.spawn = self.data['spawn']
        self.time = 0.
        self.deaths = 0
        self.complete = False
        self.message = ''
        self.message_time = 0.
        self.portal_lock = 0.
        self.projectiles=[]
        self.boss=Boss(index,self.difficulty,self.data['arena_left'],self.data['arena_right']) if self.data['boss'] else None

    def set_difficulty(self,band):
        """Apply a profile immediately without resurrecting defeated opponents."""
        band=max(0,min(2,band))
        self.difficulty=band
        self.checkpoint_ids=self.selected_checkpoints(band)
        self.select_checkpoint(self.checkpoint)
        for enemy in self.enemies:
            enemy.set_difficulty(band)
        if self.boss:
            self.boss.set_difficulty(band)

    def near_station(self):
        p=self.player.rect
        candidates=[s for s in self.data['stations'] if abs(p.centerx-s[0])<85 and abs(p.bottom-s[1])<100]
        return min(candidates,key=lambda s:abs(p.centerx-s[0])) if candidates else None

    def selected_checkpoints(self,band):
        total=len(self.data['checkpoints'])
        if band==0 or total<=2:return tuple(range(total))
        if band==2:return (round((total-1)*.4),total-1)
        return tuple(sorted({round(n*(total-1)/3) for n in range(4)}))

    def select_checkpoint(self,index):
        """Keep stable save IDs; removed anchors fall back to a previous valid one."""
        self.checkpoint=max((i for i in self.checkpoint_ids if i<=index),default=-1)
        if self.checkpoint<0:
            self.spawn=self.data['spawn']
        else:
            x,y=self.data['checkpoints'][self.checkpoint]
            self.spawn=(x-14,y-64)

    def say(self, text):
        self.message, self.message_time = text, 3.5

    def respawn(self):
        self.player = Player(self.spawn)
        self.player.configure(self.upgrades,True)
        self.player.invincible = 1.6
        self.deaths += 1
        self.projectiles=[]
        if self.boss and self.boss.alive:
            self.boss=Boss(self.index,self.difficulty,self.data['arena_left'],self.data['arena_right'])
        self.say('Otra oportunidad. El tiempo está de tu lado.')

    def damage(self, source):
        p = self.player
        if p.invincible > 0 or p.dash_time > 0:
            return []
        if p.shield:
            p.shield=0
            p.invincible=1.2
            return ['shield']
        p.hp -= 1
        p.invincible = (1.5,1.1,.8)[self.difficulty]
        p.hurt_time = .16
        p.vy = -330
        p.vx = -260 if p.rect.centerx < source else 260
        p.dash_time = 0
        if p.hp <= 0:
            self.respawn()
            return ['death']
        return ['hurt']

    def update(self, dt, controls):
        self.time += dt
        self.message_time = max(0, self.message_time - dt)
        self.portal_lock = max(0, self.portal_lock - dt)
        for platform in self.platforms:
            platform.update(self.time)
        p = self.player
        old_bottom = p.rect.bottom
        events = p.update(dt, controls, self)
        if controls.attack and p.shot_cooldown<=0:
            self.projectiles.append(Projectile(p.rect.centerx+p.facing*21,p.rect.centery,p.facing*680,
                                               owner='player',damage=2 if 'pulse' in self.upgrades else 1,kind='pulse'))
            p.shot_cooldown=.34
            events.append('shot')
        if p.rect.top > 800:
            self.respawn()
            return events + ['death']
        for i, (x, y) in enumerate(self.data['shards']):
            if i not in self.shards and p.rect.inflate(95 if 'magnet' in self.upgrades else 20,95 if 'magnet' in self.upgrades else 20).collidepoint(x, y):
                self.shards.add(i)
                events.append('shard')
                self.say('Umbral estabilizado. Encuentra el portal.' if len(self.shards) == 3 else f'Fragmento recuperado · {len(self.shards)} de 3')
        for i, (x, y) in enumerate(self.data['echoes']):
            if i not in self.echoes and p.rect.inflate(120 if 'magnet' in self.upgrades else 12,120 if 'magnet' in self.upgrades else 12).collidepoint(x, y):
                self.echoes.add(i)
                events.append('echo')
        for i, (x, y) in enumerate(self.data['checkpoints']):
            if i not in self.checkpoint_ids:
                continue
            if i > self.checkpoint and abs(p.rect.centerx - x) < 40 and abs(p.rect.bottom - y) < 70:
                self.checkpoint = i
                self.spawn = (x - 14, y - 64)
                p.hp = p.max_hp
                p.shield=int('shield' in self.upgrades)
                events.append('checkpoint')
                self.say('Ancla temporal activada · energía restaurada')
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            if self.boss and self.boss.active and enemy.rect.right<self.data['arena_left']:
                continue
            enemy.update(dt,self)
            if p.rect.colliderect(enemy.rect):
                if ((p.vy > 0 and old_bottom <= enemy.rect.top + 12) and enemy.kind!='armored') or p.dash_time > 0:
                    enemy.hit(2 if p.dash_time>0 else 1)
                    if p.dash_time <= 0:
                        p.vy = -440
                    p.dash_ready = True
                    events.append('stomp')
                else:
                    events += self.damage(enemy.rect.centerx)
                    if self.player is not p:
                        return events
        if self.boss and self.boss.alive:
            self.boss.update(dt,self)
            if self.boss.active:
                p.rect.left=max(self.data['arena_left']+6,p.rect.left)
                if p.rect.colliderect(self.boss.rect):
                    if self.boss.phase=='exposed' and (p.dash_time>0 or (p.vy>0 and old_bottom<=self.boss.rect.top+12)):
                        defeated=self.boss.hit(2)
                        p.vy=-450
                        p.dash_ready=True
                        if defeated:
                            events.append('boss')
                    else:
                        events+=self.damage(self.boss.rect.centerx)
                        if self.player is not p:
                            return events
        for shot in self.projectiles:
            if not shot.alive:
                continue
            shot.update(dt)
            if shot.owner=='player':
                for enemy in self.enemies:
                    if enemy.alive and shot.rect.colliderect(enemy.rect):
                        defeated=enemy.hit(shot.damage)
                        shot.alive=False
                        events.append('stomp' if defeated else 'block')
                        break
                if shot.alive and self.boss and self.boss.alive and shot.rect.colliderect(self.boss.rect):
                    if self.boss.hit(shot.damage):
                        events.append('boss')
                        self.say('Guardián liberado. El camino a la próxima época está abierto.')
                    shot.alive=False
            elif shot.rect.colliderect(p.rect):
                events+=self.damage(shot.rect.centerx)
                shot.alive=False
                if self.player is not p:
                    return events
            if shot.kind!='wave' and any(shot.rect.colliderect(platform.rect) for platform in self.platforms if not platform.moving):
                shot.alive=False
        self.projectiles=[s for s in self.projectiles if s.alive]
        for hazard in self.hazards:
            if p.rect.colliderect(hazard):
                events += self.damage(hazard.centerx)
                if self.player is not p:
                    return events
        px, py = self.data['portal']
        if p.rect.colliderect(pg.FRect(px - 34, py - 120, 68, 120)):
            if len(self.shards) == 3 and (not self.boss or not self.boss.alive):
                self.complete = True
            elif self.portal_lock <= 0:
                self.say('Libera al guardián de esta época para abrir el umbral.' if self.boss and self.boss.alive and len(self.shards)==3 else f'El umbral necesita los 3 fragmentos. Tienes {len(self.shards)}. Puedes volver a buscarlos.')
                self.portal_lock = 4
        return events
