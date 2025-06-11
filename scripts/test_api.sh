#!/bin/bash

# Script de test pour l'API Nutritionnelle
# Assurez-vous que l'application est démarrée sur http://localhost:8000

BASE_URL="http://localhost:8000"
TOKEN=""

echo "🧪 Test de l'API Nutritionnelle - Université de Yaoundé I"
echo "=================================================="

# Test 1: Vérifier que l'API est accessible
echo "1. Test de connectivité..."
curl -s "$BASE_URL/health" | jq . || echo "❌ API non accessible"

# Test 2: Créer un utilisateur
echo -e "\n2. Création d'un utilisateur..."
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/utilisateurs/" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "allergies": ["Lactose"]
  }')

echo $USER_RESPONSE | jq . || echo "❌ Erreur création utilisateur"

# Test 3: Authentification
echo -e "\n3. Authentification..."
AUTH_RESPONSE=$(curl -s -X POST "$BASE_URL/utilisateurs/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123")

TOKEN=$(echo $AUTH_RESPONSE | jq -r '.access_token')
echo "Token obtenu: ${TOKEN:0:20}..."

# Test 4: Recherche d'aliments
echo -e "\n4. Recherche d'aliments..."
curl -s "$BASE_URL/aliments/?q=poutine" | jq '.[0:3]' || echo "❌ Erreur recherche aliments"

# Test 5: Récupérer tous les aliments
echo -e "\n5. Récupération de tous les aliments..."
curl -s "$BASE_URL/aliments/tous/" | jq 'length' || echo "❌ Erreur récupération aliments"

# Test 6: Aliments par catégorie
echo -e "\n6. Aliments par catégorie..."
curl -s "$BASE_URL/aliments/categorie/Plat%20principal" | jq '.[0:2]' || echo "❌ Erreur catégorie"

# Test 7: Aliments faibles en calories
echo -e "\n7. Aliments faibles en calories..."
curl -s "$BASE_URL/aliments/faibles-calories/?max_calories=300" | jq '.[0:2]' || echo "❌ Erreur calories"

# Test 8: Recommandations
echo -e "\n8. Recommandations personnalisées..."
curl -s "$BASE_URL/aliments/recommandations/?query=plat%20chaud&allergies=Lactose&max_calories=500" | jq '.[0:2]' || echo "❌ Erreur recommandations"

# Test 9: Créer un buffet (avec authentification)
if [ ! -z "$TOKEN" ]; then
    echo -e "\n9. Création d'un buffet..."
    BUFFET_RESPONSE=$(curl -s -X POST "$BASE_URL/buffets/" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "nom": "Buffet Test",
        "description": "Buffet de test pour les TP"
      }')
    
    echo $BUFFET_RESPONSE | jq . || echo "❌ Erreur création buffet"
    
    # Extraire l'ID du buffet
    BUFFET_ID=$(echo $BUFFET_RESPONSE | jq -r '.id')
    
    if [ "$BUFFET_ID" != "null" ] && [ "$BUFFET_ID" != "" ]; then
        echo -e "\n10. Récupération du buffet créé..."
        curl -s "$BASE_URL/buffets/$BUFFET_ID" | jq . || echo "❌ Erreur récupération buffet"
    fi
else
    echo -e "\n9. ❌ Impossible de tester les buffets sans token d'authentification"
fi

# Test 11: Génération de plan de repas (avec authentification)
if [ ! -z "$TOKEN" ]; then
    echo -e "\n11. Génération de plan de repas..."
    PLAN_RESPONSE=$(curl -s -X POST "$BASE_URL/plans_repas/generer-auto/1" \
      -H "Authorization: Bearer $TOKEN")
    
    echo $PLAN_RESPONSE | jq . || echo "❌ Erreur génération plan de repas"
fi

echo -e "\n✅ Tests terminés!"
echo "📖 Documentation disponible sur: $BASE_URL/docs" 