"""Gemini Deep Research Script for Kakuro Market Analysis.

Uses the Interactions API with the Deep Research agent, which is the only
supported method for deep research tasks. See:
https://ai.google.dev/gemini-api/docs/deep-research
"""

import os
import sys
from pathlib import Path
import time

try:
    from google import genai
except ImportError:
    print("Error: google-genai package not installed or outdated.")
    print("Install/upgrade with: pip install -U google-genai")
    sys.exit(1)


def build_research_prompt(requirements_text: str) -> str:
    """Build the research prompt for Kakuro market analysis."""
    return f"""Perform comprehensive deep research on the Kakuro puzzle \
book market for Amazon KDP based on the following requirements:

{requirements_text}

CRITICAL INSTRUCTIONS:
1. Provide SPECIFIC, VERIFIABLE data with sources.
2. For competitors, include actual BSRs, price points, puzzle counts, and \
review summaries.
3. For keywords, provide estimated search volumes or relative popularity \
rankings.
4. For pricing, provide a clear recommendation based on current KDP \
printing costs and competitor ranges.
5. For trends, identify seasonal patterns and market gaps.
6. Format the output as a comprehensive markdown report suitable for \
saving as multiple research documents.

Your response should be structured to address each of the four research areas in detail:
- **Competitors Analysis**
- **Keyword Research**
- **Pricing Strategy**
- **Market Trends**
"""


def main():
    """Execute deep research using Gemini API."""
    # Get API key from environment
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)

    # Create the Gemini client (new API style)
    client = genai.Client(api_key=api_key)

    # Read requirements
    project_root = Path(__file__).parent.parent
    requirements_path = project_root / "research" / "external_tool_requirements.md"

    if not requirements_path.exists():
        print(f"Error: Requirements file not found at {requirements_path}")
        sys.exit(1)

    requirements = requirements_path.read_text()
    prompt = build_research_prompt(requirements)

    print("Starting Deep Research for Kakuro market...")
    print("This may take several minutes as the agent searches external resources...")
    print()

    start_time = time.time()

    try:
        # Use the Interactions API with the Deep Research agent
        # This is the ONLY supported way to use Deep Research
        # Agent ID: deep-research-pro-preview-12-2025
        interaction = client.interactions.create(
            input=prompt, agent="deep-research-pro-preview-12-2025", background=True
        )

        print(f"Research task started: {interaction.id}")
        print("Polling for results (checking every 30 seconds)...")

        # Poll for completion
        poll_count = 0
        while True:
            interaction = client.interactions.get(interaction.id)
            poll_count += 1

            if interaction.status == "completed":
                duration = time.time() - start_time
                raw_report = interaction.outputs[-1].text

                print(f"\nResearch Completed Successfully!")
                print(f"Duration: {duration:.1f}s ({duration/60:.1f} minutes)")
                print(f"Poll attempts: {poll_count}")

                # Save raw report
                output_path = project_root / "research" / "deep_research_raw_report.md"
                output_path.write_text(raw_report)

                print(f"\nRaw research report saved to: {output_path}")
                print(
                    "\nNext step: Parse this report into the respective "
                    "research/ directories."
                )
                break

            elif interaction.status == "failed":
                print(f"\nResearch failed: {interaction.error}")
                sys.exit(1)

            else:
                elapsed = time.time() - start_time
                print(f"  [{elapsed:.0f}s] Status: {interaction.status}...")
                time.sleep(30)  # Poll every 30 seconds

    except Exception as e:
        print(f"\nError during research execution: {e}")
        print("\nTroubleshooting:")
        print(
            "1. Ensure you have the latest google-genai package: "
            "pip install -U google-genai"
        )
        print("2. Verify your API key has access to the Deep Research agent")
        print(
            "3. Check https://ai.google.dev/gemini-api/docs/deep-research "
            "for current availability"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
