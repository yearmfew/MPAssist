import re
import json

from typing import List, Dict
from agents.base_agent import BaseAgent
from utils import db_manager
from utils.template import TEMPLATE_REQUIREMENT_GATHERER, TEMPLATE_EXTRACT_REQUIREMENTS
from utils.settings import K


class RequirementFinder(BaseAgent):
    def __init__(self):
        super().__init__()
        db_manager._init_vector_store()

    def _find_requirements(self, user_input: str, conversation_history: list[dict]) -> str:

        chunks = self.get_chunks(
            query=str(conversation_history),
            k=K,
            filter={"category": "mainDocumentation"},
        )

        labelled_chunks = self._label_chunks(
            chunks,
            templateName="TEMPLATE_REQUIREMENT_GATHERER",
            priority_map={"mainDocumentation": "HIGH"},
        )

        context_text = "\n\n---\n\n".join(labelled_chunks)

        full_prompt = self.create_prompt_template(
            template=TEMPLATE_REQUIREMENT_GATHERER,
            context=context_text,
            message=user_input,
            conversation_history=conversation_history,
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

        return requirements if requirements else ["User request captured in conversation"]

    def chat_to_find_requirements(self, user_input: str, history: List[Dict]) -> Dict[str, object]:
        llm_response = self._find_requirements(user_input=user_input, conversation_history=history)

        result: Dict[str, object] = {
            "llm_response": llm_response,
            "isFinished": False,
        }

        if "[REQUIREMENTS_READY]" in llm_response:
            result["isFinished"] = True

        return result

    def extract_requirements_as_dict(self, summary: str) -> dict:
        full_prompt = self.create_prompt_template(template=TEMPLATE_EXTRACT_REQUIREMENTS, context=summary)
        llm_response = self.invoke_llm(full_prompt)

        try:
            cleaned_llm_response = re.sub(r"```json?|```", "", llm_response).strip()
            requirements_dict = json.loads(cleaned_llm_response)
        except json.JSONDecodeError:
            requirements_dict = {
                "requirements": [],
                # "layers": [],
                # "map_configurations": {},
                # "menu_configurations": {},
            }

        return requirements_dict

    def _label_chunks(
        self,
        chunks: list,
        templateName: str = "",
        priority_map: dict = {},
    ) -> list:
        labeled_chunks = []

        for chunk in chunks:
            category = chunk.metadata.get("category", "unknown")
            templateFromMetadata = chunk.metadata.get("template", "")

            if templateName == templateFromMetadata:
                priority = "CRITICAL"
            else:
                priority = priority_map.get(category, "LOW")

            labeled_chunk = f"[CATEGORY]: {category}\n" f"[PRIORITY]: {priority}\n" f"{chunk.page_content}"
            labeled_chunks.append(labeled_chunk)

        return labeled_chunks
