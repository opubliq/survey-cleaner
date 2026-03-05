# Onboarding Alexandre — guide Hubert

**Objectif**: Alexandre peut lancer `transform-codebook` sur des sondages depuis son Windows.  
**Format**: screen share — Hubert suit cette liste et dit à Alexandre quoi faire.

---

## 1. Prérequis (vérifier avant de commencer)

- [ ] Python installé et dans le PATH (`python --version` dans Git Bash)
- [ ] Git for Windows installé — inclut Git Bash ([git-scm.com](https://git-scm.com))
- [ ] Google Drive for Desktop installé et connecté au compte partagé

> On utilise **Git Bash** comme terminal (pas PowerShell, pas WSL). Ouvrir Git Bash pour toutes les commandes qui suivent.

---

## 2. Checkout la bonne branche

Le repo est déjà cloné. Se mettre sur la bonne branche:

```bash
cd ~/survey-cleaner
git fetch
git checkout feature/survey-cleaner-v2-evolve
git pull
```

---

## 3. Python + venv

Dans Git Bash :

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

> Pour vérifier que le venv est actif: `which python` doit retourner `.../survey-cleaner/venv/Scripts/python`.  
> Toujours réactiver avec `source venv/Scripts/activate` en début de session.

---

## 4. Trouver le chemin du shared folder dans Git Bash

Google Drive for Desktop monte le drive sur une lettre Windows (ex: `G:`), accessible dans Git Bash via `/g/`.

```bash
# Trouver le bon chemin:
ls /g/                    # si le drive est sur G:
ls /h/                    # ou H:, etc.
# Chercher le dossier _SharedFolder_data_produit
```

Une fois trouvé, noter le chemin — ex: `/g/_SharedFolder_data_produit`.

---

## 5. Créer le `.env`

```bash
# À la racine du repo (ou ouvrir .env dans n'importe quel éditeur de texte):
notepad .env
```

Contenu:

```
SHARED_FOLDER_PATH=/g/_SharedFolder_data_produit
```

Adapter le chemin selon ce qui a été trouvé à l'étape 4.

---

## 6. Adapter `.opencode.json`

Ce fichier donne à l'agent la permission de lire le shared folder (qui est hors du repo).  
Remplacer le chemin existant par le chemin trouvé à l'étape 4:

```bash
notepad .opencode.json
```

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "external_directory": {
      "/g/_SharedFolder_data_produit/*": "allow",
      "/g/_SharedFolder_data_produit/*/*": "allow",
      "/g/_SharedFolder_data_produit/*/*/*": "allow"
    }
  }
}
```

---

## 7. Installer opencode

```bash
curl -fsSL https://opencode.ai/install | bash
opencode --version    # doit afficher 1.2.x
```

**Clés API** — Hubert envoie `auth.json` par message, Alexandre le copie:

```bash
mkdir -p ~/.local/share/opencode
cp /chemin/vers/auth.json ~/.local/share/opencode/auth.json
```

> Dans Git Bash, `~` correspond à `C:/Users/tonnom`. Le dossier `.local/share/opencode` sera créé là.

**Modèles favoris** — ouvrir opencode depuis la racine du repo:

```bash
opencode
```

Dans le sélecteur de modèles, Ctrl+F sur chaque modèle de la liste dictée par Hubert.

---

## 8. Test de sanité

```bash
opencode --version                               # 1.2.x
echo $SHARED_FOLDER_PATH                         # doit afficher le chemin
ls "$SHARED_FOLDER_PATH/cecd_charte_2013_09/"   # doit lister data + codebook
venv/Scripts/python --version                    # doit afficher Python 3.x
```

Si les 4 passent → prêt.

---

## 9. Lancer transform-codebook

```bash
opencode prompt --model opencode/glm-5-free "transform codebook for cecd_charte_2013_09"
```

**Vérifier:**

```bash
cat "$SHARED_FOLDER_PATH/cecd_charte_2013_09/codebook.json" | head -30
```

Doit afficher du JSON avec `"survey_id"` et `"variables"`.

**Fallback si glm-5-free échoue:**

```bash
opencode prompt --model opencode/kimi-k2.5 "transform codebook for cecd_charte_2013_09"
```

---

## Référence rapide

```bash
source venv/Scripts/activate                     # toujours activer le venv en début de session
opencode prompt --model opencode/glm-5-free "transform codebook for {survey_id}"
cat "$SHARED_FOLDER_PATH/{survey_id}/codebook.json" | head -30
```

**Fichiers clés:**

```
~/.local/share/opencode/auth.json   ← clés API providers
.env                                ← SHARED_FOLDER_PATH
.opencode.json                      ← permissions agent (chemin shared folder)
venv/                               ← toujours utiliser venv/Scripts/python
.opencode/agents/transform-codebook.md  ← définition de l'agent (ne pas modifier)
```
