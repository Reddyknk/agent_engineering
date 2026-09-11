"""Class 02C golden application: sequential, loop, and parallel workflow agents."""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path

from google.adk.agents import Agent, LoopAgent, ParallelAgent, SequentialAgent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import exit_loop
from google.adk.tools.tool_context import ToolContext
from google.genai import types
import wikipedia as wikipedia_client
from langchain_community.utilities import WikipediaAPIWrapper

from adk_multiagent_systems.shared import (
    MODEL_NAME,
    PROJECT_ROOT,
    RETRY_OPTIONS,
    Graceful429Plugin,
    log_model_response,
    log_query_to_model,
)

LOGGER = logging.getLogger(__name__)
OUTPUT_DIR = PROJECT_ROOT / "movie_pitches"
WIKIPEDIA_ATTEMPTS = 3
WIKIPEDIA_BACKOFF_SECONDS = 1.0

# The `wikipedia` package ships a User-Agent that every installation shares, and
# Wikimedia rate-limits it hard: requests come back as HTTP 429 with a plain-text
# body, which the library then fails to parse as JSON. Wikimedia's API policy
# asks for a descriptive agent, and one makes the difference between 429 and 200.
wikipedia_client.set_user_agent(
    "class-02c-observability-lab/1.0 (ADK classroom exercise)"
)
wikipedia_client.set_rate_limiting(True)


def build_model() -> Gemini:
    """Create the model wrapper used by each LLM agent."""
    return Gemini(model=MODEL_NAME, retry_options=RETRY_OPTIONS)


# Tools

def append_to_state(
    tool_context: ToolContext,
    field: str,
    response: str,
) -> dict[str, str]:
    """Append new output to a list stored under a session-state key."""
    existing_state = tool_context.state.get(field, [])
    if not isinstance(existing_state, list):
        existing_state = [str(existing_state)]
    tool_context.state[field] = [*existing_state, response]
    LOGGER.info("Added an item to state key %s", field)
    return {"status": "success"}


def wikipedia(query: str) -> dict[str, str]:
    """Look up a subject on Wikipedia and return an article summary.

    Args:
        query: The subject to search for.

    Returns:
        A dict with a `status` of `success` or `unavailable`, and a `result`
        holding either the article text or an explanation of the failure.
    """
    api_wrapper = WikipediaAPIWrapper()
    last_error = "no result"

    for attempt in range(1, WIKIPEDIA_ATTEMPTS + 1):
        try:
            result = api_wrapper.run(query)
        except Exception as error:  # noqa: BLE001 - any transport or parse failure
            # Wikipedia throttles by IP, and a throttled response is an HTML
            # page that fails to parse as JSON. Without this guard the
            # exception ends the whole invocation.
            last_error = f"{type(error).__name__}: {error}"
            LOGGER.warning(
                "Wikipedia lookup failed for %r (attempt %d/%d): %s",
                query,
                attempt,
                WIKIPEDIA_ATTEMPTS,
                last_error,
            )
        else:
            if result:
                return {"status": "success", "result": result}
            last_error = "Wikipedia returned an empty result"
            LOGGER.warning(
                "Wikipedia returned nothing for %r (attempt %d/%d)",
                query,
                attempt,
                WIKIPEDIA_ATTEMPTS,
            )

        if attempt < WIKIPEDIA_ATTEMPTS:
            time.sleep(WIKIPEDIA_BACKOFF_SECONDS * attempt)

    LOGGER.error("Wikipedia unavailable for %r: %s", query, last_error)
    return {
        "status": "unavailable",
        "result": (
            f"Wikipedia could not be reached ({last_error}). Continue using what "
            "you already know about the subject, and say that the lookup failed."
        ),
    }


async def write_file(
    tool_context: ToolContext,
    directory: str,
    filename: str,
    content: str,
) -> dict[str, str]:
    """Save the finished pitch as an artifact, and as a local file when possible.

    Args:
        directory: Ignored. The destination is fixed.
        filename: Desired name; only the stem is used, sanitised.
        content: The pitch text.

    Returns:
        A dict describing where the pitch was stored.
    """
    del directory
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(filename).stem).strip("._")
    safe_stem = safe_stem or "movie_pitch"
    artifact_name = f"{safe_stem}.txt"

    # The artifact service is the only destination that survives deployment:
    # on Agent Engine the container filesystem is ephemeral. Locally it writes
    # under the agent directory and shows up in the web UI's Artifacts panel.
    version = await tool_context.save_artifact(
        artifact_name,
        types.Part.from_bytes(
            data=content.encode("utf-8"),
            mime_type="text/plain",
        ),
    )

    # A local copy keeps the classroom exercise tangible when running on a
    # laptop. It is best-effort: a read-only or absent directory is not a
    # failure, because the artifact above is already saved.
    local_path = None
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        target = OUTPUT_DIR / artifact_name
        target.write_text(content, encoding="utf-8")
        local_path = str(target)
    except OSError as error:
        LOGGER.info(
            "No local copy written to %s (%s); the artifact is saved.",
            OUTPUT_DIR,
            error,
        )

    return {
        "status": "success",
        "artifact": artifact_name,
        "version": str(version),
        "path": local_path or f"artifact:{artifact_name}",
    }


# Agents

critic = Agent(
    name="critic",
    model=build_model(),
    description="Reviews the outline so that it can be improved.",
    instruction="""
    INSTRUCTIONS:
    Consider these questions about the PLOT_OUTLINE:
    - Does it have a satisfying three-act cinematic structure?
    - Are the characters' struggles engaging?
    - Does it feel grounded in a real historical period?
    - Does it incorporate useful historical details from RESEARCH?

    If the PLOT_OUTLINE does a good job on these questions, call exit_loop.
    If significant improvements can be made, call append_to_state with field
    'CRITICAL_FEEDBACK' and add precise feedback for the next pass.
    Explain your decision and briefly summarize the feedback provided.

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    RESEARCH:
    { research? }
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[append_to_state, exit_loop],
)

box_office_researcher = Agent(
    name="box_office_researcher",
    model=build_model(),
    description="Considers the box-office potential of this film.",
    instruction="""
    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    INSTRUCTIONS:
    Write a report on the box-office potential of a movie like the one in
    PLOT_OUTLINE, using the reported performance of comparable recent films.
    """,
    output_key="box_office_report",
)

casting_agent = Agent(
    name="casting_agent",
    model=build_model(),
    description="Generates casting ideas for this film.",
    instruction="""
    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    INSTRUCTIONS:
    Generate casting ideas for the characters in PLOT_OUTLINE. Suggest actors
    who have received positive feedback in similar roles, and explain the fit.
    """,
    output_key="casting_report",
)

preproduction_team = ParallelAgent(
    name="preproduction_team",
    description="Produces box-office and casting reports at the same time.",
    sub_agents=[box_office_researcher, casting_agent],
)

file_writer = Agent(
    name="file_writer",
    model=build_model(),
    description="Creates marketing details and saves a pitch document.",
    instruction="""
    INSTRUCTIONS:
    - Create a marketable, contemporary movie title for the movie described in
      PLOT_OUTLINE. Reuse an existing title only if it is strong.
    - Use write_file to create a new txt file:
        - Use the movie title as filename.
        - Write to the movie_pitches directory.
        - Include the PLOT_OUTLINE, BOX_OFFICE_REPORT, and CASTING_REPORT.

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    BOX_OFFICE_REPORT:
    { box_office_report? }

    CASTING_REPORT:
    { casting_report? }
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[write_file],
)

screenwriter = Agent(
    name="screenwriter",
    model=build_model(),
    description=(
        "Write a logline and plot outline for a biopic about a historical "
        "character."
    ),
    instruction="""
    INSTRUCTIONS:
    Your goal is to write a logline and three-act plot outline for an inspiring
    movie about the historical character(s) described by PROMPT: { PROMPT? }

    - If there is CRITICAL_FEEDBACK, use it to improve the outline.
    - If there is RESEARCH, use relevant historical details.
    - If there is a PLOT_OUTLINE, improve upon it.
    - Use append_to_state to write the new draft to 'PLOT_OUTLINE'.
    - Summarize what you focused on in this pass.

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    RESEARCH:
    { research? }

    CRITICAL_FEEDBACK:
    { CRITICAL_FEEDBACK? }
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[append_to_state],
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
)

researcher = Agent(
    name="researcher",
    model=build_model(),
    description="Answer research questions using Wikipedia.",
    instruction="""
    PROMPT:
    { PROMPT? }

    PLOT_OUTLINE:
    { PLOT_OUTLINE? }

    CRITICAL_FEEDBACK:
    { CRITICAL_FEEDBACK? }

    INSTRUCTIONS:
    - If there is CRITICAL_FEEDBACK, research facts that address it.
    - If there is PLOT_OUTLINE, research facts that add historical detail.
    - If both are empty, gather facts about the person in PROMPT.
    - Use append_to_state to add your research to 'research'.
    - Summarize what you learned.
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[wikipedia, append_to_state],
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
)

writers_room = LoopAgent(
    name="writers_room",
    description="Iterates through research and writing to improve a movie plot outline.",
    sub_agents=[researcher, screenwriter, critic],
    max_iterations=5,
)

film_concept_team = SequentialAgent(
    name="film_concept_team",
    description="Write a film plot outline and save it as a text file.",
    sub_agents=[writers_room, preproduction_team, file_writer],
)

root_agent = Agent(
    name="greeter",
    model=build_model(),
    description="Guides the user in crafting a movie plot.",
    instruction="""
    - Tell the user you will help write a pitch for a hit movie. Ask for a
      historical figure to create a movie about.
    - When the user responds, use append_to_state to store the response in
      'PROMPT', then transfer to film_concept_team.
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
    tools=[append_to_state],
    sub_agents=[film_concept_team],
)

quota_plugin = Graceful429Plugin(
    name="graceful_429_plugin",
    fallback_text={
        "default": (
            "The model quota is temporarily exhausted. Your session state is "
            "preserved; wait briefly and retry the last step."
        )
    },
)

app = App(
    name="workflow_agents",
    root_agent=root_agent,
    plugins=[quota_plugin],
)
