"""Exercise authored connections with the actual player collision simulation."""
from types import SimpleNamespace
from crono.physics import Player,Controls,STEP,RUN

def can_traverse(world,a,b):
    source=world.platforms[a];target=world.platforms[b]
    sr,tr=source.rect,target.rect
    direction=1 if tr.centerx>=sr.centerx else -1
    # Running launches near either lip, or under an overlapping upper branch.
    starts={sr.left+3,sr.right-31}
    for value in (tr.left-140,tr.centerx-170,tr.right+110,tr.centerx+140):
        starts.add(max(sr.left+2,min(sr.right-30,value)))
    for sx in sorted(starts,reverse=direction>0):
        lunar=world.level_id==44
        nearby=[p for p in world.platforms if not p.moving and p.rect.right>sx-(900 if lunar else 420) and p.rect.left<sx+(900 if lunar else 480)]
        model=SimpleNamespace(platforms=nearby,width=world.width,mechanic=world.mechanic)
        for axis in (direction,0,-direction):
            for jump in (True,False) if tr.top>sr.top+40 else (True,):
                p=Player((sx,sr.top-64))
                p.grounded=True;p.support=source;p.vx=axis*RUN
                drop=not jump and source.oneway
                for tick in range(420 if lunar else 240):
                    inside=tr.left+5<p.rect.centerx<tr.right-5
                    descend=inside and p.rect.bottom<tr.top and p.support is not target and p.grounded and p.support and p.support.oneway
                    steer=0 if inside and p.rect.bottom<tr.top and tick>35 else axis
                    lowering=(drop and tick==0) or bool(descend)
                    p.update(STEP,Controls(axis=steer,jump=(jump and tick==0) or lowering,held=True,drop=lowering,descend=lowering),model)
                    if p.grounded:
                        if p.support is target:
                            return True
                    if p.rect.top>800:
                        break
    return False

def probe_route(world):
    reachable={0};failed=[]
    for a,b in world.data['route_links']:
        if a in reachable and b not in reachable:
            if can_traverse(world,a,b):
                reachable.add(b)
            else:
                failed.append((a,b))
    return reachable,failed
