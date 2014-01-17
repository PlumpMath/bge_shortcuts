script = """

from bge import logic
from bge import render
from bge import events

from mathutils import Vector

class FlyCamera():
    
    def __init__(self, cont):   

        self.camera = cont.owner

        self.move_speed = 0.2
        self.mouse_sensitivity = 0.002
        self.mouse_smoothing = 0.5

        self.old_x = 0.0
        self.old_y = 0.0
        
        self.screen_width = render.getWindowWidth()
        self.screen_height = render.getWindowHeight()
        self.screen_center = (self.screen_width//2, self.screen_height//2)

        render.setMousePosition(*self.screen_center) 

        # logic.mouse.position is incorrect on the first frame. This variable is used to get around that
        self.delay = 0
        
        
    def update(self):

        # Mouselook
        if self.delay >= 1:
            
            # Get the center of the screen and the current mouse position
            center = Vector(self.screen_center)
            mouse_position = Vector([logic.mouse.position[0] * self.screen_width, logic.mouse.position[1] * self.screen_height])

            x = center.x - mouse_position.x
            y = center.y - mouse_position.y
            
            # Smooth movement
            self.old_x = (self.old_x*self.mouse_smoothing + x*(1.0-self.mouse_smoothing))
            self.old_y = (self.old_y*self.mouse_smoothing + y*(1.0-self.mouse_smoothing))
                
            x = self.old_x* self.mouse_sensitivity
            y = self.old_y* self.mouse_sensitivity
                 
            # set the values
            self.camera.applyRotation([0, 0, x], False)
            self.camera.applyRotation([y, 0, 0], True)
                
            # Center mouse in game window
            render.setMousePosition(*self.screen_center)
            
        if self.delay <= 1:
            self.delay += 1
        
        
        # Keyboard movement
        keyboard = logic.keyboard.events
        
        if logic.getAverageFrameRate() != 0:
            frame_equaliser = 60 / logic.getAverageFrameRate()
        else:
            frame_equaliser == 1
        
        speed = self.move_speed * frame_equaliser
        
                
        if keyboard[events.LEFTSHIFTKEY]:
            speed = self.move_speed * 3 * frame_equaliser

        if keyboard[events.LEFTCTRLKEY]:
            speed = self.move_speed / 3 * frame_equaliser
        
        if keyboard[events.WKEY]:
            self.camera.applyMovement([0, 0, -speed], True)

        if keyboard[events.SKEY]:
            self.camera.applyMovement([0, 0, speed], True)
            
        if keyboard[events.AKEY]:
            self.camera.applyMovement([-speed, 0, 0], True)
            
        if keyboard[events.DKEY]:
            self.camera.applyMovement([speed, 0, 0], True)
            
        if keyboard[events.EKEY]:
            self.camera.applyMovement([0, speed, 0], True)
            
        if keyboard[events.QKEY]:
            self.camera.applyMovement([0, -speed, 0], True)
                        
        
        
def main(cont):
    
    if 'fly_camera' not in cont.owner:

        cont.owner['fly_camera'] = FlyCamera(cont)

    cont.owner['fly_camera'].update()



"""