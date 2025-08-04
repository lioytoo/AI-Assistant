import os
os.environ["XDG_CACHE_HOME"] = os.path.expanduser("~/.cache")

from TTS.api import TTS
from TTS.utils.manage import ModelManager


# For each m in models,
# it checks if "en/" and "/tts_models" are both present in the string m.
# If both conditions are true, m is included in the new list.
manager = ModelManager()
models = manager.list_models()

available_English_models = [m for m in models if "en/" in m and "/tts_models" in m]
#available_English_models = manager.list_models()

# List available models
#print("\nAvailable models:")

for model in available_English_models:
    print(" -", model)

tts = TTS(model_name="tts_models/en/vctk/vits")

tts.tts_to_file(text="Hello Light! Your setup is working.", file_path="output.wav")
