# Chess Project ♟️

Ce projet est une simulation de jeu d'échecs avec une intelligence artificielle implémentant l'algorithme **Minimax** et une interface graphique avec **Pygame**.

## 🚀 Fonctionnalités
- 🏆 **IA Basique & IA Intelligente** (Minimax avec élagage Alpha-Bêta)
- 🎨 **Interface Graphique** (Affichage du plateau avec Pygame)
- 🎭 **Simulation Automatique** (Deux IA qui s'affrontent)
- 🛠️ **Tests Unitaires** (Framework `unittest`)

---

## 📌 Installation

1. **Cloner le projet**  
   ```bash
   git clone https://github.com/artmoreau/chess.git
   cd chess_project

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt

3. **Lancer le jeu**
   ```bash
   python src/main.py

## 🛠️ Tests

1. **Lancer les tests**  
   ```bash
   python -m unittest discover tests/

## 📂 Structure du Projet

- **chess/**
  - **src/**
    - `main.py` - Lancer le jeu
    - `board.py` - Gestion du plateau
    - `piece.py` - Gestion des pièces
    - `player.py` - IA et joueurs
    - `controller.py` - Gestion du jeu
    - `gui.py` - Interface graphique
    - `config.py` - Paramètres globaux
    - `utils.py` - Fonction utiles
  - **assets/** - Images des pièces
  - **tests/** - Tests unitaires
  - `requirements.txt` - Dépendances
  - `README.md` - Documentation
  - `pyproject.toml` - Configuration moderne


## 🚀 Projet développé par Arthur Moreau 🎯
