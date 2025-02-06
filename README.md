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

1. **Ouvrir 4 terminaux dans n'importe quel ordre, lancez `coordinator.py` `priority_traffic_gen` `light.py`  et `display.py` 


2. Vous pouvez également lancer le programme **`normal_traffic_gen`** dans un autre terminal pour simuler un trafic normal.

4. Une fois tous les programmes lancés, le système commencera à simuler les véhicules et leurs interactions à l'intersection.

### Fermeture des programmes :

- **Pour arrêter tous les programmes**,  appuyez sur la touche `Q` dans le terminal de `display`.

Si il y a des erreurs ou lancement lié à des fichier/pipes/queues mal supprimer, lancer le fichier .sh
