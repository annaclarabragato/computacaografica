import os
import pygame

class AudioManager:
    """Gerencia a reprodução de músicas e efeitos sonoros no jogo."""
    
    def __init__(self):
        """Inicializa o mixer do pygame e carrega os arquivos de áudio necessários."""
        pygame.mixer.init()
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_dir, "musicas")
        
        if not os.path.exists(assets_path):
            raise FileNotFoundError(f"🚨 ERRO: O diretório de músicas não foi encontrado: {assets_path}")
        
        self.sounds = {}
        
        bounce_path = os.path.join(assets_path, "efeitomolaa.mp3")
        if os.path.exists(bounce_path):
            self.sounds["mola"] = pygame.mixer.Sound(bounce_path)
        else:
            print(f"🚨 ERRO: O arquivo 'bounce.wav' não foi encontrado em {bounce_path}")
        
        self.music_files = [
            os.path.join(assets_path, "linkin-park.mp3"),
            os.path.join(assets_path, "one-step-closer.mp3")
        ]
        
        self.current_music_index = 0
        self.music_playing = False
        
        if os.path.exists(self.music_files[self.current_music_index]):
            pygame.mixer.music.load(self.music_files[self.current_music_index])
            pygame.mixer.music.set_volume(0.5)
        else:
            raise FileNotFoundError(f"🚨 ERRO: Arquivo de música não encontrado: {self.music_files[self.current_music_index]}")

    def play_music(self):
        """Inicia a reprodução da música em loop."""
        if not self.music_playing:
            pygame.mixer.music.play(-1)
            self.music_playing = True

    def stop_music(self):
        """Para a reprodução da música."""
        pygame.mixer.music.stop()
        self.music_playing = False

    def play_sound(self, sound_name):
        """Toca um efeito sonoro específico, se estiver carregado.
        
        Args:
            sound_name (str): Nome do efeito sonoro a ser reproduzido.
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"⚠️ Aviso: Som '{sound_name}' não encontrado!")

    def next_music(self):
        """Troca para a próxima música da lista e a reproduz."""
        self.current_music_index = (self.current_music_index + 1) % len(self.music_files)
        pygame.mixer.music.load(self.music_files[self.current_music_index])
        pygame.mixer.music.play(-1)  # -1 faz tocar em loop
        print(f"🎵 Tocando agora: {self.music_files[self.current_music_index]}")
        
    def toggle_music(self):
        """Pausa ou retoma a reprodução da música."""
        if pygame.mixer.music.get_busy():  # Verifica se a música está tocando
            pygame.mixer.music.pause()
            self.music_playing = False
            print("⏸️ Música pausada.")
        else:
            pygame.mixer.music.unpause()
            self.music_playing = True
            print("▶️ Música retomada.")