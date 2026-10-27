"""Full update/render timings under projectile pressure; native SDL, not phone FPS."""
import os,sys,tempfile,time,json,argparse,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'.vendor')]
os.environ.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',PYGAME_HIDE_SUPPORT_PROMPT='1')
from crono.game import Game
from crono.physics import Controls
from crono.combat import Projectile
def benchmark():
    result={}
    with tempfile.TemporaryDirectory(dir=ROOT/'.test-tmp') as d:
        g=Game(True,Path(d)/'save.json');g.save.data['touch_controls']=True;g.configure_viewport(1600/720)
        for level in (2,23,48):
            g.load(*divmod(level,3));g.begin();g.tutorial_active=False;w=g.world;w.practice_mode=True
            p=w.player;p.invincible=9999;p.rect.midbottom=(w.boss.left+300,584);w.shards={0,1,2};w.boss.active=True;g.camera=w.width-1600
            samples=[]
            for i in range(360):
                if i%12==0:
                    for n in range(20):w.projectiles.append(Projectile(p.rect.centerx+100+n*3,400+n*3,-100,owner='player' if n%2 else 'enemy'))
                start=time.perf_counter();w.update(1/60,Controls());g.time=i/60;g.render()
                if i>=60:samples.append((time.perf_counter()-start)*1000)
            ordered=sorted(samples);result[str(level)]=dict(median_ms=round(statistics.median(samples),3),p95_ms=round(ordered[285],3),p99_ms=round(ordered[297],3))
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args();result=benchmark()
    if args.output:args.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
