import requests
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

console = Console()

def get_public_ip():
    """
    Récupère l'adresse IP publique actuelle
    """
    try:
        # Utilise un service pour obtenir l'IP publique
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json()['ip']
    except requests.RequestException as e:
        console.print(f"[yellow]⚠ Échec du service principal, tentative avec le service de secours...[/yellow]")
        # Service alternatif en cas d'échec
        try:
            response = requests.get('https://ifconfig.me/ip', timeout=5)
            return response.text.strip()
        except:
            return None

def update_dynhost(username, password, hostname, ip=None):
    """
    Met à jour un enregistrement DynHost OVH
    
    :param username: Identifiant DynHost (ex: mondomaine.com-monhost)
    :param password: Mot de passe DynHost
    :param hostname: Nom d'hôte complet (ex: monhost.mondomaine.com)
    :param ip: IP à définir (optionnel, détection auto si None)
    :return: Tuple (succès, message)
    """
    # Si aucune IP n'est fournie, on détecte l'IP actuelle
    if ip is None:
        ip = get_public_ip()
        if ip is None:
            return False, "Impossible de détecter l'IP publique"
        console.print(f"[cyan]🌐 IP publique détectée : [bold]{ip}[/bold][/cyan]")
    
    url = "https://www.ovh.com/nic/update"
    
    params = {
        'system': 'dyndns',
        'hostname': hostname,
        'myip': ip
    }
    
    try:
        response = requests.get(url, params=params, auth=(username, password), timeout=10)
        response.raise_for_status()
        
        result = response.text.strip()
        
        # Interprétation des codes de retour OVH
        if result.startswith('good'):
            return True, f"✓ Mise à jour réussie : {result}"
        elif result.startswith('nochg'):
            return True, f"✓ IP inchangée : {result}"
        else:
            return False, f"✗ Erreur de mise à jour : {result}"
            
    except requests.RequestException as e:
        return False, f"✗ Erreur de connexion : {e}"

def load_config():
    """
    Charge la configuration depuis le fichier .env
    """
    # Charge les variables d'environnement depuis le fichier .env
    load_dotenv()
    
    username = os.getenv('DYNHOST_USERNAME')
    password = os.getenv('DYNHOST_PASSWORD')
    hostname = os.getenv('DYNHOST_HOSTNAME')
    
    # Vérification que toutes les variables sont présentes
    if not all([username, password, hostname]):
        raise ValueError(
            "Configuration incomplète dans le fichier .env\n"
            "Vérifiez que DYNHOST_USERNAME, DYNHOST_PASSWORD et DYNHOST_HOSTNAME sont définis"
        )
    
    return username, password, hostname

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        # Charger la configuration
        username, password, hostname = load_config()

        console.print(Panel(
            f"[bold cyan]Hostname :[/bold cyan] {hostname}",
            title="[bold]🔧 Configuration OVH DynHost[/bold]",
            border_style="cyan"
        ))

        # Afficher l'IP actuelle
        current_ip = get_public_ip()
        if current_ip:
            console.print(f"[dim]Votre IP publique actuelle : {current_ip}[/dim]\n")

        # Mettre à jour le DynHost
        success, message = update_dynhost(username, password, hostname)

        if success:
            console.print(f"[green bold]{message}[/green bold]")
        else:
            console.print(f"[red bold]{message}[/red bold]")

    except ValueError as e:
        console.print(f"[red bold]❌ Erreur de configuration :[/red bold] {e}")
    except Exception as e:
        console.print(f"[red bold]❌ Erreur inattendue :[/red bold] {e}")