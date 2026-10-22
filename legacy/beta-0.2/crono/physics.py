"""Deterministic 120 Hz platform physics, independent of rendering and input APIs."""
from dataclasses import dataclass
import math
import pygame as pg
from .levels import level_data

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


class Platform:
    def __init__(self, spec):
        self.rect = pg.FRect(spec['x'], spec['y'], spec['w'], spec['h'])
        self.origin = self.rect.x
        self.moving = spec['moving']
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
        self.anim = 0.
        self.trail = []

    def update(self, dt, controls, world):
        events = []
        self.invincible = max(0, self.invincible - dt)
        self.hurt_time = max(0, self.hurt_time - dt)
        self.cooldown = max(0, self.cooldown - dt)
        self.coyote = .115 if self.grounded else max(0, self.coyote - dt)
        self.buffer = .14 if controls.jump else max(0, self.buffer - dt)
        if self.support and self.grounded:
            self.rect.x += self.support.dx
        if abs(controls.axis) > .1:
            self.facing = 1 if controls.axis > 0 else -1
        if controls.dash and self.dash_ready and self.cooldown <= 0:
            self.dash_time = .16
            self.cooldown = .46
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
            if self.hurt_time<=0:
                self.vx = approach(self.vx, controls.axis * RUN, accel * dt)
            if self.buffer > 0 and self.coyote > 0:
                self.vy = JUMP
                self.buffer = self.coyote = 0
                self.grounded = False
                events.append('jump')
            if not controls.held and self.vy < -250:
                self.vy = approach(self.vy, -250, 4200 * dt)
            self.vy = min(950, self.vy + GRAVITY * dt)
        # Axis-separated collisions; float positions avoid low-speed quantisation.
        self.rect.x += self.vx * dt
        for p in world.platforms:
            if p.moving:  # Ferries are one-way platforms.
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
            if self.rect.colliderect(p.rect):
                if self.vy >= 0 and old_bottom <= p.rect.top + 1:
                    self.rect.bottom = p.rect.top
                    self.vy = 0
                    self.grounded = True
                    self.support = p
                    self.dash_ready = True
                elif self.vy < 0 and not p.moving:
                    self.rect.top = p.rect.bottom
                    self.vy = 0
        self.anim += dt * (abs(self.vx) / 65 if self.grounded else 1)
        return events


class Enemy:
    def __init__(self, spec, era):
        x, y, self.left, self.right = spec
        self.rect = pg.FRect(x, y, 44, 34)
        self.direction = -1
        self.speed = 67 + era * 11
        self.alive = True

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt
        if self.rect.left <= self.left:
            self.rect.left = self.left
            self.direction = 1
        if self.rect.right >= self.right:
            self.rect.right = self.right
            self.direction = -1


class World:
    def __init__(self, index):
        self.index = index
        self.data = level_data(index)
        self.width = self.data['width']
        self.platforms = [Platform(p) for p in self.data['platforms']]
        self.player = Player(self.data['spawn'])
        self.enemies = [Enemy(s, index) for s in self.data['enemies']]
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

    def say(self, text):
        self.message, self.message_time = text, 3.5

    def respawn(self):
        self.player = Player(self.spawn)
        self.player.invincible = 1.6
        self.deaths += 1
        self.say('Otra oportunidad. El tiempo está de tu lado.')

    def damage(self, source):
        p = self.player
        if p.invincible > 0 or p.dash_time > 0:
            return []
        p.hp -= 1
        p.invincible = 1.5
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
        if p.rect.top > 800:
            self.respawn()
            return events + ['death']
        for i, (x, y) in enumerate(self.data['shards']):
            if i not in self.shards and p.rect.inflate(20, 20).collidepoint(x, y):
                self.shards.add(i)
                events.append('shard')
                self.say('Umbral estabilizado. Encuentra el portal.' if len(self.shards) == 3 else f'Fragmento recuperado · {len(self.shards)} de 3')
        for i, (x, y) in enumerate(self.data['echoes']):
            if i not in self.echoes and p.rect.inflate(12, 12).collidepoint(x, y):
                self.echoes.add(i)
                events.append('echo')
        for i, (x, y) in enumerate(self.data['checkpoints']):
            if i > self.checkpoint and abs(p.rect.centerx - x) < 40 and abs(p.rect.bottom - y) < 70:
                self.checkpoint = i
                self.spawn = (x - 14, y - 64)
                p.hp = 3
                events.append('checkpoint')
                self.say('Ancla temporal activada · energía restaurada')
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            enemy.update(dt)
            if p.rect.colliderect(enemy.rect):
                if (p.vy > 0 and old_bottom <= enemy.rect.top + 12) or p.dash_time > 0:
                    enemy.alive = False
                    if p.dash_time <= 0:
                        p.vy = -440
                    p.dash_ready = True
                    events.append('stomp')
                else:
                    events += self.damage(enemy.rect.centerx)
                    if self.player is not p:
                        return events
        for hazard in self.hazards:
            if p.rect.colliderect(hazard):
                events += self.damage(hazard.centerx)
                if self.player is not p:
                    return events
        px, py = self.data['portal']
        if p.rect.colliderect(pg.FRect(px - 34, py - 120, 68, 120)):
            if len(self.shards) == 3:
                self.complete = True
            elif self.portal_lock <= 0:
                self.say(f'El umbral necesita los 3 fragmentos. Tienes {len(self.shards)}. Puedes volver a buscarlos.')
                self.portal_lock = 4
        return events
