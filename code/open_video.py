import os
import sys

import pygame
from moviepy.editor import VideoFileClip

class IntroPlayer:
    VIDEO_PATH = "../videos/opening.mp4"
    AUDIO_PATH = "../videos/copy_opening.mp3"

    def __init__(self, video_path=None, audio_path=None):
        self.video_path = video_path if video_path is not None else IntroPlayer.VIDEO_PATH
        self.audio_path = audio_path if audio_path is not None else IntroPlayer.AUDIO_PATH

    def play(self):
        if not os.path.exists(self.audio_path):
            clip = VideoFileClip(self.video_path)
            clip.audio.write_audiofile(self.audio_path, logger=None)
            clip.close()

        clip = VideoFileClip(self.video_path)
        fps = clip.fps
        size = clip.size

        pygame.init()
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        pygame.display.set_caption("Intro Video")
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        skip_video = False

        for frame in clip.iter_frames(fps=fps, dtype='uint8'):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()  # 直接退出整个程序
                    elif event.key == pygame.K_RETURN:
                        skip_video = True  # 快进

            if skip_video:
                break

            surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(surf, (0, 0))
            pygame.display.flip()
            clock.tick(fps)

        pygame.mixer.music.stop()
        clip.close()
