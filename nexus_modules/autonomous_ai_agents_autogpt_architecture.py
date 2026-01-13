import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoModelForCausalLM, AutoTokenizer

class AutoGPT(nn.Module):
    def __init__(self, model_name, device):
        super(AutoGPT, self).__init__()
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.device = device

    def forward(self, input_ids, attention_mask):
        outputs = self.model(input_ids, attention_mask=attention_mask)
        return outputs

    def generate(self, prompt, max_length):
        inputs = self.tokenizer(prompt, return_tensors='pt').to(self.device)
        outputs = self.model.generate(**inputs, max_length=max_length)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = AutoGPT('gpt2', device)
    prompt = 'Merhaba, bu bir test yazidir.'
    print(model.generate(prompt, 100))

if __name__ == '__main__':
    main()
# NEXUS-ONE CORE MODULE