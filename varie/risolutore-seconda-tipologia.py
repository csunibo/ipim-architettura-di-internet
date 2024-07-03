#dati input 
print("INSERIMENTO DATI")
sst = int(input("sst: "))
n_segmenti = int(input("F segmenti: "))
pacchetti_persi = list(map(int, input("pacchetti persi (separati da virgola): ").split(',')))
print()


#inizializzazione variabili
cw = 1
round_counter = 0
fine = False #diventa true quando è terminato l'invio di pacchetti, interrompendo il ciclo
three_dup_ack = 0 #contatore ack duplicati
perdita = False #segnala se è stato perso un pacchetto, rimane True finchè il pacchetto non viene rinviato
timeout = False 
rinvio = 0
pacchetto = 1
riga = []


print("ROUND\tCW\tSST\tPACCHETTI\t\t\t\tEVENTI")

while not fine:

    round_counter += 1
    evento = ""
    
    for pacchetto in range (pacchetto, pacchetto + cw):
        riga.append(pacchetto)

        #perdita pacchetto
        if pacchetto in pacchetti_persi:
            evento += "p, "

            if not perdita:
                rinvio = pacchetto
                perdita = True

            pacchetti_persi.pop(0) #rimozione pacchetto già perso dalla lista

        #ricezione ack duplicato
        elif perdita:
            three_dup_ack += 1


        #invio ultimo pacchetto
        if pacchetto == n_segmenti:

            if not perdita: #termine connessione
                fine = True 
                evento += "TIMEOUT"

            elif three_dup_ack < 3: # se c'è perdita ma non 3DUPACK allora si verifica timeout
                timeout = True

            break


    print(f"{round_counter}\t{cw}\t{sst}\t{riga}", end="\t\t\t\t")

    if three_dup_ack >= 3 or timeout:
        sst = cw // 2

        if timeout:
            evento += "TIMEOUT"
            cw = 1
        else: 
            cw = sst
            evento += "3DUPACK"

        perdita, timeout = False, False
        three_dup_ack = 0
        pacchetto = rinvio

    else:
        pacchetto += 1

        #slow start
        if cw < sst:
            cw = cw * 2

        #congestion avoidance
        else:
            cw += 1

    print(f"{evento}")
    riga.clear()

    
