# /// script
# dependencies = ["pygame-ce"]
# ///
"""Android entry point: the same game with a cooperative WebAssembly loop."""
import asyncio
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'

async def main():
    from crono.mobile import initialize
    initialize()
    from crono.game import Game
    game=Game();game.save.data['touch_controls']=True
    game.save.data['fullscreen']=False
    while game.running:
        dt=min(game.clock.tick(0)/1000,.1)
        game.events();game.update(dt);game.render()
        await asyncio.sleep(0)
    if getattr(game,'session_started',False) and not game.world.complete:game.save.capture(game.world)
    game.save.write()
    from crono.mobile import bridge
    if bridge():bridge().finishGame()
    import pygame
    pygame.quit()

asyncio.run(main())
