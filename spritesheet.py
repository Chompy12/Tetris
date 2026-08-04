import pygame

class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)
        self.sprite_sheet_width = self.sprite_sheet.get_width()
        self.sprite_sheet_height = self.sprite_sheet.get_height()
    
    def get_image(self, x, y, width, height, color_key=None):
        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        return image