import os
import subprocess
import socket
import webbrowser
import requests
import json

os.system("clear")

wersja = "1.2.0"

def is_internet_available():
    try:
        # Próbuje nawiązać połączenie z serwerem Google na porcie 80 (HTTP).
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def check_for_update():
    if is_internet_available():
        repo_owner = 'Kmarz23'
        repo_name = 'PlTerminal'
        
        response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases')

        if response.status_code == 200:
            releases = json.loads(response.text)
            if releases:
                latest_release = releases[0]  # Zakładamy, że najnowszy release znajduje się na początku listy
                latest_version = latest_release.get('tag_name')
                if latest_version:
                    if latest_version > current_version:
                        odp = input(f"Dostępna jest nowa wersja systemu: {latest_version}. Czy chcesz pobrać (T/N)")
                        if odp == 'T' or odp ==  't':
                        	os.system(f"wget https://github.com/Kmarz23/PlTerminal/archive/refs/tags/{latest_version}.tar.gz")
                        	os.system(f"tar -xzvf {latest_version}.tar.gz")
                        	os.system(f"rm ~/PlTerminal.py")
                        	os.system(f"cp PlTerminal-{latest_version}/PlTerminal-Debian.py ~")
                        	os.system("clear")
                        	print("\nPo ponownym uruchomieniu terminala zainicuje się nowa wersja.\n")
            else:
                print("Brak dostępnych wydań w repozytorium.")
        else:
            print("Błąd podczas pobierania danych z GitHuba.")
    else:
        print("Brak dostępu do internetu. Sprawdź swoje połączenie.")

current_version = wersja  # Aktualna wersja systemu

check_for_update()


sciezka = os.getcwd()


# Kody kolorów ANSI
BIALE = '\033[0;37m'  # biały
NIEBIESKI = '\033[0;34m'  # niebieski
RESET = '\033[0m'  # reset kolorów

def polecenie_pomoc():
    print("\nPomoc:\n")
    print("Dostępne polecenia:\n")
    print("  pomoc - wyświetla tę pomoc\n")
    print("  lp - wyświetla listę plików w bieżącym katalogu\n")
    print("  zk - pozwala zmienić katalog\n")
    print("  wersja - wyświetla aktualną wersje nakładki\n")
    print("  wyjscie - pozwala wyjść z tej nakładki\n")
    print("  pp instaluj - instaluje pakiet (nie ma potrzeby")
    print("  dodawać przed tym polecenia sudo(jest to już uwzględnone))\n")
    print("  altor - pokazuje kto jest altorem\n")
    print("  kp - pozwala skopiować i wkleić plik\n")
    print("  Nie ma tu jeszcze wszystkich komend jakie mają być wprowadzone,")
    print("  ale morzna wprowadzać inne linux'sowe komendy\n")

def polecenie_lista_plikow():
    try:
        pliki = os.listdir('.')
        print("\nLista plików w bieżącym katalogu:\n")
        for plik in pliki:
            if os.path.isfile(plik):
                print(BIALE + plik + RESET, "\n")
            elif os.path.isdir(plik):
                print(NIEBIESKI + plik + RESET, "\n")
    except PermissionError:
        print("\nBrak uprawnień do listowania plików w tym katalogu.\n")

def zmien_katalog():
    katalog = input("\nPodaj nazwę katalogu lub wpisz '..' aby \npowrócić do poprzedniego katalogu: ")
    print("\n")
    
    if katalog == '..':
        os.chdir('..')
    elif os.path.exists(katalog) and os.path.isdir(katalog):
        os.chdir(katalog)
    else:
        print(f"Katalog '{katalog}' nie istnieje.\n")

def fwersja():
	print(f"Aktualna wersja to: {wersja}\n")

def pp_i():
    try:
        pakiet = input("\nPodaj nazwę pakietu: ")
        if not pakiet:
            raise ValueError("Nazwa pakietu nie może być pusta.")
        
        os.system(f"sudo apt install {pakiet}")
        
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def inna_komenda(komenda):
    print()
    try:
        subprocess.run(komenda, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Wystąpił błąd podczas wykonywania komendy: {e}")

def altor():
	print("\nAłtorem jest: Kmarz23/KmarzPL\n")

def kp():
    sciezka1 = input("Podaj ścieżkę do kopiowania pliku: ")
    sciezka2 = input("Podaj ścieżkę do wklejenia pliku: ")
    try:
        os.system(f"cp {sciezka1} {sciezka2}")
    except Exception as e:
        print(f"Wystąpił błąd {e}")

# Dodaj więcej funkcji obsługujących inne polecenia

def main():
    print("Witaj w polskiej nakładce dla dystrybucji GNU/Linux!")
    print("Wersja:", wersja, "\n")
    print(f"Aby uzyskać listę komend wpisz 'pomoc'\n")

    while True:
        sciezka = os.getcwd()
        komenda = input(f"{sciezka} $ ").lower()

        if komenda == 'pomoc':
            polecenie_pomoc()
        elif komenda == 'lp':
            polecenie_lista_plikow()
        elif komenda == 'zk':
            zmien_katalog()
        elif komenda == 'wersja':
        	fwersja()
        elif komenda == 'pp instaluj':
        	pp_i()
        elif komenda == 'altor':
        	altor()
	elif komenda == 'kp':
		kp()
        # Dodaj więcej warunków dla innych poleceń
        elif komenda == 'wyjscie':
            print("Do widzenia!")
            break
        elif komenda != '':
        	inna_komenda(komenda)
        else:
            print("Nieznane polecenie. Wprowadź 'pomoc' dla pomocy.")

if __name__ == "__main__":
    main()
