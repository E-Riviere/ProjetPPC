# At the Crossroad

## Description

"At the Crossroad" est un projet de gestion de la circulation dans une intersection, conçu pour simuler le passage des véhicules prioritaires ou non.

## Prérequis

Le projet nécessite Python 3 et les bibliothèques suivantes :

- `socket`
- `time`
- `curses`
- `numpy`
- `os`
- `multiprocessing`
- `signal`
- `sysv_ipc`

## Lancement

### Étapes à suivre :

1. **Ouvrir trois terminaux dans n'importe quel ordre, lancez `coordinator.py` `priority_traffic_gen` `light.py` 


2. Vous pouvez également lancer le programme **`normal_traffic_gen`** dans un autre terminal pour simuler un trafic normal, ou **`display`** dans un autre terminal pour visualiser l'état de l'intersection.

4. Une fois tous les programmes lancés, le système commencera à simuler les véhicules et leurs interactions à l'intersection.

### Fermeture des programmes :

- **Pour arrêter tous les programmes**, envoyez un `CTRL-C` (SIGINT) dans le terminal où `coordinator` est exécuté.
- **Pour fermer uniquement `display`**, appuyez sur la touche `Q` dans le terminal de `display`.
