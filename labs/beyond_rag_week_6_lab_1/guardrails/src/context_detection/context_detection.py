from enum import Enum
from typing import Dict
import re
from rich import print as rprint
import ollama
from pathlib import Path

CONTEXT_DETECTOR_MODEL="gpt-oss:20b"
CONTEXT_DETECTOR_PROMPT="src/context_detection/context_detection_prompt.md"

def read_prompt_from_file(prompt_path: str) -> str:
    path = Path(prompt_path)
    with path.open('r', encoding='utf-8') as file:
        prompt = file.read()
    return prompt

class ContextType(Enum):
    CONVERSATIONAL = "conversational"  # follow-ups, clarifications, references to previous conversation
    DOMAIN = "domain"  # requires domain knowledge, technical context, or specific expertise
    NONE = "none"

class ContextNeedDetector:
    def __init__(self):
        pass

    def needs_contextualization(self, query: str, conversation_summary: str = "") -> Dict:
        """LLM-based context detection with two types: Conversational and Domain"""
        
        # LLM assessment
        llm_assessment = self._llm_context_assessment(query)
        
        return {
            'needs_context': llm_assessment['needs_context'],
            'confidence': llm_assessment['confidence'],
            'context_type': llm_assessment['primary_type'],
            'reasoning': llm_assessment['reason']
        }

    def _llm_context_assessment(self, query: str) -> Dict:
        """LLM-based context assessment with confidence scoring"""
        
        system_prompt = read_prompt_from_file(CONTEXT_DETECTOR_PROMPT)

        prompt = system_prompt.format(
            query=query
        )
        
        try:
            response = ollama.generate(
                model=CONTEXT_DETECTOR_MODEL,
                prompt=prompt,
                options={"temperature": 0.1}
            )
            
            result = self._parse_llm_response(response['response'])
            return result
            
        except Exception as e:
            print(f"⚠️  LLM context assessment error: {e}")
            return {
                'needs_context': False,
                'confidence': 0.0,
                'primary_type': ContextType.NONE,
                'reason': 'LLM assessment failed'
            }

    def _parse_llm_response(self, response: str) -> Dict:
        """Parse structured LLM response"""
        try:
            lines = response.strip().split('\n')
            result = {
                'needs_context': False,
                'confidence': 0.0,
                'primary_type': ContextType.NONE,
                'reason': 'Unknown'
            }
            
            for line in lines:
                if 'NEEDS_CONTEXT:' in line:
                    result['needs_context'] = 'YES' in line.upper()
                elif 'CONFIDENCE:' in line:
                    try:
                        result['confidence'] = float(re.search(r'(\d+\.?\d*)', line).group(1))
                    except Exception as e:
                        print(f"⚠️  Confidence parsing error: {e}")
                        result['confidence'] = 0.5
                elif 'CONTEXT_TYPE:' in line:
                    type_match = re.search(r'(CONVERSATIONAL|DOMAIN|NONE)', line.upper())
                    if type_match:
                        result['primary_type'] = ContextType(type_match.group(1).lower())
                elif 'REASON:' in line:
                    result['reason'] = line.split('REASON:')[1].strip()
                    
            return result
            
        except Exception as e:
            return {
                'needs_context': False,
                'confidence': 0.0,
                'primary_type': ContextType.NONE,
                'reason': f'Parse error: {e}'
            }

def needs_contextualization(query: str) -> bool:
    """Simplified context detection using only LLM assessment"""
    detector = ContextNeedDetector()
    result = detector.needs_contextualization(query)
    rprint(result)
    return (result['needs_context'], result['context_type'])

def main():
    
    # Test progressive conversation with simplified context detection
    conversation_flow = [
        # "Do elephants have trunk?",
        # "Tell me about animal friendships",
        # "How do elephants show loyalty?",
        # "That's fascinating! What about their memory?",
        # "How does this compare to human relationships?",
        # "Tell me more about emotional bonds",
        # "What wisdom can we learn from this?",
        # # Domain context examples
        # "What are the ecological implications of elephant migration patterns?",
        # "How do these behaviors impact biodiversity in savanna ecosystems?",
        # "What's the conservation status and IUCN classification?",
        # "Can you explain the genetic diversity within elephant populations?",
        "What are the behavioral adaptations for climate change resilience?"
    ]
    
    for i, query in enumerate(conversation_flow, 1):
        rprint(f"\n[bold yellow]--- Turn {i}: {query} ---[/bold yellow]")
        response = needs_contextualization(query)
        rprint(f"🤖 [bold magenta]Response:[/bold magenta] {response}")
        
        rprint("="*60)

if __name__ == "__main__":
    main()
