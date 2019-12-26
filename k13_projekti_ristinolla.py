# TIE-02101 Johdatus ohjelmointiin
# Samuli Petäjistö, samuli.petajisto@tuni.fi, opiskelijanumero: 287071
# Tehtävä 13.11. käyttöliittymä projekti: Samuli TicTacToe

# Ohjelman laajuus: skaalautuva

# Käyttöohje:
# Ristinollan ideana on, että kaksi pelaajaa laittavat vuorotellen pelilaudalle
# ristin tai nollan. Ensimmäinen pelaaja joka saa vaakatasossa,
# pystytasossa tai vinottain pelin asetuksissa määritellyn sarjan voittaa.
# Pelaajat aloittavat vuorotellen jokaisen erän, jolloin
# aloittavan pelaajan etu tasaantuu. Peli pitää kirjaa voittojen lukumäärästä.
# Pelilauta on skaalautuva eli pelin asetusmuuttujista voi vaihtaa pelilaudan
# koon. Suositeltava koko on 3 - 8 riippuen näytön koosta. Peli kertoo
# Pelaajille kumman vuoro on ja ilmoittaa kumpi voitti pelin tai pelilaudan
# ollessa täynnä tasapelin. Kun peli päättyy joko voittoon tai tasapeliin
# Laudalle ei voi enää lisätä merkkejä. Uusi erä käynnistuu uusi peli nappu-
# lasta

from tkinter import *

# Pelin käyttämien kuvatiedostojen nimet
GAME_ASSETS = ["tyhjä.gif", "nolla.gif", "risti.gif"]

#
#
#
#
# ####### MUUTETTAVAT ASETUKSET ##########################

# MUUTA PELILAUDAN KOKOA
BOARD_SIZE = 6
# MUUTA VOITTOON VAADITTAVAN SUORAN MÄÄRÄ
STREAK_FOR_WIN = 4

#########################################################
#
#
#
#

# ÄLÄ MUUTA
P1_MARK = "o"
P2_MARK = "x"
EMPTY_MARK = "-"
STATE_GAME_RUNNING = 0
STATE_P1_WON = 1
STATE_P2_WON = 2
STATE_STALEMATE = 3

# DEBUG, MUUTA TULSOTETAANKO PELILAUTA KONSOLIIN SIIRTOJEN VÄLISSÄ
tulosta_lista_konsoliin = True

class TicTacToe:
    def __init__(self):
        """ Rakentaja
        Alustetaan muuttujat
        :return None.
        """
        self.__game_window = Tk()

        # Päivitetään ikkunan otsikko
        self.__game_window.title("Samuli TicTacToe")

        # Estetään ikkunan suurentaminen
        # self.__game_window.resizable(0, 0)

        # Alustetaan pelin kuvalista
        self.__game_images = []

        # Tallennetaan pelilaudan nappulat listaan
        self.__board_buttons = []

        # Pelaajan 1 tai 2 vuoro ja aloittavan vuoro
        self.__turn = 1
        self.__starting_player = 1

        # Pidetään yllä siirtojen lukumäärä tasapelitarkastelua varten
        self.__turns_played = 0

        # Pistelasku molemmalle pelaajalle
        self.__p1_score = 0
        self.__p2_score = 0

        # Luodaan lista kuvaamaan pelilautaa
        self.__board_list = []

        # Pelin tila.
        self._game_state = STATE_GAME_RUNNING

        # Luodaan pelin hallintaan liittyvät nappulat ja tekstit
        self.__new_game_button = Button(self.__game_window, text="Uusi peli",
                                        command=self.init_gameboard)
        self.__new_game_button.grid(row=0, column=0)

        # Kertoo vuoron ja pelin tilan
        self.__info_label = Label(self.__game_window, text="Pelajaan O vuoro", bg="white")
        self.__info_label.grid(row=0, column=1)

        # Pelaajan 1 puolta indikoiva teksti
        self.__p1_label = Label(self.__game_window, text="Pelajaa O")
        self.__p1_label.grid(row=1, column=0)

        # Pelaajan 2 puolta indikoiva teksti
        self.__p2_label = Label(self.__game_window, text="Pelajaa X")
        self.__p2_label.grid(row=1, column=2)

        # Pelin pistetilannetta indikoiva teksti
        self.__score_label = Label(self.__game_window, text=" 0 - 0 ")
        self.__score_label.grid(row=1, column=1)

        # Kuinka pitkällä suoralla voittaa
        self.__streak_label = Label(self.__game_window, text=str(STREAK_FOR_WIN) + " merkin sarjalla voittaa")
        self.__streak_label.grid(row=0, column=2)

        # Tallennetaan pelin kuvat listaan
        for game_image in GAME_ASSETS:
            img = PhotoImage(file=game_image)
            self.__game_images.append(img)

        # Alustetaan peli
        self.init_gameboard()

    def button_press(self, x, y, button):
        """ Käsittelee pelaajan painalluksen pelilaudan nappuloilla
        :param: x: int, painetun nappulan x-koordinaatti nappulalistassa
        :param: y: int, painetun nappulan y-koordinaatti nappulalistassa
        :param: button: Button, painettu nappula

        :return None
        """
        # Jos peli on käynnissä
        if self._game_state == STATE_GAME_RUNNING:
            print("pressed", "x:", x, "y:", y)

            # Tarkistetaan pystytäänkö merkkiä laittamaan
            if self.__turn == 1:
                if self.__board_list[y][x] == EMPTY_MARK:
                    self.__board_list[y][x] = P1_MARK
                    button.configure(image=self.__game_images[1])
                    self.update_turn(x, y)
            elif self.__turn == 2:
                if self.__board_list[y][x] == EMPTY_MARK:
                    self.__board_list[y][x] = P2_MARK
                    button.configure(image=self.__game_images[2])
                    self.update_turn(x, y)

            # Tulostetaan pelilaudan lista konsoliin
            if tulosta_lista_konsoliin:
                self.print_gameboard_list()

    def init_gameboard(self):
        """ Alustaa pelilaudan alkutilaan ohjelman avaamisen ja
         uorojen jälkeen
        :param: None

        :return None
        """
        self._game_state = STATE_GAME_RUNNING
        self.__board_list = []
        self.__turn = self.__starting_player
        self.__turns_played = 0
        self.__score_label.configure(text=str(self.__p1_score) +
                                                            " - " +
                                                            str(self.__p2_score))
        # Päivitetään vuoron ilmaisin
        if self.__starting_player == 1:
            self.__info_label.configure(text="Pelajaan O vuoro", bg="white")
        else:
            self.__info_label.configure(text="Pelajaan X vuoro", bg="white")

        # Alustetaan pelilauta tyhjillä ruudukoilla
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                new_button = Button(self.__game_window)
                new_button.configure(image=self.__game_images[0])
                new_button.configure(command=lambda x=x, y=y, button=new_button: self.button_press(x, y, button))
                new_button.grid(row=y + 2, column=x, sticky=W + E + N + S)

                self.__board_buttons.append(new_button)

        # Alustetaan pelilautalista tyhjillä merkeillä
        for x in range(BOARD_SIZE):
            temp_list = []
            for y in range(BOARD_SIZE):
                temp_list.append(EMPTY_MARK)
            self.__board_list.append(temp_list)

        self.print_gameboard_list()

        # Vaihdetaan aloittava pelaaja aina joka vuorolle
        if self.__starting_player == 1:
            self.__starting_player = 2
        else:
            self.__starting_player = 1

    def update_turn(self, last_x, last_y):
        """ Jokaisen merkinlaiton jälkeen suorittaa tarkastukset. Siirron
        jälkeen tarkastetaan vaakarivi, pystyrivi ja vinottaiset rivit. Mikäli
        ei ole voittajaa ja lauta ei ole täynnä, päivittää vuoron seuraavalle
        pelaajalle.
        :param: last_x: int, viimeksi painetun nappulan x-koordinaatti
        :param: last_y: int, viimeksi painetun nappulan y-koordinaatti

        :return None
        """

        # Päivitetään pelattujen vuorojen määrä
        self.__turns_played += 1

        # Tarkastetaan vuoron jälkeen onko voittajia, pelaaja 1
        if self.__turn == 1:
            # Tallennetaan pisin suora
            streak = 0

            # Tarkastetaan pelatun merkin vaakarivi
            for x in range(0, BOARD_SIZE):
                if self.__board_list[last_y][x] == P1_MARK:
                    streak += 1
                else:
                    streak = 0
                # Jos sarja ylittää voittoon vaadittavan määrän julistetaan
                # voittaja ja keskeytetään vuoron päivitys
                if streak == STREAK_FOR_WIN:
                    self.set_game_state(STATE_P1_WON)
                    return

            streak = 0

            # Tarkastetaan pelatun merkin pystyrivi
            for y in range(0, BOARD_SIZE):
                if self.__board_list[y][last_x] == P1_MARK:
                    streak += 1
                else:
                    streak = 0
                if streak == STREAK_FOR_WIN:
                    self.set_game_state(STATE_P1_WON)
                    return

            streak = 0

            # Tarkastetaan vinottaiset rivit, suunta 1, ylhäältä alas
            for y in range(0, BOARD_SIZE):
                streak = 0
                for x in range(0, y + 1):
                    if self.__board_list[y-x][x] == P1_MARK:
                        streak += 1
                    else:
                        streak = 0
                    if streak == STREAK_FOR_WIN:
                        self.set_game_state(STATE_P1_WON)
                        return

            streak = 0

            # Tarkastetaan vinottaiset rivit, suunta 1, vasemmalta oikealle
            for x in range(0, BOARD_SIZE):
                streak = 0
                for y in range(BOARD_SIZE - 1, x, -1):
                    if self.__board_list[y][x - y] == P1_MARK:
                        streak += 1
                    else:
                        streak = 0
                    if streak == STREAK_FOR_WIN:
                        self.set_game_state(STATE_P1_WON)
                        return

            streak = 0

            # Tarkastetaan vinottaiset rivit, suunta 2, ylhäältä alas
            for y in range(0, BOARD_SIZE):
                streak = 0
                for x in range(BOARD_SIZE - 1, BOARD_SIZE - (y + 2), -1):
                    if self.__board_list[ y - BOARD_SIZE+1+x][x] == P1_MARK:
                        streak += 1
                    else:
                        streak = 0
                    if streak == STREAK_FOR_WIN:
                        self.set_game_state(STATE_P1_WON)
                        return

            streak = 0

            # Tarkastetaan vinottaiset rivit, suunta 2, oikealta vasemmalle
            for x in range(BOARD_SIZE - 1, 0, -1):
                streak = 0
                for y in range(BOARD_SIZE - 1, BOARD_SIZE - (x + 2), -1):
                    if self.__board_list[y][x - BOARD_SIZE+1+y] == P1_MARK:
                        streak += 1
                    else:
                        streak = 0
                    if streak == STREAK_FOR_WIN:
                        self.set_game_state(STATE_P1_WON)
                        return
            streak = 0

        # Pelaaja 2
        elif self.__turn == 2:

            # Tallennetaan pisin suora
            streak = 0

            # Tarkastetaan pelatun merkin vaakarivi
            for x in range(0, BOARD_SIZE):
                if self.__board_list[last_y][x] == P2_MARK:
                    streak += 1
                else:
                    streak = 0
                if streak == STREAK_FOR_WIN:
                    self.set_game_state(STATE_P2_WON)
                    return

            streak = 0

            # Tarkastetaan pelatun merkin pystyrivi
            for y in range(0, BOARD_SIZE):
                if self.__board_list[y][last_x] == P2_MARK:
                    streak += 1
                else:
                    streak = 0
                if streak == STREAK_FOR_WIN:
                    self.set_game_state(STATE_P2_WON)
                    return

            streak = 0

            # Tarkastetaan vinottaiset rivit, suunta 1, ylhäältä alas
            for y in range(0, BOARD_SIZE):
                streak = 0
                for x in range(0, y + 1):
                    if self.__board_list[y-x][x] == P2_MARK:
                        streak += 1
                    else:
                        streak = 0
                    if streak == STREAK_FOR_WIN:
                        self.set_game_state(STATE_P2_WON)
                        return

            streak = 0

            # Tarkastetaan vinottaiset rivit, suunta 1, vasemmalta oikealle
            for x in range(0, BOARD_SIZE):
                streak = 0
                for y in range(BOARD_SIZE - 1, x, -1):
                    if self.__board_list[y][x - y] == P2_MARK:
                        streak += 1
                    else:
                        streak = 0
                    if streak == STREAK_FOR_WIN:
                        self.set_game_state(STATE_P2_WON)
                        return

            streak = 0

            # Tarkastetaan vinottaiset rivit, suunta 2, ylhäältä alas
            for y in range(0, BOARD_SIZE):
                streak = 0
                for x in range(BOARD_SIZE - 1, BOARD_SIZE - (y + 2), -1):
                    if self.__board_list[y - BOARD_SIZE+1+x][x] == P2_MARK:
                        streak += 1
                    else:
                        streak = 0
                    if streak == STREAK_FOR_WIN:
                        self.set_game_state(STATE_P2_WON)
                        return

            streak = 0

            # Tarkastetaan vinottaiset rivit, suunta 2, oikealta vasemmalle
            for x in range(BOARD_SIZE - 1, 0, -1):
                streak = 0
                for y in range(BOARD_SIZE - 1, BOARD_SIZE - (x + 2), -1):
                    if self.__board_list[y][x - BOARD_SIZE+1+y] == P2_MARK:
                        streak += 1
                    else:
                        streak = 0
                    if streak == STREAK_FOR_WIN:
                        self.set_game_state(STATE_P2_WON)
                        return
            streak = 0

        # Tarkastetaan onko tasapeli
        if self.__turns_played == BOARD_SIZE * BOARD_SIZE:
            self.set_game_state(STATE_STALEMATE)
            return

        # Kaikki tarkastukset tehty ja peli jatkuu. Vaihdetaan vuoroa
        # Ja päivitetään infoteksti
        if self.__turn == 1:
            self.__turn = 2
            self.__info_label.configure(text="Pelaajan X vuoro")
        else:
            self.__turn = 1
            self.__info_label.configure(text="Pelaajan O vuoro")

    def set_game_state(self, state):
        """ Asetettaa pelin tilan ja päivittää käyttöliittymän tekstit sen
        mukaisesti. Tilat joko "pelaajan 1 voitto", "pelaajan 2 voitto" tai
        "tasapeli"
        :param: state: int, tila johon peli asetetaan. Käytetään muttumattomia
        muuttujia ilmaisemaan pelin tilaa

        :return None
        """
        if state == STATE_P1_WON:
            self._game_state = STATE_P1_WON
            self.__info_label.configure(text="PELAAJA O VOITTI!")
            self.__info_label.configure(bg="green")
            self.__p1_score += 1
        elif state == STATE_P2_WON:
            self._game_state = STATE_P2_WON
            self.__info_label.configure(text="PELAAJA X VOITTI!")
            self.__info_label.configure(bg="green")
            self.__p2_score += 1
        elif state == STATE_STALEMATE:
            self._game_state = STATE_STALEMATE
            self.__info_label.configure(text="TASAPELI")
            self.__info_label.configure(bg="yellow")

    def new_game(self):
        """  Kutsuu ohjelman alussa alustusfunktion ja peli alkaa
        :return None
        """
        self.init_gameboard()

    def start(self):
        """ Käynnistää peli-ikkunan
        :return None
        """
        self.__game_window.mainloop()

    def quit(self):
        """ Sulkee peli-ikkunan
        :return None
        """
        self.__game_window.destroy()

    def print_gameboard_list(self):
        """ Apufunktio, joka tulostaa pelattuja merkkejä ylläpitävän listan
        :return None
        """
        for row in self.__board_list:
            print(row)

def main():
    """ Ohjelman pääfunktio, joka käynnistää ikkunan
    :return None
    """

    gameui = TicTacToe()
    gameui.start()

main()