class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = int(superficie)
        self.padiglione = padiglione
        self.prezzo_base = float(prezzo_base)
        self.espositore = None

    def prezzo_finale(self):
        return self.prezzo_base

    def __lt__(self, other):
        return self.prezzo_finale() < other.prezzo_finale()

    def __str__(self):
        if self.espositore is None:
            stato = "Disponibile"
        else:
            stato = f"Assegnato a {self.espositore.codice}"

        return f"{self.codice} (Standard): {self.superficie}mq - Pad {self.padiglione} - {self.prezzo_finale():.2f}€ - {stato}"


class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.numero_prese = int(numero_prese)

    def prezzo_finale(self):

        aumento = self.prezzo_base * 0.07 * self.numero_prese
        return self.prezzo_base + aumento

    def __str__(self):
        if self.espositore is None:
            stato = "Disponibile"
        else:
            stato = f"Assegnato a {self.espositore.codice}"

        return f"{self.codice} (Extra): {self.superficie}mq - Pad {self.padiglione} - {self.prezzo_finale():.2f}€ - {self.numero_prese} prese - {stato}"


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def prezzo_finale(self):

        return self.prezzo_base * 1.30

    def __str__(self):
        if self.espositore is None:
            stato = "Disponibile"
        else:
            stato = f"Assegnato a {self.espositore.codice}"

        return f"{self.codice} (Premium): {self.superficie}mq - Pad {self.padiglione} - {self.prezzo_finale():.2f}€ - {self.posizione} - {stato}"


class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __str__(self):
        if self.stand is None:
            return f"{self.codice}: {self.nome} {self.cognome} - Nessuno stand"
        else:
            return f"{self.codice}: {self.nome} {self.cognome} - Stand {self.stand.codice}"


class LingottoFiere:
    def __init__(self, nome):
        self.nome = nome
        self.stands = []
        self.espositori = []

    def carica_file_dati(self, file_path):

        with open(file_path, "r") as file:
            linee = file.readlines()

            for riga in linee:
                riga = riga.strip()
                if len(riga) > 0:
                    dati = riga.split(",")
                    codice = dati[0]

                    if "ST" in codice:
                        superficie = dati[1]
                        padiglione = dati[2]
                        prezzo = dati[3]

                        if len(dati) == 4:
                            s = Stand(codice, superficie, padiglione, prezzo)
                            self.stands.append(s)
                        elif len(dati) == 5:
                            extra = dati[4]
                            if extra.isdigit():
                                s = StandPreseExtra(codice, superficie, padiglione, prezzo, extra)
                                self.stands.append(s)
                            else:
                                s = StandPremium(codice, superficie, padiglione, prezzo, extra)
                                self.stands.append(s)

                    elif "ES" in codice:
                        nome = dati[1]
                        cognome = dati[2]
                        e = Espositore(codice, nome, cognome)
                        self.espositori.append(e)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        stand_trovato = None
        espositore_trovato = None


        for s in self.stands:
            if s.codice == codice_stand:
                stand_trovato = s


        for e in self.espositori:
            if e.codice == codice_espositore:
                espositore_trovato = e


        if stand_trovato is None:
            raise Exception("Stand non trovato.")
        if espositore_trovato is None:
            raise Exception("Espositore non trovato.")
        if stand_trovato.espositore is not None:
            raise Exception("Lo stand è già stato assegnato.")
        if espositore_trovato.stand is not None:
            raise Exception("L'espositore ha già uno stand.")

        stand_trovato.espositore = espositore_trovato
        espositore_trovato.stand = stand_trovato

    def elenca_espositori(self):
        for e in self.espositori:
            print(e)

    def stand_ordinati_per_prezzo(self):
        copia_stands = list(self.stands)
        copia_stands.sort()
        return copia_stands