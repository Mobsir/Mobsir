import torch
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, GPT2TokenizerFast
from tqdm import tqdm

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning",
    cache_dir="./models_cache")
tokenizer = GPT2TokenizerFast.from_pretrained("nlpconnect/vit-gpt2-image-captioning",
    cache_dir="./models_cache")


image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning",
    cache_dir="./models_cache")


def get_caption(model, image_processor, tokenizer, image_path):
  """
    Generate a caption for a given image using a ViT-GPT2 image captioning model.

    This function:
    - Opens the image and ensures it is in RGB mode.
    - Processes the image using the ViT image processor.
    - Uses the encoder-decoder model to generate a caption.
    - Decodes and returns the caption as a string.

    Args:
        model (VisionEncoderDecoderModel): Pre-trained image captioning model.
        image_processor (ViTImageProcessor): Pre-trained image processor.
        tokenizer (GPT2TokenizerFast): Tokenizer to decode model output.
        image_path (str): Path to the input image file.

    Returns:
        str: Generated caption describing the image.
    """
    # Open the image
  image = Image.open(image_path)
  if image.mode != "RGB":
    image = image.convert(mode="RGB")


  img = image_processor(image, return_tensors="pt")


  output = model.generate(**img)

  caption = tokenizer.batch_decode(output, skip_special_tokens=True)[0]

  return caption

    
