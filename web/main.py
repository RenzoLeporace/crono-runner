# /// script
# dependencies = ["pygame-ce"]
# ///
"""Browser entry point: the same game as PC and Android with a cooperative WebAssembly loop.

web/crono-web.js offers the same bridge as the Android app (saves, voice, links, files),
so crono/ runs unchanged. tools/build_web.py stages this file as the app's main.py.
"""
import asyncio
import json
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'

def window_aspect(platform):
    return float(platform.window.innerWidth)/max(1,float(platform.window.innerHeight))

async def main():
    import platform
    # The bridge reads saved games from IndexedDB; wait for it before the game loads them.
    while not bool(platform.window.CronoWeb.isReady()):await asyncio.sleep(.05)
    from crono.mobile import initialize
    initialize()
    from crono.game import Game
    from crono.viewport import width_for_aspect
    game=Game()
    game.save.data['fullscreen']=False
    # Phones and tablets start with the on-screen controls; mouse and keyboard play like the PC version.
    if bool(platform.window.CronoWeb.touchFirst()):game.save.data['touch_controls']=True
    game.configure_viewport(window_aspect(platform))
    frame_samples=[];render_samples=[];frame_number=0;pending_width=None;stable_size=0
    while game.running:
        frame_start=time.perf_counter()
        frame_number+=1
        # Follow window resizes once the new size is stable, as in the Android build.
        if frame_number%30==0 and game.state in ('menu','play','voyage'):
            aspect=window_aspect(platform)
            width=width_for_aspect(aspect)
            stable_size=stable_size+1 if pending_width==width else 1
            pending_width=width
            if stable_size>=3 and abs(width-game.viewport_width)>28 and aspect>1:game.configure_viewport(aspect)
        real_dt=game.clock.tick(0)/1000
        game.events()
        game.update(min(real_dt,.1))
        game.render()
        frame_samples.append(real_dt);render_samples.append(time.perf_counter()-frame_start)
        if len(frame_samples)==120:
            index=max(0,int(len(frame_samples)*.95)-1)
            metrics=dict(fps=round(len(frame_samples)/max(.001,sum(frame_samples)),1),render_ms_p95=round(sorted(render_samples)[index]*1000,2),
                viewport=game.viewport_width,state=game.state,level=game.world.level_id)
            platform.window.eval('window.CronoFrameStats='+json.dumps(metrics))
            frame_samples.clear();render_samples.clear()
        await asyncio.sleep(max(0,1/60-(time.perf_counter()-frame_start)))
    if getattr(game,'session_started',False) and not game.world.complete:game.save.capture(game.world)
    game.save.write()
    import pygame
    pygame.quit()
    platform.window.CronoWeb.finished()

asyncio.run(main())
