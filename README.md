# NYC PokeTracker

Tracker temps réel Pokémon GO NYC.

## Lancement local

```
python server.py
```
Puis ouvrir : http://localhost:8080/nyc-poketracker-pwa.html

## Hébergement gratuit sur Render.com

### 1. Créer un dépôt GitHub

1. Va sur https://github.com/new
2. Crée un repo **public** (ex: `poketracker-nyc`)
3. Upload ces 3 fichiers :
   - `nyc-poketracker-pwa.html`
   - `server.py`
   - `requirements.txt`

   Depuis PowerShell dans le dossier Downloads :
   ```
   git init
   git add nyc-poketracker-pwa.html server.py requirements.txt
   git commit -m "Initial commit"
   git remote add origin https://github.com/TON_USERNAME/poketracker-nyc.git
   git push -u origin main
   ```

### 2. Déployer sur Render

1. Va sur https://render.com → **Sign up** (gratuit, avec GitHub)
2. Clique **New +** → **Web Service**
3. Connecte ton repo GitHub `poketracker-nyc`
4. Configure :
   - **Name** : `poketracker-nyc` (ou ce que tu veux)
   - **Runtime** : `Python 3`
   - **Build Command** : *(laisser vide)*
   - **Start Command** : `python server.py`
   - **Instance Type** : `Free`
5. Clique **Create Web Service**

Render déploie en ~2 minutes et te donne une URL publique :
```
https://poketracker-nyc.onrender.com/nyc-poketracker-pwa.html
```

### ⚠️ Limitations du tier gratuit Render

- **Se met en veille** après 15 min d'inactivité (premier chargement ~30s)
- Pour éviter la veille : utilise https://uptimerobot.com (gratuit) pour pinger toutes les 5 min

### Alternative : Railway.app

1. Va sur https://railway.app → Sign up avec GitHub
2. **New Project** → **Deploy from GitHub repo**
3. Sélectionne ton repo
4. **Add variable** : `START_COMMAND = python server.py`
5. Railway détecte Python automatiquement

$5 de crédits gratuits/mois = environ 500h de runtime.
