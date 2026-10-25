# Laszlo et les pizzas à 10 000 bitcoins : TikTok de 40 s

Vidéo : `laszlo_pizza_tiktok.mp4` (1080x1920, 40 s) : voix off, musique, effets sonores, sous-titres mot par mot.
Pistes séparées pour CapCut : `laszlo_pizza_voix_off.mp3` (voix traitée) et `laszlo_pizza_musique.mp3` (musique seule).
Sous-titres : `laszlo_pizza_soustitres.srt`

## Voix off (ton conteur, rythmé)

**[0-3 s, HOOK]**
Cet homme a payé deux pizzas… des centaines de millions d'euros.

**[3-12 s, CONTEXTE]**
Mai 2010. Le bitcoin vient à peine de naître.
Il ne vaut presque rien. Même pas un centime.
Et personne ne s'en sert pour acheter quoi que ce soit.

**[12-28 s, L'HISTOIRE]**
Laszlo Hanyecz, un programmeur de Floride, poste un message sur un forum :
« 10 000 bitcoins pour deux pizzas. »
Quatre jours passent…
Puis un étudiant de 19 ans accepte.
Laszlo envoie ses 10 000 bitcoins.
Et les pizzas arrivent.
Le tout premier achat en bitcoin.

**[28-36 s, LA CHUTE]**
À l'époque, ça valait 41 dollars.
Aujourd'hui ? Ces bitcoins vaudraient plus d'un demi-milliard d'euros.

**[36-40 s, FIN]**
Et toi, tu les aurais gardés ?
Abonne-toi pour plus d'histoires d'argent.

## Description TikTok

Il a échangé 10 000 bitcoins contre 2 pizzas en 2010… Aujourd'hui, ça vaudrait plus d'un demi-milliard d'euros 🍕💸 Et toi, tu aurais gardé ou mangé ? 👇

#bitcoin #crypto #histoirevraie #argent #pizzaday

## Production
- Voix masculine : modèle Kokoro, mélange de la voix française ff_siwis (30-45 %) et des timbres masculins am_onyx + hm_omega. Naturel noté 4,2/5 par UTMOS (voix humaines : environ 4,3). Pour chaque phrase, la formulation la mieux comprise par Whisper a été retenue automatiquement. Traitement : EQ, compression, légère réverbération.
- Musique originale : piano, cordes, chœur (banque MuseScore General), batterie et basse 808 synthétisées. Breakdown sur « Quatre jours passent… », montée puis drop sur le compteur (31 s).
- Effets sonores : impacts, whooshs, tic-tac, frappe clavier, pièces, « ka-ching ».
- Mix : la musique baisse automatiquement sous la voix, master à -14 LUFS.
- Régénérer : `voice.py` (voix), puis `music.py` (musique et mix), puis `render.py` (image).

## Sources / chiffres
- Message original : forum bitcointalk.org, 18 mai 2010. Pizzas livrées le 22 mai 2010 (le « Bitcoin Pizza Day »). Jeremy Sturdivant, 19 ans, a commandé chez Papa John's.
- Valeur de 2010 : ~41 $. Valeur actuelle calculée avec ~55 000 €/BTC (10 000 × 55 000 € = 550 M€). Vérifie le cours avant de publier : pour changer, modifie `BTC_PRICE_EUR` dans `source/render.py` et relance `python3 source/render.py sortie.mp4`. Voix : `python3 source/voice.py <dossier_modèle> write voix.wav` (modèle : release sherpa-onnx `vits-piper-fr_FR-tom-medium`, moteur `pip install piper-tts`).
