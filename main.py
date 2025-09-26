import pygame
import os
import settings
from camera import Camera
from object import Object


class Program:
    def __init__(self, win_size: tuple) -> None:
        self.window = None
        self.clock = None
        self.running = False

        self.win_size = win_size

        self.fonts = {}
        self.controls_text = []
        self.show_controls = True

        self.camera = None

        self.objects = {}
        self.object_idx = 0
        self.current_object = None

    def start(self) -> None:
        pygame.init()
        pygame.font.init()

        self.window = pygame.display.set_mode(self.win_size)
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.display.set_caption("Cube Engine")

        self.init_fonts()

        self.camera = Camera()

        self.load_models()
        self.switch_current_object()

        self.program_loop()

    def init_fonts(self) -> None:
        self.fonts["medium"] = pygame.font.Font("resources/font/Silkscreen-Regular.ttf", 20)
        self.fonts["small"] = pygame.font.Font("resources/font/Silkscreen-Regular.ttf", 14)

        self.controls_text = [self.fonts["medium"].render("[C] Toggle figure vertices", False, settings.L_GREY),
                              self.fonts["medium"].render("[UP] Increase rotation speed", False, settings.L_GREY),
                              self.fonts["medium"].render("[DOWN] Decrease rotation speed", False, settings.L_GREY),
                              self.fonts["medium"].render("[Z] Scale up figure", False, settings.L_GREY),
                              self.fonts["medium"].render("[S] Scale down figure", False, settings.L_GREY),
                              self.fonts["medium"].render("[W] Switch to another figure", False, settings.L_GREY),
                              self.fonts["medium"].render("[R] Reset figure settings", False, settings.L_GREY)]

    def load_models(self) -> None:
        for file in os.listdir("resources"):
            if file.endswith(".obj"):
                file_name = file.split(".")[0]

                self.objects[file_name] = Object(self.window, self.camera, file_name)
                self.objects[file_name].load()

    def switch_current_object(self, increase: bool = False) -> None:
        if increase:
            self.object_idx += 1

        self.current_object = self.objects[list(self.objects.keys())[self.object_idx]]

    def program_loop(self) -> None:
        while self.running:
            self.clock.tick(settings.MAX_FRAMERATE)
            self.window.fill(settings.BG)

            # Check for pygame event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    match event.key:  # Faster than if/elif/else
                        case pygame.K_ESCAPE:
                            self.running = False
                        case pygame.K_UP:
                            self.current_object.rotation_speed += 0.01
                        case pygame.K_DOWN:
                            self.current_object.rotation_speed -= 0.01
                        case pygame.K_w:
                            self.switch_current_object(True)
                        case pygame.K_c:
                            self.current_object.show_vertices = False if self.current_object.show_vertices is True else True  # Ternary operator -> takes less place
                        case pygame.K_F1:
                            self.show_controls = False if self.show_controls is True else True
                        case pygame.K_r:
                            self.current_object.reset()
            
            # Camera
            self.camera.update()
            
            # Project object on the screen
            self.current_object.angle_x += self.current_object.rotation_speed
            self.current_object.angle_y += self.current_object.rotation_speed

            self.current_object.project()

            # Render dynamic texts
            fps_text = self.fonts["medium"].render(str(round(self.clock.get_fps())), False, settings.L_GREY)
            loaded_text = self.fonts["small"].render(f"Current model: {self.current_object.model_name}.obj", False, settings.L_GREY)
            cam_pos_text = self.fonts["small"].render(f"{round(self.camera.pos[0], 3)}, {round(self.camera.pos[1], 3)}, {round(self.camera.pos[2], 3)}", False, settings.L_GREY)

            self.window.blit(fps_text, (settings.WIN_WIDTH - 60, 20)) # - 60 | little offset to make it looks better
            self.window.blit(loaded_text, (20, settings.WIN_HEIGHT - 40))
            self.window.blit(cam_pos_text, (settings.WIN_WIDTH - 200, settings.WIN_HEIGHT - 40))

            if self.show_controls:
                i = 0
                for text in self.controls_text:
                    self.window.blit(text, (20, 20 + i))
                    i += 30

            pygame.display.flip()

    print("Exiting")
    pygame.quit()


if __name__ == "__main__":
    program = Program((settings.WIN_WIDTH, settings.WIN_HEIGHT))
    program.start()

# Made entirely by Fsubject
