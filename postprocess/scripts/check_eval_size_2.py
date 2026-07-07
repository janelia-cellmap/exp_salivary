import torch


from fly_organelles.model import StandardUnet

if not torch.cuda.is_available():
    raise ValueError("CUDA is not available")

device = torch.device("cuda")

# Load model
model_backbone = StandardUnet(1)
model = torch.nn.Sequential(model_backbone, torch.nn.Sigmoid())
model.to(device)
model.eval()

dummy_input = torch.randn(1, 1, 378, 378, 378, device=device)

# Run inference
with torch.no_grad():
    output = model(dummy_input)

print(output.shape)
# torch.Size([1, 1, 256, 256, 256])
