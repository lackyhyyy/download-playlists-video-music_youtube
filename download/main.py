import os
from colorama import Fore, init
from datetime import datetime
from pytube import Playlist
from pytube import YouTube
from tqdm import tqdm
from progress.bar import Bar
import sys

log_file_path = "downloads//download_log.txt"

# Функция для записи в лог
def log(message):
    # Получаем текущее время

    # Формируем строку для записи в лог
    log_entry = f"{message}\n"

    # Открываем файл логов в режиме добавления
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        # Записываем строку в файл
        log_file.write(log_entry)
       
init(autoreset=True)

def stop():
    sys.exit()
    
        
class download_yt:
    def download(url_input):
        try:
            log_file = open('downloads/download_log.txt', 'w', encoding='utf-8')

            playlist = Playlist(url_input)
            print(f'Найден плейлист: {Fore.RED}{playlist.title}{Fore.WHITE}')
            log(f'{datetime.now()} Плейлист: {playlist.title} найден\n\n')
            if not os.path.exists(f'downloads/playlist/{playlist.title}'):
                os.makedirs(f'downloads/playlist/{playlist.title}')

            process_count = 1
            countener_ch = 0
            countener_accept = 0
            countener_b = 0

            total_videos = len(playlist.videos)

            for video in playlist.videos:
                video_filename = f"downloads/playlist/{playlist.title}/{video.title}.mp3"
                if os.path.exists(video_filename):
                    log(f'{datetime.now()} - Файл {video.title} уже существует, пропускаем\n')
                    countener_b += 1
                    print(f'{Fore.YELLOW}[{process_count}/{total_videos}] Файл {video.title} уже существует, пропускаем{Fore.RESET}')
                    process_count += 1
                    continue

                try:
                    print(f'{Fore.BLUE}[{process_count}/{total_videos}] Скачиваеться файл: {video.title}{Fore.RESET}')
                    video_stream = video.streams.filter(only_audio=True).first()

                    # Use a progress bar
                    bar = Bar(f'    Скачивание: {video.title}', max=100)
                    bytes_downloaded = 0
                    total_bytes = video_stream.filesize

                    def progress_function(stream, chunk, bytes_remaining):
                        nonlocal bytes_downloaded
                        bytes_downloaded += len(chunk)
                        percent = (bytes_downloaded / total_bytes) * 100
                        bar.goto(int(percent))

                    yt = YouTube(video.watch_url)
                    yt.register_on_progress_callback(progress_function)
                    yt.streams.filter(only_audio=True).first().download(filename=video_filename)
                    bar.finish()

                    log(f'{datetime.now()} - Скачан файл: {video.title}\n')
                    print(f'    {Fore.GREEN}[{process_count}/{total_videos}] Скачан файл: {video.title}{Fore.RESET}')
                    countener_accept += 1
                    process_count += 1
                except Exception as e:
                    log(f'{datetime.now()} - Ошибка при скачивании {video.title}: {str(e)}\n')
                    countener_ch += 1
                    print(f'{Fore.RED}[{process_count}/{total_videos}] Ошибка при скачивании: {Fore.RED}{video.title}: {str(e)}{Fore.RESET}')
                    process_count += 1

            log_file.close()
            print(f'{Fore.GREEN}Скачивание плейлиста завершено.{Fore.RESET}\n')
            print(f"{Fore.RED}Ошибок: {countener_ch}{Fore.RESET},{Fore.GREEN} Скачано удачно: {countener_accept}{Fore.RESET},{Fore.YELLOW} Уже было скаченно до этого: {countener_b}{Fore.RESET}")
            input()
            main()
        except Exception as e:
            print(f'{Fore.RED}Ошибка: {str(e)}{Fore.RESET}')
            input()

    def download_video_yt(url_inupt):
        try:
            
            countener_ch = 0
            countener_accept = 0
            countener_b = 0
            
            yt = YouTube(url_inupt)
            print(f'Найден трек: {Fore.RED}{yt.title}{Fore.WHITE}')

            if not os.path.exists('downloads'):
                os.makedirs('downloads')

            log_file = open('downloads/download_log.txt', 'w', encoding='utf-8')

            if not os.path.exists("downloads/treck"):
                os.makedirs("downloads/treck")

            treck_filename = f"downloads//treck//{yt.title}.mp3"

            try:
                video_stream = yt.streams.filter(only_audio=True).first()
                video_stream.download(filename=treck_filename)
                log_file.write(f'{datetime.now()} - Скачан файл: {yt.title}\n')
                print(f'{Fore.GREEN}Скачан файл: {yt.title}{Fore.RESET}')
                countener_accept += 1
                print(f"{Fore.RED}Ошибок: {countener_ch}{Fore.RESET},{Fore.GREEN} Скачано удачно: {countener_accept}{Fore.RESET}")
                input()
                main()
            except Exception as e:
                log_file.write(f'{datetime.now()} - Ошибка при скачивании {yt.title}: {str(e)}\n')
                print(f'{Fore.RED}Ошибка при скачивании: {Fore.RED}{yt.title}{Fore.WHITE}: {str(e)}{Fore.RESET}\n\n')
                countener_ch += 1
                print(f"{Fore.RED}Ошибок: {countener_ch}{Fore.RESET},{Fore.GREEN} Скачано удачно: {countener_accept}{Fore.RESET}")
                input()
                main()

            log_file.close()
            print(f'{Fore.GREEN}Скачивание завершено.{Fore.RESET}')
            input()
            return main()
        except Exception as e:
            print(f'{Fore.RED}Ошибка: {str(e)}{Fore.RESET}')
            input()

    def download_vidio_mp4(url_input):
        try:
            
            countener_ch = 0
            countener_accept = 0
            countener_b = 0
            
            yt = YouTube(url_input)
            print(f"Найдено видио: {Fore.RED}{yt.title}{Fore.WHITE}")
            
            if not os.path.exists('downloads'):
                os.makedirs('downloads')
                
            log_file = open('downloads/download_log.txt', 'w', encoding='utf-8')

            video_filename = f"downloads//vidio//{yt.title}.mp4"

            if not os.path.exists("downloads//vidio"):
                os.makedirs("downloads//vidio")
                
            try:
                video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                video_stream.download(filename=video_filename)
                log_file.write(f'{datetime.now()} - Скачан файл: {yt.title}\n')
                print(f'    {Fore.GREEN}Скачан файл: {yt.title}{Fore.RESET}')
                countener_accept += 1 
                print(f"{Fore.RED}Ошибок: {countener_ch}{Fore.RESET},{Fore.GREEN} Скачано удачно: {countener_accept}{Fore.RESET}")
                input()
                main()
            except Exception as e:
                log_file.write(f'{datetime.now()} - Ошибка при скачивании {yt.title}: {str(e)}\n')
                print(f'{Fore.RED}Ошибка при скачивании: {Fore.RED}{yt.title}{Fore.WHITE}: {str(e)}{Fore.RESET}')
                countener_ch += 1
                print(f"\n{Fore.RED}Ошибок: {countener_ch}{Fore.RESET},{Fore.GREEN} Скачано удачно: {countener_accept}{Fore.RESET}")
                input()
                main()
        except Exception as e:
            print(f'{Fore.RED}Ошибка: {str(e)}{Fore.RESET}')
            input()


class Menu_dow:
    def download_treck():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Введите ссылку на видео, которое хотите скачать:")
        url_input = input(f"{Fore.GREEN}: ")
        print(f"{Fore.RESET}")
        if url_input == "back":
            main()
        download_yt.download_video_yt(url_input)
            
    def download_playlist():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Введите ссылку на плейлист, который хотите скачать:")
        url_input = input(f"{Fore.GREEN}: ")
        print(f"{Fore.RESET}")
        if url_input == "back":
            main()
        download_yt.download(url_input)

    def download_vidio():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Введите ссылку на видио, которое хотите скачать:")
        url_input = input(f"{Fore.GREEN}: ")
        print(f"{Fore.RESET}")
        if url_input == "back":
            main()
        download_yt.download_vidio_mp4(url_input)    
        
def main():
    os.system("cls")
    print(f"{Fore.RESET}1. Скачать плейлист")
    print("3. Скачать трек (.mp3)")
    print("3  Скачать видио (.mp4)")
    print("4. Выйти из программы")
    choice = input(": ")
    if choice == "1":
        Menu_dow.download_playlist()
    elif choice == "2":
        Menu_dow.download_treck()   
    elif choice == "3":
        Menu_dow.download_vidio()
    elif choice == "4":
        exit()
    elif choice == "exit":
        sys.exit()
    elif choice == "restart":
        python = sys.executable
        os.execl(python, python, *sys.argv)
    else:
        main()
        

            
if __name__ == "__main__":
    main()


