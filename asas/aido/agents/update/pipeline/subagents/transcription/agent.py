from google.adk.agents import Agent

from aido.agents.create.pipeline.subagents.transcription.tools.transcribe_video import (
    transcribe_video,
)


update_transcription_agent = Agent(
    name="UpdateTranscriptionAgent",
    model="gemini-2.5-flash",
    description="Transcreve o novo material de referencia para comparar com o manual existente.",
    tools=[transcribe_video],
    instruction="""
Receba o caminho completo do video (ou audio) informado pelo usuario.
Chame a ferramenta `transcribe_video` com esse caminho exatamente como argumento `video_path`.
Retorne apenas o texto bruto transcrito, sem comentarios adicionais.
""".strip(),
    output_key="transcribed_text",
)


__all__ = ["update_transcription_agent"]
