import cv2
import numpy as np
import os
import torch
from torch.nn import functional as F
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from PIL import Image


class RealESRGAN:
    def __init__(self, device, scale=4, anime=False):
        self.device = device
        self.scale = scale

        # Elegir arquitectura según tipo
        if anime:
            self.model = RRDBNet(
                num_in_ch=3,
                num_out_ch=3,
                num_feat=64,
                num_block=6,  # anime usa 6 bloques
                num_grow_ch=32,
                scale=self.scale
            )
            self.weights_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"
        else:
            self.model = RRDBNet(
                num_in_ch=3,
                num_out_ch=3,
                num_feat=64,
                num_block=23,
                num_grow_ch=32,
                scale=self.scale
            )
            self.weights_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"

        # Carga de pesos
        model_path = load_file_from_url(self.weights_url, model_dir="weights")
        loadnet = torch.load(model_path, map_location=self.device)
        state_dict = loadnet.get('params_ema', loadnet)
        self.model.load_state_dict(state_dict, strict=False)  # strict=False evita Missing key(s)
        self.model.to(self.device)
        self.model.eval()

    def load_weights(self, model_path, download=True):
        """Load pretrained model weights"""
        if not os.path.isfile(model_path):
            if download:
                # Download the model if it doesn't exist
                model_path = load_file_from_url(
                    url=model_path,
                    model_dir="weights",
                    progress=True,
                    file_name=os.path.basename(model_path)
                )
            else:
                raise FileNotFoundError(f"Model file not found: {model_path}")

        # Load the model
        loadnet = torch.load(model_path, map_location=self.device)

        if 'params' in loadnet:
            self.model.load_state_dict(loadnet['params'], strict=True)
        elif 'params_ema' in loadnet:
            self.model.load_state_dict(loadnet['params_ema'], strict=True)
        else:
            self.model.load_state_dict(loadnet, strict=True)
        self.model.to(self.device)
        self.model.eval()

    @torch.no_grad()
    def predict(self, img):
        """Predict single image"""
        if self.model is None:
            raise ValueError("Model not loaded. Call load_weights() first.")

        # Convert PIL to numpy
        if isinstance(img, np.ndarray):
            img = img
        else:
            img = np.array(img)

        # Prepare image
        img = img.astype(np.float32) / 255.
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        # Convert to tensor
        img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
        img = img.unsqueeze(0).to(self.device)

        # Inference
        output = self.model(img)

        # Post-process
        output = output.data.squeeze().float().cpu().clamp_(0, 1).numpy()
        output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
        output = (output * 255.0).round().astype(np.uint8)

        # Convert back to PIL
        from PIL import Image
        return Image.fromarray(output)
