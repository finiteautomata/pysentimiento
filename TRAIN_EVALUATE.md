
## Train

```bash
python bin/train_sentiment.py "dccuchile/bert-base-spanish-wwm-cased" models/beto-sentiment-analysis/ --epochs 5 --lang es
python bin/train_sentiment.py "distilbert-base-multilingual-cased" models/distilbert-es-sentiment-analysis/ --epochs 5 --lang es
python bin/train_sentiment.py "bert-base-multilingual-cased" models/mbert-es-sentiment-analysis/ --epochs 5 --lang es

# Sentiment English

python bin/train_sentiment.py "distilbert-base-multilingual-cased" models/distilbert-en-sentiment-analysis/ --epochs 10 --lang en
python bin/train_sentiment.py "bert-base-multilingual-cased" models/mbert-en-sentiment-analysis/ --epochs 10 --lang en

python bin/train_sentiment.py "bert-base-uncased" models/bert-base-sentiment-analysis/ --epochs 10 --lang en
python bin/train_sentiment.py "roberta-base" models/roberta-base-sentiment-analysis/ --epochs 10 --lang en
python bin/train_sentiment.py "vinai/bertweet-base" models/bertweet-base-sentiment-analysis/ --epochs 10 --lang en

# Emotion Spanish

python bin/train_emotion.py "dccuchile/bert-base-spanish-wwm-cased" models/beto-emotion-analysis/ --epochs 5 --lang es
python bin/train_emotion.py "distilbert-base-multilingual-cased" models/distilbert-es-emotion-analysis/ --epochs 5 --lang es
python bin/train_emotion.py "bert-base-multilingual-cased" models/mbert-es-emotion-analysis/ --epochs 5 --lang es

# Emotion English
python bin/train_emotion.py "distilbert-base-multilingual-cased" models/distilbert-en-emotion-analysis/ --epochs 5 --lang en
python bin/train_emotion.py "bert-base-multilingual-cased" models/mbert-en-emotion-analysis/ --epochs 5 --lang en

python bin/train_emotion.py "bert-base-uncased" models/bert-base-emotion-analysis/ --epochs 5 --lang en
python bin/train_emotion.py "roberta-base" models/roberta-base-emotion-analysis/ --epochs 5 --lang en
python bin/train_emotion.py "vinai/bertweet-base" models/bertweet-base-emotion-analysis/ --epochs 5 --lang en
```

## Evaluation

```bash
python bin/eval_sentiment.py models/beto-sentiment-analysis/ evaluations/sentiment_beto.json --lang es
python bin/eval_sentiment.py models/distilbert-es-sentiment-analysis/ evaluations/sentiment_distilbert_es.json --lang es
python bin/eval_sentiment.py models/mbert-es-sentiment-analysis/ evaluations/sentiment_mbert_es.json --lang es


python bin/eval_sentiment.py models/mbert-en-sentiment-analysis/ evaluations/sentiment_mbert_en.json --lang en
python bin/eval_sentiment.py models/distilbert-en-sentiment-analysis/ evaluations/sentiment_distilbert_en.json --lang en
python bin/eval_sentiment.py models/bert-base-sentiment-analysis/ evaluations/sentiment_bert_base.json --lang en
python bin/eval_sentiment.py models/bertweet-base-sentiment-analysis/ evaluations/sentiment_bertweet_base.json --lang en
python bin/eval_sentiment.py models/roberta-base-sentiment-analysis/ evaluations/sentiment_roberta_base.json --lang en

# Emotion Spanish

python bin/eval_emotion.py models/beto-emotion-analysis/ evaluations/emotion_beto.json --lang es
python bin/eval_emotion.py models/distilbert-es-emotion-analysis/ evaluations/emotion_distilbert_es.json --lang es
python bin/eval_emotion.py models/mbert-es-emotion-analysis/ evaluations/emotion_mbert_es.json --lang es

# Emotion English
python bin/eval_emotion.py models/distilbert-en-emotion-analysis/ evaluations/emotion_distilbert_en.json --lang en
python bin/eval_emotion.py models/mbert-en-emotion-analysis/ evaluations/emotion_mbert_en.json --lang en

python bin/eval_emotion.py models/bert-base-emotion-analysis/ evaluations/emotion_bert_base.json --lang en
python bin/eval_emotion.py models/bertweet-base-emotion-analysis/ evaluations/emotion_bertweet_base.json --lang en
python bin/eval_emotion.py models/roberta-base-emotion-analysis/ evaluations/emotion_roberta.json --lang en
```


## Smoke test

```
python bin/train_sentiment.py "dccuchile/bert-base-spanish-wwm-cased" models/test/ --epochs 5 --limit 500 && python bin/train_sentiment.py "bert-base-uncased" models/test/ --epochs 5 --limit 500 --lang en && rm -Rf models/test/

# Emotion
python bin/train_emotion.py "dccuchile/bert-base-spanish-wwm-cased" models/test/ --lang es --epochs 3 --limit 500 && python bin/train_emotion.py "vinai/bertweet-base" models/test/ --lang en --epochs 3 --limit 500 && rm -Rf models/test/
```