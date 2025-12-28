import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders, message_from_string
from email.header import decode_header
from email.utils import parsedate_to_datetime, parseaddr, formatdate, make_msgid
import json
import os
import threading
import datetime
import time
import shlex
import traceback
from html.parser import HTMLParser
import webbrowser
import tempfile
import re
import warnings
import urllib.request
import sys
import socket
import hashlib
import random
import string
import requests
import certifi
import base64

# --- SILENCIAR AVISOS ---
warnings.filterwarnings("ignore", category=UserWarning) 
try:
    from cryptography.utils import CryptographyDeprecationWarning
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
except ImportError: pass

# --- BIBLIOTECAS EXT ---
try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    import pgpy
    from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm
    HAS_PGP = True
except ImportError:
    HAS_PGP = False

# --- ÍCONES ---
try:
    import resources_icons
except ImportError:
    resources_icons = None

def get_icon(name):
    if resources_icons and name in resources_icons.icons:
        try: return tk.PhotoImage(data=resources_icons.icons[name])
        except Exception: return None
    return None

# --- CONSTANTES VISUAIS ---
BG_DARK = "#2b2b2b"       
BG_LIGHT = "#3c3f41"      
FG_WHITE = "#ffffff"      
ACCENT = "#4a88c7"        
BG_HEADER = "#323232"     
FG_DANGER = "#e74c3c"
FG_SAFE = "#2ecc71"
FG_WARN = "#f1c40f"

# --- FICHEIROS ---
FILES = {
    "profiles": "email_profiles.json",
    "servers": "known_servers.json",
    "contacts": "contacts.json",
    "settings": "app_settings.json",
    "pgp": "pgp_keys.json",
    "key": "secret.key",
    "cache": "email_cache.json"
}

# --- SISTEMA DE TRADUÇÃO COMPLETO ---
LANG_MAP = {
    "Português": "pt", "English": "en", "Español": "es", 
    "Français": "fr", "Deutsch": "de", "Italiano": "it", 
    "Русский": "ru", "中文": "zh"
}

FLAG_ICONS = {
    "pt": "flag_pt", "en": "flag_en", "es": "flag_es",
    "fr": "flag_fr", "de": "flag_de", "it": "flag_it",
    "ru": "flag_ru", "zh": "flag_zh"
}

T_DATA = {
    "pt": {
        "app_title": "CorreioPro Ultimate", "pgp_your_name": "Seu Nome (para a chave)", "multi_send_help": "Para múltiplos emails, separe por vírgula (ex: a@a.com, b@b.com)", "pgp_your_email": "Seu Email (associado à chave)",
         "pgp_passphrase": "Senha da Chave Privada", "login_title": "CORREIO PRO", "connect": "Entrar", "manage_profiles": "Perfis", "about": "Sobre", 
        "compose": " Escrever", "contacts": " Contactos", "pgp_keys": " Chaves PGP", "exit": " Sair", "reply": " Responder", "forward": " Encaminhar", 
        "forensic": " Forense", "save": " Guardar", "delete": " Apagar", "from": "De:", "subject": "Assunto:", "date": "Data", "ready": "Pronto", 
        "loading": "A carregar...", "loaded": "emails", "safe_view": " Ver Seguro", "full_view": " Ver Original", "decrypt_btn": " Desencriptar", 
        "auth_title": "Autenticação", "pass_ask": "Password para", "error": "Erro", "success": "Sucesso", "confirm": "Confirmar", "delete_confirm": "Apagar?", 
        "forensic_title": "Análise", "score": "Pontuação", "verdict": "Veredito", "safe": "CONFIÁVEL", "suspect": "SUSPEITO", "danger": "PERIGOSO", 
        "harvest_btn": " Varrer Enviados", "import_btn": " Importar vCard", "add": "Adicionar", "del_sel": "Apagar Selecionado", "name": "Nome", 
        "email": "Email", "preset": "Predefinição:", "edit": "Editar:", "save_btn": "Guardar", "ssl": "SSL", "save_pass": "Guardar Pass", 
        "signature": "Assinatura:", "to": "Para:", "attach": "Anexar", "send": "Enviar", "encrypt_pgp": " Encriptar PGP", "new_preset": "Novo Servidor", 
        "new_preset_btn": "Adicionar", "files": "ficheiros", "pass_help": "Ajuda Password", 
        "pass_help_text": "Se usa Gmail/Outlook com 2FA, tem de gerar uma 'App Password' (Senha de Aplicação) nas definições da sua conta.",
        "receipt": "Pedir Recibo de Leitura", "cached": " (Offline Cache)", "select_prof": "Selecione um perfil primeiro!",
        "prev": "<", "next": ">", "refresh_tip": "Atualizar Caixa", "show_pass": "Mostrar Password", "help_icon": "Ajuda", "analyze_file": "Analisar Ficheiro (.eml)",
        "wipe_btn": " DESTRUIR DADOS", "wipe_confirm": "ATENÇÃO:\n\nIsto irá sobrescrever e apagar TODAS as chaves, perfis e caches locais.\n\nEsta ação é IRREVERSÍVEL.\n\nContinuar?",
        "proxy_title": "Proxy / Tor", "search_lbl": "Procurar:", "proxy_enable": "Ativar SOCKS5 Proxy", "proxy_addr": "Endereço (ex: 127.0.0.1)", "proxy_port": "Porta (ex: 9050)",
        "sending": "A Enviar...", "wait": "Aguarde...",
        "pin_title": "PIN de Perfil", "pin_ask": "Este perfil está bloqueado.\nIntroduza o PIN:", "pin_wrong": "PIN Incorreto!",
        "burner_btn": "Email Temporário", "burner_win": "Email Temporário", "burner_win": "Identidade Descartável", "new_id": "Nova Identidade", "copy_id": "Copiar", "burner_copy": "Copiar Email", "stego_btn": "Esconder Segredo", "stego_found": "🔍 SEGREDO DETETADO"
    },
    "en": {
        "app_title": "CorreioPro Ultimate", "multi_send_help": "For multiple emails, separate with comma (ex: a@a.com, b@b.com)", "pgp_your_name": "Your Name (for the key)", "pgp_your_email": "Your Email (linked to the key)", "pgp_passphrase": "Private Key Passphrase", "login_title": "MAIL PRO", "connect": "Login", "manage_profiles": "Profiles", "about": "About", 
        "compose": " Compose", "contacts": " Contacts", "pgp_keys": " PGP Keys", "exit": " Logout", "reply": " Reply", "forward": " Forward", 
        "forensic": " Forensic", "save": " Save", "delete": " Delete", "from": "From:", "subject": "Subject:", "date": "Date", "ready": "Ready", 
        "loading": "Loading...", "loaded": "emails", "safe_view": " Safe View", "full_view": " Original View", "decrypt_btn": " Decrypt", 
        "auth_title": "Auth", "pass_ask": "Password for", "error": "Error", "success": "Success", "confirm": "Confirm", "delete_confirm": "Delete?", 
        "forensic_title": "Analysis", "score": "Score", "verdict": "Verdict", "safe": "TRUSTED", "suspect": "SUSPICIOUS", "danger": "DANGEROUS", 
        "harvest_btn": " Scan Sent", "import_btn": " Import vCard", "add": "Add", "del_sel": "Delete Selected", "name": "Name", 
        "email": "Email", "preset": "Preset:", "edit": "Edit:", "save_btn": "Save", "ssl": "SSL", "save_pass": "Save Pass", 
        "signature": "Signature:", "to": "To:", "attach": "Attach", "send": "Send", "encrypt_pgp": " Encrypt PGP", "new_preset": "New Server", 
        "new_preset_btn": "Add", "files": "files", "pass_help": "Password Help", 
        "pass_help_text": "If you use Gmail/Outlook with 2FA, you must generate an 'App Password' in your account settings.",
        "receipt": "Request Read Receipt", "cached": " (Offline Cache)", "select_prof": "Select a profile first!",
        "prev": "<", "next": ">", "refresh_tip": "Refresh Inbox", "show_pass": "Show Password", "help_icon": "Help", "analyze_file": "Analyze File (.eml)",
        "wipe_btn": " WIPE DATA", "wipe_confirm": "WARNING:\n\nThis will overwrite and delete ALL local keys, profiles, and caches.\n\nThis action is IRREVERSIBLE.\n\nProceed?",
        "proxy_title": "Proxy / Tor", "search_lbl": "Search:", "proxy_enable": "Enable SOCKS5 Proxy", "proxy_addr": "Address (ex: 127.0.0.1)", "proxy_port": "Port (ex: 9050)",
        "sending": "Sending...", "wait": "Please Wait...",
        "pin_title": "Profile PIN", "pin_ask": "This profile is locked.\nEnter PIN:", "pin_wrong": "Wrong PIN!",
        "burner_btn": "Temp Mail", "burner_win": "Temp Mail", "new_id": "New Identity", "copy_id": "Copy", "burner_title": "Disposable Identity", "burner_copy": "Copy Email", "stego_btn": "Hide Secret", "stego_found": "🔍 SECRET DETECTED"
    },
    # Other languages omitted for brevity
    "es": {"app_title": "CorreioPro Ultimate", "multi_send_help": "Para múltiples correos, separe con coma (ej: a@a.com, b@b.com)", "pgp_your_name": "Tu Nombre (para la clave)", "pgp_your_email": "Tu Email (asociado a la clave)", "login_title": "CORREO PRO", "pgp_passphrase": "Contraseña de la Clave Privada", "connect": "Entrar", "burner_win": "Identidad Descartable", "new_id": "Nueva Identidad", "copy_id": "Copiar", "manage_profiles": "Perfiles", "about": "Acerca", "compose": " Redactar", "contacts": " Contactos", "pgp_keys": " Claves PGP", "exit": " Salir", "reply": " Responder", "forward": " Reenviar", "forensic": " Forense", "save": " Guardar", "delete": " Borrar", "from": "De:", "subject": "Asunto:", "date": "Fecha", "ready": "Listo", "loading": "Cargando...", "loaded": "correos", "safe_view": " Vista Segura", "full_view": " Vista Original", "decrypt_btn": " Descifrar", "auth_title": "Autenticación", "pass_ask": "Clave para", "error": "Error", "success": "Éxito", "confirm": "Confirmar", "delete_confirm": "Borrar?", "forensic_title": "Análisis", "score": "Puntuación", "verdict": "Veredicto", "safe": "FIABLE", "suspect": "SOSPECHOSO", "danger": "PELIGROSO", "harvest_btn": " Escanear Enviados", "import_btn": " Importar vCard", "add": "Añadir", "del_sel": "Borrar", "name": "Nombre", "email": "Email", "preset": "Preajuste:", "edit": "Editar:", "save_btn": "Guardar", "ssl": "SSL", "save_pass": "Guardar Clave", "signature": "Firma:", "to": "Para:", "attach": "Adjuntar", "send": "Enviar", "encrypt_pgp": " Cifrar PGP", "new_preset": "Nuevo Servidor", "new_preset_btn": "Añadir", "files": "archivos", "pass_help": "Ayuda", "pass_help_text": "Si usa 2FA, genere una 'Contraseña de Aplicación' en su cuenta.", "receipt": "Solicitar confirmación de lectura", "cached": " (Caché Offline)", "select_prof": "¡Seleccione un perfil primero!", "prev": "<", "next": ">", "refresh_tip": "Actualizar", "show_pass": "Mostrar Clave", "help_icon": "Ayuda", "analyze_file": "Analizar Archivo (.eml)", "wipe_btn": " BORRAR DATOS", "wipe_confirm": "ADVERTENCIA:\n\nEsto sobrescribirá y eliminará TODAS las claves locales.\n\nAcción IRREVERSIBLE.\n\n¿Continuar?", "proxy_title": "Proxy / Tor", "search_lbl": "Buscar:", "proxy_enable": "Activar SOCKS5", "proxy_addr": "Dirección", "proxy_port": "Puerto", "sending": "Enviando...", "wait": "Espere...", "pin_title": "PIN de Perfil", "pin_ask": "Perfil bloqueado.\nIngrese PIN:", "pin_wrong": "PIN Incorrecto!", "burner_btn": "Generar Alias", "burner_title": "Identidad Descartable", "burner_copy": "Copiar Email", "stego_btn": "Ocultar Secreto", "stego_found": "🔍 SECRETO DETECTADO"},
    "fr": {"app_title": "CorreioPro Ultimate", "multi_send_help": "Pour plusieurs emails, séparez par une virgule (ex: a@a.com, b@b.com)", "pgp_your_name": "Votre Nom (pour la clé)", "pgp_your_email": "Votre E-mail (lié à la clé)", "pgp_passphrase": "Phrase de passe de la Clé Privée","login_title": "MAIL PRO", "connect": "Connexion", "burner_win": "Identité Jetable", "new_id": "Nouvelle Identité", "copy_id": "Copier", "manage_profiles": "Profils", "about": "Info", "compose": " Écrire", "contacts": " Contacts", "pgp_keys": " Clés PGP", "exit": " Quitter", "reply": " Répondre", "forward": " Transférer", "forensic": " Forensique", "save": " Sauver", "delete": " Supprimer", "from": "De:", "subject": "Sujet:", "date": "Date", "ready": "Prêt", "loading": "Chargement...", "loaded": "emails", "safe_view": " Vue Sûre", "full_view": " Vue Originale", "decrypt_btn": " Déchiffrer", "auth_title": "Authentification", "pass_ask": "Mot de passe pour", "error": "Erreur", "success": "Succès", "confirm": "Confirmer", "delete_confirm": "Supprimer?", "forensic_title": "Analyse", "score": "Score", "verdict": "Verdict", "safe": "FIABLE", "suspect": "SUSPECT", "danger": "DANGEREUX", "harvest_btn": " Scan Envoyés", "import_btn": " Importer vCard", "add": "Ajouter", "del_sel": "Supprimer", "name": "Nom", "email": "Email", "preset": "Preset:", "edit": "Editer:", "save_btn": "Sauver", "ssl": "SSL", "save_pass": "Sauver MDP", "signature": "Signature:", "to": "À:", "attach": "Joindre", "send": "Envoyer", "encrypt_pgp": " Chiffrer PGP", "new_preset": "Nouveau Serveur", "new_preset_btn": "Ajouter", "files": "fichiers", "pass_help": "Aide", "pass_help_text": "Si 2FA activé, utilisez un 'Mot de passe d'application'.", "receipt": "Demander un accusé de réception", "cached": " (Cache hors ligne)", "select_prof": "Sélectionnez un profil !", "prev": "<", "next": ">", "refresh_tip": "Actualiser", "show_pass": "Voir MDP", "help_icon": "Aide", "analyze_file": "Analyser Fichier (.eml)", "wipe_btn": " EFFACER DONNÉES", "wipe_confirm": "ATTENTION:\n\nCeci écrasera et supprimera TOUTES les clés locales.\n\nIRRÉVERSIBLE.\n\nContinuer?", "proxy_title": "Proxy / Tor", "search_lbl": "Chercher:", "proxy_enable": "Activer SOCKS5", "proxy_addr": "Adresse", "proxy_port": "Port", "sending": "Envoi...", "wait": "Patientez...", "pin_title": "PIN de Profil", "pin_ask": "Profil verrouillé.\nEntrer PIN:", "pin_wrong": "Mauvais PIN!", "burner_btn": "Générer Alias", "burner_title": "Identité Jetable", "burner_copy": "Copier Email", "stego_btn": "Cacher Secret", "stego_found": "🔍 SECRET DÉTECTÉ"},
    "de": {"app_title": "CorreioPro Ultimate", "multi_send_help": "Für mehrere E-Mails mit Komma trennen (z.B. a@a.com, b@b.com)", "pgp_your_name": "Ihr Name (für den Schlüssel)", "pgp_your_email": "Ihre E-Mail (zum Schlüssel)", "pgp_passphrase": "Passwort für privaten Schlüssel","login_title": "MAIL PRO", "connect": "Anmelden", "burner_win": "Wegwerf-Identität", "new_id": "Neue Identität", "copy_id": "Kopieren", "manage_profiles": "Profile", "about": "Über", "compose": " Schreiben", "contacts": " Kontakte", "pgp_keys": " PGP Schlüssel", "exit": " Abmelden", "reply": " Antworten", "forward": " Weiterleiten", "forensic": " Forensik", "save": " Speichern", "delete": " Löschen", "from": "Von:", "subject": "Betreff:", "date": "Datum", "ready": "Bereit", "loading": "Laden...", "loaded": "E-Mails", "safe_view": " Sichere Ansicht", "full_view": " Originalansicht", "decrypt_btn": " Entschlüsseln", "auth_title": "Authentifizierung", "pass_ask": "Passwort für", "error": "Fehler", "success": "Erfolg", "confirm": "Bestätigen", "delete_confirm": "Löschen?", "forensic_title": "Analyse", "score": "Punktzahl", "verdict": "Urteil", "safe": "VERTRAUENSWÜRDIG", "suspect": "VERDÄCHTIG", "danger": "GEFÄHRLICH", "harvest_btn": " Gesendete Scannen", "import_btn": " vCard Importieren", "add": "Hinzufügen", "del_sel": "Löschen", "name": "Name", "email": "E-Mail", "preset": "Voreinstellung:", "edit": "Bearbeiten:", "save_btn": "Speichern", "ssl": "SSL", "save_pass": "PW Speichern", "signature": "Signatur:", "to": "An:", "attach": "Anhängen", "send": "Senden", "encrypt_pgp": " PGP Verschlüsseln", "new_preset": "Neuer Server", "new_preset_btn": "Hinzufügen", "files": "Dateien", "pass_help": "Hilfe", "pass_help_text": "Bei 2FA, bitte ein 'App-Passwort' generieren.", "receipt": "Lesebestätigung anfordern", "cached": " (Offline-Cache)", "select_prof": "Profil auswählen!", "prev": "<", "next": ">", "refresh_tip": "Aktualisieren", "show_pass": "PW Anzeigen", "help_icon": "Hilfe", "analyze_file": "Datei Analysieren (.eml)", "wipe_btn": " DATEN LÖSCHEN", "wipe_confirm": "WARNUNG:\n\nDies überschreibt und löscht ALLE lokalen Schlüssel.\n\nUNWIDERRUFLICH.\n\nFortfahren?", "proxy_title": "Proxy / Tor", "search_lbl": "Suchen:", "proxy_enable": "SOCKS5 Aktivieren", "proxy_addr": "Adresse", "proxy_port": "Port", "sending": "Senden...", "wait": "Warten...", "pin_title": "Profil PIN", "pin_ask": "Profil gesperrt.\nPIN eingeben:", "pin_wrong": "Falsche PIN!", "burner_btn": "Alias Generieren", "burner_title": "Wegwerf-Identität", "burner_copy": "Email Kopieren", "stego_btn": "Geheimnis Verbergen", "stego_found": "🔍 GEHEIMNIS ENTDECKT"},
    "it": {"app_title": "CorreioPro Ultimate", "multi_send_help": "Per più email, separare con virgola (es: a@a.com, b@b.com)","pgp_your_name": "Il tuo Nome (per la chiave)", "pgp_your_email": "La tua Email (associata alla chiave)", "pgp_passphrase": "Passphrase Chiave Privata","login_title": "POSTA PRO", "connect": "Accedi", "manage_profiles": "Profili", "about": "Info", "compose": " Scrivi", "burner_win": "Identità Usa e Getta", "new_id": "Nuova Identità", "copy_id": "Copia", "contacts": " Contatti", "pgp_keys": " Chiavi PGP", "exit": " Esci", "reply": " Rispondi", "forward": " Inoltra", "forensic": " Forense", "save": " Salva", "delete": " Elimina", "from": "Da:", "subject": "Oggetto:", "date": "Data", "ready": "Pronto", "loading": "Caricamento...", "loaded": "email", "safe_view": " Vista Sicura", "full_view": " Vista Originale", "decrypt_btn": " Decifra", "auth_title": "Autenticazione", "pass_ask": "Password per", "error": "Errore", "success": "Successo", "confirm": "Conferma", "delete_confirm": "Eliminare?", "forensic_title": "Analisi", "score": "Punteggio", "verdict": "Verdetto", "safe": "AFFIDABILE", "suspect": "SOSPETTO", "danger": "PERICOLOSO", "harvest_btn": " Scansiona Inviati", "import_btn": " Importa vCard", "add": "Aggiungi", "del_sel": "Elimina Selezionato", "name": "Nome", "email": "Email", "preset": "Preset:", "edit": "Modifica:", "save_btn": "Salva", "ssl": "SSL", "save_pass": "Salva Pass", "signature": "Firma:", "to": "A:", "attach": "Allega", "send": "Invia", "encrypt_pgp": " Cifra PGP", "new_preset": "Nuovo Server", "new_preset_btn": "Aggiungi", "files": "file", "pass_help": "Aiuto", "pass_help_text": "Se usi 2FA, genera una 'App Password' nel tuo account.", "receipt": "Richiedi conferma di lettura", "cached": " (Cache Offline)", "select_prof": "Seleziona un profilo!", "prev": "<", "next": ">", "refresh_tip": "Aggiorna", "show_pass": "Mostra Pass", "help_icon": "Aiuto", "analyze_file": "Analizza File (.eml)", "wipe_btn": " CANCELLA DATI", "wipe_confirm": "ATTENZIONE:\n\nQuesto sovrascriverà ed eliminerà TUTTE le chiavi locali.\n\nIRREVERSIBILE.\n\nProcedere?", "proxy_title": "Proxy / Tor", "search_lbl": "Cerca:", "proxy_enable": "Attiva SOCKS5", "proxy_addr": "Indirizzo", "proxy_port": "Porta", "sending": "Invio...", "wait": "Attendere...", "pin_title": "PIN Profilo", "pin_ask": "Profilo bloccato.\nInserisci PIN:", "pin_wrong": "PIN Errato!", "burner_btn": "Genera Alias", "burner_title": "Identità Usa e Getta", "burner_copy": "Copia Email", "stego_btn": "Nascondi Segreto", "stego_found": "🔍 SEGRETO RILEVATO"},
    "ru": {"app_title": "CorreioPro Ultimate", "multi_send_help": "Для нескольких писем разделяйте запятой (ex: a@a.com, b@b.com)", "pgp_your_name": "Ваше Имя (для ключа)", "pgp_your_email": "Ваш Email (связан с ключом)", "pgp_passphrase": "Пароль от приватного ключа","login_title": "ПОЧТА PRO", "connect": "Войти","burner_win": "Временная Личность", "new_id": "Новая Личность", "copy_id": "Копировать", "manage_profiles": "Профили", "about": "О нас", "compose": " Написать", "contacts": " Контакты", "pgp_keys": " Ключи PGP", "exit": " Выход", "reply": " Ответить", "forward": " Переслать", "forensic": " Анализ", "save": " Сохранить", "delete": " Удалить", "from": "От:", "subject": "Тема:", "date": "Дата", "ready": "Готово", "loading": "Загрузка...", "loaded": "писем", "safe_view": " Безопасно", "full_view": " Оригинал", "decrypt_btn": " Расшифровать", "auth_title": "Вход", "pass_ask": "Пароль для", "error": "Ошибка", "success": "Успешно", "confirm": "Подтвердить", "delete_confirm": "Удалить?", "forensic_title": "Анализ", "score": "Оценка", "verdict": "Вердикт", "safe": "НАДЕЖНО", "suspect": "ПОДОЗРИТЕЛЬНО", "danger": "ОПАСНО", "harvest_btn": " Сканировать Отпр.", "import_btn": " Импорт vCard", "add": "Добавить", "del_sel": "Удалить", "name": "Имя", "email": "Email", "preset": "Шаблон:", "edit": "Ред.:", "save_btn": "Сохранить", "ssl": "SSL", "save_pass": "Сохр. пароль", "signature": "Подпись:", "to": "Кому:", "attach": "Вложить", "send": "Отправить", "encrypt_pgp": " Шифровать PGP", "new_preset": "Новый Сервер", "new_preset_btn": "Добавить", "files": "файлов", "pass_help": "Помощь", "pass_help_text": "Если 2FA, создайте 'Пароль приложения' в настройках.", "receipt": "Запросить уведомление о прочтении", "cached": " (Офлайн)", "select_prof": "Выберите профиль!", "prev": "<", "next": ">", "refresh_tip": "Обновить", "show_pass": "Показать пароль", "help_icon": "Помощь", "analyze_file": "Анализ файла (.eml)", "wipe_btn": " УДАЛИТЬ ДАННЫЕ", "wipe_confirm": "ВНИМАНИЕ:\n\nЭто перезапишет и удалит ВСЕ локальные ключи.\n\nНЕОБРАТИМО.\n\nПродолжить?", "proxy_title": "Proxy / Tor", "search_lbl": "Поиск:", "proxy_enable": "Вкл. SOCKS5", "proxy_addr": "Адрес", "proxy_port": "Порт", "sending": "Отправка...", "wait": "Ждите...", "pin_title": "PIN профиля", "pin_ask": "Профиль заблокирован.\nВведите PIN:", "pin_wrong": "Неверный PIN!", "burner_btn": "Создать Алиас", "burner_title": "Временная почта", "burner_copy": "Копировать", "stego_btn": "Скрыть Секрет", "stego_found": "🔍 СЕКРЕТ ОБНАРУЖЕН"},
    "zh": {"app_title": "CorreioPro 旗舰版", "multi_send_help": "对于多个电子邮件，请用逗号分隔 (例如: a@a.com, b@b.com)", "pgp_your_name": "您的名字 (用于密钥)", "pgp_your_email": "您的邮箱 (关联到密钥)", "pgp_passphrase": "私钥的密码","login_title": "专业邮件", "connect": "登录", "burner_win": "临时身份", "new_id": "新身份", "copy_id": "复制", "manage_profiles": "配置", "about": "关于", "compose": " 写邮件", "contacts": " 联系人", "pgp_keys": " PGP 密钥", "exit": " 退出", "reply": " 回复", "forward": " 转发", "forensic": " 取证分析", "save": " 保存", "delete": " 删除", "from": "发件人:", "subject": "主题:", "date": "日期", "ready": "就绪", "loading": "加载中...", "loaded": "封邮件", "safe_view": " 安全视图", "full_view": " 原始视图", "decrypt_btn": " 解密", "auth_title": "认证", "pass_ask": "密码:", "error": "错误", "success": "成功", "confirm": "确认", "delete_confirm": "删除?", "forensic_title": "分析", "score": "评分", "verdict": "结论", "safe": "可信", "suspect": "可疑", "danger": "危险", "harvest_btn": " 扫描已发送", "import_btn": " 导入 vCard", "add": "添加", "del_sel": "删除选中", "name": "姓名", "email": "邮箱", "preset": "预设:", "edit": "编辑:", "save_btn": "保存", "ssl": "SSL", "save_pass": "保存密码", "signature": "签名:", "to": "收件人:", "attach": "附件", "send": "发送", "encrypt_pgp": " PGP 加密", "new_preset": "新服务器", "new_preset_btn": "添加", "files": "文件", "pass_help": "帮助", "pass_help_text": "如果您使用 2FA，请在设置中生成“应用密码”。", "receipt": "请求回执", "cached": " (离线缓存)", "select_prof": "请先选择配置文件！", "prev": "<", "next": ">", "refresh_tip": "刷新", "show_pass": "显示密码", "help_icon": "帮助", "analyze_file": "分析文件 (.eml)", "wipe_btn": " 擦除数据", "wipe_confirm": "警告：\n\n这将覆盖并删除所有本地密钥。\n\n此操作不可逆。\n\n继续吗？", "proxy_title": "Proxy / Tor", "search_lbl": "搜索:", "proxy_enable": "启用 SOCKS5", "proxy_addr": "地址", "proxy_port": "端口", "sending": "发送中...", "wait": "请稍候...", "pin_title": "配置文件 PIN", "pin_ask": "此配置文件已锁定。\n请输入 PIN：", "pin_wrong": "PIN 错误！", "burner_btn": "生成别名", "burner_title": "临时身份", "burner_copy": "复制邮箱", "stego_btn": "隐藏秘密", "stego_found": "🔍 发现秘密"}
}

CURRENT_LANG = "pt"

def T(key):
    return T_DATA.get(CURRENT_LANG, T_DATA["pt"]).get(key, key)

def load_settings():
    global CURRENT_LANG
    if os.path.exists(FILES["settings"]):
        try: 
            data = json.load(open(FILES["settings"]))
            CURRENT_LANG = data.get("lang", "pt")
        except: pass

def save_settings(lang_code):
    global CURRENT_LANG
    CURRENT_LANG = lang_code
    json.dump({"lang": lang_code}, open(FILES["settings"], "w"))

# --- HELPER: TOOLTIP ---
class CreateToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                       background="#2b2b2b", fg="#ffffff", relief=tk.SOLID, borderwidth=1,
                       font=("Segoe UI", 8, "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window: self.tip_window.destroy(); self.tip_window = None

# --- THE GHOST LINK (SOCKS5 PURE PYTHON) ---
class Socks5Socket(socket.socket):
    def __init__(self, proxy_ip, proxy_port, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto, fileno)
        self.proxy_ip = proxy_ip
        self.proxy_port = int(proxy_port)

    def connect(self, address):
        super().connect((self.proxy_ip, self.proxy_port))
        self.sendall(b"\x05\x01\x00")
        if self.recv(2) != b"\x05\x00": raise Exception("Proxy Handshake Failed")
        dest_ip, dest_port = address
        try: dest_addr_bin = socket.inet_aton(socket.gethostbyname(dest_ip))
        except: raise Exception("DNS Resolution Failed")
        self.sendall(b"\x05\x01\x00\x01" + dest_addr_bin + dest_port.to_bytes(2, 'big'))
        resp = self.recv(4)
        if resp[1] != 0: raise Exception(f"Proxy Connection Refused: {resp[1]}")
        if resp[3] == 1: self.recv(4 + 2)
        elif resp[3] == 3: l = self.recv(1)[0]; self.recv(l + 2)
        elif resp[3] == 4: self.recv(16 + 2)

PROXY_CONFIG = {"enabled": False, "ip": "127.0.0.1", "port": "9050"}

# --- STEGANOGRAPHY (DEAD DROP) ---
class Stego:
    # Text Zero-Width Logic
    ZWSP = '\u200b' 
    ZWNJ = '\u200c'
    # Image Binary Marker (A unique byte sequence we look for)
    IMG_MARKER = b'<<__DARK_MAIL_SECRET__>>'
    
    @staticmethod
    def encode(secret_text):
        if not secret_text: return ""
        binary = ''.join(format(ord(c), '08b') for c in secret_text)
        return binary.replace('0', Stego.ZWNJ).replace('1', Stego.ZWSP)

    @staticmethod
    def decode(stego_text):
        if not stego_text: return None
        binary = ""
        for char in stego_text:
            if char == Stego.ZWSP: binary += '1'
            elif char == Stego.ZWNJ: binary += '0'
        if len(binary) < 8 or len(binary) % 8 != 0: return None
        try:
            chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
            decoded = ''.join(chr(int(c, 2)) for c in chars)
            return decoded if any(c.isalnum() for c in decoded) else None
        except: return None

    # --- NEW: IMAGE INJECTION ---
    @staticmethod
    def inject_image(filepath, secret):
        try:
            with open(filepath, "rb") as f:
                img_data = f.read()
            # Encode secret to base64 so it handles special chars
            secret_bytes = base64.b64encode(secret.encode('utf-8'))
            # Glue it: [IMAGE_DATA] + [MARKER] + [SECRET]
            new_data = img_data + Stego.IMG_MARKER + secret_bytes
            return new_data
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def extract_image(file_bytes):
        try:
            if Stego.IMG_MARKER in file_bytes:
                # Split at the marker and take the last part
                raw_secret = file_bytes.split(Stego.IMG_MARKER)[-1]
                return base64.b64decode(raw_secret).decode('utf-8')
        except: pass
        return None

class GhostGenerator:
    FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Robin", "Cameron", "Quinn"]
    LAST_NAMES = ["Smith", "Doe", "Brown", "Wilson", "Thomson", "Evans", "Walker", "Roberts", "Green", "Hall"]
    
    @staticmethod
    def generate():
        fn = random.choice(GhostGenerator.FIRST_NAMES)
        ln = random.choice(GhostGenerator.LAST_NAMES)
        full_name = f"{fn} {ln}"
        # Generate a secure random password
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = ''.join(random.choice(chars) for i in range(16))
        # Generate a username
        user = f"{fn.lower()}.{ln.lower()}{random.randint(10,99)}"
        
        return {"name": full_name, "user": user, "pass": pwd}
        
# --- BURNER MAIL MODULE (FINAL) ---
class BurnerMail:
    API_BASE = "https://api.guerrillamail.com/ajax.php"
    
    class HTMLFilter(HTMLParser):
        def __init__(self): super().__init__(); self.text = []
        def handle_data(self, d): self.text.append(d)
        def get_text(self): return ''.join(self.text)

    def __init__(self, root, icons):
        self.root = root
        self.icons = icons
        self.email_addr = None
        self.session_id = None
        self.win = None
        self.running = False
        self.tree = None
        self.txt_body = None
        self.displayed_ids = set()
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.session.verify = certifi.where()
        hostname_hash = hashlib.sha1(socket.gethostname().encode()).hexdigest()
        self.agent_id = f"custom_agent_{hostname_hash}"

    def _req(self, params):
        try:
            resp = self.session.get(self.API_BASE, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception: return None

    def start(self):
        if self.win and self.win.winfo_exists(): self.win.lift(); return
        self.win = tk.Toplevel(self.root); self.win.title(T("burner_win"))
        self.win.geometry("800x550") # Increased width slightly
        
        # Header Frame
        h_frame = tk.Frame(self.win)
        h_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Email Label (Left)
        self.lbl_email = tk.Label(h_frame, text=T("loading"), fg="#e74c3c", font=("Consolas", 12, "bold"))
        self.lbl_email.pack(side=tk.LEFT)
        
        btn_cfg = {"compound": tk.LEFT}
        
        # 1. COPY BUTTON
        if self.icons.get("copy"): ttk.Button(h_frame, text=T("copy_id"), image=self.icons["copy"], command=self.copy_email, **btn_cfg).pack(side=tk.RIGHT, padx=2)
        else: ttk.Button(h_frame, text=T("copy_id"), command=self.copy_email).pack(side=tk.RIGHT, padx=2)
        
        # 2. NEW EMAIL ADDRESS BUTTON (Refresh Inbox)
        if self.icons.get("refresh"): ttk.Button(h_frame, text=T("new_id"), image=self.icons["refresh"], command=lambda: threading.Thread(target=self.gen_email, daemon=True).start(), **btn_cfg).pack(side=tk.RIGHT, padx=2)
        else: ttk.Button(h_frame, text=T("new_id"), command=lambda: threading.Thread(target=self.gen_email, daemon=True).start()).pack(side=tk.RIGHT, padx=2)

        # 3. GHOST PERSONA GENERATOR BUTTON
        def generate_persona():
            # This generates the Fake Name/Pass you were looking for
            p = GhostGenerator.generate()
            msg = f"NAME: {p['name']}\nUSER: {p['user']}\nPASS: {p['pass']}"
            
            top = tk.Toplevel(self.win); top.title("Ghost Persona"); top.geometry("300x220")
            tk.Label(top, text="FAKE IDENTITY", fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(pady=5)
            t = tk.Text(top, height=5, width=30); t.pack(pady=5, padx=10); t.insert("1.0", msg)
            
            def cp_all(): 
                top.clipboard_clear(); top.clipboard_append(msg); messagebox.showinfo("Copied", "Identity Copied!", parent=top)
            
            if self.icons.get("copy"): ttk.Button(top, text="Copy All", image=self.icons["copy"], compound=tk.LEFT, command=cp_all).pack(pady=5)
            else: ttk.Button(top, text="Copy All", command=cp_all).pack(pady=5)

        # Added explicit text "Ghost ID" to make sure it's visible
        if self.icons.get("ghost"): ttk.Button(h_frame, text="Ghost ID", image=self.icons["ghost"], command=generate_persona, **btn_cfg).pack(side=tk.RIGHT, padx=10)
        else: ttk.Button(h_frame, text="Ghost ID", command=generate_persona).pack(side=tk.RIGHT, padx=10)

        # Body List
        self.tree = ttk.Treeview(self.win, columns=("F", "S", "D"), show="headings", height=8)
        self.tree.heading("F", text=T("from")); self.tree.column("F", width=120)
        self.tree.heading("S", text=T("subject")); self.tree.column("S", width=250)
        self.tree.heading("D", text=T("date")); self.tree.column("D", width=80)
        self.tree.pack(fill=tk.X, padx=10)
        self.tree.bind("<<TreeviewSelect>>", self.read_mail)
        self.txt_body = tk.Text(self.win, font=("Consolas", 10))
        self.txt_body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.running = True
        threading.Thread(target=self.gen_email, daemon=True).start()
        self.win.protocol("WM_DELETE_WINDOW", self.close)

    def gen_email(self):
        # 1. Clear the UI list
        self.displayed_ids.clear()
        if self.tree: self.tree.delete(*self.tree.get_children())
        
        # --- FIX: FORCE NEW IDENTITY ---
        # Tell the API to destroy the current address if one exists
        if self.session_id and self.email_addr:
            try:
                self._req({'f': 'forget_me', 'sid_token': self.session_id, 'email_addr': self.email_addr})
            except: pass
        
        # CLEAR COOKIES (This is the key step to stop getting the same email)
        self.session.cookies.clear()
        self.session_id = None 
        # -------------------------------

        # 2. Request a fresh address
        params = {'f': 'get_email_address', 'agent': self.agent_id}
        data = self._req(params)
        
        if data and 'email_addr' in data:
            self.email_addr = data['email_addr']
            self.session_id = data['sid_token']
            
            # Update the red text label
            if self.win and self.win.winfo_exists(): 
                self.win.after(0, lambda: self.lbl_email.config(text=self.email_addr))

    def loop_check(self):
        while self.running:
            if self.session_id:
                params = {'f': 'get_email_list', 'sid_token': self.session_id, 'offset': 0, 'seq': 1}
                data = self._req(params)
                if data and 'list' in data and data['list']:
                    new_emails = [m for m in data['list'] if m['mail_id'] not in self.displayed_ids]
                    if new_emails and self.win: self.win.after(0, self.update_list, new_emails)
            time.sleep(15)

    def update_list(self, new_msgs):
        if not self.tree: return
        for m in reversed(new_msgs):
            if m['mail_id'] not in self.displayed_ids:
                d_str = "..."
                try: d_str = time.strftime('%H:%M', time.localtime(int(m['mail_timestamp'])))
                except: pass
                self.tree.insert("", 0, iid=m['mail_id'], values=(m['mail_from'], m['mail_subject'], d_str))
                self.displayed_ids.add(m['mail_id'])

    def read_mail(self, event):
        sel = self.tree.selection()
        if not sel: return
        mail_id = sel[0]
        def fetch():
            params = {'f': 'fetch_email', 'sid_token': self.session_id, 'email_id': mail_id}
            data = self._req(params)
            if data and 'mail_body' in data:
                s = self.HTMLFilter(); s.feed(data['mail_body']); body_text = s.get_text()
                if self.txt_body: self.win.after(0, lambda: (self.txt_body.delete("1.0", tk.END), self.txt_body.insert("1.0", body_text)))
        threading.Thread(target=fetch, daemon=True).start()

    def close(self):
        self.running = False
        if self.win: self.win.destroy()
    def copy_email(self): 
        if self.email_addr and self.win: 
            self.win.clipboard_clear(); self.win.clipboard_append(self.email_addr); messagebox.showinfo("Copied", self.email_addr, parent=self.win)


        
# --- GESTOR DE SEGURANÇA ---
class SecurityManager:
    def __init__(self):
        self.key = None
        if HAS_CRYPTO: self.load_key()
        self.pgp_keyring = self.load_pgp_keyring()

    def load_key(self):
        if not os.path.exists(FILES["key"]):
            self.key = Fernet.generate_key()
            with open(FILES["key"], "wb") as f: f.write(self.key)
        else:
            with open(FILES["key"], "rb") as f: self.key = f.read()

    def encrypt(self, text):
        if not HAS_CRYPTO or not text: return ""
        return Fernet(self.key).encrypt(text.encode()).decode()

    def decrypt(self, text):
        if not HAS_CRYPTO or not text: return ""
        try: return Fernet(self.key).decrypt(text.encode()).decode()
        except: return ""

    def load_pgp_keyring(self):
        default = {"private_keys": {}, "public_keys": {}}
        if os.path.exists(FILES["pgp"]):
            try: 
                data = json.load(open(FILES["pgp"]))
                if "my_private" in data:
                    if isinstance(data["my_private"], str) and data["my_private"]:
                        default["private_keys"]["legacy_key"] = data["my_private"]
                    if "public_keys" in data:
                        default["public_keys"] = data["public_keys"]
                    return default
                return data
            except: return default
        return default

    def save_pgp_keyring(self):
        json.dump(self.pgp_keyring, open(FILES["pgp"], "w"), indent=4)

    def generate_pgp_key(self, name, email, password):
        if not HAS_PGP: return False, "PGPy em falta"
        try:
            key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
            uid = pgpy.PGPUID.new(name, email=email)
            key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                        hashes=[HashAlgorithm.SHA256], ciphers=[SymmetricKeyAlgorithm.AES256], compression=[CompressionAlgorithm.ZLIB])
            key.protect(password, SymmetricKeyAlgorithm.AES256, HashAlgorithm.SHA256)
            self.pgp_keyring["private_keys"][email] = str(key)
            self.pgp_keyring["public_keys"][email] = str(key.pubkey)
            self.save_pgp_keyring()
            return True, T("success")
        except Exception as e: return False, str(e)

    def import_public_key(self, email_addr, key_text):
        if not HAS_PGP: return
        try:
            k, _ = pgpy.PGPKey.from_blob(key_text)
            self.pgp_keyring["public_keys"][email_addr] = str(k)
            self.save_pgp_keyring()
            return True
        except: return False

    def encrypt_pgp_message(self, message, recipient_email):
        if not HAS_PGP: return message
        pub_block = self.pgp_keyring["public_keys"].get(recipient_email)
        if not pub_block: return None 
        try:
            pub_key, _ = pgpy.PGPKey.from_blob(pub_block)
            msg = pgpy.PGPMessage.new(message)
            encrypted = pub_key.encrypt(msg)
            return str(encrypted)
        except: return None

    def decrypt_pgp_message(self, encrypted_text, password, my_email=None):
        if not HAS_PGP: return "Erro Lib"
        target_key_block = None
        if my_email and my_email in self.pgp_keyring["private_keys"]:
            target_key_block = self.pgp_keyring["private_keys"][my_email]
        keys_to_try = []
        if target_key_block: keys_to_try.append(target_key_block)
        keys_to_try.extend(list(self.pgp_keyring["private_keys"].values()))
        for kb in keys_to_try:
            try:
                priv_key, _ = pgpy.PGPKey.from_blob(kb)
                with priv_key.unlock(password):
                    msg = pgpy.PGPMessage.from_blob(encrypted_text)
                    decrypted = priv_key.decrypt(msg)
                    return decrypted.message
            except: continue
        return "Decryption Failed (Wrong Password or Key)"

    def save_encrypted_json(self, filename, data):
        """Saves a JSON object to a file, but AES-256 encrypted."""
        try:
            json_str = json.dumps(data)
            encrypted_data = self.encrypt(json_str) 
            with open(filename, "w") as f:
                f.write(encrypted_data)
        except Exception as e: print(f"Cache Save Error: {e}")

    def load_encrypted_json(self, filename):
        """Loads a file, tries to decrypt it. Handles legacy plain text automatically."""
        if not os.path.exists(filename): return {}
        
        with open(filename, "r") as f:
            content = f.read()
            
        # Try Decrypting First
        try:
            decrypted_str = Fernet(self.key).decrypt(content.encode()).decode()
            return json.loads(decrypted_str)
        except:
            # If decryption fails, it might be an old PLAIN TEXT file (Legacy support)
            try: return json.loads(content)
            except: return {} 

    def emergency_wipe(self):
        targets = [FILES["key"], FILES["profiles"], FILES["contacts"], FILES["pgp"], FILES["cache"]]
        for t in targets:
            if os.path.exists(t):
                try:
                    size = os.path.getsize(t)
                    with open(t, "wb") as f: f.write(os.urandom(size))
                    os.remove(t)
                except: pass
        sys.exit(0)

    def hash_pin(self, pin): return hashlib.sha256(pin.encode()).hexdigest()
    def verify_pin(self, pin, stored_hash): return self.hash_pin(pin) == stored_hash

security = SecurityManager()

# --- FORENSE ---
class EmailForensics:
    @staticmethod
    def extract_email(text):
        match = re.search(r'[\w\.-]+@[\w\.-]+', str(text))
        return match.group(0) if match else ""

    @staticmethod
    def get_domain(email_addr):
        if "@" in email_addr: return email_addr.split("@")[1].lower()
        return ""

    @staticmethod
    def is_public_ip(ip):
        try:
            if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip): return False
            first = int(ip.split('.')[0])
            if first == 10: return False
            if first == 172 and 16 <= int(ip.split('.')[1]) <= 31: return False
            if first == 192 and int(ip.split('.')[1]) == 168: return False
            if first == 127: return False
            return True
        except: return False

    @staticmethod
    def get_geo_data(ip):
        try:
            with urllib.request.urlopen(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,org,mobile,proxy") as url:
                data = json.loads(url.read().decode())
                if data.get("status") == "success": return data
        except: pass
        return None

    @staticmethod
    def analyze(msg_obj):
        report = []
        score = 100 
        h_from = clean_header(msg_obj['From'])
        h_return = clean_header(msg_obj['Return-Path'])
        h_auth = str(msg_obj['Authentication-Results']).lower()
        h_mailer = str(msg_obj['X-Mailer']).lower()
        email_from = EmailForensics.extract_email(h_from)
        email_return = EmailForensics.extract_email(h_return)
        if email_return and email_from:
            dom_from = EmailForensics.get_domain(email_from)
            dom_ret = EmailForensics.get_domain(email_return)
            whitelist = ["amazonses.com", "google.com", "outlook.com", "sendgrid.net", "mailchimp.com"]
            is_subdomain = dom_ret.endswith("." + dom_from) or dom_from.endswith("." + dom_ret)
            if dom_from != dom_ret and not is_subdomain and dom_ret not in whitelist:
                score -= 30
                report.append(f"[X] SPOOF ALERT: From '{dom_from}' but routed via '{dom_ret}'.")
            else:
                report.append(f"[OK] Domain Alignment Verified ({dom_from}).")
        if "spf=fail" in h_auth or "dkim=fail" in h_auth:
            score -= 40
            report.append("[X] CRITICAL: SPF/DKIM Validation Failed.")
        elif "spf=pass" in h_auth:
            report.append("[OK] SPF Validation Passed.")
        suspicious_agents = ["php", "python", "java", "script", "wmailer", "postfix"]
        if any(x in h_mailer for x in suspicious_agents):
            score -= 10
            report.append(f"[!] WARNING: Automated Mailer detected ({h_mailer}).")
        geo_data = None
        found_ip = None
        received_headers = msg_obj.get_all('Received') or []
        for r in reversed(received_headers):
            ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', str(r))
            for ip in ips:
                if EmailForensics.is_public_ip(ip):
                    found_ip = ip
                    break
            if found_ip: break
        if found_ip:
            geo_data = EmailForensics.get_geo_data(found_ip)
            if geo_data:
                geo_data['ip'] = found_ip
                if geo_data.get('proxy'): score -= 20
        return score, report, geo_data

# --- UTILITÁRIOS ---
def check_files():
    # --- UPDATED SERVER LIST ---
    default_servers = {
        "Gmail": {
            "smtp": "smtp.gmail.com", "smtp_port": "465", 
            "imap": "imap.gmail.com", "imap_port": "993", "ssl": True
        },
        "Outlook / Hotmail": {
            "smtp": "smtp-mail.outlook.com", "smtp_port": "587", 
            "imap": "outlook.office365.com", "imap_port": "993", "ssl": False 
            # Note: SSL=False triggers STARTTLS on port 587 in this app logic
        },
        "Yahoo Mail": {
            "smtp": "smtp.mail.yahoo.com", "smtp_port": "465", 
            "imap": "imap.mail.yahoo.com", "imap_port": "993", "ssl": True
        },
        "iCloud": {
            "smtp": "smtp.mail.me.com", "smtp_port": "587", 
            "imap": "imap.mail.me.com", "imap_port": "993", "ssl": False
        },
        "Yandex": {
            "smtp": "smtp.yandex.com", "smtp_port": "465", 
            "imap": "imap.yandex.com", "imap_port": "993", "ssl": True
        },
        "Zoho": {
            "smtp": "smtp.zoho.com", "smtp_port": "465", 
            "imap": "imap.zoho.com", "imap_port": "993", "ssl": True
        },
        "GMX": {
            "smtp": "mail.gmx.net", "smtp_port": "587", 
            "imap": "imap.gmx.net", "imap_port": "993", "ssl": False
        },
        "ProtonMail (Bridge)": {
            "smtp": "127.0.0.1", "smtp_port": "1025", 
            "imap": "127.0.0.1", "imap_port": "1143", "ssl": False
        }
    }

    if not os.path.exists(FILES["servers"]):
        with open(FILES["servers"], 'w') as f: json.dump(default_servers, f, indent=4)
        
    if not os.path.exists(FILES["contacts"]):
        with open(FILES["contacts"], 'w') as f: json.dump({}, f)

def load_json(f):
    if os.path.exists(f): 
        try: return json.load(open(f)) 
        except: return {}
    return {}
def save_json(f, d): json.dump(d, open(f, 'w'), indent=4)

class HTMLFilter(HTMLParser):
    def __init__(self): super().__init__(); self.text = []; self.ignore = False
    def handle_starttag(self, t, a): 
        if t in ["style", "script", "head", "title", "meta", "link"]: self.ignore = True
        elif t in ["br", "p", "div", "tr", "li", "h1", "h2", "h3", "h4"]: self.text.append("\n")
    def handle_endtag(self, t):
        if t in ["style", "script", "head", "title", "meta", "link"]: self.ignore = False
        elif t in ["p", "div", "tr", "li"]: self.text.append("\n")
    def handle_data(self, d): 
        if not self.ignore: 
            content = d.strip()
            if content: self.text.append(content + " ")

def html_to_text(h): 
    f = HTMLFilter()
    try:
        f.feed(h)
        full_text = "".join(f.text)
        return re.sub(r'\n\s*\n', '\n\n', full_text).strip()
    except: return "Complex HTML Content"

def clean_header(h):
    if not h: return "(Sem Assunto)"
    try:
        val = ""
        for b, enc in decode_header(h):
            if isinstance(b, bytes):
                try: val += b.decode(enc or 'utf-8', errors='ignore')
                except: val += b.decode('utf-8', errors='ignore')
            else: val += str(b)
        return val
    except: return str(h)

# --- BACKEND ---
class EmailBackend:
    def __init__(self, c, p, l): self.c = c; self.p = p; self.log = l
    
    def _create_socket(self, host, port):
        if PROXY_CONFIG["enabled"]:
            print(f"[*] Ghost Link: Tunneling to {host}:{port}")
            s = Socks5Socket(PROXY_CONFIG["ip"], PROXY_CONFIG["port"])
            s.connect((host, int(port)))
            return s
        else:
            return socket.create_connection((host, int(port)))

    def conn_imap(self):
        if PROXY_CONFIG["enabled"]:
            sock = self._create_socket(self.c['imap_server'], self.c['imap_port'])
            if self.c['use_ssl']:
                import ssl
                ctx = ssl.create_default_context()
                sock = ctx.wrap_socket(sock, server_hostname=self.c['imap_server'])
            m = imaplib.IMAP4_SSL(self.c['imap_server'], port=self.c['imap_port']) if self.c['use_ssl'] else imaplib.IMAP4(self.c['imap_server'], port=self.c['imap_port'])
            m.sock = sock; m.file = sock.makefile('rb')
        else:
            m = imaplib.IMAP4_SSL(self.c['imap_server'], int(self.c['imap_port'])) if self.c['use_ssl'] else imaplib.IMAP4(self.c['imap_server'], int(self.c['imap_port']))
        m.login(self.c['email'], self.p); return m
    
    def conn_smtp(self):
        if PROXY_CONFIG["enabled"]:
            sock = self._create_socket(self.c['smtp_server'], self.c['smtp_port'])
            if self.c['use_ssl']:
                import ssl
                ctx = ssl.create_default_context()
                sock = ctx.wrap_socket(sock, server_hostname=self.c['smtp_server'])
            s = smtplib.SMTP(self.c['smtp_server'], self.c['smtp_port'])
            s.sock = sock; s.file = sock.makefile('rb')
        else:
            s = smtplib.SMTP_SSL(self.c['smtp_server'], int(self.c['smtp_port'])) if self.c['use_ssl'] else smtplib.SMTP(self.c['smtp_server'], int(self.c['smtp_port']))
        
        if not self.c['use_ssl'] and not PROXY_CONFIG["enabled"]: s.starttls()
        s.login(self.c['email'], self.p); return s

    def list_folders(self):
        try: 
            m = self.conn_imap(); _, f = m.list(); m.logout()
            return [shlex.split(x.decode())[-1] for x in f]
        except: return ["INBOX"]

    def harvest_contacts(self):
        self.log("A procurar pasta Enviados...")
        try:
            m = self.conn_imap()
            _, folders = m.list()
            sent_folder = None
            candidates = ["Sent", "Enviados", "Sent Items", "Itens Enviados", "Sent Messages"]
            clean_folders = [shlex.split(x.decode())[-1] for x in folders]
            for f in clean_folders:
                for c in candidates:
                    if c.lower() in f.lower():
                        sent_folder = f; break
                if sent_folder: break
            
            if not sent_folder: m.logout(); return 0, "Pasta enviados não encontrada."

            self.log(f"A ler {sent_folder}...")
            m.select(f'"{sent_folder}"')
            typ, data = m.search(None, 'ALL')
            ids = data[0].split()[-50:]
            new_contacts = {}
            for i in ids:
                try:
                    _, d = m.fetch(i, '(RFC822.HEADER)')
                    msg = email.message_from_bytes(d[0][1])
                    to_header = clean_header(msg['To'])
                    if to_header:
                        raw_email = EmailForensics.extract_email(to_header)
                        raw_name = to_header.split("<")[0].strip().replace('"', '')
                        if not raw_name: raw_name = raw_email.split("@")[0]
                        if raw_email and "@" in raw_email: new_contacts[raw_name] = raw_email
                except: pass
            m.close(); m.logout(); return len(new_contacts), new_contacts
        except Exception as e: return 0, str(e)

    def fetch(self, fbox="INBOX", page=0, lim=30, search=None):
        self.log(T("loading"))
        try:
            m = self.conn_imap(); m.select(f'"{fbox}"')
            crit = f'(SUBJECT "{search}")' if search else 'ALL'
            typ, d = m.search("UTF-8", crit)
            if typ != 'OK': typ, d = m.search(None, crit)
            
            all_ids = d[0].split()
            all_ids.reverse() 
            start = page * lim; end = start + lim
            if start >= len(all_ids): return [] 
            ids = all_ids[start:end] 
            
            res = []
            for i in ids:
                try:
                    _, d = m.fetch(i, '(RFC822)')
                    raw_bytes = d[0][1] 
                    msg = email.message_from_bytes(raw_bytes)
                    subj = clean_header(msg['subject'])
                    frm_full = clean_header(msg['from'])
                    to_full = clean_header(msg['to'])
                    realname, emailaddr = parseaddr(frm_full)
                    display_name = realname if realname else emailaddr
                    date_str = str(msg['Date'])
                    try: dt = parsedate_to_datetime(msg['Date']); date_str = dt.strftime("%d/%m/%Y %H:%M")
                    except: pass
                    
                    body, html, atts = "", "", []
                    if msg.is_multipart():
                        for p in msg.walk():
                            ctype = p.get_content_type()
                            cdisp = str(p.get("Content-Disposition"))
                            filename = p.get_filename()
                            if filename:
                                fn = clean_header(filename)
                                atts.append({'name': fn, 'data': p.get_payload(decode=True)})
                            elif ctype == "text/plain" and "attachment" not in cdisp:
                                body += p.get_payload(decode=True).decode(errors='ignore')
                            elif ctype == "text/html" and "attachment" not in cdisp:
                                html += p.get_payload(decode=True).decode(errors='ignore')
                    else:
                        pay = msg.get_payload(decode=True).decode(errors='ignore')
                        if msg.get_content_type() == "text/html": html = pay
                        else: body = pay
                    if not body and html: body = html_to_text(html)
                    res.append({
                        'id': i.decode(), 'from_full': frm_full, 'to_full': to_full, 'from_short': display_name,
                        'subject': subj, 'date': date_str, 'body': body, 'html': html, 'attachments': atts, 'raw_msg': msg, 'raw_bytes': raw_bytes
                    })
                except Exception as e: print(f"Erro {i}: {e}")
            m.close(); m.logout(); return res
        except Exception as e: self.log(f"{T('error')}: {e}"); return []

    def send(self, to, sub, body, atts=[], request_receipt=False):
        try:
            # --- HANDLE MULTIPLE RECIPIENTS ---
            if isinstance(to, str):
                # Replace ; with , and split into a list
                clean_to = to.replace(';', ',')
                # Remove empty spaces and build list
                recipients = [addr.strip() for addr in clean_to.split(',') if addr.strip()]
                # Rebuild string for the MIME Header (Visual)
                to_header = ", ".join(recipients)
            else:
                recipients = to
                to_header = ", ".join(to)
            
            if not recipients: return False, "No recipients specified."
            # ----------------------------------

            m = MIMEMultipart()
            m['From'] = self.c['email']
            m['To'] = to_header # MIME header needs a String
            m['Subject'] = sub
            m['Date'] = formatdate(localtime=True)
            m['Message-ID'] = make_msgid()
            
            if request_receipt: 
                m['Disposition-Notification-To'] = self.c['email']
                m['Return-Receipt-To'] = self.c['email']
            
            m.attach(MIMEText(body, 'plain'))
            
            for p in atts:
                with open(p, "rb") as f:
                    part = MIMEBase("application", "octet-stream"); part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(p)}")
                m.attach(part)
            
            s = self.conn_smtp()
            # SMTP .sendmail expects a LIST ['a@a.com', 'b@b.com']
            s.sendmail(self.c['email'], recipients, m.as_string())
            s.quit()
            
            try:
                imap = self.conn_imap(); sent_folder = "Sent"
                _, flds = imap.list(); clean = [shlex.split(x.decode())[-1] for x in flds]
                for f in clean:
                    if f.lower() in ['sent', 'enviados', 'sent items', 'itens enviados', 'outbox']: sent_folder = f; break
                imap.append(f'"{sent_folder}"', '\\Seen', imaplib.Time2Internaldate(time.time()), m.as_bytes()); imap.logout()
            except Exception as e: print(f"IMAP Save Error: {e}")
            
            self.log(T("success")); return True, "Success"
        except Exception as e: self.log(f"{T('error')}: {e}"); return False, str(e)

    def delete(self, fbox, eid):
        try: m = self.conn_imap(); m.select(f'"{fbox}"'); m.store(eid, '+FLAGS', '\\Deleted'); m.expunge(); m.logout(); return True
        except: return False   
        

# --- IDENTITY PROFILER (OSINT) ---
class IdentityProfiler:
    DISPOSABLE_DOMAINS = ["tempmail.com", "guerrillamail.com", "sharklasers.com", "yopmail.com", "mailinator.com", "10minutemail.com"]

    @staticmethod
    def get_profile(email_addr):
        # 1. Clean Email
        email_addr = email_addr.lower().strip()
        domain = email_addr.split("@")[1] if "@" in email_addr else ""
        
        profile = {
            "email": email_addr,
            "domain": domain,
            "has_gravatar": False,
            "mx_status": "Unknown",
            "is_disposable": False,
            "score": 100
        }

        # 2. Check Disposable
        if any(d in domain for d in IdentityProfiler.DISPOSABLE_DOMAINS):
            profile["is_disposable"] = True
            profile["score"] -= 50

        # 3. Check Gravatar (Public Profile)
        try:
            # Gravatar uses MD5 hash of email
            email_hash = hashlib.md5(email_addr.encode()).hexdigest()
            gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
            r = requests.head(gravatar_url, timeout=3)
            if r.status_code == 200:
                profile["has_gravatar"] = True
                profile["gravatar_url"] = gravatar_url
            else:
                profile["score"] -= 10 # Minor penalty for anonymity
        except: pass

        # 4. DNS/MX Check (Simulated for pure Python without dnspython)
        # We try to connect to the domain on port 25 or 443 just to see if it's alive
        try:
            socket.gethostbyname(domain)
            profile["mx_status"] = "Active"
        except:
            profile["mx_status"] = "Unreachable"
            profile["score"] -= 40
            
        return profile

    @staticmethod
    def show_window(root, email_addr, icons):
        p = IdentityProfiler.get_profile(email_addr)
        
        w = tk.Toplevel(root)
        w.title("Identity Profiler")
        w.geometry("400x350")
        w.configure(bg=BG_DARK)
        
        # Header
        h_frame = tk.Frame(w, bg=BG_HEADER, pady=10)
        h_frame.pack(fill=tk.X)
        
        # Score Color
        color = FG_SAFE if p["score"] > 80 else FG_WARN if p["score"] > 50 else FG_DANGER
        verdict = "TRUSTED IDENTITY" if p["score"] > 80 else "UNKOWN / SUSPICIOUS"
        
        tk.Label(h_frame, text=f"{p['score']}%", font=("Segoe UI", 24, "bold"), fg=color, bg=BG_HEADER).pack()
        tk.Label(h_frame, text=verdict, font=("Segoe UI", 10, "bold"), fg=FG_WHITE, bg=BG_HEADER).pack()

        # Details
        d_frame = tk.Frame(w, bg=BG_DARK, padx=20, pady=20)
        d_frame.pack(fill=tk.BOTH, expand=True)

        def row(label, val, icon_key=None, val_color="white"):
            r = tk.Frame(d_frame, bg=BG_DARK, pady=5)
            r.pack(fill=tk.X)
            if icon_key and icons.get(icon_key):
                tk.Label(r, image=icons[icon_key], bg=BG_DARK).pack(side=tk.LEFT, padx=5)
            tk.Label(r, text=label, width=15, anchor="w", bg=BG_DARK, fg="#95a5a6", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
            tk.Label(r, text=val, bg=BG_DARK, fg=val_color, font=("Segoe UI", 10)).pack(side=tk.LEFT)

        row("Target:", p['email'], "contact")
        row("Domain:", p['domain'], "server_network")
        
        mx_color = FG_SAFE if p['mx_status'] == "Active" else FG_DANGER
        row("Server Status:", p['mx_status'], "link", mx_color)

        if p['is_disposable']:
             row("Type:", "BURNER / TRASH", "delete", FG_DANGER)
        else:
             row("Type:", "Standard Provider", "shield_safe", FG_SAFE)

        grav_text = "Found (Public)" if p['has_gravatar'] else "Hidden / None"
        grav_color = ACCENT if p['has_gravatar'] else "gray"
        row("Social Profile:", grav_text, "globe", grav_color)

        tk.Button(w, text="Close", command=w.destroy, bg=BG_HEADER, fg="white", width=20).pack(pady=10)

# --- GUI ---
class DarkMailApp:
    def __init__(self, root):
        load_settings()
        self.root = root; self.root.title(T("app_title")); self.root.geometry("1100x750")
        app_icon = get_icon("mail")
        if app_icon: self.root.iconphoto(False, app_icon)
        self.setup_theme(); check_files()
        self.profiles = load_json(FILES["profiles"]).get("profiles", {})
        self.contacts = load_json(FILES["contacts"])
        self.servers = load_json(FILES["servers"])
        self.curr_prof = None; self.back = None
        self.auto_refresh_job = None
        self.page = 0
        self.root.bind('<Control-n>', lambda e: self.open_compose())
        self.root.bind('<F5>', lambda e: self.refresh())
        self.root.bind('<Delete>', lambda e: self.delete())
        self.root.bind('<Control-r>', lambda e: self.reply())
        self.root.bind('<Control-f>', lambda e: self.fwd())
        icon_names = ["compose","mask","proxy","link","ghost","copy","refresh","delete","settings","clock","contact","reply","forward","spy","save","import","harvest","eye","key","address_book","add","shield_safe","unlock","paperclip","help","lock","mail", "plus", "question_mark","globe", "pin", "flag_generic", "city", "server_network", "alert", "mobile", "check"]
        icon_names += list(FLAG_ICONS.values())
        self.icons = {}
        for k in icon_names: self.icons[k] = get_icon(k)
        self.show_login()

    def setup_theme(self):
        s = ttk.Style(); s.theme_use('clam')
        self.root.configure(bg=BG_DARK)
        s.configure("TFrame", background=BG_DARK)
        s.configure("TLabel", background=BG_DARK, foreground=FG_WHITE, font=("Segoe UI", 10))
        s.configure("TButton", background=BG_HEADER, foreground=FG_WHITE, borderwidth=1, relief="raised", font=("Segoe UI", 10))
        s.map("TButton", background=[("active", ACCENT)], foreground=[("active", "white")])
        s.configure("Treeview", background="white", fieldbackground="white", foreground="black", font=("Segoe UI", 10), rowheight=25, borderwidth=0)
        s.configure("Treeview.Heading", background=BG_HEADER, foreground=FG_WHITE, font=("Segoe UI", 10, "bold"), relief="flat")
        s.map("Treeview", background=[("selected", ACCENT)], foreground=[("selected", "white")])
        s.configure("TEntry", fieldbackground=BG_LIGHT, foreground=FG_WHITE, borderwidth=0, insertbackground="white")
        s.configure("TCombobox", fieldbackground=BG_LIGHT, foreground=FG_WHITE, background=BG_DARK, borderwidth=0)
        s.configure("TCheckbutton", background=BG_DARK, foreground=FG_WHITE)

    def show_about(self):
        w = tk.Toplevel(self.root); w.title(T("about")); w.geometry("400x320"); w.configure(bg=BG_DARK)
        ttk.Label(w, text="CorreioPro Ultimate", font=("Segoe UI", 16, "bold"), foreground=ACCENT).pack(pady=(20, 10))
        ttk.Label(w, text="Forensics & Encryption", font=("Segoe UI", 10, "italic")).pack(pady=5)
        f_dev = ttk.Frame(w); f_dev.pack(pady=5)
        ttk.Label(f_dev, text="Developer:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        lbl_link = ttk.Label(f_dev, text="github.com/peterpt/EmailPro", font=("Segoe UI", 10), foreground="#3498db", cursor="hand2"); lbl_link.pack(side=tk.LEFT, padx=5)
        lbl_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/peterpt/EmailPro"))
        f_ai = ttk.Frame(w); f_ai.pack(pady=2)
        ttk.Label(f_ai, text="AI Architect:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        ttk.Label(f_ai, text="Gemini AI Model", font=("Segoe UI", 10), foreground="#9b59b6").pack(side=tk.LEFT, padx=5)
        f_icon = ttk.Frame(w); f_icon.pack(pady=2)
        ttk.Label(f_icon, text="Icons:", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        lbl_flati = ttk.Label(f_icon, text="Flaticon.com", font=("Segoe UI", 10), foreground="#e67e22", cursor="hand2"); lbl_flati.pack(side=tk.LEFT, padx=5)
        lbl_flati.bind("<Button-1>", lambda e: webbrowser.open("https://www.flaticon.com"))
        ttk.Label(w, text="Powered by ~1800 lines of Python.", font=("Segoe UI", 8)).pack(side=tk.BOTTOM, pady=20)

    def show_login(self):
        if self.auto_refresh_job: self.root.after_cancel(self.auto_refresh_job)
        for w in self.root.winfo_children(): w.destroy()
        f = ttk.Frame(self.root); f.place(relx=0.5, rely=0.5, anchor="center")
        f_lang = ttk.Frame(self.root); f_lang.place(relx=0.98, rely=0.02, anchor="ne")
        lbl_flag = tk.Label(f_lang, bg=BG_DARK); lbl_flag.pack(side=tk.LEFT, padx=5)
        v_lang = tk.StringVar(); cb_lang = ttk.Combobox(f_lang, textvariable=v_lang, values=list(LANG_MAP.keys()), state="readonly", width=15)
        def update_flag(lang_name):
            iso = LANG_MAP.get(lang_name)
            flag_name = FLAG_ICONS.get(iso)
            if self.icons.get(flag_name): lbl_flag.config(image=self.icons[flag_name])
            else: lbl_flag.config(image="")
        for k, v in LANG_MAP.items():
            if v == CURRENT_LANG: cb_lang.set(k); v_lang.set(k); update_flag(k)
        def change_lang(e):
            code = LANG_MAP[cb_lang.get()]; save_settings(code); update_flag(cb_lang.get()); self.show_login() 
        cb_lang.bind("<<ComboboxSelected>>", change_lang); cb_lang.pack(side=tk.LEFT)
        ttk.Label(f, text=T("login_title"), font=("Segoe UI", 20, "bold"), foreground=ACCENT).pack(pady=20)
        self.v_prof = tk.StringVar(); cb = ttk.Combobox(f, textvariable=self.v_prof, values=list(self.profiles.keys()), state="readonly", width=30)
        cb.set(''); cb.pack(pady=10)
        bf = ttk.Frame(f); bf.pack(pady=20)
        ttk.Button(bf, text=T("connect"), command=self.do_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(bf, text=T("manage_profiles"), command=self.edit_profs).pack(side=tk.LEFT, padx=5)
        if self.icons.get("spy"): ttk.Button(self.root, text=T("analyze_file"), image=self.icons["spy"], compound=tk.LEFT, command=self.load_external_file).place(relx=0.5, rely=0.98, anchor="s")
        else: ttk.Button(self.root, text=T("analyze_file"), command=self.load_external_file).place(relx=0.5, rely=0.98, anchor="s")
        ttk.Button(self.root, text=T("about"), command=self.show_about, width=6).place(relx=0.98, rely=0.98, anchor="se")

    def open_burner(self):
        burner = BurnerMail(self.root, self.icons)
        burner.start()

    def do_login(self):
        n = self.v_prof.get(); 
        if not n: messagebox.showwarning(T("auth_title"), T("select_prof")); return
        p_data = self.profiles[n]
        if "pin_hash" in p_data and p_data["pin_hash"]:
            pin = simpledialog.askstring(T("pin_title"), T("pin_ask"), show="*", parent=self.root)
            if not pin or not security.verify_pin(pin, p_data["pin_hash"]): messagebox.showerror(T("error"), T("pin_wrong")); return
        pwd = None
        if "encrypted_password" in p_data: pwd = security.decrypt(p_data["encrypted_password"])
        if not pwd: pwd = simpledialog.askstring(T("auth_title"), f"{T('pass_ask')} {n}:", show="*", parent=self.root)
        if pwd:
            self.curr_prof = p_data; self.back = EmailBackend(p_data, pwd, self.log)
            try: self.back.conn_imap().logout(); self.main_ui()
            except Exception as e: messagebox.showerror(T("error"), str(e))

    def load_external_file(self):
        fn = filedialog.askopenfilename(filetypes=[("Email File", "*.eml")])
        if not fn: return
        try:
            with open(fn, "rb") as f:
                raw_bytes = f.read(); msg = email.message_from_bytes(raw_bytes); self.show_forensic_window(msg)
        except Exception as e: messagebox.showerror(T("error"), str(e))

    def show_forensic_window(self, msg_obj):
        score, report, geo = EmailForensics.analyze(msg_obj)
        win = tk.Toplevel(self.root); win.title(T("forensic_title")); win.geometry("550x550"); win.configure(bg=BG_DARK)
        color = FG_SAFE if score > 80 else FG_WARN if score > 50 else FG_DANGER
        status_text = T("safe") if score > 80 else T("suspect") if score > 50 else T("danger")
        ttk.Label(win, text=f"{T('score')}: {score}/100", font=("Segoe UI", 18, "bold"), foreground=color).pack(pady=(15, 5))
        ttk.Label(win, text=f"{T('verdict')}: {status_text}", font=("Segoe UI", 12), foreground=color).pack(pady=(0, 15))
        t = tk.Text(win, bg=BG_LIGHT, fg=FG_WHITE, font=("Consolas", 10), height=10, padx=10, pady=10, borderwidth=0)
        t.pack(fill=tk.X, padx=10)
        for line in report: t.insert(tk.END, "• " + line + "\n\n")
        if geo:
            ttk.Separator(win, orient='horizontal').pack(fill='x', padx=20, pady=10)
            def add_row(icon_key, label, value, val_color="white"):
                row = tk.Frame(win, bg=BG_DARK); row.pack(fill=tk.X, padx=30, pady=2)
                if self.icons.get(icon_key): tk.Label(row, image=self.icons[icon_key], bg=BG_DARK).pack(side=tk.LEFT, padx=(0, 10))
                else: tk.Label(row, text="[?]", bg=BG_DARK, fg="gray").pack(side=tk.LEFT, padx=(0, 10))
                tk.Label(row, text=label, bg=BG_DARK, fg="#bdc3c7", font=("Segoe UI", 10, "bold"), width=15, anchor="w").pack(side=tk.LEFT)
                tk.Label(row, text=value, bg=BG_DARK, fg=val_color, font=("Segoe UI", 10)).pack(side=tk.LEFT)
            h_frame = tk.Frame(win, bg=BG_DARK); h_frame.pack(pady=(5, 10))
            if self.icons.get("globe"): tk.Label(h_frame, image=self.icons["globe"], bg=BG_DARK).pack(side=tk.LEFT, padx=5)
            tk.Label(h_frame, text="ORIGIN TRACE", bg=BG_DARK, fg=ACCENT, font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT)
            add_row("pin", "Source IP:", geo.get('ip'))
            add_row("flag_generic", "Country:", geo.get('country'))
            add_row("city", "City:", geo.get('city'))
            add_row("server_network", "ISP / Org:", f"{geo.get('isp')} / {geo.get('org')}")
            if geo.get('mobile'): add_row("mobile", "Connection:", "Mobile Network", FG_WARN)
            if geo.get('proxy'): add_row("alert", "Threat:", "Proxy/VPN Detected", FG_DANGER)

    def change_page(self, direction):
        new_page = self.page + direction
        if new_page < 0: return
        self.page = new_page
        self.l_page.config(text=f"Page {self.page + 1}")
        self.refresh()

    def main_ui(self):
        for w in self.root.winfo_children(): w.destroy()
        tb = ttk.Frame(self.root, padding=5); tb.pack(fill=tk.X)
        btn = {"compound": tk.LEFT, "width": 0}
        
        ttk.Button(tb, text=T("compose"), image=self.icons["compose"], command=self.open_compose, **btn).pack(side=tk.LEFT, padx=2)
        ttk.Button(tb, text=T("contacts"), image=self.icons["contact"], command=self.open_contacts, **btn).pack(side=tk.LEFT, padx=2)
        ttk.Button(tb, text=T("pgp_keys"), image=self.icons["key"], command=self.open_pgp_manager, **btn).pack(side=tk.LEFT, padx=2)
        
        # --- BURNER BUTTON (NEW) ---
        def open_burner_win():
            b = BurnerMail(self.root, self.icons) 
            b.start()

        if self.icons.get("clock"): 
            ttk.Button(tb, text=T("burner_btn"), image=self.icons["clock"], compound=tk.LEFT, command=open_burner_win).pack(side=tk.LEFT, padx=2)
        else:
            ttk.Button(tb, text=T("burner_btn"), command=open_burner_win).pack(side=tk.LEFT, padx=2)

        # --- SEARCH BOX ---
        f_search = ttk.Frame(tb); f_search.pack(side=tk.LEFT, padx=(20, 0))
        ttk.Label(f_search, text=T("search_lbl"), font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.v_sch = tk.StringVar(); e_sch = ttk.Entry(f_search, textvariable=self.v_sch, width=25); e_sch.pack(side=tk.LEFT)
        
        ttk.Button(tb, text=T("exit"), command=self.show_login).pack(side=tk.RIGHT)
        
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=BG_DARK, sashwidth=4)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        lf = ttk.Frame(paned); paned.add(lf, width=450)
        cb = ttk.Frame(lf); cb.pack(fill=tk.X, pady=5)
        self.v_fld = tk.StringVar(value="INBOX")
        self.cb_f = ttk.Combobox(cb, textvariable=self.v_fld, state="readonly", width=15); self.cb_f.pack(side=tk.LEFT, padx=5)
        def run_refresh(): self.page = 0; self.l_page.config(text="Page 1"); self.refresh()
        self.cb_f.bind("<<ComboboxSelected>>", lambda e: run_refresh()); e_sch.bind("<Return>", lambda e: run_refresh())
        btn_prev = ttk.Button(cb, text=T("prev"), width=3, command=lambda: self.change_page(-1))
        btn_prev.pack(side=tk.LEFT, padx=(5,0)); CreateToolTip(btn_prev, T("prev"))
        self.l_page = ttk.Label(cb, text="Page 1", width=8, anchor="center"); self.l_page.pack(side=tk.LEFT)
        btn_next = ttk.Button(cb, text=T("next"), width=3, command=lambda: self.change_page(1))
        btn_next.pack(side=tk.LEFT, padx=(0,5)); CreateToolTip(btn_next, T("next"))
        btn_refresh = ttk.Button(cb, image=self.icons["refresh"], command=lambda: self.refresh())
        btn_refresh.pack(side=tk.LEFT, padx=5); CreateToolTip(btn_refresh, T("refresh_tip"))
        self.tree = ttk.Treeview(lf, columns=("F", "S", "D"), show="headings")
        self.tree.heading("F", text=T("from"), command=lambda: self.sort_tree("F", False))
        self.tree.heading("S", text=T("subject"), command=lambda: self.sort_tree("S", False))
        self.tree.heading("D", text=T("date"), command=lambda: self.sort_tree("D", False))
        self.tree.column("F", width=120); self.tree.column("S", width=200); self.tree.column("D", width=120, anchor="e")
        self.tree.pack(fill=tk.BOTH, expand=True); self.tree.bind("<<TreeviewSelect>>", self.sel_mail)
        rf = ttk.Frame(paned); paned.add(rf)
        ab = ttk.Frame(rf); ab.pack(fill=tk.X, pady=5)
        ttk.Button(ab, text=T("reply"), image=self.icons["reply"], command=self.reply, **btn).pack(side=tk.LEFT, padx=5)
        ttk.Button(ab, text=T("forward"), image=self.icons["forward"], command=self.fwd, **btn).pack(side=tk.LEFT, padx=5)
        ttk.Button(ab, text=T("forensic"), image=self.icons["spy"], command=self.forensic_scan, **btn).pack(side=tk.LEFT, padx=5)
        ttk.Button(ab, text=T("save"), image=self.icons["save"], command=self.save_email_local, **btn).pack(side=tk.LEFT, padx=5)
        ttk.Button(ab, text=T("delete"), image=self.icons["delete"], command=self.delete, **btn).pack(side=tk.RIGHT, padx=5)
        hf = ttk.Frame(rf, padding=10); hf.pack(fill=tk.X)
        self.l_frm = ttk.Label(hf, text=T("from"), font=("Segoe UI", 10, "bold")); self.l_frm.pack(anchor="w")
        self.l_sub = ttk.Label(hf, text=T("subject"), font=("Segoe UI", 11)); self.l_sub.pack(anchor="w")
        txt_frame = ttk.Frame(rf); txt_frame.pack(fill=tk.BOTH, expand=True)
        sb = ttk.Scrollbar(txt_frame, orient="vertical"); sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt = tk.Text(txt_frame, bg=BG_LIGHT, fg=FG_WHITE, font=("Consolas", 10), padx=10, pady=10, yscrollcommand=sb.set)
        self.txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); sb.config(command=self.txt.yview)
        self.stat = ttk.Label(self.root, text=T("ready"), background=BG_HEADER); self.stat.pack(side=tk.BOTTOM, fill=tk.X)
        self.load_from_cache(); threading.Thread(target=self.load_flds, daemon=True).start(); self.refresh(); self.start_auto_refresh()

    def sort_tree(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l): self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

    def log(self, m): 
        now = datetime.datetime.now().strftime("%H:%M")
        
        # Check Connection Mode
        if PROXY_CONFIG["enabled"]:
            mode_txt = " [TOR/PROXY]"
            mode_icon = self.icons.get("proxy") # Use the new Proxy icon
        else:
            mode_txt = " [DIRECT]"
            mode_icon = self.icons.get("globe") # Use Globe icon
            
        # Update Status Bar with Icon + Text
        if mode_icon:
            self.stat.config(text=f" {m} ({now}){mode_txt}", image=mode_icon, compound=tk.LEFT)
        else:
            self.stat.config(text=f"{m} ({now}){mode_txt}")

    def start_auto_refresh(self): self.auto_refresh_job = self.root.after(60000, self.auto_refresh_loop)
    def auto_refresh_loop(self):
        if self.back: threading.Thread(target=lambda: self.refresh(silent=True), daemon=True).start()
        self.start_auto_refresh()
    def load_flds(self): fs = self.back.list_folders(); self.root.after(0, lambda: self.cb_f.config(values=fs))

    def load_from_cache(self):
        # USE SECURE LOAD
        raw = security.load_encrypted_json(FILES["cache"])
        
        if raw:
            self.emails = raw
            for i in self.tree.get_children(): self.tree.delete(i)
            
            is_sent_folder = any(x in self.v_fld.get().lower() for x in ['sent', 'enviados', 'outbox', 'itens enviados'])
            if is_sent_folder: self.tree.heading("F", text=T("to"))
            else: self.tree.heading("F", text=T("from"))

            for x, e in enumerate(self.emails):
                display = e['to_full'] if is_sent_folder else e['from_short']
                self.tree.insert("", "end", iid=x, values=(display, e['subject'], e['date']), tags=('cached',))
            
            self.tree.tag_configure('cached', foreground='#95a5a6')
            self.log(f"Loaded {len(self.emails)} emails from Secure Vault")

    def refresh(self, silent=False):
        f = self.v_fld.get(); s = self.v_sch.get()
        is_sent_folder = any(x in f.lower() for x in ['sent', 'enviados', 'outbox', 'itens enviados'])
        if is_sent_folder: self.tree.heading("F", text=T("to"))
        else: self.tree.heading("F", text=T("from"))
        def t():
            if not silent: self.log(T("loading"))
            es = self.back.fetch(f, self.page, 30, s); self.emails = es
            cache_data = []
            for e in es:
                item = e.copy()
                if 'raw_msg' in item: del item['raw_msg']
                if 'raw_bytes' in item: del item['raw_bytes']
                clean_atts = []
                for a in item['attachments']: clean_atts.append({'name': a['name'], 'data': None}) 
                item['attachments'] = clean_atts
                cache_data.append(item)
            if self.page == 0: security.save_encrypted_json(FILES["cache"], cache_data)
            def up():
                for i in self.tree.get_children(): self.tree.delete(i)
                for x, e in enumerate(es): 
                    display = e['to_full'] if is_sent_folder else e['from_short']
                    self.tree.insert("", "end", iid=x, values=(display, e['subject'], e['date']))
                if not silent: self.log(f"{len(es)} {T('loaded')}")
            self.root.after(0, up)
        threading.Thread(target=t, daemon=True).start()

    def sel_mail(self, e):
        s = self.tree.selection()
        if not s: return
        em = self.emails[int(s[0])]
        
        # 1. Update Header Labels
        header_text = f"{T('from')} {em['from_full']}"
        if em.get('to_full'): header_text += f"  |  {T('to')} {em['to_full']}"
        self.l_frm.config(text=header_text)
        self.l_sub.config(text=f"{T('subject')} {em['subject']}")
        
        # 2. Reset Text Area
        self.txt.delete(1.0, tk.END)
        
        # --- FEATURE: IDENTITY PROFILER BUTTON ---
        sender_email = re.search(r'[\w\.-]+@[\w\.-]+', em['from_full'])
        sender_email = sender_email.group(0) if sender_email else ""
        
        if sender_email:
            def run_profile(): IdentityProfiler.show_window(self.root, sender_email, self.icons)
            
            f_id = tk.Frame(self.txt, bg=BG_LIGHT, pady=5)
            self.txt.window_create("1.0", window=f_id)
            
            if self.icons.get("contact"):
                tk.Button(f_id, text=f" Verify Identity: {sender_email}", image=self.icons["contact"], compound=tk.LEFT, bg="#2980b9", fg="white", command=run_profile, font=("Segoe UI", 9, "bold")).pack(anchor="w")
            else:
                tk.Button(f_id, text=f"🆔 Verify Identity: {sender_email}", bg="#2980b9", fg="white", command=run_profile).pack(anchor="w")
            
            self.txt.insert(tk.END, "\n")

        # 3. Insert Email Body
        self.txt.insert(tk.END, em['body'])
        btn_cfg = {"compound": tk.LEFT}

        # --- FEATURE: TEXT STEGANOGRAPHY ---
        if Stego.decode(em['body']):
            def show_secret(): messagebox.showinfo("Secret", Stego.decode(em['body']))
            self.txt.window_create(tk.END, window=tk.Button(self.txt, text=T("stego_found"), bg=FG_WARN, fg="black", command=show_secret))
            self.txt.insert(tk.END, "\n")

        # --- FEATURE: LINK HUNTER --- 
        urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*', em['body'])
        if urls:
            def scan_links():
                scan_win = tk.Toplevel(self.root); scan_win.title("Link Hunter"); scan_win.geometry("700x450"); scan_win.configure(bg=BG_DARK)
                res_txt = tk.Text(scan_win, bg=BG_LIGHT, fg=FG_WHITE, font=("Consolas", 10), padx=10, pady=10); res_txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                def add_result(icon_name, text, color="white"):
                    if not scan_win.winfo_exists(): return
                    res_txt.insert(tk.END, "\n")
                    if self.icons.get(icon_name): res_txt.window_create(tk.END, window=tk.Label(res_txt, image=self.icons[icon_name], bg=BG_LIGHT)); res_txt.insert(tk.END, "  ")
                    else: res_txt.insert(tk.END, "[*] ")
                    res_txt.insert(tk.END, text + "\n"); tag=f"c_{random.randint(0,99)}"; res_txt.tag_add(tag, "end-2l", "end-1c"); res_txt.tag_config(tag, foreground=color); res_txt.see(tk.END)
                def run_check():
                    mode = "Proxy/Tor" if PROXY_CONFIG['enabled'] else "Direct"
                    scan_win.after(0, lambda: res_txt.insert(tk.END, f"Scanning {len(urls)} links via {mode}...\n------------------\n"))
                    for u in urls:
                        try:
                            proxies = {'http': f"socks5h://{PROXY_CONFIG['ip']}:{PROXY_CONFIG['port']}", 'https': f"socks5h://{PROXY_CONFIG['ip']}:{PROXY_CONFIG['port']}"} if PROXY_CONFIG["enabled"] else {}
                            resp = requests.head(u, allow_redirects=True, timeout=5, proxies=proxies)
                            icon = "alert" if resp.url != u else "shield_safe" if resp.status_code < 400 else "alert"
                            color = ACCENT if resp.url != u else FG_SAFE if resp.status_code < 400 else FG_DANGER
                            scan_win.after(0, lambda i=icon, t=f"{resp.status_code} {resp.url}", c=color: add_result(i, t, c))
                        except Exception as e: scan_win.after(0, lambda: add_result("alert", str(e)[:50], FG_DANGER))
                threading.Thread(target=run_check, daemon=True).start()

            f_lnk = tk.Frame(self.txt, bg=BG_LIGHT, pady=2); self.txt.window_create(tk.END, window=f_lnk)
            if self.icons.get("link"): tk.Button(f_lnk, text=f" Scan {len(urls)} Links", image=self.icons["link"], compound=tk.LEFT, bg="#e67e22", fg="white", command=scan_links).pack(anchor="w")
            else: tk.Button(f_lnk, text=f"🔍 Scan {len(urls)} Links", bg="#e67e22", fg="white", command=scan_links).pack(anchor="w")
            self.txt.insert(tk.END, "\n")

        # --- FEATURE: HTML VIEWERS ---
        if em['html']:
            def opn_safe():
                h = re.sub(r'<img[^>]*>', '<!-- IMG -->', em['html'], flags=re.IGNORECASE)
                with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f: f.write(h); webbrowser.open('file://'+f.name)
            def opn_full():
                with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f: f.write(em['html']); webbrowser.open('file://'+f.name)
            
            self.txt.insert(tk.END, "\n\n"); f_btns = tk.Frame(self.txt, bg=BG_LIGHT); self.txt.window_create(tk.END, window=f_btns)
            if self.icons.get("shield_safe"): tk.Button(f_btns, text=T("safe_view"), image=self.icons["shield_safe"], bg="#27ae60", fg="white", command=opn_safe, **btn_cfg).pack(side=tk.LEFT, padx=5)
            else: tk.Button(f_btns, text=T("safe_view"), bg="#27ae60", fg="white", command=opn_safe).pack(side=tk.LEFT, padx=5)
            if self.icons.get("unlock"): tk.Button(f_btns, text=T("full_view"), image=self.icons["unlock"], bg="#f39c12", fg="black", command=opn_full, **btn_cfg).pack(side=tk.LEFT)
            else: tk.Button(f_btns, text=T("full_view"), bg="#f39c12", fg="black", command=opn_full).pack(side=tk.LEFT)

        # --- FEATURE: PGP ---
        if "-----BEGIN PGP MESSAGE-----" in em['body']:
            def decrypt_msg():
                pwd = simpledialog.askstring("PGP", T("pass_ask"), show="*")
                if pwd:
                    dec = security.decrypt_pgp_message(em['body'], pwd, my_email=self.curr_prof['email'])
                    self.txt.delete(1.0, tk.END); self.txt.insert(tk.END, "\n[DECRYPTED]\n" + dec)
            self.txt.insert(tk.END, "\n")
            if self.icons.get("unlock"): self.txt.window_create(tk.END, window=tk.Button(self.txt, text=T("decrypt_btn"), image=self.icons["unlock"], bg="#9b59b6", fg="white", command=decrypt_msg, **btn_cfg))
            else: self.txt.window_create(tk.END, window=tk.Button(self.txt, text=T("decrypt_btn"), bg="#9b59b6", fg="white", command=decrypt_msg))

        # --- FEATURE: ATTACHMENTS (UPDATED WITH SCANNER) ---
        if em['attachments']: 
            self.txt.insert(tk.END, "\n\n--------------------------------------------------\n"); self.txt.insert(tk.END, f"📎 {len(em['attachments'])} {T('files')}:\n")
            
            def save_att(data, name):
                if data is None: messagebox.showwarning("Offline", "Offline Mode"); return
                clean = "".join([c for c in name if c.isalnum() or c in "._-"])
                fn = filedialog.asksaveasfilename(initialfile=clean)
                if fn: 
                    with open(fn, "wb") as f: f.write(data)
                    messagebox.showinfo("OK", "Saved")
            
            # New Scan Function
            def scan_att(data):
                if data is None: return
                res = Stego.extract_image(data)
                if res: messagebox.showinfo("SECRET FOUND!", f"Hidden Message:\n\n{res}")
                else: messagebox.showinfo("Scan", "No hidden steganography detected in this file.")

            for att in em['attachments']:
                f_att = tk.Frame(self.txt, bg=BG_LIGHT); self.txt.window_create(tk.END, window=f_att)
                lbl = f"Save: {att['name']}" if att['data'] else f"{att['name']} (Offline)"
                
                # Save Button
                if self.icons.get("save"): tk.Button(f_att, text=lbl, image=self.icons["save"], compound=tk.LEFT, command=lambda a=att: save_att(a['data'], a['name']), bg="#34495e", fg="white").pack(side=tk.LEFT, padx=5)
                else: tk.Button(f_att, text=lbl, command=lambda a=att: save_att(a['data'], a['name']), bg="#34495e", fg="white").pack(side=tk.LEFT, padx=5)
                
                # Scan Button (Only if data exists)
                if att['data']:
                    if self.icons.get("eye"): tk.Button(f_att, image=self.icons["eye"], command=lambda a=att: scan_att(a['data']), bg="#e67e22").pack(side=tk.LEFT)
                    else: tk.Button(f_att, text="Scan", command=lambda a=att: scan_att(a['data']), bg="#e67e22", fg="white").pack(side=tk.LEFT)

                self.txt.insert(tk.END, "\n")

    def open_compose(self, to="", sub="", body="", atts=[]):
        w = tk.Toplevel(self.root); w.title(T("compose")); w.geometry("650x750"); w.configure(bg=BG_DARK)
        f = ttk.Frame(w, padding=15); f.pack(fill=tk.BOTH, expand=True)
        
        # --- HEADER ---
        r1 = ttk.Frame(f); r1.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(r1, text=T("to"), width=8, anchor="w").pack(side=tk.LEFT)
        e_to = ttk.Entry(r1); e_to.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5); e_to.insert(0, to)
        CreateToolTip(e_to, T("multi_send_help"))
        if self.icons.get("address_book"): ttk.Button(r1, image=self.icons["address_book"], command=lambda: self.pick_c(e_to), width=3).pack(side=tk.LEFT)
        else: ttk.Button(r1, text="...", width=3, command=lambda: self.pick_c(e_to)).pack(side=tk.LEFT)
        
        r2 = ttk.Frame(f); r2.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(r2, text=T("subject"), width=8, anchor="w").pack(side=tk.LEFT)
        e_s = ttk.Entry(r2); e_s.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5); e_s.insert(0, sub)
        
        # --- EDITOR ---
        t = tk.Text(f, bg=BG_LIGHT, fg=FG_WHITE, height=15, font=("Consolas", 10), borderwidth=0, padx=10, pady=10)
        t.pack(fill=tk.BOTH, expand=True)
        if len(body) < 5: 
            sig = self.curr_prof.get("signature", "")
            if sig: t.insert(tk.END, "\n\n" + sig)
        else: t.insert(1.0, body)

        # --- CONTROLS ---
        ctrl_frame = tk.Frame(f, bg=BG_DARK, pady=10); ctrl_frame.pack(fill=tk.X)
        f_opts = tk.Frame(ctrl_frame, bg=BG_DARK); f_opts.pack(side=tk.LEFT, anchor="n")
        
        v_pgp = tk.BooleanVar(value=False); v_receipt = tk.BooleanVar(value=False)
        c1 = tk.Checkbutton(f_opts, text=T("encrypt_pgp"), variable=v_pgp, bg=BG_DARK, fg="white", selectcolor=BG_DARK, activebackground=BG_DARK, anchor="w"); c1.pack(fill=tk.X, pady=2)
        c2 = tk.Checkbutton(f_opts, text=T("receipt"), variable=v_receipt, bg=BG_DARK, fg="white", selectcolor=BG_DARK, activebackground=BG_DARK, anchor="w"); c2.pack(fill=tk.X, pady=2)

        # --- SPY TOOLS COLUMN ---
        f_spy = tk.Frame(ctrl_frame, bg=BG_DARK); f_spy.pack(side=tk.RIGHT, anchor="n")

        # 1. Text Stego
        def insert_stego():
            secret = simpledialog.askstring("Stego", "Secret Message:", parent=w)
            if secret:
                current_text = t.get("1.0", tk.END).strip(); hidden_text = Stego.encode(secret)
                t.delete("1.0", tk.END); t.insert("1.0", current_text + hidden_text)
                messagebox.showinfo("Stego", "Secret hidden in text!", parent=w)
        
        icon_stego = self.icons.get("eye")
        btn_stego = tk.Button(f_spy, text=f" {T('stego_btn')}", image=icon_stego, compound=tk.LEFT, command=insert_stego, bg=BG_HEADER, fg="white", relief="flat", width=160, anchor="w", padx=10) if icon_stego else tk.Button(f_spy, text=T("stego_btn"), command=insert_stego, bg=BG_HEADER, fg="white", width=20)
        btn_stego.pack(pady=2)

        # 2. AI Camouflage
        def run_camo():
            raw = t.get("1.0", tk.END); poisoned = ""
            for char in raw:
                poisoned += char
                if char.isalnum() and random.random() > 0.5: poisoned += '\u200c' 
            t.delete("1.0", tk.END); t.insert("1.0", poisoned)
            messagebox.showinfo("Camouflage", "Text Poisoned.", parent=w)

        icon_camo = self.icons.get("mask") or self.icons.get("spy")
        btn_camo = tk.Button(f_spy, text=" AI Camouflage", image=icon_camo, compound=tk.LEFT, command=run_camo, bg=BG_HEADER, fg="white", relief="flat", width=160, anchor="w", padx=10) if icon_camo else tk.Button(f_spy, text="🦎 AI Camouflage", command=run_camo, bg=BG_HEADER, fg="white", width=20)
        btn_camo.pack(pady=2)

        # 3. IMAGE INJECTOR
        ats = list(atts) 
        
        def run_img_inject():
            fn = filedialog.askopenfilename(title="Select Image to Inject", filetypes=[("Images", "*.jpg *.jpeg *.png *.gif *.bmp")])
            if not fn: return
            sec = simpledialog.askstring("Inject", "Enter Secret Message:", parent=w)
            if not sec: return
            new_data = Stego.inject_image(fn, sec)
            if new_data:
                path, ext = os.path.splitext(fn)
                new_fn = path + "_SECRET" + ext
                with open(new_fn, "wb") as f: f.write(new_data)
                ats.append(new_fn)
                l_a.config(text=f"{len(ats)} {T('files')}")
                messagebox.showinfo("Injected", f"Created & Attached:\n{os.path.basename(new_fn)}", parent=w)
            else:
                messagebox.showerror("Error", "Injection Failed", parent=w)

        icon_inj = self.icons.get("plus") 
        btn_inj = tk.Button(f_spy, text=" Image Injector", image=icon_inj, compound=tk.LEFT, command=run_img_inject, bg=BG_HEADER, fg="white", relief="flat", width=160, anchor="w", padx=10) if icon_inj else tk.Button(f_spy, text="🖼️ Image Injector", command=run_img_inject, bg=BG_HEADER, fg="white", width=20)
        btn_inj.pack(pady=2)

        # --- FOOTER ---
        bot_frame = tk.Frame(f, bg=BG_DARK, pady=10); bot_frame.pack(fill=tk.X, side=tk.BOTTOM)
        l_a = ttk.Label(bot_frame, text=f"{len(ats)} {T('files')}")
        def add(): fs = filedialog.askopenfilenames(parent=w); ats.extend(fs); l_a.config(text=f"{len(ats)} {T('files')}")
        
        ttk.Button(bot_frame, text=T("attach"), command=add, width=10).pack(side=tk.LEFT); l_a.pack(side=tk.LEFT, padx=10)

        # Send Logic
        def snd(): 
            final_to = e_to.get().strip()
            final_sub = e_s.get()
            final_body = t.get(1.0, tk.END)
            req_rec = v_receipt.get()
            
            # --- PGP LOGIC (SAFETY CHECK) ---
            if v_pgp.get():
                # Check for multiple recipients
                if "," in final_to or ";" in final_to:
                    messagebox.showwarning("PGP Limitation", "Cannot encrypt for multiple recipients at once.\nPlease send individual emails for PGP safety.", parent=w)
                    return

                if final_to not in security.pgp_keyring["public_keys"]:
                    messagebox.showerror(T("error"), f"PGP Public Key Missing!\n\nYou must import the Public Key for:\n{final_to}", parent=w)
                    return

                enc_body = security.encrypt_pgp_message(final_body, final_to)
                if enc_body: final_body = enc_body
                else: 
                    messagebox.showerror(T("error"), "PGP Encryption Failed.", parent=w); return
            # --------------------------------

            w.destroy()
            threading.Thread(target=lambda: self._send_thread(final_to, final_sub, final_body, ats, req_rec)).start()

        ttk.Button(bot_frame, text=T("send"), command=snd, width=15).pack(side=tk.RIGHT)

        def check_recipient_key(event=None):
            recip = e_to.get().strip()
            if recip in security.pgp_keyring["public_keys"]: v_pgp.set(True); c1.config(fg=FG_SAFE, text=f"{T('encrypt_pgp')} (OK)")
            else: v_pgp.set(False); c1.config(fg="white", text=T("encrypt_pgp"))
        e_to.bind("<FocusOut>", check_recipient_key)

    def _send_thread(self, to, sub, body, atts, req_rec):
        wait_win = tk.Toplevel(self.root); wait_win.title(T("wait")); wait_win.geometry("300x120"); wait_win.configure(bg=BG_DARK)
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 60
        wait_win.geometry(f"+{x}+{y}")
        ttk.Label(wait_win, text=T("sending"), font=("Segoe UI", 12)).pack(pady=20)
        bar = ttk.Progressbar(wait_win, mode='indeterminate', length=200); bar.pack(pady=10); bar.start(10)
        ok, msg = self.back.send(to, sub, body, atts, request_receipt=req_rec)
        wait_win.destroy()
        if ok: messagebox.showinfo(T("success"), msg, parent=self.root)
        else: messagebox.showerror(T("error"), msg, parent=self.root)

    def save_email_local(self):
        sel = self.tree.selection()
        if not sel: return
        if not os.path.exists("Saved_Emails"): os.makedirs("Saved_Emails")
        saved_count = 0
        
        for item in sel:
            idx = int(item)
            email_obj = self.emails[idx]
            
            # Check offline status
            if 'raw_bytes' not in email_obj:
                messagebox.showwarning("Offline", "Cannot save offline email to EML. Please refresh.")
                return

            # --- GENERATE SMART FILENAME ---
            # 1. Clean Sender (Alphanumeric only)
            sender = "".join([c for c in email_obj['from_short'] if c.isalnum()])[:15]
            if not sender: sender = "Unknown"
            
            # 2. Clean Subject
            subject = "".join([c for c in email_obj['subject'] if c.isalnum()])[:20]
            if not subject: subject = "NoSubject"
            
            # 3. Timestamp (to ensure uniqueness)
            ts = int(time.time())
            
            default_name = f"{sender}_{subject}_{ts}.eml"
            
            # Open Save Dialog with the smart name pre-filled
            filename = filedialog.asksaveasfilename(
                initialdir="Saved_Emails", 
                initialfile=default_name, 
                title="Save Email", 
                filetypes=[("EML File", "*.eml")]
            )
            
            if filename:
                try:
                    with open(filename, "wb") as f: 
                        f.write(email_obj['raw_bytes'])
                    saved_count += 1
                except Exception as e: 
                    print(f"Error: {e}")
                    
        if saved_count > 0:
            messagebox.showinfo(T("save"), f"{saved_count} saved successfully!")
            
    def forensic_scan(self):
        s = self.tree.selection()
        if not s: return
        em = self.emails[int(s[0])]
        if 'raw_msg' not in em: messagebox.showinfo("Offline", "Forensic scan requires live connection. Please refresh."); return
        score, report, geo = EmailForensics.analyze(em['raw_msg'])
        win = tk.Toplevel(self.root); win.title(T("forensic_title")); win.geometry("550x550"); win.configure(bg=BG_DARK)
        color = FG_SAFE if score > 80 else FG_WARN if score > 50 else FG_DANGER
        status_text = T("safe") if score > 80 else T("suspect") if score > 50 else T("danger")
        ttk.Label(win, text=f"{T('score')}: {score}/100", font=("Segoe UI", 18, "bold"), foreground=color).pack(pady=(15, 5))
        ttk.Label(win, text=f"{T('verdict')}: {status_text}", font=("Segoe UI", 12), foreground=color).pack(pady=(0, 15))
        t = tk.Text(win, bg=BG_LIGHT, fg=FG_WHITE, font=("Consolas", 10), height=10, padx=10, pady=10, borderwidth=0)
        t.pack(fill=tk.X, padx=10)
        for line in report: t.insert(tk.END, "• " + line + "\n\n")
        if geo:
            ttk.Separator(win, orient='horizontal').pack(fill='x', padx=20, pady=10)
            def add_row(icon_key, label, value, val_color="white"):
                row = tk.Frame(win, bg=BG_DARK); row.pack(fill=tk.X, padx=30, pady=2)
                if self.icons.get(icon_key): tk.Label(row, image=self.icons[icon_key], bg=BG_DARK).pack(side=tk.LEFT, padx=(0, 10))
                else: tk.Label(row, text="[?]", bg=BG_DARK, fg="gray").pack(side=tk.LEFT, padx=(0, 10))
                tk.Label(row, text=label, bg=BG_DARK, fg="#bdc3c7", font=("Segoe UI", 10, "bold"), width=15, anchor="w").pack(side=tk.LEFT)
                tk.Label(row, text=value, bg=BG_DARK, fg=val_color, font=("Segoe UI", 10)).pack(side=tk.LEFT)
            h_frame = tk.Frame(win, bg=BG_DARK); h_frame.pack(pady=(5, 10))
            if self.icons.get("globe"): tk.Label(h_frame, image=self.icons["globe"], bg=BG_DARK).pack(side=tk.LEFT, padx=5)
            tk.Label(h_frame, text="ORIGIN TRACE", bg=BG_DARK, fg=ACCENT, font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT)
            add_row("pin", "Source IP:", geo.get('ip'))
            add_row("flag_generic", "Country:", geo.get('country'))
            add_row("city", "City:", geo.get('city'))
            add_row("server_network", "ISP / Org:", f"{geo.get('isp')} / {geo.get('org')}")
            if geo.get('mobile'): add_row("mobile", "Connection:", "Mobile Network", FG_WARN)
            if geo.get('proxy'): add_row("alert", "Threat:", "Proxy/VPN Detected", FG_DANGER)       

    def delete(self):
        # Get all selected items (tuple)
        selected_items = self.tree.selection()
        
        if selected_items and messagebox.askyesno(T("confirm"), T("delete_confirm")): 
            
            def run_delete_loop():
                # Loop through every selected item
                for item in selected_items:
                    try:
                        # The Treeview ID (item) matches the index in self.emails
                        index = int(item)
                        email_uid = self.emails[index]['id']
                        current_folder = self.v_fld.get()
                        
                        # Call backend delete for this specific ID
                        self.back.delete(current_folder, email_uid)
                    except Exception as e:
                        print(f"Error deleting item {item}: {e}")
                
                # Refresh UI only once after all deletions are done
                self.refresh()

            # Run the loop in a background thread so the app doesn't freeze
            threading.Thread(target=run_delete_loop, daemon=True).start()

    def reply(self):
        s = self.tree.selection()
        if s: 
            org = self.emails[int(s[0])]; rto = org['from_full'].split("<")[1].strip(">") if "<" in org['from_full'] else org['from_full']
            sig = self.curr_prof.get("signature", "")
            self.open_compose(rto, f"Re: {org['subject']}", f"\n\n{sig}\n\n> -------- Original --------\n> {org['from_full']}:\n> {org['body'][:200]}...")

    def fwd(self):
        s = self.tree.selection()
        if s:
            org = self.emails[int(s[0])]; tfs = []
            if 'raw_bytes' in org:
                for a in org['attachments']:
                    t = tempfile.NamedTemporaryFile(delete=False, suffix="_"+a['name']); t.write(a['data']); t.close(); tfs.append(t.name)
            sig = self.curr_prof.get("signature", "")
            self.open_compose("", f"Fwd: {org['subject']}", f"\n\n{sig}\n\n> Fwd: {org['subject']}\n\n{org['body']}", tfs)

    def open_pgp_manager(self):
        w = tk.Toplevel(self.root); w.title("PGP"); w.geometry("600x500"); w.configure(bg=BG_DARK)
        tabs = ttk.Notebook(w); tabs.pack(fill=tk.BOTH, expand=True)
        t_list = ttk.Frame(tabs); tabs.add(t_list, text="Keys")
        t_gen = ttk.Frame(tabs); tabs.add(t_gen, text="Generate")
        t_imp = ttk.Frame(tabs); tabs.add(t_imp, text="Import")
        lb = tk.Listbox(t_list, bg=BG_LIGHT, fg=FG_WHITE); lb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # --- NEW: Only show keys for CURRENT profile or Global ---
        current_email = self.curr_prof.get("email", "")
        if current_email in security.pgp_keyring["private_keys"]:
            lb.insert(tk.END, f"🔑 Private: {current_email} (ACTIVE)")
        for k_email in security.pgp_keyring["private_keys"]:
            if k_email != current_email: lb.insert(tk.END, f"🔒 Private: {k_email}")
        for email_k in security.pgp_keyring["public_keys"]: lb.insert(tk.END, f"🌍 Public: {email_k}")
        
        def copy_public():
            if current_email in security.pgp_keyring["public_keys"]:
                pub = security.pgp_keyring["public_keys"][current_email]
                w.clipboard_clear(); w.clipboard_append(pub); messagebox.showinfo(T("success"), "Copied!")
            else: messagebox.showwarning("Error", "No Public Key for this profile.")
        
        ttk.Button(t_list, text="Copy My Public Key", command=copy_public).pack(pady=10)
        ttk.Label(t_gen, text=T("pgp_your_name")).pack(pady=5); e_n = ttk.Entry(t_gen); e_n.pack()
        ttk.Label(t_gen, text=T("pgp_your_email")).pack(pady=5); e_e = ttk.Entry(t_gen); e_e.pack()
        e_e.insert(0, current_email)
        ttk.Label(t_gen, text=T("pgp_passphrase")).pack(pady=5); e_p = ttk.Entry(t_gen, show="*"); e_p.pack()
        def run_gen():
            if not e_n.get() or not e_e.get() or not e_p.get(): return
            ok, msg = security.generate_pgp_key(e_n.get(), e_e.get(), e_p.get())
            if ok: messagebox.showinfo(T("success"), msg); w.destroy()
            else: messagebox.showerror(T("error"), msg)
        ttk.Button(t_gen, text="Generate (RSA 4096)", command=run_gen).pack(pady=20)
        ttk.Label(t_imp, text="Email:").pack(pady=5); e_ie = ttk.Entry(t_imp); e_ie.pack()
        ttk.Label(t_imp, text="Block:").pack(pady=5); t_block = tk.Text(t_imp, height=10, bg=BG_LIGHT, fg=FG_WHITE); t_block.pack(fill=tk.BOTH, padx=10)
        def run_imp():
            if security.import_public_key(e_ie.get(), t_block.get(1.0, tk.END)): messagebox.showinfo(T("success"), "OK"); w.destroy()
            else: messagebox.showerror(T("error"), "Invalid")
        ttk.Button(t_imp, text="Import", command=run_imp).pack(pady=10)

    def pick_c(self, e):
        compose_window = e.winfo_toplevel()
        d = load_json(FILES["contacts"])
        if not d: messagebox.showinfo(T("contacts"), "No contacts found.", parent=compose_window); return
        t = tk.Toplevel(self.root); t.title(T("contacts")); t.geometry("300x400"); t.configure(bg=BG_DARK)
        l = tk.Listbox(t, bg=BG_LIGHT, fg=FG_WHITE, borderwidth=0, highlightthickness=0); l.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        [l.insert(tk.END, m) for m in d.values()]
        def p(): 
            if l.curselection(): e.insert(tk.END, l.get(l.curselection()[0]) + "; "); t.destroy()
        ttk.Button(t, text="Ok", command=p).pack(pady=5)

    def open_contacts(self):
        w = tk.Toplevel(self.root); w.title(T("contacts")); w.geometry("450x450"); w.configure(bg=BG_DARK)
        d = load_json(FILES["contacts"])
        lb = tk.Listbox(w, bg=BG_LIGHT, fg=FG_WHITE); lb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for n, m in d.items(): lb.insert(tk.END, f"{n} <{m}>")
        f = ttk.Frame(w); f.pack(fill=tk.X, padx=10, pady=5)
        e_n = ttk.Entry(f, width=15); e_n.pack(side=tk.LEFT); e_n.insert(0, T("name"))
        e_m = ttk.Entry(f, width=15); e_m.pack(side=tk.LEFT, padx=5); e_m.insert(0, T("email"))
        imp_frame = ttk.Frame(w); imp_frame.pack(pady=5); btn_cfg = {"compound": tk.LEFT} 
        def run_harvest():
            def t():
                count, res = self.back.harvest_contacts()
                if count > 0:
                    d.update(res); save_json(FILES["contacts"], d)
                    w.after(0, lambda: [lb.delete(0, tk.END), [lb.insert(tk.END, f"{k} <{v}>") for k,v in d.items()], messagebox.showinfo(T("success"), f"{count} OK")])
                else: w.after(0, lambda: messagebox.showwarning("!", str(res)))
            threading.Thread(target=t, daemon=True).start()
        if self.icons.get("harvest"): ttk.Button(imp_frame, text=T("harvest_btn"), image=self.icons["harvest"], command=run_harvest, **btn_cfg).pack(side=tk.LEFT, padx=5)
        else: ttk.Button(imp_frame, text=T("harvest_btn"), command=run_harvest).pack(side=tk.LEFT, padx=5)
        def run_import_vcf():
            fn = filedialog.askopenfilename(filetypes=[("vCard", "*.vcf")])
            if fn:
                try:
                    count = 0
                    with open(fn, 'r', encoding='utf-8') as vfile:
                        content = vfile.read(); entries = content.split("BEGIN:VCARD")
                        for entry in entries:
                            name_match = re.search(r"FN:(.*)", entry); email_match = re.search(r"EMAIL.*:(.*)", entry)
                            if name_match and email_match: d[name_match.group(1).strip()] = email_match.group(1).strip(); count += 1
                    if count > 0: save_json(FILES["contacts"], d); lb.delete(0, tk.END); [lb.insert(tk.END, f"{k} <{v}>") for k,v in d.items()]; messagebox.showinfo(T("success"), f"{count} OK")
                except Exception as e: messagebox.showerror(T("error"), str(e))
        if self.icons.get("import"): ttk.Button(imp_frame, text=T("import_btn"), image=self.icons["import"], command=run_import_vcf, **btn_cfg).pack(side=tk.LEFT, padx=5)
        else: ttk.Button(imp_frame, text=T("import_btn"), command=run_import_vcf).pack(side=tk.LEFT, padx=5)
        def add(): d[e_n.get()] = e_m.get(); save_json(FILES["contacts"], d); lb.insert(tk.END, f"{e_n.get()} <{e_m.get()}>")
        def dele(): 
            s = lb.curselection(); 
            if s: del d[lb.get(s[0]).split(" <")[0]]; save_json(FILES["contacts"], d); lb.delete(s[0])
        if self.icons.get("add"): ttk.Button(f, image=self.icons["add"], command=add).pack(side=tk.LEFT)
        else: ttk.Button(f, text="[+]", command=add).pack(side=tk.LEFT)
        ttk.Button(w, text=T("del_sel"), command=dele).pack(pady=5)
        
    def edit_profs(self):
        w = tk.Toplevel(self.root); w.geometry("600x600"); w.configure(bg=BG_DARK); f = ttk.Frame(w, padding=20); f.pack(fill=tk.BOTH, expand=True)
        cb_e = ttk.Combobox(f, values=list(self.profiles.keys()), state="readonly"); cb_e.grid(row=0,column=1); cb_p = ttk.Combobox(f, values=list(self.servers.keys()), state="readonly"); cb_p.grid(row=2,column=1)
        ttk.Label(f, text=T("edit")).grid(row=0,column=0); ttk.Label(f, text=T("preset")).grid(row=2,column=0)
        def add_new_preset():
            d = tk.Toplevel(w); d.title(T("new_preset")); d.configure(bg=BG_DARK); fd = ttk.Frame(d, padding=10); fd.pack()
            e_name = ttk.Entry(fd); e_smtp = ttk.Entry(fd); e_ps = ttk.Entry(fd); e_imap = ttk.Entry(fd); e_pi = ttk.Entry(fd)
            v_s = tk.BooleanVar(value=True); rows = [("Nome", e_name), ("SMTP", e_smtp), ("Porta", e_ps), ("IMAP", e_imap), ("Porta", e_pi)]
            for i, (l, e) in enumerate(rows): ttk.Label(fd, text=l).grid(row=i, column=0); e.grid(row=i, column=1)
            ttk.Checkbutton(fd, text=T("ssl"), variable=v_s).grid(row=5, column=1)
            def save_preset():
                name = e_name.get()
                if name:
                    servers = load_json(FILES["servers"]); servers[name] = {"smtp": e_smtp.get(), "smtp_port": e_ps.get(), "imap": e_imap.get(), "imap_port": e_pi.get(), "ssl": v_s.get()}
                    save_json(FILES["servers"], servers); self.servers = servers
                    cb_p['values'] = list(servers.keys()); cb_p.set(name); messagebox.showinfo(T("success"), f"'{name}' saved!"); d.destroy()
            ttk.Button(fd, text=T("save_btn"), command=save_preset).grid(row=6, column=1, pady=10)
        if self.icons.get("plus"): 
            ttk.Button(f, image=self.icons["plus"], command=add_new_preset).grid(row=2, column=2, padx=5)
        elif self.icons.get("add"): 
            ttk.Button(f, image=self.icons["add"], command=add_new_preset).grid(row=2, column=2, padx=5)
        else: 
            ttk.Button(f, text="[+]", width=3, command=add_new_preset).grid(row=2, column=2, padx=5)
        ents = {}
        for i, k in enumerate(["Nome","Email","Pass","SMTP","P_SMTP","IMAP","P_IMAP"]):
            ttk.Label(f, text=k).grid(row=i+3,column=0)
            if k == "Pass":
                pf = ttk.Frame(f); pf.grid(row=i+3,column=1); e = ttk.Entry(pf, width=25, show="*"); e.pack(side=tk.LEFT)
                def show_help(): messagebox.showinfo(T("pass_help"), T("pass_help_text"))
                # TOOLTIPS HERE
                btn_help = tk.Button(pf, image=self.icons["help"], command=show_help, bg=BG_DARK, relief="flat", cursor="hand2") if self.icons.get("help") else tk.Button(pf, text="[?]", command=show_help, bg=BG_DARK, fg=FG_WARN, relief="flat")
                btn_help.pack(side=tk.LEFT, padx=5); CreateToolTip(btn_help, T("help_icon"))

                btn_eye = tk.Button(pf, image=self.icons["eye"], command=lambda e=e: e.config(show='' if e.cget('show')=='*' else '*'), bg=BG_DARK, relief="flat", cursor="hand2") if self.icons.get("eye") else tk.Button(pf, text="[Show]", command=lambda e=e: e.config(show='' if e.cget('show')=='*' else '*'), bg=BG_DARK, fg="white", relief="flat")
                btn_eye.pack(side=tk.LEFT, padx=5); CreateToolTip(btn_eye, T("show_pass"))
            else: e = ttk.Entry(f, width=30); e.grid(row=i+3,column=1)
            ents[k] = e
        v_ssl = tk.BooleanVar(value=True); ttk.Checkbutton(f, text=T("ssl"), variable=v_ssl).grid(row=10,column=1)
        v_sp = tk.BooleanVar(value=False); ttk.Checkbutton(f, text=T("save_pass"), variable=v_sp).grid(row=11,column=1)
        ttk.Label(f, text="PIN (Op.)").grid(row=12, column=0); e_pin = ttk.Entry(f, show="*"); e_pin.grid(row=12, column=1)
        ttk.Label(f, text=T("signature")).grid(row=13, column=0, sticky="n", pady=10); txt_sig = tk.Text(f, height=5, width=30, bg=BG_LIGHT, fg=FG_WHITE); txt_sig.grid(row=13, column=1, pady=10)
        ttk.Label(f, text=T("proxy_title")).grid(row=14, column=0, pady=(20,0)); pf_proxy = ttk.Frame(f); pf_proxy.grid(row=14, column=1, pady=(20,0))
        v_proxy_en = tk.BooleanVar(value=PROXY_CONFIG["enabled"]); e_p_ip = ttk.Entry(pf_proxy, width=15); e_p_ip.insert(0, PROXY_CONFIG["ip"]); e_p_port = ttk.Entry(pf_proxy, width=6); e_p_port.insert(0, PROXY_CONFIG["port"])
        def toggle_proxy():
            PROXY_CONFIG["enabled"] = v_proxy_en.get(); PROXY_CONFIG["ip"] = e_p_ip.get(); PROXY_CONFIG["port"] = e_p_port.get()
        ttk.Checkbutton(pf_proxy, text=T("proxy_enable"), variable=v_proxy_en, command=toggle_proxy).pack(anchor="w")
        ttk.Label(pf_proxy, text="IP:").pack(side=tk.LEFT); e_p_ip.pack(side=tk.LEFT, padx=2); ttk.Label(pf_proxy, text="Port:").pack(side=tk.LEFT); e_p_port.pack(side=tk.LEFT, padx=2)
        def confirm_wipe():
            if messagebox.askyesno(T("wipe_btn"), T("wipe_confirm"), icon='warning'): security.emergency_wipe()
        if self.icons.get("alert"): tk.Button(f, text=T("wipe_btn"), image=self.icons["alert"], compound=tk.LEFT, command=confirm_wipe, bg=FG_DANGER, fg="white", font=("Segoe UI", 9, "bold")).grid(row=15, column=0, pady=20)
        else: tk.Button(f, text=T("wipe_btn"), command=confirm_wipe, bg=FG_DANGER, fg="white", font=("Segoe UI", 9, "bold")).grid(row=15, column=0, pady=20)
        def load_exist(e):
            n = cb_e.get(); d = self.profiles.get(n)
            if d and "pin_hash" in d and d["pin_hash"]:
                pin = simpledialog.askstring(T("pin_title"), T("pin_ask"), show="*", parent=w)
                if not pin or not security.verify_pin(pin, d["pin_hash"]): messagebox.showerror(T("error"), T("pin_wrong")); cb_e.set(''); return
            if d:
                ents["Nome"].delete(0, tk.END); ents["Nome"].insert(0, n); ents["Email"].delete(0, tk.END); ents["Email"].insert(0, d['email'])
                ents["SMTP"].delete(0, tk.END); ents["SMTP"].insert(0, d['smtp_server']); ents["P_SMTP"].delete(0, tk.END); ents["P_SMTP"].insert(0, d['smtp_port'])
                ents["IMAP"].delete(0, tk.END); ents["IMAP"].insert(0, d['imap_server']); ents["P_IMAP"].delete(0, tk.END); ents["P_IMAP"].insert(0, d['imap_port'])
                v_ssl.set(d['use_ssl']); v_sp.set("encrypted_password" in d); ents["Pass"].delete(0, tk.END); txt_sig.delete(1.0, tk.END)
                if "signature" in d: txt_sig.insert(1.0, d["signature"])
        cb_e.bind("<<ComboboxSelected>>", load_exist)
        def load_preset(e):
            d = self.servers.get(cb_p.get())
            if d:
                ents["SMTP"].delete(0, tk.END); ents["SMTP"].insert(0, d['smtp']); ents["P_SMTP"].delete(0, tk.END); ents["P_SMTP"].insert(0, d['smtp_port'])
                ents["IMAP"].delete(0, tk.END); ents["IMAP"].insert(0, d['imap']); ents["P_IMAP"].delete(0, tk.END); ents["P_IMAP"].insert(0, d['imap_port'])
                v_ssl.set(d['ssl'])
        cb_p.bind("<<ComboboxSelected>>", load_preset)
        def save():
            toggle_proxy(); n = ents["Nome"].get(); d = load_json(FILES["profiles"]); p = d.get("profiles", {}).get(n, {})
            new_p = {"email": ents["Email"].get(), "smtp_server": ents["SMTP"].get(), "smtp_port": ents["P_SMTP"].get(), "imap_server": ents["IMAP"].get(), "imap_port": ents["P_IMAP"].get(), "use_ssl": v_ssl.get(), "signature": txt_sig.get(1.0, tk.END).strip()}
            pin = e_pin.get()
            if pin: new_p["pin_hash"] = security.hash_pin(pin)
            elif "pin_hash" in p: new_p["pin_hash"] = p["pin_hash"]
            raw = ents["Pass"].get()
            if v_sp.get():
                if raw and HAS_CRYPTO: new_p["encrypted_password"] = security.encrypt(raw)
                elif "encrypted_password" in p: new_p["encrypted_password"] = p["encrypted_password"]
            d.setdefault("profiles", {})[n] = new_p; save_json(FILES["profiles"], d); self.profiles = d["profiles"]
            self.show_login(); w.destroy()
        ttk.Button(f, text=T("save_btn"), command=save).grid(row=15,column=1, pady=20)

            

if __name__ == "__main__":
    root = tk.Tk(); app = DarkMailApp(root); root.mainloop()
