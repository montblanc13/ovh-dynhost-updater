# OVH DynHost Updater

Un outil Python simple et élégant pour mettre à jour automatiquement vos enregistrements DNS DynHost OVH avec votre adresse IP publique actuelle.

## Fonctionnalités

- 🌐 Détection automatique de l'IP publique
- 🔄 Mise à jour automatique des enregistrements DynHost OVH
- 🎨 Interface en ligne de commande colorée avec Rich
- ⚡ Rapide et léger
- 🔒 Configuration sécurisée via fichier `.env`
- 🛡️ Gestion des erreurs avec services de secours

## Prérequis

- Python 3.12 ou supérieur
- [uv](https://github.com/astral-sh/uv) (gestionnaire de paquets Python)

## Installation

1. Clonez le dépôt :
```bash
git clone <url-du-repo>
cd ovh-dynhost-updater
```

2. Installez les dépendances :
```bash
uv sync
```

3. Créez un fichier `.env` à la racine du projet :
```bash
cp .env.example .env  # Si vous avez un exemple
# OU créez le fichier manuellement
```

4. Configurez vos identifiants DynHost dans le fichier `.env` :
```env
DYNHOST_USERNAME=votre-domaine.com-hostname
DYNHOST_PASSWORD=votre-mot-de-passe-dynhost
DYNHOST_HOSTNAME=hostname.votre-domaine.com
```

## Configuration OVH

Pour obtenir vos identifiants DynHost :

1. Connectez-vous à votre [espace client OVH](https://www.ovh.com/manager/)
2. Allez dans la section **Web Cloud** > **Noms de domaine**
3. Sélectionnez votre domaine
4. Allez dans l'onglet **DynHost**
5. Créez un identifiant DynHost si vous n'en avez pas
6. Notez le format de l'identifiant : `domaine.com-suffixe`

## Utilisation

Exécutez le script :
```bash
uv run main.py
```

Le script va :
1. Charger la configuration depuis `.env`
2. Détecter votre IP publique actuelle
3. Mettre à jour l'enregistrement DynHost sur OVH
4. Afficher le résultat avec des couleurs

### Exemple de sortie

```
╭─────────────────────────────────────────╮
│ 🔧 Configuration OVH DynHost            │
│ Hostname : subdomain.votredomaine.com   │
╰─────────────────────────────────────────╯

🌐 IP publique détectée : 203.0.113.42
✓ Mise à jour réussie : good 203.0.113.42
```

## Automatisation

### Cron (Linux/macOS)

Pour exécuter le script automatiquement toutes les 5 minutes :

```bash
*/5 * * * * cd /chemin/vers/ovh-dynhost-updater && /chemin/vers/uv run main.py >> /var/log/dynhost.log 2>&1
```

### Systemd Timer (Linux)

Créez un service et un timer systemd pour une meilleure gestion.

**Service** (`~/.config/systemd/user/ovh-dynhost.service`) :
```ini
[Unit]
Description=OVH DynHost Updater

[Service]
Type=oneshot
WorkingDirectory=/chemin/vers/ovh-dynhost-updater
ExecStart=/chemin/vers/uv run main.py
```

**Timer** (`~/.config/systemd/user/ovh-dynhost.timer`) :
```ini
[Unit]
Description=Run OVH DynHost Updater every 5 minutes

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
```

Activez le timer :
```bash
systemctl --user enable --now ovh-dynhost.timer
```

### Task Scheduler (Windows)

Utilisez le Planificateur de tâches Windows pour exécuter le script régulièrement.

## Codes de retour OVH

Le script interprète les codes de retour de l'API DynHost OVH :

| Code | Signification |
|------|---------------|
| `good [IP]` | Mise à jour réussie |
| `nochg [IP]` | IP inchangée, pas de mise à jour nécessaire |
| `badauth` | Identifiants incorrects |
| `notfqdn` | Hostname invalide |
| `nohost` | Hostname non configuré dans DynHost |
| `abuse` | Hostname bloqué pour abus |

## Dépendances

- [requests](https://requests.readthedocs.io/) - Pour les requêtes HTTP
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Pour la gestion des variables d'environnement
- [rich](https://rich.readthedocs.io/) - Pour l'affichage enrichi dans le terminal

## Sécurité

⚠️ **Important** :
- Ne commitez **jamais** votre fichier `.env` dans Git
- Le fichier `.env` est déjà dans `.gitignore`
- Gardez vos identifiants DynHost confidentiels

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

Ce projet est sous licence MIT.

## Support

En cas de problème :
1. Vérifiez que vos identifiants sont corrects dans `.env`
2. Vérifiez que le hostname est bien configuré dans votre espace client OVH
3. Consultez les logs pour plus de détails sur les erreurs

## Auteur

Créé avec ❤️ pour simplifier la gestion des DNS dynamiques OVH
