# IntentIdentification

This is a package to detect intent of utterances, trained on the SNIPS dataset, with 98% accuracy.

It can detection any of the following intents in an input utterance:
1. PlayMusic	
2. GetWeather	
3. BookRestaurant	
4. RateBook	
5. SearchScreeningEvent	
6. SearchCreativeWork	
7. AddToPlaylist	

Example usage:

import IntentIdentification

predictor = IntentIdentification.Predictor()

confidence, pred_intent = predictor("find animated movies playing near me")