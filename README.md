# DOCUMENTATION COMPLÈTE DU PROJET PYTRELLO

## 1. PRÉSENTATION GÉNÉRALE

PyTrello est comme Trello développé en Python avec PyQt5, avec une interface graphique complète pour la gestion de projets selon la méthode Kanban. Cette application permet aux utilisateurs de créer des tableaux, des listes et des cartes pour organiser leurs tâches, avec des fonctionnalités avancées comme le glisser-déposer, les étiquettes, les checklists, et la gestion des dates d'échéance.

## 2. ARCHITECTURE DU PROJET

### 2.1 Structure des fichiers

Le projet est organisé selon une architecture MVC (Modèle-Vue-Contrôleur) adaptée :

- **main.py** : Point d'entrée de l'application
- **main_window.py** : Fenêtre principale qui gère les différentes vues
- **database.py** : Gestion de la base de données SQLite
- **Dossier components/** : Widgets réutilisables (cartes, listes, etc.)
- **Dossier views/** : Vues principales de l'application
- **Dossier models/** : Modèles de données
- **Dossier utils/** : Utilitaires divers
- **Dossier assets/** : Ressources (styles, images, polices)

### 2.2 Base de données

La base de données SQLite comprend les tables suivantes :
- users : Gestion des utilisateurs
- boards : Tableaux de projets
- lists : Listes dans les tableaux
- cards : Cartes dans les listes
- labels : Étiquettes pour les cartes
- card_labels : Association entre cartes et étiquettes
- checklists : Listes de vérification
- checklist_items : Éléments des listes de vérification
- attachments : Pièces jointes

## 3. DESIGN ET INTERFACE UTILISATEUR

### 3.1 Philosophie de design

Le design de PyTrello suit les principes modernes d'UI/UX avec une approche "dark mode" pour réduire la fatigue oculaire. Les choix de design ont été guidés par :

- **Cohérence visuelle** : Palette de couleurs harmonieuse et cohérente
- **Hiérarchie visuelle** : Distinction claire entre les différents niveaux d'information
- **Accessibilité** : Contraste suffisant pour une bonne lisibilité
- **Feedback visuel** : Réactions visuelles aux interactions utilisateur
- **Minimalisme** : Interface épurée sans éléments superflus

### 3.2 Palette de couleurs

- **Fond principal** : #1E1E1E (gris très foncé)
- **Fond secondaire** : #252525 (gris foncé)
- **Accent primaire** : #7C4DFF (violet)
- **Accent secondaire** : #00B8D4 (bleu clair)
- **Cartes** : #2D2D2D (gris moyen)
- **Listes** : #333333 (gris légèrement plus clair)
- **Texte principal** : #FFFFFF (blanc)
- **Texte secondaire** : #B3B3B3 (gris clair)
- **Bordures** : #404040 (gris moyen)
- **Alerte/Erreur** : #FF4081 (rose)

Cette palette offre un bon équilibre entre esthétique moderne et lisibilité, tout en permettant une distinction claire entre les différents éléments de l'interface.

### 3.3 Composants d'interface

- **Header** : Barre supérieure avec logo, titre du tableau actif et boutons d'action
- **Sidebar** : Menu latéral pour la navigation entre les différentes vues
- **Tableaux** : Affichage des tableaux disponibles sous forme de cartes
- **Listes** : Colonnes verticales contenant des cartes
- **Cartes** : Éléments représentant des tâches avec titre, étiquettes et métadonnées
- **Notifications** : Panneau latéral affichant les rappels et alertes
- **Projets du jour** : Panneau affichant les tâches prévues pour la journée

## 4. FONCTIONNALITÉS IMPLÉMENTÉES

### 4.1 Gestion des utilisateurs
- Inscription et connexion
- Gestion de session
- Déconnexion

### 4.2 Tableaux
- Création de tableaux
- Affichage des tableaux de l'utilisateur
- Modification et suppression de tableaux

### 4.3 Listes
- Création de listes dans un tableau
- Renommage et suppression de listes
- Réorganisation des listes (prévu)

### 4.4 Cartes
- Création de cartes dans les listes
- Édition complète (titre, description, date d'échéance)
- Glisser-déposer entre listes
- Affichage des métadonnées (échéance, checklists, pièces jointes)

### 4.5 Étiquettes
- Création d'étiquettes colorées
- Association aux cartes
- Personnalisation des couleurs

### 4.6 Checklists
- Ajout de listes de vérification aux cartes
- Gestion des éléments (ajout, suppression, marquage)
- Suivi de progression

### 4.7 Pièces jointes
- Ajout de fichiers aux cartes
- Gestion des pièces jointes

### 4.8 Vues spéciales
- Vue Calendrier : Affichage des tâches par date
- Vue Chronologie : Affichage chronologique des tâches
- Notifications : Alertes pour les échéances proches
- Projets du jour : Tâches prévues pour la journée

## 5. DÉFIS TECHNIQUES ET SOLUTIONS

### 5.1 Persistance des données
**Défi** : Assurer la persistance des données et gérer les erreurs de connexion à la base de données.
**Solution** : Implémentation d'un système de reconnexion automatique et de gestion d'erreurs robuste dans la classe Database.

### 5.2 Glisser-déposer
**Défi** : Implémenter le glisser-déposer des cartes entre listes.
**Solution** : Utilisation des événements de drag & drop de PyQt5 avec une gestion personnalisée des données transférées.

### 5.3 Interface réactive
**Défi** : Créer une interface fluide et réactive malgré les opérations de base de données.
**Solution** : Optimisation des requêtes et utilisation de signaux pour mettre à jour l'interface de manière asynchrone.

### 5.4 Cohérence visuelle
**Défi** : Maintenir une cohérence visuelle à travers toute l'application.
**Solution** : Création d'un fichier de style centralisé (main.qss) et utilisation de classes CSS cohérentes.

### 5.5 Vue chronologie
**Défi** : Afficher efficacement les tâches sur une chronologie sans surcharger l'interface.
**Solution** : Regroupement des tâches par date et affichage uniquement des dates avec des tâches planifiées.

## 6. AMÉLIORATIONS ET OPTIMISATIONS

### 6.1 Améliorations UI/UX
- Uniformisation des boutons avec la couleur d'accent principale (#7C4DFF)
- Distinction claire entre les cartes (#2D2D2D) et les listes (#333333)
- Ajout d'effets de survol subtils pour améliorer l'expérience utilisateur
- Amélioration du contraste pour une meilleure lisibilité
- Ajout d'icônes et d'indicateurs visuels pour les métadonnées

### 6.2 Optimisations de code
- Refactorisation des composants pour une meilleure réutilisabilité
- Amélioration de la gestion des erreurs
- Optimisation des requêtes à la base de données
- Ajout de méthodes manquantes (rename_list, delete_list, etc.)

### 6.3 Chronologie optimisée
- Affichage uniquement des dates avec des tâches planifiées
- Amélioration du style des tâches dans la vue chronologie
- Boutons d'action plus clairs et cohérents avec le reste de l'interface

## 7. STRATÉGIES DE DÉVELOPPEMENT

### 7.1 Approche itérative
Le développement a suivi une approche itérative, en commençant par les fonctionnalités de base (tableaux, listes, cartes) puis en ajoutant progressivement des fonctionnalités plus avancées (étiquettes, checklists, glisser-déposer).

### 7.2 Modularité
L'architecture du projet favorise la modularité, avec des composants réutilisables et des vues indépendantes. Cela facilite la maintenance et l'évolution du projet.

### 7.3 Séparation des préoccupations
La séparation entre la logique métier (modèles, base de données) et l'interface utilisateur (vues, composants) permet une meilleure organisation du code et facilite les tests.

### 7.4 Design centré utilisateur
Les choix de design et d'interface ont été guidés par les besoins des utilisateurs, avec un focus sur l'ergonomie et la facilité d'utilisation.

## 8. PERSPECTIVES D'ÉVOLUTION

### 8.1 Fonctionnalités futures
- Collaboration en temps réel
- Filtrage et recherche avancée
- Intégration avec d'autres services (calendriers, e-mails)
- Mode hors ligne avec synchronisation
- Personnalisation avancée de l'interface

### 8.2 Améliorations techniques
- Migration vers PyQt6 ou PySide6
- Optimisation des performances pour les grands tableaux
- Tests automatisés
- Packaging pour différentes plateformes

## 9. CONCLUSION

PyTrello est un projet qui démontre les capacités de Python et PyQt5 pour le développement d'applications de bureau modernes et fonctionnelles. L'attention portée au design, à l'expérience utilisateur et à l'architecture logicielle en fait un exemple de bonne pratique pour le développement d'interfaces graphiques en Python.

Le projet combine des aspects techniques avancés (glisser-déposer, base de données, styles personnalisés) avec une approche centrée sur l'utilisateur, résultant en une application intuitive et agréable à utiliser pour la gestion de projets selon la méthode Kanban.

