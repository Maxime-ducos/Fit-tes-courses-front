from google.cloud import storage
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Initialisation du client Google Cloud Storage
def initialize_storage_client():
    """
    Initialise et retourne un client Google Cloud Storage.
    Assurez-vous que la variable GOOGLE_APPLICATION_CREDENTIALS est configurée.
    """
    return storage.Client()

# Fonction pour uploader un fichier dans le bucket
def upload_file(bucket_name, local_file_path, destination_blob_name):
    """
    Upload un fichier local dans le bucket spécifié.
    Args:
        bucket_name (str): Nom du bucket.
        local_file_path (str): Chemin du fichier local à uploader.
        destination_blob_name (str): Nom du fichier dans le bucket.
    """
    client = initialize_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    print(f"Fichier {local_file_path} uploadé vers {bucket_name}/{destination_blob_name}.")

# Fonction pour télécharger un fichier depuis le bucket
def download_file(bucket_name, source_blob_name, destination_file_path):
    """
    Télécharge un fichier depuis le bucket vers un chemin local.
    Args:
        bucket_name (str): Nom du bucket.
        source_blob_name (str): Nom du fichier dans le bucket.
        destination_file_path (str): Chemin local pour sauvegarder le fichier.
    """
    client = initialize_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_path)
    print(f"Fichier {source_blob_name} téléchargé depuis {bucket_name} vers {destination_file_path}.")

# Fonction pour lister les fichiers dans le bucket
def list_files(bucket_name):
    """
    Liste tous les fichiers présents dans le bucket.
    Args:
        bucket_name (str): Nom du bucket.
    Returns:
        list: Une liste des noms des fichiers.
    """
    client = initialize_storage_client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    file_names = [blob.name for blob in blobs]
    print(f"Fichiers dans le bucket {bucket_name} : {file_names}")
    return file_names

# Fonction pour télécharger tous les fichiers d'un répertoire du bucket
def download_directory(bucket_name, source_directory, destination_directory):
    """
    Télécharge tous les fichiers d'un répertoire logique du bucket vers un répertoire local.
    Args:
        bucket_name (str): Nom du bucket.
        source_directory (str): Nom du répertoire dans le bucket.
        destination_directory (str): Chemin local pour sauvegarder les fichiers.
    """
    client = initialize_storage_client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=source_directory)

    for blob in blobs:
        local_path = f"{destination_directory}/{blob.name[len(source_directory):]}"
        blob.download_to_filename(local_path)
        print(f"Fichier {blob.name} téléchargé dans {local_path}.")


# Fonction pour uploader un répertoire entier vers le bucket
def upload_directory(bucket_name, local_directory, destination_directory):
    """
    Upload tous les fichiers d'un répertoire local vers un répertoire logique dans le bucket.
    Args:
        bucket_name (str): Nom du bucket.
        local_directory (str): Chemin du répertoire local.
        destination_directory (str): Nom du répertoire dans le bucket.
    """
    client = initialize_storage_client()
    bucket = client.bucket(bucket_name)

    for root, _, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)
            blob_name = os.path.join(destination_directory, os.path.relpath(local_path, local_directory))
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(local_path)
            print(f"Fichier {local_path} uploadé vers {bucket_name}/{blob_name}.")

# Fonction pour vérifier l'existence d'un fichier dans le bucket
def file_exists(bucket_name, blob_name):
    """
    Vérifie si un fichier existe dans le bucket.
    Args:
        bucket_name (str): Nom du bucket.
        blob_name (str): Nom du fichier dans le bucket.
    Returns:
        bool: True si le fichier existe, False sinon.
    """
    client = initialize_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    exists = blob.exists()
    print(f"Le fichier {blob_name} existe dans le bucket {bucket_name}: {exists}")
    return exists

# Fonction pour supprimer un fichier du bucket
def delete_file(bucket_name, blob_name):
    """
    Supprime un fichier dans le bucket.
    Args:
        bucket_name (str): Nom du bucket.
        blob_name (str): Nom du fichier dans le bucket à supprimer.
    """
    client = initialize_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    print(f"Fichier {blob_name} supprimé du bucket {bucket_name}.")
