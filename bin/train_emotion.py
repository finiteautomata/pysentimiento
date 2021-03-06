import sys
import fire
import torch
from transformers import (
    Trainer, TrainingArguments,
)
import pandas as pd
from pysentimiento.tass import load_model
from pysentimiento.emotion import load_datasets
from pysentimiento.emotion.datasets import id2label, label2id
from pysentimiento.metrics import compute_metrics
from sklearn.utils.class_weight import compute_class_weight

extra_args = {
    "vinai/bertweet-base": {
        "preprocessing_args": {"user_token": "@USER", "url_token": "HTTPURL"}
    }
}


class MultiLabelTrainer(Trainer):
    def __init__(self, class_weight, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weight = class_weight

    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        loss_fct = torch.nn.CrossEntropyLoss(weight=self.class_weight)
        num_labels = self.model.config.num_labels
        loss = loss_fct(logits, labels)
        return (loss, outputs) if return_outputs else loss


def train(
    base_model, output_path, lang="es", epochs=5, batch_size=32, eval_batch_size=16,
    warmup_proportion=.1, limit=None
):
    """
    """

    print("="*80 + '\n', "="*80 + '\n')
    print(f"Training {base_model} in language {lang}", "\n" * 2)
    print("Loading dataset")
    if lang not in ["es", "en"]:
        print("lang must be one of 'es', 'en'")
        sys.exit(1)



    load_extra_args = extra_args[base_model] if base_model in extra_args else {}

    train_dataset, dev_dataset, test_dataset = load_datasets(lang=lang, **load_extra_args)


    if limit:
        """
        Smoke test
        """
        print("\n\n", f"Limiting to {limit} instances")
        train_dataset = train_dataset.select(range(limit))
        dev_dataset = dev_dataset.select(range(limit))
        test_dataset = test_dataset.select(range(limit))


    device = "cuda" if torch.cuda.is_available() else "cpu"
    class_weight = torch.Tensor(
        compute_class_weight('balanced', list(id2label), y=train_dataset["label"])
    ).to(device)

    model, tokenizer = load_model(base_model,
        id2label=id2label,
        label2id=label2id
    )

    model = model.to(device)
    model.train()

    def tokenize(batch):
        return tokenizer(batch['text'], padding='max_length', truncation=True)


    train_dataset = train_dataset.map(tokenize, batched=True, batch_size=batch_size)
    dev_dataset = dev_dataset.map(tokenize, batched=True, batch_size=eval_batch_size)
    test_dataset = test_dataset.map(tokenize, batched=True, batch_size=eval_batch_size)

    def format_dataset(dataset):
        dataset = dataset.map(lambda examples: {'labels': examples['label']})
        columns = ['input_ids', 'attention_mask', 'labels']
        if 'token_type_ids' in dataset.features:
            columns.append('token_type_ids')
        dataset.set_format(type='torch', columns=columns)
        print(columns)
        return dataset

    train_dataset = format_dataset(train_dataset)
    dev_dataset = format_dataset(dev_dataset)
    test_dataset = format_dataset(test_dataset)

    print("\n\nTraining\n")



    total_steps = (epochs * len(train_dataset)) // batch_size
    warmup_steps = total_steps // 10
    training_args = TrainingArguments(
        output_dir='./results/' + output_path,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=eval_batch_size,
        warmup_steps=warmup_steps,
        evaluation_strategy="epoch",
        do_eval=False,
        weight_decay=0.01,
        logging_dir='./logs',
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
    )

    trainer = MultiLabelTrainer(
        class_weight=class_weight,
        model=model,
        args=training_args,
        compute_metrics=lambda x: compute_metrics(x, id2label=id2label),
        train_dataset=train_dataset,
        eval_dataset=dev_dataset,
    )

    trainer.train()


    test_results = trainer.evaluate(test_dataset)
    print("\n\n")
    print("Test results")
    print("============")
    for k, v in test_results.items():
        print(f"{k:<16} : {v:.3f}")


    print(f"Saving model to {output_path}")
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)

if __name__ == "__main__":
    fire.Fire(train)
