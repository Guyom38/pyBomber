import moteur as CM
#import wss as WSS

import asyncio
import websockets
import json

class webSocket():  
    async def tache1_socket( actions_websocket):   
        print("     + Initialisation Tache Socket :")  
        async with websockets.connect("wss://ws.ladnet.net") as websocket: #, extra_headers={'http_proxy_host': "haproxy", 'http_proxy_port': 3128}
            print("         + boucle thread websocket")
            while True:
                message = await websocket.recv()
                donnees = json.loads(message)
                await actions_websocket.put(donnees)
                
                print(str(donnees))
        
async def tache2(actions_websocket):
    print("     + Initialisation Tache JEU :")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, tache2_jeu, actions_websocket)        
                    
def tache2_jeu(actions_websocket):
    print("+ Démarrage du moteur Bomberman")
    MOTEUR = CM.CMoteur(actions_websocket)
    MOTEUR.Demarrer()

async def main():
    print("Initialisation des taches :")
    actions_websocket = asyncio.Queue()
    
    await asyncio.gather(
        webSocket.tache1_socket(actions_websocket),
        tache2(actions_websocket)
    )    
       
asyncio.run(main())

