from threading import Thread
from tkinter import StringVar
from os import remove
from gtts import gTTS
from random import shuffle
from playsound import playsound
from pyautogui import sleep


class Bingo:

    def __init__(self, qtd_numeros=90):
        self.numeros = list(range(1, qtd_numeros+1))
        shuffle(self.numeros)
        self.sorteados = []
        self.pausado = False
        self.finalizado = False
        self.observador_externo = None

    def mostra_sorteados(self):
        print()
        print("Números sorteados até o momento: ")
        print(*self.sorteados, sep='  ')
        print()

    def restam_numeros(self):
        return len(self.numeros) > 0

    def proximo_numero(self):
        if self.restam_numeros():
            sorteado = self.numeros.pop()
            self.sorteados.append(sorteado)
            return sorteado
        else:
            return None

    def finalizar(self):
        self.finalizado = True
        exit()

    def pausar(self):
        self.pausado = True

    def continuar(self):
        self.pausado = False

    def esta_pausado(self):
        return self.pausado

    def foi_finalizado(self):
        return self.finalizado

    def play_pause(self):
        if self.esta_pausado():
            self.continuar()
        else:
            self.pausar()

    def adicionar_observador_externo(self, observador):
        self.observador_externo = observador

    def reportar_ao_observador(self):
        if self.observador_externo is not None:
            self.observador_externo.set(self.ultimo_sorteado())

    def realizar_sorteio(self):
        Locutor.falar('Atenção o show vai começar! Cartela na mão.')
        playsound('countdown.wav')
        while not self.foi_finalizado() and self.restam_numeros():
            numero = self.proximo_numero()
            self.reportar_ao_observador()
            Locutor.falar_numero(numero)
            sleep(5)
            if self.esta_pausado():
                playsound('sirene.mp3')
                Locutor.falar("Alguém disse: ")
                playsound('bingo.mp3')
                Locutor.falar("Vamos conferir!")
                self.mostra_sorteados()
                while self.esta_pausado() and not self.foi_finalizado():
                    sleep(1)
        Locutor.falar("Jogo encerrado, parabéns ao vencedor!")
        playsound('palmas.wav')
        return

    def ultimo_sorteado(self):
        if len(self.sorteados) > 0:
            return str(self.sorteados[-1])
        else:
            return 'Ops!'

    def run(self):
        t = Thread(target=self.realizar_sorteio)
        t.start()


class Locutor:

    frases = {1: 'começou o jogo',
              5: 'cachorro',
              10: 'craque de bola',
              22: 'dois pattinhos na lagoa!',
              31: 'preparem os fogos',
              33: 'idade de cristo',
              45: 'fim do primeiro tempo',
              51: 'uma boa ideia',
              71: 'dona clotilde, é a senhora?',
              90: 'fim de jogo',
              }

    def falar(texto):
        if type(texto) != str:
            texto = str(texto)
        audio = gTTS(texto, lang='pt', slow=False)
        audio.save('fala.mp3')
        playsound('fala.mp3')
        remove('fala.mp3')

    def fazer_graca(numero):
        if numero in Locutor.frases.keys():
            Locutor.falar(Locutor.frases[numero])

    def falar_numero(numero):
        Locutor.falar(numero)
        Locutor.fazer_graca(numero)
