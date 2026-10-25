"""A wider camera and continuous parallax, with cached individual art assets."""
import importlib
import pygame as pg

RENDER_MODULES=('art','period_art','argentina_art','egypt_art','journey_art','educational_art','enemy_art','heritage','humanoid_art')

def width_for_aspect(aspect):
    return max(960,min(2560,round(720*aspect)))


def set_render_width(width,clear=False):
    for name in RENDER_MODULES:
        module=importlib.import_module('crono.'+name)
        changed=getattr(module,'W',None)!=width
        if hasattr(module,'W'):module.W=width
        if changed:
            for name in ('sky','sky_image','gradient','backdrop'):
                value=getattr(module,name,None)
                if hasattr(value,'cache_clear'):value.cache_clear()
        if clear:
            for value in vars(module).values():
                if callable(value) and hasattr(value,'cache_clear'):value.cache_clear()

class ViewportUI:
    def configure_viewport(self,aspect=None):
        if aspect is None:
            w,h=self.display.get_size();aspect=w/max(1,h)
        width=width_for_aspect(aspect)
        if getattr(self,'viewport_width',None)==width:return
        self.viewport_width=width;self.ui_scale=min(1,width/1280)
        self.ui_offset=((width-1280*self.ui_scale)/2,(720-720*self.ui_scale)/2)
        self.ui_canvas=pg.Surface((1280,720),pg.SRCALPHA);self.canvas=self.ui_canvas
        self.world_canvas=pg.Surface((width,720));self.display=pg.display.set_mode((width,720),pg.RESIZABLE)
        set_render_width(width,True)
        self.menu_world_background=None;self.mobile_menu_background=None
        if hasattr(self,'artist'):self.artist.mobile_layer=None

    def present(self):
        width=self.viewport_width;world=self.world_canvas
        if self.state not in ('play','voyage'):
            if self.touch_enabled():
                key=(self.world.index,self.world.stage,width)
                cached=getattr(self,'menu_world_background',None)
                if cached is None or cached[0]!=key:
                    picture=pg.Surface((width,720));self.artist.background(picture,self.world.index,0,0,self.world.stage)
                    cached=(key,picture);self.menu_world_background=cached
                world.blit(cached[1],(0,0))
            else:self.artist.background(world,self.world.index,self.camera,self.time,self.world.stage)
        ui=self.ui_canvas
        if self.ui_scale!=1:ui=pg.transform.scale(ui,(width,round(720*self.ui_scale)))
        world.blit(ui,self.ui_offset)
        dw,dh=self.display.get_size();ratio=min(dw/width,dh/720)
        size=(max(1,round(width*ratio)),max(1,round(720*ratio)))
        self.display.fill((8,24,33))
        picture=world if size==world.get_size() else pg.transform.scale(world,size) if self.touch_enabled() else pg.transform.smoothscale(world,size)
        self.display.blit(picture,((dw-size[0])//2,(dh-size[1])//2));pg.display.flip()

def mobile_backdrop(artist,s,world,camera):
    # Keep sky and landmarks in their own coordinate spaces. Flattening them
    # into one scrolling screenshot made every buffer rebuild snap the scenery.
    # Art modules cache their skies and building images without resizing or
    # flushing those caches as the camera moves.
    key=(world.level_id,s.get_width())
    if getattr(artist,'mobile_layer',None)!=key:artist.mobile_layer=key
    artist.background(s,world.index,camera,0,world.stage)
    from .educational_art import map_features
    map_features(s,world,camera,0)
    if world.index==7:
        from .argentina_art import props
        props(s,world,camera,0)
    elif world.index<7:
        from .period_art import props
        props(s,world,camera,0)
