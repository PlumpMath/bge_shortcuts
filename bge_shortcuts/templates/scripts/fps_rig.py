from bge import logic
from bge import events
from bge import render

from mathutils import Vector

class FPSRig():
    
    def __init__(self, cont):
        
        self.body = cont.owner
        self.camera = self.body.children['shortcuts_fps_camera']
        
        # Player movement variables
        self.move_speed = 5.0
        self.run_multiplier = 2.0        
        self.jump_force = 5.0
        
        # Mouse variables
        self.mouse_sensitivity = 0.002
        self.mouse_smoothing = 0.5
    
        # Used for smoothing the mouselook
        self.old_x = 0.0
        self.old_y = 0.0
        
        # Screen variables used for the mouselook
        self.screen_width = render.getWindowWidth()
        self.screen_height = render.getWindowHeight()
        self.screen_center = (self.screen_width//2, self.screen_height//2)
        
        # Set the mouse position to the center of the screen
        render.setMousePosition(*self.screen_center) 
        
        # logic.mouse.position is incorrect on the first frame. This variable is used to get around that
        self.delay = 0
        
        
    def update(self):
        
        # ---------
        # Mouselook
        # ---------
        
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
            self.body.applyRotation([0, 0, x], False)
            self.camera.applyRotation([y, 0, 0], True)
                
            # Center mouse in game window
            render.setMousePosition(*self.screen_center)
            
        if self.delay <= 1:
            self.delay += 1        
        
         
         
        # --------
        # Movement
        # --------
        
        keyboard = logic.keyboard.events
        
        # Use two variables to track the directions
        forward = 0
        side = 0
        
        # Get the keyboard inputs and manipulate the direction variables
        if keyboard[events.WKEY]:
            forward += 1
        
        if keyboard[events.SKEY]:
            forward -= 1  
        
        if keyboard[events.AKEY]:
            side -= 1            
        
        if keyboard[events.DKEY]:
            side += 1            
        
        # Calculate the speed that the player will be moving at. Holding left shift activates the run multiplier
        speed = self.move_speed
        if keyboard[events.LEFTSHIFTKEY]:
            speed = self.move_speed * self.run_multiplier
            
        # Calculate the z_speed (fall speed) and add the jump force if the player presses the spacebar
        z_speed = self.body.getLinearVelocity().z            
        if keyboard[events.SPACEKEY] == 1:            
            z_speed += self.jump_force            
        
        # Move the object using linear velocities
        self.body.setLinearVelocity([side * speed, forward * speed, z_speed], True)


def main(cont):
        
    if 'fps_rig' not in cont.owner:        
        cont.owner['fps_rig'] = FPSRig(cont)
        
    cont.owner['fps_rig'].update()        
