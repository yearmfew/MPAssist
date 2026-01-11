import re

from typing import List, Dict
from agents.base_agent import BaseAgent
from utils import db_manager
from utils.template import TEMPLATE_REQUIREMENT_GATHERER
from langchain_core.prompts import PromptTemplate


class RequirementFinder(BaseAgent):
    def __init__(self):
        super().__init__()
        db_manager._init_vector_store()

    def _find_requirements(
        self, user_input: str, conversation_history: list[dict]
    ) -> str:
        prompt_template = PromptTemplate.from_template(TEMPLATE_REQUIREMENT_GATHERER)

        full_prompt = prompt_template.format(
            message=user_input, conversation_history=conversation_history
        )

        llm_response = self.invoke_llm(full_prompt)

        return llm_response

    def extract_requirements_from_message_as_list(self, message: str) -> list[str]:
        pattern = r"(?i)final requirements summary:(.*?)\[REQUIREMENTS_READY\]"
        match = re.search(pattern, message, re.DOTALL)

        if not match:
            return ["User request captured in conversation"]

        section = match.group(1).strip()

        requirements = []
        items = re.findall(r"^\d+\.\s+(.+)$", section, re.MULTILINE)

        for item in items:
            clean_item = item.strip()
            if not clean_item.lower().startswith(("these requirements", "ready to")):
                requirements.append(clean_item)

        return (
            requirements if requirements else ["User request captured in conversation"]
        )

    def chat_to_find_requirements(
        self, user_input: str, history: List[Dict]
    ) -> Dict[str, object]:
        llm_response = self._find_requirements(
            user_input=user_input, conversation_history=history
        )

        result: Dict[str, object] = {
            "llm_response": llm_response,
            "isFinished": False,
        }

        if "[REQUIREMENTS_READY]" in llm_response:
            result["isFinished"] = True

        return result
