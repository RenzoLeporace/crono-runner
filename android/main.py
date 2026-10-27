# /// script
# dependencies = ["pygame-ce"]
# ///
"""Android entry point: the same game with a cooperative WebAssembly loop."""
import asyncio
import os
import time
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'

async def main():
    import platform
    from crono.mobile import initialize
    initialize()
    from crono.mobile import bridge
    native=bridge();diagnostics=bool(native and native.performanceLogging())
    from crono.game import Game
    from crono.viewport import width_for_aspect
    game=Game();game.save.data['touch_controls']=True
    game.save.data['fullscreen']=False
    import platform
    aspect=float(platform.window.innerWidth)/max(1,float(platform.window.innerHeight))
    game.configure_viewport(aspect)
    frame_samples=[];render_samples=[];frame_number=0;pending_width=None;stable_size=0
    while game.running:
        frame_start=time.perf_counter()
        frame_number+=1
        if frame_number%30==0 and game.state in ('menu','play','voyage'):
            aspect=float(platform.window.innerWidth)/max(1,float(platform.window.innerHeight))
            width=width_for_aspect(aspect)
            stable_size=stable_size+1 if pending_width==width else 1
            pending_width=width
            if stable_size>=3 and abs(width-game.viewport_width)>28 and aspect>1:game.configure_viewport(aspect)
        real_dt=game.clock.tick(0)/1000
        dt=min(real_dt,.1)
        game.events();game.update(dt);game.render()
        frame_samples.append(real_dt);render_samples.append(time.perf_counter()-frame_start)
        if len(frame_samples)==120:
            metrics=dict(fps=round(len(frame_samples)/max(.001,sum(frame_samples)),1),render_ms_p95=round(sorted(render_samples)[113]*1000,2),viewport=game.viewport_width,state=game.state,level=game.world.level_id,projectiles=len(game.world.projectiles))
            platform.window.eval('window.CronoFrameStats='+json.dumps(metrics))
            if diagnostics:platform.window.console.log('CRONO_FRAME_STATS '+json.dumps(metrics))
            frame_samples.clear();render_samples.clear()
        await asyncio.sleep(max(0,1/60-(time.perf_counter()-frame_start)))
    if getattr(game,'session_started',False) and not game.world.complete:game.save.capture(game.world)
    game.save.write()
    from crono.mobile import bridge
    if bridge():bridge().finishGame()
    import pygame
    pygame.quit()

asyncio.run(main())
