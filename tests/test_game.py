"""Regression checks against real simulation and UI, with no interactive window."""
import os
import sys
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
TEMP_ROOT=ROOT/'.test-tmp'
TEMP_ROOT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'.vendor'))
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
import pygame as pg
from crono.physics import World, Player, Platform, Controls, STEP, RUN
from crono.save import Save, defaults


def advance(world,seconds,controls=None):
    for _ in range(round(seconds/STEP)):
        world.update(STEP,controls or Controls())


class PhysicsTests(unittest.TestCase):
    def setUp(self):
        self.world=World(0)
        advance(self.world,.1)

    def test_ground_and_idle_stability(self):
        advance(self.world,5)
        self.assertAlmostEqual(self.world.player.rect.bottom,584)
        self.assertTrue(self.world.player.grounded)
        self.assertEqual(self.world.player.hp,3)

    def test_acceleration_and_friction(self):
        p=self.world.player
        advance(self.world,.4,Controls(axis=1))
        self.assertEqual(p.vx,RUN)
        x=p.rect.x
        advance(self.world,.4)
        self.assertEqual(p.vx,0)
        self.assertGreater(p.rect.x,x)

    def test_variable_jump_height(self):
        peaks=[]
        for held in (False,True):
            w=World(0)
            advance(w,.1)
            w.update(STEP,Controls(jump=True,held=held))
            peak=w.player.rect.y
            for _ in range(90):
                w.update(STEP,Controls(held=held))
                peak=min(peak,w.player.rect.y)
            peaks.append(peak)
        self.assertGreater(peaks[0]-peaks[1],45)

    def test_coyote_time(self):
        p=self.world.player
        p.rect.x=681
        p.support=None
        p.grounded=True
        self.world.update(STEP,Controls(axis=1))
        advance(self.world,.04,Controls(axis=1))
        self.world.update(STEP,Controls(jump=True,held=True))
        self.assertLess(p.vy,-600)

    def test_buffered_jump(self):
        p=self.world.player
        p.rect.bottom=575
        p.vy=180
        p.grounded=False
        p.coyote=0
        p.support=None
        self.world.update(STEP,Controls(jump=True,held=True))
        advance(self.world,.08,Controls(held=True))
        self.assertLess(p.vy,-500)

    def test_no_auto_jump_from_holding(self):
        self.world.update(STEP,Controls(jump=True,held=True))
        advance(self.world,1.4,Controls(held=True))
        self.assertTrue(self.world.player.grounded)
        self.assertEqual(self.world.player.vy,0)

    def test_dash_once_in_air(self):
        p=self.world.player
        p.rect.y=200
        p.grounded=False
        self.world.update(STEP,Controls(dash=True,axis=1))
        self.assertGreater(p.vx,800)
        advance(self.world,.2)
        self.world.update(STEP,Controls(dash=True))
        self.assertEqual(p.dash_time,0)
        advance(self.world,1)
        self.assertTrue(p.dash_ready)

    def test_dash_cannot_tunnel_through_wall(self):
        wall=Platform(dict(x=180,y=0,w=40,h=584,moving=False))
        self.world.platforms.append(wall)
        self.world.update(STEP,Controls(dash=True,axis=1))
        advance(self.world,.2,Controls(axis=1))
        self.assertLessEqual(self.world.player.rect.right,180)

    def test_moving_platform_carries_player(self):
        w=self.world
        ferry=next(p for p in w.platforms if p.moving)
        p=w.player
        p.rect.midbottom=(ferry.rect.centerx,ferry.rect.top)
        p.grounded=True
        p.support=ferry
        offset=p.rect.x-ferry.rect.x
        advance(w,.25)
        self.assertAlmostEqual(p.rect.x-ferry.rect.x,offset,delta=.2)

    def test_fall_respawns_without_losing_fragments(self):
        self.world.shards.add(0)
        self.world.player.rect.y=830
        self.world.update(STEP,Controls())
        self.assertEqual(self.world.deaths,1)
        self.assertEqual(self.world.shards,{0})
        self.assertEqual(self.world.player.hp,3)

    def test_checkpoint_restores_health_and_spawn(self):
        w=self.world
        w.player.rect.midbottom=(1460,584)
        w.player.hp=1
        w.update(STEP,Controls())
        self.assertEqual(w.checkpoint,0)
        self.assertEqual(w.player.hp,3)
        w.respawn()
        self.assertEqual(w.player.rect.midbottom,(1460,584))

    def test_invulnerability_prevents_repeated_damage(self):
        p=self.world.player
        self.world.damage(200)
        self.world.damage(200)
        self.assertEqual(p.hp,2)

    def test_stomp_defeats_enemy(self):
        w=self.world
        enemy=w.enemies[0]
        w.player.rect.midbottom=(enemy.rect.centerx,enemy.rect.top-1)
        w.player.vy=250
        events=w.update(STEP,Controls())
        self.assertIn('stomp',events)
        self.assertFalse(enemy.alive)
        self.assertLess(w.player.vy,0)

    def test_dash_defeats_enemy(self):
        w=self.world
        enemy=w.enemies[0]
        w.player.rect.midbottom=(enemy.rect.centerx-20,584)
        events=w.update(STEP,Controls(axis=1,dash=True))
        self.assertIn('stomp',events)
        self.assertEqual(w.player.hp,3)

    def test_portal_requires_all_fragments(self):
        w=self.world
        w.player.rect.midbottom=w.data['portal']
        w.update(STEP,Controls())
        self.assertFalse(w.complete)
        w.shards={0,1,2}
        w.update(STEP,Controls())
        self.assertTrue(w.complete)


class CampaignTests(unittest.TestCase):
    def test_all_required_routes_reachable_with_real_jump_physics(self):
        """Build a reachability graph from simulated jumps, including all solids.

        Launches may use a run-up anywhere on a platform. This does not teleport a
        player through a level: it checks geometric routes, separately from combat.
        No dash or moving ferry is needed for any required fragment or the exit.
        """
        for level_id in range(15):
            era,stage=divmod(level_id,3)
            w=World(era,stage)
            solids=[p for p in w.platforms if not p.moving]
            model=SimpleNamespace(platforms=solids,width=w.width)
            reachable={0}
            changed=True
            edges=0
            while changed:
                changed=False
                for source_index in tuple(reachable):
                    source=solids[source_index]
                    candidates=[(i,t) for i,t in enumerate(solids) if i not in reachable
                        and t.rect.top>=source.rect.top-115
                        and t.rect.left<source.rect.right+240 and t.rect.right>source.rect.left-240]
                    if not candidates:
                        continue
                    starts=list(range(int(source.rect.left),int(source.rect.right-28)+1,28))
                    starts.append(source.rect.right-28)
                    for sx in starts:
                        for direction in (-1,0,1):
                            p=Player((sx,source.rect.top-64))
                            p.grounded=True
                            p.support=source
                            p.vx=direction*RUN
                            for tick in range(160):
                                p.update(STEP,Controls(direction,tick==0,True),model)
                                if p.grounded:
                                    landed=solids.index(p.support)
                                    if landed not in reachable:
                                        reachable.add(landed)
                                        edges+=1
                                        changed=True
                                    break
                                if p.rect.top>800:
                                    break
            for x,y in w.data['shards']:
                holders=[i for i,p in enumerate(solids) if p.rect.left<=x<=p.rect.right and 0<p.rect.top-y<60]
                self.assertTrue(any(i in reachable for i in holders),f'Fragment {(x,y)} unreachable in era {era}; nodes={reachable}')
            self.assertIn(4,reachable,f'Exit island unreachable in era {era}')
            self.assertEqual(len(w.data['echoes']),17)
            print(f'Map {era+1}.{stage+1}: all fragments and exit reachable; {len(reachable)}/{len(solids)} surfaces, {edges} links')

    def test_campaign_unlocks_all_five_eras_and_ending(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as folder:
            save=Save(Path(folder)/'progress.json')
            for level_id in range(15):
                era,stage=divmod(level_id,3)
                w=World(era,stage)
                w.shards={0,1,2}
                if w.boss:
                    w.boss.hp=0
                    w.boss.alive=False
                w.player.rect.midbottom=w.data['portal']
                w.update(STEP,Controls())
                self.assertTrue(w.complete)
                save.completed(w)
                self.assertEqual(save.data['unlocked'],min(14,level_id+1))
            self.assertTrue(Save(save.path).data['finished'])


class SaveTests(unittest.TestCase):
    def test_checkpoint_and_collectibles_roundtrip(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as folder:
            save=Save(Path(folder)/'progress.json')
            w=World(2)
            w.checkpoint=1
            w.shards={0,2}
            w.echoes={1,4,9}
            w.enemies[0].alive=False
            save.capture(w)
            restored=World(2)
            Save(save.path).restore(restored)
            self.assertEqual(restored.shards,w.shards)
            self.assertEqual(restored.echoes,w.echoes)
            self.assertEqual(restored.checkpoint,1)
            self.assertFalse(restored.enemies[0].alive)
            self.assertEqual(restored.player.rect.bottom,584)

    def test_corrupt_save_is_recoverable(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as folder:
            path=Path(folder)/'progress.json'
            path.write_text('{bad json')
            save=Save(path)
            self.assertTrue(save.warning)
            self.assertEqual(save.data['unlocked'],0)
            save.capture(World(0))
            self.assertTrue(Save(path).data['started'])

    def test_invalid_saved_values_cannot_crash_restore(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as folder:
            save=Save(Path(folder)/'progress.json')
            save.data['progress']=dict(index=0,shards=[-1,'bad',2,8],echoes=None,checkpoint='wrong',defeated=[None,100])
            save.write()
            w=World(0)
            Save(save.path).restore(w)
            self.assertEqual(w.shards,{2})


class InterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from crono.game import Game
        cls.temp=tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        cls.game=Game(True,Path(cls.temp.name)/'progress.json')

    @classmethod
    def tearDownClass(cls):
        pg.quit()
        cls.temp.cleanup()

    def setUp(self):
        self.game.save.data=defaults()
        self.game.world=World(0)
        self.game.set_state('menu')

    def test_every_screen_and_era_renders(self):
        game=self.game
        for era in range(5):
            game.world=World(era)
            for state in ('menu','chapters','help','intro','play','pause','help_play','complete','ending'):
                game.state=state
                game.render()
                self.assertTrue(game.buttons,f'No actions in {state}')

    def test_keyboard_menu_play_pause_resume(self):
        game=self.game
        game.set_state('menu')
        game.render()
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_RETURN))
        game.events()
        self.assertEqual(game.state,'intro')
        game.render()
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_RETURN))
        game.events()
        self.assertEqual(game.state,'play')
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_ESCAPE))
        game.events()
        self.assertEqual(game.state,'pause')
        before=game.world.time
        game.update(.2)
        self.assertEqual(game.world.time,before)
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_ESCAPE))
        game.events()
        self.assertEqual(game.state,'play')

    def test_final_portal_reaches_ending_and_continue_returns_there(self):
        game=self.game
        game.world=World(4,2)
        game.world.shards={0,1,2}
        game.world.boss.alive=False
        game.world.boss.hp=0
        game.world.player.rect.midbottom=game.world.data['portal']
        game.set_state('play')
        game.update(STEP)
        self.assertEqual(game.state,'complete')
        game.render()
        game.activate()
        self.assertEqual(game.state,'ending')
        game.set_state('menu')
        game.continue_game()
        self.assertEqual(game.state,'ending')


if __name__=='__main__':
    unittest.main(verbosity=2)

