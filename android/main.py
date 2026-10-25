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
    while str(platform.window.eval('window.CronoWebReady === false')).lower()=='true':await asyncio.sleep(.01)
    from crono.mobile import initialize
    initialize()
    from crono.game import Game
    game=Game();game.save.data['touch_controls']=True
    game.save.data['fullscreen']=False
    import platform
    aspect=float(platform.window.innerWidth)/max(1,float(platform.window.innerHeight))
    game.configure_viewport(aspect)
    frame_samples=[];render_samples=[]
    while game.running:
        frame_start=time.perf_counter()
        if game.state in ('menu','play','voyage'):
            aspect=float(platform.window.innerWidth)/max(1,float(platform.window.innerHeight))
            if abs(aspect-game.viewport_width/720)>.04 and aspect>1:game.configure_viewport(aspect)
        dt=min(game.clock.tick(0)/1000,.1)
        game.events();game.update(dt);game.render()
        frame_samples.append(dt);render_samples.append(time.perf_counter()-frame_start)
        if len(frame_samples)==120:
            metrics=dict(fps=round(len(frame_samples)/max(.001,sum(frame_samples)),1),render_ms_p95=round(sorted(render_samples)[113]*1000,2),viewport=game.viewport_width)
            platform.window.eval('window.CronoFrameStats='+json.dumps(metrics))
            frame_samples.clear();render_samples.clear()
        if str(platform.window.eval('typeof window.CronoWebStorageError'))!='undefined':game.save.warning=str(platform.window.CronoWebStorageError)
        await asyncio.sleep(max(0,1/60-(time.perf_counter()-frame_start)))
    if getattr(game,'session_started',False) and not game.world.complete:game.save.capture(game.world)
    game.save.write()
    from crono.mobile import bridge
    if bridge():bridge().finishGame()
    import pygame
    pygame.quit()

asyncio.run(main())
