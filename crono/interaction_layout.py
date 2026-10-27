"""Place interactables on existing surfaces without competing activation regions."""

def arrange(world):
    w=world
    for i,(x,y) in enumerate(w.data['checkpoints']):
        for _ in range(5):
            overhead=[p for p in w.platforms if p.active and not p.moving and p.rect.left<x+25 and p.rect.right>x-25 and 14<y-p.rect.top<105]
            if not overhead:break
            ledge=min(overhead,key=lambda p:p.rect.top);x,y=ledge.rect.centerx,ledge.rect.top
        w.data['checkpoints'][i]=(x,y)
    occupied=list(w.data['checkpoints'])
    floors=[p for p in w.platforms if p.active and not p.moving and p.rect.w>=110 and p.rect.top<=650]
    def reserve(point,radius=180,min_x=-1,max_x=None):
        x,y=point
        options=[]
        for floor in floors:
            r=floor.rect
            pad=min(64,r.w/3)
            nearest=max(r.left+pad,min(r.right-pad,x))
            if options and abs(nearest-x)+abs(r.top-y)*2>min(v[0] for v in options):continue
            xs=[max(r.left+pad,min(r.right-pad,x)),r.centerx]
            xs+=list(range(round(r.left+pad),round(r.right-pad)+1,24))
            for xx in sorted(set(xs),key=lambda v:abs(v-x)):
                yy=r.top
                if xx<=min_x or max_x is not None and xx>=max_x:continue
                if any(abs(xx-ox)<radius and abs(yy-oy)<145 for ox,oy in occupied):continue
                if any(abs(xx-h.centerx)<95 and abs(yy-h.bottom)<80 for h in w.hazards):continue
                # A raised platform may not hide an exhibit or block its approach.
                if any(p.active and p.rect.left<xx+48 and p.rect.right>xx-48 and 12<yy-p.rect.top<105 for p in w.platforms):continue
                options.append((abs(xx-x)+abs(yy-y)*2,(xx,yy)))
                break
        if not options:raise ValueError(f'Mapa {w.level_id}: no hay lugar libre para {point} entre {min_x} y {max_x}')
        result=min(options,key=lambda v:v[0])[1]
        occupied.append(result);return result
    for site in (w.rescue_site,w.rift_site):
        if site:occupied.append(site[:2])
    if 'repair_ship' in w.data:occupied.append(w.data['repair_ship'])
    sites=w.data['cultural_sites']
    for i,(x,y,key) in enumerate(sites):
        if x>w.width*.55:
            floor=min((w.platforms[n] for n in w.data['main_nodes']),key=lambda p:abs(p.rect.centerx-w.width*.35))
            x,y=floor.rect.centerx,floor.rect.top
        x,y=reserve((x,y));sites[i]=(x,y,key)
    for i,(x,y,topic) in enumerate(w.data['stations']):
        if i==1 and x<=sites[0][0]+200:
            floor=min((w.platforms[n] for n in w.data['main_nodes']),key=lambda p:abs(p.rect.centerx-w.width*.67))
            x,y=floor.rect.centerx,floor.rect.top
        x,y=reserve((x,y));w.data['stations'][i]=(x,y,topic)
    if w.traits.exposure_kind:
        floor=min((w.platforms[n] for n in w.data['main_nodes']),key=lambda p:abs(p.rect.centerx-w.width*.22))
        w.traits.coat_pos=reserve((floor.rect.centerx,floor.rect.top),105,w.width*.15,w.width*.40)
    m=w.mechanic;old_devices=list(m.devices)
    m.devices=[reserve(point,200) for point in old_devices]
    f=m.field;old_points=list(f.points)
    f.points=[(x,y-40) for x,y in (reserve((x,y+40),185 if f.kind in ('chain','cipher') else 105) for x,y in old_points)]
    if f.kind=='moonrepair':w.data['repair_parts']=list(f.points)
    from .field_systems import LIFTS,LIGHTS
    for i,lift in enumerate(f.lifts):
        if f.kind in LIFTS:
            dx=m.devices[i][0]-old_devices[i][0];dy=m.devices[i][1]-old_devices[i][1]
        else:
            dx=f.points[i][0]-old_points[i][0];dy=f.points[i][1]-old_points[i][1]
        lift.rect.move_ip(dx,dy);lift.origin+=dx;lift.origin_y+=dy
    f.escort_x,f.escort_y=m.devices[0]
    w.traits.points=[reserve(point,105) for point in w.traits.points]
    # Anchors reserved first: IDs, order and safe spawn points remain stable.
    w.interaction_positions=occupied
