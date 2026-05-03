import json
import logging
from groq import Groq

class AIEngine:
    """Handles interactions with the Groq API for codebase analysis."""

    # Model Fallback Chain: High capability -> High speed/Reliability
    MODEL_FALLBACK_CHAIN = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ]

    def __init__(self, api_key, model=None):
        self.client = Groq(api_key=api_key)
        self.primary_model = model if model else self.MODEL_FALLBACK_CHAIN[0]
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("AIEngine")

    def _apply_smart_truncation(self, content, max_tokens=6000):
        """
        Truncates content if it exceeds the token limit, preserving
        the head and tail of the file to maintain architectural context.
        """
        # Simple character-to-token approximation (approx 4 chars per token)
        approx_chars = int(max_tokens * 4)
        if len(content) <= approx_chars:
            return content

        # Preserve 70% head and 20% tail to give more context to the start
        head_size = int(approx_chars * 0.7)
        tail_size = int(approx_chars * 0.2)

        return f"{content[:head_size]}\n\n... [TRUNCATED FOR TOKEN LIMIT] ...\n\n{content[-tail_size:]}"

    def _call_groq_with_fallback(self, prompt):
        """Tries models in the fallback chain until one succeeds."""
        # Prioritize the user's selected model, then fallback through the chain
        models_to_try = []
        if self.primary_model:
            models_to_try.append(self.primary_model)

        for m in self.MODEL_FALLBACK_CHAIN:
            if m not in models_to_try:
                models_to_try.append(m)

        last_exception = None
        for model in models_to_try:
            try:
                # Minimizing tokens by using a more concise system prompt
                # and explicitly asking for brevity in the user prompt.
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a senior architect. Be concise. Respond ONLY with JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=model,
                    response_format={"type": "json_object"},
                    temperature=0.1, # Lower temperature for more accurate/deterministic results
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                self.logger.warning(f"Model {model} failed: {e}. Trying next fallback...")
                last_exception = e
                continue

        self.logger.error(f"All models in fallback chain failed. Last error: {last_exception}")
        return "{}"

    def analyze_file(self, filename, content):
        """Sends file content to Groq for purpose summary and issue detection."""
        truncated_content = self._apply_smart_truncation(content)

        prompt = (
            f"Analyze the following file '{filename}' and provide:\n"
            "1. A concise summary of its purpose.\n"
            "2. A list of any issues (bugs, security risks, smells, performance problems).\n"
            "Format your response as a JSON object with keys 'summary' (string) and 'issues' (list of objects with 'issue', 'severity', and 'suggestion').\n"
            "If no issues are found, 'issues' should be an empty list.\n"
            "Return ONLY the JSON object.\n\n"
            f"File Content:\n---\n{truncated_content}\n---"
        )

        response_text = self._call_groq_with_fallback(prompt)
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON received for {filename}")
            return {"summary": "Analysis failed (Invalid JSON)", "issues": []}

    def generate_final_report(self, all_analyses):
        """Aggregates all file analyses into a final system-wide audit report."""
        prompt = (
            "Based on the following individual file analyses, generate a final system-wide audit report. "
            "Provide an overall system health score (0-100), the top 3 most critical risks, and a summary of the architecture's quality.\n"
            "Format the response as JSON with keys: 'health_score', 'critical_risks' (list), and 'overall_summary'.\n"
            "Return ONLY the JSON object.\n\n"
            f"Analyses:\n{json.dumps(all_analyses, indent=2)}"
        )

        response_text = self._call_groq_with_fallback(prompt)
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON received for final report")
            return {"health_score": 0, "critical_risks": [], "overall_summary": "Final report generation failed."}
