from configparser import ConfigParser
import os

class Config:
    def __init__(self, config_file="uiconfigfile.ini"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, config_file)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Config file not found: {full_path}")

        self.config = ConfigParser()
        self.config.read(full_path)

    def _get_list(self, key, section="DEFAULT"):
        """Fetch a comma-separated value and return a list"""
        value = self.config.get(section, key, fallback="")
        return [item.strip() for item in value.split(",")] if value else []

    def get_llm_options(self):
        return self._get_list("LLM_OPTIONS")

    def get_usecase_options(self):
        return self._get_list("USECASE_OPTIONS")

    def get_groq_model_options(self):
        return self._get_list("GROQ_MODEL_OPTIONS")

    def get_page_title(self):
        return self.config.get("DEFAULT", "PAGE_TITLE", fallback="Agentic Chatbot")
