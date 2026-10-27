"""Focused regressions for exposure, object placement and local collision queries."""
import os
import random
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.campaign import TOTAL_LEVELS
from crono.field_systems import PICKUPS
from crono.physics import Controls,STEP,World
from crono.save import Save


def stand(world,point):
    """Stand on an actual existing surface; do not alter collision geometry."""
    floor=next(p for p in world.platforms if p.active and not p.moving
               and p.rect.left<=point[0]<=p.rect.right and abs(p.rect.top-point[1])<.01)
    player=world.player
    player.rect.midbottom=point;player.vx=player.vy=0
    player.grounded=True;player.support=floor;player.invincible=99999
    return floor


def exposed_floor(world):
    for floor in world.platforms:
        if not floor.active or floor.moving or floor.rect.w<180:continue
        for fraction in (.2,.5,.8):
            point=(floor.rect.left+floor.rect.w*fraction,floor.rect.top)
            if any(abs(point[0]-x)<160 and abs(point[1]-y)<130 for x,y in world.traits.points):continue
            if abs(point[0]-world.traits.coat_pos[0])<100:continue
            if world.boss and point[0]>=world.boss.left-200:continue
            return point
    raise AssertionError('No exposed reachable floor found')


def quiet_world(level):
    world=World(*divmod(level,3));world.enemies=[];world.hazards=[]
    return world


def anchors_and_objects(world):
    for i,point in enumerate(world.data['stations']):yield 'archivo'+str(i),point[:2]
    for i,point in enumerate(world.data['cultural_sites']):yield 'curiosidad'+str(i),point[:2]
    for i,point in enumerate(world.mechanic.devices):yield 'puesto'+str(i),point
    if world.mechanic.field.kind in PICKUPS:
        for i,(x,y) in enumerate(world.mechanic.field.points):yield 'pieza'+str(i),(x,y+40)
    for i,point in enumerate(world.traits.points):yield 'refugio'+str(i),point
    for i,point in enumerate(world.data['checkpoints']):yield 'ancla'+str(i),point
    if world.traits.exposure_kind:yield 'equipo',world.traits.coat_pos
    if world.rescue_site:yield 'rescate',world.rescue_site[:2]
    if world.rift_site:yield 'grieta',world.rift_site[:2]
    if 'repair_ship' in world.data:yield 'nave',world.data['repair_ship']


class EnvironmentFollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT/'.test-tmp').mkdir(exist_ok=True);pg.init();pg.display.set_mode((1600,720))
        from crono.art import font,rendered_text
        font.cache_clear();rendered_text.cache_clear()

    @classmethod
    def tearDownClass(cls):pg.quit()

    def test_cold_exposure_is_active_in_ice_and_southern_war_maps(self):
        for level in (3,4,5,28,33,48):
            with self.subTest(level=level):
                world=quiet_world(level);self.assertEqual(world.traits.exposure_kind,'cold')
                point=exposed_floor(world);stand(world,point)
                for _ in range(120):world.update(STEP,Controls())
                unprotected=100-world.traits.resource
                self.assertGreater(unprotected,0)
                world.traits.resource=100;world.traits.coat=True;stand(world,point)
                for _ in range(120):world.update(STEP,Controls())
                protected=100-world.traits.resource
                self.assertGreater(protected,0);self.assertLess(protected,unprotected)

    def test_freezing_returns_to_start_even_after_an_anchor(self):
        world=quiet_world(3);world.select_checkpoint(world.checkpoint_ids[1])
        self.assertGreaterEqual(world.checkpoint,0)
        stand(world,exposed_floor(world));world.traits.resource=.001
        old_player=world.player;events=world.update(STEP,Controls())
        self.assertIn('death',events);self.assertIsNot(old_player,world.player)
        self.assertEqual(world.checkpoint,-1);self.assertEqual(world.spawn,world.data['spawn'])
        self.assertEqual(tuple(world.player.rect.topleft),tuple(world.data['spawn']))
        self.assertEqual(world.traits.resource,100)

    def test_equipment_is_on_a_reachable_later_surface_and_pickup_does_not_disable_exposure(self):
        for level in (3,28,33,44,48,49):
            with self.subTest(level=level):
                world=quiet_world(level);traits=world.traits
                self.assertGreater(traits.coat_pos[0],world.width*.15)
                self.assertLess(traits.coat_pos[0],world.width*.40)
                stand(world,traits.coat_pos);world.update(STEP,Controls())
                self.assertTrue(traits.coat)
                stand(world,exposed_floor(world));before=traits.resource
                for _ in range(120):world.update(STEP,Controls())
                self.assertLess(traits.resource,before)

    def test_real_refuges_recover_heat_oxygen_and_filter(self):
        for level,kind in ((3,'cold'),(44,'oxygen'),(49,'gas')):
            with self.subTest(level=level):
                world=quiet_world(level);traits=world.traits
                self.assertEqual(traits.exposure_kind,kind)
                stand(world,traits.points[0]);traits.resource=20
                for _ in range(120):world.update(STEP,Controls())
                self.assertGreater(traits.resource,40);self.assertTrue(traits.safe())
                self.assertEqual(world.deaths,0)

    def test_oxygen_and_filter_exhaustion_use_the_saved_anchor(self):
        for level in (44,49):
            with self.subTest(level=level):
                world=quiet_world(level);world.select_checkpoint(world.checkpoint_ids[1]);expected=tuple(world.spawn)
                stand(world,exposed_floor(world));world.traits.resource=.001
                events=world.update(STEP,Controls())
                self.assertIn('death',events);self.assertEqual(tuple(world.player.rect.topleft),expected)
                self.assertEqual(world.traits.resource,100)

    def test_protection_and_remaining_resource_survive_save_restore(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp') as folder:
            for level in (3,33,44,48,49):
                with self.subTest(level=level):
                    world=quiet_world(level);world.traits.coat=True;world.traits.resource=37.25
                    save=Save(Path(folder)/f'level-{level}.json');save.capture(world)
                    restored=quiet_world(level);Save(save.path).restore(restored)
                    self.assertTrue(restored.traits.coat);self.assertAlmostEqual(restored.traits.resource,37.25)

    def test_all_anchors_are_ordered_and_keep_the_boss_approach(self):
        for level in range(TOTAL_LEVELS):
            with self.subTest(level=level):
                world=World(*divmod(level,3));xs=[point[0] for point in world.data['checkpoints']]
                self.assertEqual(xs,sorted(set(xs)))
                if world.boss:self.assertEqual(world.data['checkpoints'][-1],(world.boss.left+70,584))

    def test_interactables_stand_on_active_existing_surfaces(self):
        for level in range(TOTAL_LEVELS):
            world=World(*divmod(level,3))
            for name,point in anchors_and_objects(world):
                with self.subTest(level=level,object=name):
                    self.assertTrue(any(p.active and not p.moving and p.rect.left<=point[0]<=p.rect.right
                                        and abs(p.rect.top-point[1])<.01 for p in world.platforms),point)

    def test_anchors_are_not_drawn_through_upper_walkways(self):
        for level in range(TOTAL_LEVELS):
            world=World(*divmod(level,3))
            for index,(x,y) in enumerate(world.data['checkpoints']):
                with self.subTest(level=level,anchor=index):
                    self.assertFalse(any(p.active and p.rect.left<x+25 and p.rect.right>x-25
                                         and 14<y-p.rect.top<105 for p in world.platforms),(x,y))

    def test_no_anchor_book_pickup_or_refuge_overlaps_another_object(self):
        for level in range(TOTAL_LEVELS):
            world=World(*divmod(level,3));objects=list(anchors_and_objects(world))
            for i,(name,point) in enumerate(objects):
                for other,other_point in objects[i+1:]:
                    with self.subTest(level=level,first=name,second=other):
                        self.assertFalse(abs(point[0]-other_point[0])<100 and abs(point[1]-other_point[1])<80,
                                         (point,other_point))

    def test_curiosity_precedes_the_second_archive(self):
        for level in range(TOTAL_LEVELS):
            with self.subTest(level=level):
                world=World(*divmod(level,3))
                self.assertLess(world.data['cultural_sites'][0][0]+100,world.data['stations'][1][0])

    def test_impacts_follow_the_visible_warning_in_meteors_ash_and_bombardments(self):
        for level in (2,15,16,34,46,48,49):
            with self.subTest(level=level):
                world=quiet_world(level);field=world.mechanic.field
                world.mechanic.state['step']=1;stand(world,world.mechanic.devices[0]);field.clock=3.99
                field.update(.02,Controls());self.assertEqual(len(field.marks),1);self.assertFalse(field.impacts)
                for _ in range(60):field.update(.02,Controls())
                self.assertFalse(field.marks);self.assertTrue(field.impacts)
                image=pg.Surface((400,720));image.fill((0,0,0));field.draw(image,world.player.rect.centerx-200,0)
                before=pg.image.tobytes(image,'RGB');field.impacts=[]
                image.fill((0,0,0));field.draw(image,world.player.rect.centerx-200,0)
                self.assertTrue(before!=pg.image.tobytes(image,'RGB'),'El impacto debe modificar píxeles visibles')

    def test_nearby_collision_queries_match_bruteforce_with_live_lifts(self):
        rng=random.Random(272026)
        for level in range(TOTAL_LEVELS):
            world=World(*divmod(level,3))
            for phase in (0.,.75,2.4):
                for i,platform in enumerate(world.platforms):
                    if platform.moving:platform.update(phase)
                    platform.active=i%5!=0
                for _ in range(55):
                    rect=pg.FRect(rng.uniform(-100,world.width+100),rng.uniform(80,720),rng.choice((14,28,120,600)),rng.choice((10,64,150)))
                    expected=[p for p in world.platforms if p.active and p.rect.colliderect(rect)]
                    result=[p for p in world.near_platforms(rect) if p.active and p.rect.colliderect(rect)]
                    self.assertEqual(result,expected,(level,phase,rect))
            # Replacing the list, even at the same length, must invalidate bins.
            original=world.platforms;world.platforms=list(reversed(original))
            query=pg.FRect(0,0,world.width,800)
            self.assertEqual([p for p in world.near_platforms(query) if p.active],
                             [p for p in world.platforms if p.active])


if __name__=='__main__':unittest.main(verbosity=2)
