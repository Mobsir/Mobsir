from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

tokenizer = AutoTokenizer.from_pretrained("marefa-nlp/marefa-mt-en-ar")
model = AutoModelForSeq2SeqLM.from_pretrained("marefa-nlp/marefa-mt-en-ar")

def translate_text(text):
    """ Translate English text to Arabic using the Marefa model """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=50)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def translate_objects(object_names):
    """   Translate a list of object names from English to Arabic."""
    return [translate_text(name) for name in object_names]

