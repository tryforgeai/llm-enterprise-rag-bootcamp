import re
from typing import Dict, Any
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


def _load_seq2seq_corrector(model_id: str, use_cuda: bool):
    """
    Load a seq2seq model (T5-style) using AutoModelForSeq2SeqLM.
    Compatible with transformers 5.x (text2text-generation pipeline was removed).
    Returns a callable that accepts (text, max_length=..., do_sample=..., clean_up_tokenization_spaces=...)
    and returns [{"generated_text": str}], with a .model.name_or_path for grammar prefix detection.
    """
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    device = "cuda" if use_cuda else "cpu"
    model = model.to(device)

    class _Seq2SeqWrapper:
        def __init__(self, model, tokenizer, device, model_id):
            self.model = type("_ModelRef", (), {"name_or_path": model_id})()
            self._model = model
            self._tokenizer = tokenizer
            self._device = device

        def __call__(self, text, max_length=128, do_sample=False, clean_up_tokenization_spaces=True):
            inputs = self._tokenizer(
                text, return_tensors="pt", truncation=True, max_length=512
            ).to(self._device)
            out = self._model.generate(
                **inputs, max_length=max_length, do_sample=do_sample
            )
            gen = self._tokenizer.decode(
                out[0],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=clean_up_tokenization_spaces,
            )
            return [{"generated_text": gen}]

    return _Seq2SeqWrapper(model, tokenizer, device, model_id)


class TwoStageQueryNormalization:
    def __init__(self, 
                 use_pyspellchecker: bool = True,
                 use_textblob: bool = True,
                 use_huggingface_grammar: bool = True,
                 use_ollama: bool = False,
                 hf_grammar_model: str = "vennify/t5-base-grammar-correction",
                 hf_spelling_model: str = "oliverguhr/spelling-correction-english-base",
                 ollama_model: str = "qwen3:8b",#"llama3.2:1b",
                 use_cuda: bool = False):
        """
        Two-Stage Query Normalization Pipeline:
        Stage 1: Spelling Correction (PySpellChecker/TextBlob/Huggingface Spelling Model)
        Stage 2: Grammar Correction (Huggingface Grammar Model/Ollama)
        
        Args:
            use_pyspellchecker: Use PySpellChecker for spelling correction (Stage 1)
            use_textblob: Use TextBlob for spelling correction fallback (Stage 1)
            use_huggingface_grammar: Use Huggingface model for grammar correction (Stage 2)
            use_ollama: Use Ollama LLM for grammar correction (Stage 2)
            hf_grammar_model: Huggingface grammar correction model
            hf_spelling_model: Huggingface spelling correction model
            ollama_model: Ollama model name for grammar correction
        """
        
        self.use_pyspellchecker = use_pyspellchecker
        self.use_textblob = use_textblob
        self.use_huggingface_grammar = use_huggingface_grammar
        self.use_ollama = use_ollama
        self.ollama_model = ollama_model
        
        # Stage 1: Initialize Spelling Correctors
        self._init_spelling_correctors(hf_spelling_model, use_cuda)
        
        # Stage 2: Initialize Grammar Correctors
        self._init_grammar_correctors(hf_grammar_model, use_cuda)
        
        # Initialize NLTK for traditional normalization
        self._init_nltk()
        
        print("🚀 Two-Stage Normalizer initialized:")
        print(f"   Stage 1 (Spelling): PySpell={self.use_pyspellchecker}, TextBlob={self.use_textblob}, Ollama={self.use_ollama}")
        print(f"   Stage 2 (Grammar): HuggingFace={self.use_huggingface_grammar}, Ollama={self.use_ollama}")
    
    def _init_spelling_correctors(self, hf_spelling_model: str, use_cuda: bool):
        """Initialize spelling correction components"""
        
        # PySpellChecker initialization
        self.spell_checker = None
        if self.use_pyspellchecker:
            try:
                from spellchecker import SpellChecker
                self.spell_checker = SpellChecker()
                print("✅ PySpellChecker loaded for spelling correction")
            except ImportError:
                print("❌ PySpellChecker not found. Install with: pip install pyspellchecker")
                self.use_pyspellchecker = False
        
        # Huggingface Spelling Model (optional)
        self.hf_spell_corrector = None
        try:
            self.hf_spell_corrector = _load_seq2seq_corrector(
                hf_spelling_model, use_cuda
            )
            if self.hf_spell_corrector:
                print(f"✅ Huggingface spelling model loaded: {hf_spelling_model}")
        except Exception as e:
            print(f"⚠️ Huggingface spelling model failed to load: {e}")
    
    def _init_grammar_correctors(self, hf_grammar_model: str, use_cuda: bool):
        """Initialize grammar correction components"""
        
        # Huggingface Grammar Model
        self.hf_grammar_corrector = None
        if self.use_huggingface_grammar:
            try:
                self.hf_grammar_corrector = _load_seq2seq_corrector(
                    hf_grammar_model, use_cuda
                )
                if self.hf_grammar_corrector:
                    print(f"✅ Huggingface grammar model loaded: {hf_grammar_model}")
                else:
                    self.use_huggingface_grammar = False
            except Exception as e:
                print(f"❌ Failed to load Huggingface grammar model: {e}")
                self.use_huggingface_grammar = False
    
    def _init_nltk(self):
        """Initialize NLTK components"""
        try:
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt', quiet=True)
            self.stemmer = PorterStemmer()
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            print(f"❌ Failed to initialize NLTK: {e}")
            self.stemmer = None
            self.stop_words = set()
    
    # STAGE 1: SPELLING CORRECTION METHODS
    
    def _correct_spelling_pyspellchecker(self, text: str) -> str:
        """Advanced spelling correction using PySpellChecker"""
        if not self.use_pyspellchecker or not self.spell_checker:
            return text
        
        try:
            words = text.split()
            corrected_words = []
            
            for word in words:
                # Extract clean word (remove punctuation)
                clean_word = re.sub(r'[^\w]', '', word.lower())
                original_case = word[0].isupper() if word else False
                
                if clean_word and clean_word not in self.spell_checker:
                    # Get spelling correction
                    correction = self.spell_checker.correction(clean_word)
                    if correction and correction != clean_word:
                        # Preserve original case and punctuation
                        if original_case:
                            correction = correction.capitalize()
                        corrected_word = word.replace(clean_word, correction, 1)
                        corrected_words.append(corrected_word)
                    else:
                        corrected_words.append(word)
                else:
                    corrected_words.append(word)
            
            return " ".join(corrected_words)
        except Exception as e:
            print(f"PySpellChecker correction failed: {e}")
            return text
    
    def _correct_spelling_textblob(self, text: str) -> str:
        """Fallback spelling correction using TextBlob"""
        if not self.use_textblob:
            return text
        
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            return str(blob.correct())
        except ImportError:
            print("❌ TextBlob not available")
            return text
        except Exception as e:
            print(f"TextBlob correction failed: {e}")
            return text
    
    def _correct_spelling_huggingface(self, text: str) -> str:
        """Spelling correction using Huggingface model"""
        if not self.hf_spell_corrector:
            return text
        
        try:
            result = self.hf_spell_corrector(
                text,
                max_length=128,
                do_sample=False
            )
            return result[0]['generated_text'].strip()
        except Exception as e:
            print(f"Huggingface spelling correction failed: {e}")
            return text
    
    def _correct_spelling_ollama(self, text: str) -> str:
        """Spelling correction using Ollama LLM"""
        if not self.use_ollama:
            return text
        
        try:
            import ollama
            
            prompt = f"""Fix spelling errors in this text. Preserve the original meaning and formatting:

Text: {text}

Return only the corrected text without any additional formatting or explanations."""

            response = ollama.generate(
                model=self.ollama_model,
                prompt=prompt,
                options={
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 100
                }
            )
            
            corrected = response['response'].strip()
            
            # Clean up response
            corrected = re.sub(r'^(spelling-corrected:?|corrected:?|fixed:?)\s*', '', corrected, flags=re.IGNORECASE)
            corrected = re.sub(r'\s*(that\'s it|done)\.?$', '', corrected, flags=re.IGNORECASE)
            
            return corrected if corrected else text
            
        except ImportError:
            print("❌ Ollama package not available. Install with: pip install ollama")
            return text
        except Exception as e:
            print(f"Ollama spelling correction failed: {e}")
        
        return text
    
    # STAGE 2: GRAMMAR CORRECTION METHODS
    
    def _correct_grammar_huggingface(self, text: str) -> str:
        """Grammar correction using Huggingface model"""
        if not self.use_huggingface_grammar or not self.hf_grammar_corrector:
            return text
        
        try:
            # Add grammar prefix for T5 models
            input_text = f"grammar: {text}" if "t5" in self.hf_grammar_corrector.model.name_or_path.lower() else text
            
            result = self.hf_grammar_corrector(
                input_text, 
                max_length=128, 
                clean_up_tokenization_spaces=True,
                do_sample=False
            )
            return result[0]['generated_text'].strip()
        except Exception as e:
            print(f"Huggingface grammar correction failed: {e}")
            return text
    
    def _correct_grammar_ollama(self, text: str) -> str:
        """Grammar correction using Ollama LLM"""
        if not self.use_ollama:
            return text
        
        try:
            import ollama
            
            prompt = f"""Fix grammar and spelling errors in this text. Preserve the original meaning:

Text: {text}

Return only the corrected text without any additional formatting or explanations."""

            response = ollama.generate(
                model=self.ollama_model,
                prompt=prompt,
                options={
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 100
                }
            )
            
            corrected = response['response'].strip()
            
            # Clean up response
            corrected = re.sub(r'^(grammar-corrected:?|corrected:?|fixed:?)\s*', '', corrected, flags=re.IGNORECASE)
            corrected = re.sub(r'\s*(that\'s it|done)\.?$', '', corrected, flags=re.IGNORECASE)
            
            return corrected if corrected else text
            
        except ImportError:
            print("❌ Ollama package not available. Install with: pip install ollama")
            return text
        except Exception as e:
            print(f"Ollama grammar correction failed: {e}")
        
        return text
    
    # TRADITIONAL NORMALIZATION
    
    def _traditional_normalize(self, text: str) -> str:
        """Apply traditional NLP normalization"""
        # Convert to lowercase
        normalized = text.lower()
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Remove punctuation except apostrophes
        normalized = re.sub(r'[^\w\s\']', '', normalized)
        
        # Handle contractions
        contractions = {
            "won't": "will not", "can't": "cannot", "n't": " not",
            "'re": " are", "'ve": " have", "'ll": " will", "'d": " would",
            "'m": " am", "it's": "it is", "that's": "that is"
        }
        
        for contraction, expansion in contractions.items():
            normalized = normalized.replace(contraction, expansion)
        
        # Clean up spaces
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    # MAIN NORMALIZATION PIPELINE
    
    def normalize(self, query: str, 
                 apply_spelling_correction: bool = True,
                 apply_grammar_correction: bool = True,
                 apply_traditional_normalization: bool = True,
                 remove_stopwords: bool = False,
                 apply_stemming: bool = False) -> Dict[str, Any]:
        """
        Two-Stage Query Normalization Pipeline
        
        Returns:
            Dict with complete processing results from both stages
        """
        
        if not query or not query.strip():
            return {
                'original': query,
                'stage1_spelling_corrected': query,
                'stage2_grammar_corrected': query,
                'final_normalized': query,
                'methods_used': []
            }
        
        original_query = query.strip()
        current_text = original_query
        methods_used = []
        
        # STAGE 1: SPELLING CORRECTION
        stage1_result = current_text
        if apply_spelling_correction:
            print("🔍 Stage 1: Spelling Correction")
            
            # Try PySpellChecker first (most accurate for individual words)
            if self.use_pyspellchecker and self.spell_checker:
                spell_corrected = self._correct_spelling_pyspellchecker(current_text)
                if spell_corrected != current_text:
                    stage1_result = spell_corrected
                    current_text = spell_corrected
                    methods_used.append('stage1_pyspellchecker')
                    print(f"   ✅ PySpellChecker: {original_query} → {spell_corrected}")
            
            # Fallback to TextBlob if no changes from PySpellChecker
            elif self.use_textblob:
                textblob_corrected = self._correct_spelling_textblob(current_text)
                if textblob_corrected != current_text:
                    stage1_result = textblob_corrected
                    current_text = textblob_corrected
                    methods_used.append('stage1_textblob')
                    print(f"   ✅ TextBlob: {original_query} → {textblob_corrected}")
            
            # Try Huggingface spelling model if available
            elif self.hf_spell_corrector:
                hf_spell_corrected = self._correct_spelling_huggingface(current_text)
                if hf_spell_corrected != current_text:
                    stage1_result = hf_spell_corrected
                    current_text = hf_spell_corrected
                    methods_used.append('stage1_huggingface_spelling')
                    print(f"   ✅ HF Spelling: {original_query} → {hf_spell_corrected}")
            
            # Try Ollama for spelling correction if available
            elif self.use_ollama:
                ollama_spell_corrected = self._correct_spelling_ollama(current_text)
                if ollama_spell_corrected != current_text:
                    stage1_result = ollama_spell_corrected
                    current_text = ollama_spell_corrected
                    methods_used.append('stage1_ollama_spelling')
                    print(f"   ✅ Ollama Spelling: {original_query} → {ollama_spell_corrected}")
        
        # STAGE 2: GRAMMAR CORRECTION
        stage2_result = current_text
        if apply_grammar_correction:
            print("📝 Stage 2: Grammar Correction")
            
            # Try Huggingface grammar model first
            if self.use_huggingface_grammar and self.hf_grammar_corrector:
                grammar_corrected = self._correct_grammar_huggingface(current_text)
                if grammar_corrected != current_text:
                    stage2_result = grammar_corrected
                    current_text = grammar_corrected
                    methods_used.append('stage2_huggingface_grammar')
                    print(f"   ✅ HF Grammar: {stage1_result} → {grammar_corrected}")
            
            # Fallback to Ollama for grammar correction
            elif self.use_ollama:
                ollama_corrected = self._correct_grammar_ollama(current_text)
                if ollama_corrected != current_text:
                    stage2_result = ollama_corrected
                    current_text = ollama_corrected
                    methods_used.append('stage2_ollama')
                    print(f"   ✅ Ollama Grammar: {stage1_result} → {ollama_corrected}")
        
        # STAGE 3: TRADITIONAL NORMALIZATION
        final_normalized = current_text
        if apply_traditional_normalization:
            normalized = self._traditional_normalize(current_text)
            if normalized != current_text:
                final_normalized = normalized
                methods_used.append('traditional_normalization')
        
        # Optional: Advanced processing
        if remove_stopwords and self.stop_words:
            words = final_normalized.split()
            words = [word for word in words if word.lower() not in self.stop_words]
            final_normalized = ' '.join(words)
            methods_used.append('stopword_removal')
        
        if apply_stemming and self.stemmer:
            words = final_normalized.split()
            words = [self.stemmer.stem(word) for word in words]
            final_normalized = ' '.join(words)
            methods_used.append('stemming')
        
        return {
            'original': original_query,
            'stage1_spelling_corrected': stage1_result,
            'stage2_grammar_corrected': stage2_result,
            'final_normalized': final_normalized,
            'methods_used': methods_used if methods_used else ['none']
        }
    
    def batch_normalize(self, queries: list, **kwargs) -> list:
        """Process multiple queries through 2-stage pipeline"""
        return [self.normalize(query, **kwargs) for query in queries]


# Example usage demonstrating the 2-stage approach
def example_two_stage_usage():
    # Initialize 2-stage normalizer
    normalizer = TwoStageQueryNormalization(
        use_pyspellchecker=True,      # Stage 1: Spelling
        use_textblob=True,            # Stage 1: Spelling fallback
        use_huggingface_grammar=True, # Stage 2: Grammar
        use_ollama=True              # Stage 1 & 2: Spelling & Grammar fallback
    )
    
    # Test queries with spelling + grammar errors
    test_queries = [
        "Dolphns have binn observed teaching each other complex hunting techniques.",
        "Ths is a smple query with mispellings and bad grammer.",
        # "What are the benifit's of useing RAG systms?",
        # "How to implemnt a chatbot wit good performace?",
        # "Show me informtion about machne lerning algoritms"
    ]
    
    print("=" * 80)
    print("TWO-STAGE QUERY NORMALIZATION RESULTS")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\n🔤 Processing: {query}")
        
        result = normalizer.normalize(
            query,
            apply_spelling_correction=True,
            apply_grammar_correction=True,
            apply_traditional_normalization=True
        )
        
        print(f"📝 Original:        {result['original']}")
        print(f"🔍 Stage 1 (Spell): {result['stage1_spelling_corrected']}")
        print(f"📝 Stage 2 (Grammar): {result['stage2_grammar_corrected']}")
        print(f"🎯 Final Normalized: {result['final_normalized']}")
        print(f"⚙️  Methods Used: {' → '.join(result['methods_used'])}")
        print("-" * 60)

if __name__ == "__main__":
    example_two_stage_usage()
