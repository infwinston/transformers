from datasets import load_dataset
from tokenizers import trainers, Tokenizer, normalizers, ByteLevelBPETokenizer

# load dataset
dataset = load_dataset("oscar", "unshuffled_deduplicated_no", split="train")

# Instantiate tokenizer
tokenizer = ByteLevelBPETokenizer()

def batch_iterator(batch_size=1000):
    for i in range(0, len(dataset), batch_size):
        yield dataset[i: i + batch_size]["text"]

# Customized training
tokenizer.train_from_iterator(batch_iterator(), vocab_size=50265, min_frequency=2, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])

# Save files to disk
tokenizer.save("./norwegian-roberta-base/tokenizer.json")


from transformers import RobertaConfig

config = RobertaConfig.from_pretrained("roberta-base", vocab_size=50265)
config.save_pretrained("./norwegian-roberta-base")
