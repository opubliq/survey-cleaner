#!/usr/bin/env python3
"""
Survey Processing Orchestrator

Manages the end-to-end workflow for cleaning survey data via Anthropic API:
1. Initialize survey structure (via survey-init-agent)
2. Process variables one-by-one (via survey-variable-cleaner-agent)
3. Finalize outputs (run clean.py, validate)

Usage:
    python surveys/process_survey.py ces19
    python surveys/process_survey.py test --limit 5
"""

import sys
import subprocess
import json
import re
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import logging
from anthropic import Anthropic
from dotenv import load_dotenv
from agent_tools import TOOL_DEFINITIONS, execute_tool
from cost_calculator import CostTracker, MODEL_ALIASES

# Load environment variables from .env file
load_dotenv()


def load_agent_instructions(agent_name: str) -> str:
    """Load agent instructions from markdown file

    Args:
        agent_name: Name of agent (e.g., "survey-init-agent")

    Returns:
        Agent instructions as string (removes frontmatter)
    """
    agent_file = Path(f".claude/agents/{agent_name}.md")
    if not agent_file.exists():
        raise FileNotFoundError(f"Agent file not found: {agent_file}")

    content = agent_file.read_text()

    # Remove YAML frontmatter (between --- markers)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    return content


def _format_tool_detail(tool_name: str, tool_input: dict) -> str:
    """Format tool call for logging with relevant details

    Args:
        tool_name: Name of tool
        tool_input: Tool parameters

    Returns:
        Formatted string for logging
    """
    if tool_name == "bash":
        cmd = tool_input.get("command", "")
        # Truncate long commands
        if len(cmd) > 60:
            cmd = cmd[:57] + "..."
        return f"bash: {cmd}"

    elif tool_name == "read_file":
        path = tool_input.get("file_path", "")
        # Show just filename if in surveys dir
        if path.startswith("surveys/"):
            path = path.replace("surveys/", "")
        return f"read: {path}"

    elif tool_name == "write_file":
        path = tool_input.get("file_path", "")
        content_len = len(tool_input.get("content", ""))
        if path.startswith("surveys/"):
            path = path.replace("surveys/", "")
        return f"write: {path} ({content_len} chars)"

    elif tool_name == "edit_file":
        path = tool_input.get("file_path", "")
        if path.startswith("surveys/"):
            path = path.replace("surveys/", "")
        return f"edit: {path}"

    else:
        return f"{tool_name}: {tool_input}"


def call_agent(
    agent_name: str,
    prompt: str,
    logger=None,
    context: dict = None,
    model: str = "sonnet",
    cost_tracker: Optional[CostTracker] = None
) -> str:
    """Call agent via Anthropic API with agentic tool use loop

    This function implements an agentic workflow where:
    1. Agent requests tools to execute (bash, read, write, edit)
    2. We execute them locally
    3. Send results back to agent
    4. Loop until agent completes task

    Args:
        agent_name: Name of agent to call
        prompt: User prompt for the agent
        logger: Optional logger for output
        context: Optional dict of context to inject into system prompt (e.g., cleaning_rules)
        model: Model to use ("sonnet" or "haiku", default: "sonnet")
        cost_tracker: Optional CostTracker instance for cost monitoring

    Returns:
        Final agent response as string
    """
    # Resolve model alias to full name
    model_name = MODEL_ALIASES.get(model, model)

    if logger:
        logger.info(f"Calling {agent_name} via API ({model}) with tool use...")

    # Load agent instructions
    instructions = load_agent_instructions(agent_name)

    # Build system prompt with prompt caching
    # Structure: base instructions + context (both cached)
    system_blocks = [
        {
            "type": "text",
            "text": instructions,
            "cache_control": {"type": "ephemeral"}
        }
    ]

    # Inject context if provided (also cached)
    if context and "cleaning_rules" in context:
        context_str = "\n\n## Context: Cleaning Rules (surveys/cleaning_rules.json)\n\n"
        context_str += "```json\n"
        context_str += json.dumps(context["cleaning_rules"], indent=2)
        context_str += "\n```\n\n"
        context_str += "**Note**: You already have access to cleaning_rules.json above. Do NOT read it again via tools.\n"

        system_blocks.append({
            "type": "text",
            "text": context_str,
            "cache_control": {"type": "ephemeral"}
        })

    # Use system blocks instead of single string for caching
    system = system_blocks

    # Initialize Anthropic client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = Anthropic(api_key=api_key)

    # Initialize conversation
    messages = [{"role": "user", "content": prompt}]

    # Agentic loop
    iteration = 0
    max_iterations = 50  # Safety limit

    try:
        while iteration < max_iterations:
            iteration += 1

            if logger:
                logger.info(f"  API call {iteration}...")

            # Call API with tools and caching
            response = client.messages.create(
                model=model_name,
                max_tokens=8000,
                system=system,
                messages=messages,
                tools=TOOL_DEFINITIONS
            )

            # Track cost if tracker provided
            if cost_tracker and hasattr(response, 'usage'):
                cost_tracker.add_call(response.usage.__dict__, model_name)

            # Check stop reason
            if response.stop_reason == "end_turn":
                # Agent is done, extract final text
                if logger:
                    logger.info(f"  Agent completed after {iteration} iterations")

                # Extract text content from response
                text_parts = []
                for block in response.content:
                    if hasattr(block, 'text'):
                        text_parts.append(block.text)

                return "\n".join(text_parts) if text_parts else "Task completed"

            elif response.stop_reason == "tool_use":
                # Agent wants to use tools
                tool_results = []
                tool_count = 0

                # Process all content blocks
                for block in response.content:
                    if block.type == "tool_use":
                        tool_count += 1
                        if logger:
                            # Log tool with details
                            tool_detail = _format_tool_detail(block.name, block.input)
                            logger.info(f"    Tool {tool_count}: {tool_detail}")

                        # Execute tool locally
                        result = execute_tool(block.name, block.input)

                        # Add result
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })

                if logger:
                    logger.info(f"    ✓ Executed {tool_count} tools")

                # Add assistant message to conversation
                messages.append({"role": "assistant", "content": response.content})

                # Add tool results as user message
                messages.append({"role": "user", "content": tool_results})

            elif response.stop_reason == "max_tokens":
                if logger:
                    logger.warning("  Agent hit max_tokens limit")

                # Extract what we have
                text_parts = []
                for block in response.content:
                    if hasattr(block, 'text'):
                        text_parts.append(block.text)

                return "\n".join(text_parts) if text_parts else "Max tokens reached"

            else:
                if logger:
                    logger.warning(f"  Unknown stop_reason: {response.stop_reason}")
                break

        # Hit max iterations
        if logger:
            logger.warning(f"Agent hit max iterations ({max_iterations})")

        return "Agent exceeded maximum iterations"

    except Exception as e:
        if logger:
            logger.error(f"API call failed: {e}")
        raise


class SurveyOrchestrator:
    def __init__(self, survey_name: str, limit: int = None):
        self.survey_name = survey_name
        self.survey_dir = Path(f"surveys/{survey_name}")
        self.todo_file = self.survey_dir / "variables_todo.md"
        self.pending_vars_file = self.survey_dir / "pending_vars.txt"
        self.log_file = self.survey_dir / "process.log"
        self.limit = limit

        # Setup logging
        self.setup_logging()

        # Load cleaning rules once (cached for all variables)
        self.cleaning_rules = self._load_cleaning_rules()

        # Initialize cost tracking
        self.cost_tracker = CostTracker(survey_name)

    def _load_cleaning_rules(self) -> dict:
        """Load cleaning rules from JSON file (cached)

        Returns:
            Dict with cleaning rules, or empty dict if file not found
        """
        rules_file = Path("surveys/cleaning_rules.json")
        if rules_file.exists():
            try:
                with open(rules_file, 'r', encoding='utf-8') as f:
                    rules = json.load(f)
                self.logger.info("✓ Loaded cleaning_rules.json (cached for all variables)")
                return rules
            except Exception as e:
                self.logger.warning(f"Failed to load cleaning_rules.json: {e}")
                return {}
        else:
            self.logger.warning("cleaning_rules.json not found")
            return {}

    def setup_logging(self):
        """Setup logging to both file and console"""
        # Create log directory if needed
        self.survey_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ],
            force=True  # Override any existing config
        )
        self.logger = logging.getLogger(__name__)

    def parse_todo(self) -> Tuple[List[str], List[str], List[str], List[Dict]]:
        """Parse variables_todo.md and categorize variables

        Returns:
            Tuple of (pending, in_progress, completed, questions)
            questions is a list of dicts with 'variable' and 'question' keys
        """
        if not self.todo_file.exists():
            return [], [], [], []

        content = self.todo_file.read_text()

        pending = []
        in_progress = []
        completed = []
        questions = []

        # Parse pending variables
        pending_pattern = r'- \[ \] (.+)'
        pending_matches = re.findall(pending_pattern, content)
        pending = [m.strip() for m in pending_matches]

        # Parse in progress
        progress_pattern = r'- \[~\] (.+)'
        progress_matches = re.findall(progress_pattern, content)
        in_progress = [m.strip() for m in progress_matches]

        # Parse completed
        completed_pattern = r'- \[x\] (.+)'
        completed_matches = re.findall(completed_pattern, content)
        completed = [m.strip() for m in completed_matches]

        # Parse questions
        question_pattern = r'- \[\?\] ([^:]+): QUESTION: (.+)'
        question_matches = re.findall(question_pattern, content)
        questions = [
            {'variable': var.strip(), 'question': q.strip()}
            for var, q in question_matches
        ]

        return pending, in_progress, completed, questions

    def get_pending_variables(self) -> List[str]:
        """Get list of pending variables from pending_vars.txt

        Returns:
            List of variable names
        """
        if not self.pending_vars_file.exists():
            return []

        content = self.pending_vars_file.read_text()
        variables = [line.strip() for line in content.splitlines() if line.strip()]
        return variables

    def init_survey(self) -> bool:
        """Initialize survey structure using survey-init-agent via API

        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"Initializing survey: {self.survey_name}")

        # Check if already initialized
        if self.todo_file.exists() and self.pending_vars_file.exists():
            self.logger.info("Survey already initialized (variables_todo.md and pending_vars.txt exist)")
            return True

        # Call survey-init-agent via API (use Haiku for simple task)
        try:
            result = call_agent(
                agent_name="survey-init-agent",
                prompt=f"Initialize survey surveys/{self.survey_name}",
                logger=self.logger,
                model="haiku",
                cost_tracker=self.cost_tracker
            )

            # Log agent output
            self.logger.info("Agent output:")
            self.logger.info(result)

            # Check if files were created
            if self.todo_file.exists() and self.pending_vars_file.exists():
                self.logger.info("✓ Survey initialized successfully")
                return True
            else:
                self.logger.error("✗ Initialization incomplete - required files not created")
                return False

        except Exception as e:
            self.logger.error(f"Failed to initialize survey: {e}")
            return False

    def process_variable(self, variable: str) -> str:
        """Process a single variable using survey-variable-cleaner-agent via API

        Args:
            variable: Variable name to process

        Returns:
            Status: 'completed', 'question', 'error', or 'unknown'
        """
        self.logger.info(f"Processing variable: {variable}")

        # Prepare context with cleaning rules (avoid re-reading file)
        context = {}
        if self.cleaning_rules:
            context["cleaning_rules"] = self.cleaning_rules

        # Call survey-variable-cleaner-agent via API (use Sonnet for complex task)
        try:
            result = call_agent(
                agent_name="survey-variable-cleaner-agent",
                prompt=f"Process ONLY variable '{variable}' in surveys/{self.survey_name}",
                logger=self.logger,
                context=context,
                model="sonnet",
                cost_tracker=self.cost_tracker
            )

            # Log agent output (truncated)
            output_preview = result[:500] + "..." if len(result) > 500 else result
            self.logger.info(f"Agent output preview: {output_preview}")

        except Exception as e:
            self.logger.error(f"API call failed for variable {variable}: {e}")
            return 'error'

        # Parse status from variables_todo.md
        if not self.todo_file.exists():
            self.logger.warning("variables_todo.md not found")
            return 'unknown'

        content = self.todo_file.read_text()

        # Check status markers
        if f"[x] {variable}" in content:
            self.logger.info(f"  → Completed ✓")
            return 'completed'
        elif f"[-] {variable}" in content:
            # Extract skip reason
            match = re.search(rf'\[-\] {re.escape(variable)} - SKIPPED: (.+)', content)
            skip_reason = match.group(1) if match else "Unknown reason"
            self.logger.info(f"  → Skipped: {skip_reason}")
            return 'completed'  # Count as completed (processed)
        elif f"[?] {variable}" in content:
            # Extract question text
            match = re.search(rf'\[\?\] {re.escape(variable)}[^:]*: QUESTION: (.+)', content)
            question_text = match.group(1) if match else "Unknown question"
            self.logger.warning(f"  → Question: {question_text}")
            return 'question'
        elif f"[!] {variable}" in content:
            self.logger.error(f"  → Error !")
            return 'error'
        else:
            self.logger.warning(f"  → Status unknown")
            return 'unknown'

    def finalize_survey(self) -> bool:
        """Run final clean.py script and validate outputs

        Returns:
            True if successful, False otherwise
        """
        self.logger.info("Finalizing survey...")

        clean_script = self.survey_dir / "clean.py"
        if not clean_script.exists():
            self.logger.error(f"clean.py not found at {clean_script}")
            return False

        # Run clean.py
        try:
            self.logger.info("Running clean.py...")
            result = subprocess.run(
                ["python", str(clean_script)],
                cwd=self.survey_dir.parent,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.logger.info("  → clean.py executed successfully ✓")
                # Log stdout (first 1000 chars)
                if result.stdout:
                    preview = result.stdout[:1000]
                    self.logger.info(f"Output: {preview}")
            else:
                self.logger.error(f"  → clean.py failed with return code {result.returncode}")
                self.logger.error(result.stderr)
                return False

        except subprocess.TimeoutExpired:
            self.logger.error("  → clean.py timed out after 5 minutes")
            return False
        except Exception as e:
            self.logger.error(f"  → Error running clean.py: {e}")
            return False

        # Validate outputs
        processed_dir = self.survey_dir / "processed"
        data_cleaned = processed_dir / "data_cleaned.csv"
        codebook_json = processed_dir / "codebook.json"

        if data_cleaned.exists():
            self.logger.info(f"  → {data_cleaned.name} exists ✓")
        else:
            self.logger.warning(f"  → {data_cleaned.name} not found")

        if codebook_json.exists():
            self.logger.info(f"  → {codebook_json.name} exists ✓")
        else:
            self.logger.warning(f"  → {codebook_json.name} not found")

        return True

    def generate_report(self, stats: Dict) -> str:
        """Generate final processing report

        Args:
            stats: Dictionary with processing statistics

        Returns:
            Report string
        """
        report = f"""
{'='*70}
SURVEY PROCESSING REPORT: {self.survey_name}
{'='*70}

Started:  {stats['start_time']}
Finished: {stats['end_time']}
Duration: {stats['duration']}

VARIABLES PROCESSED:
  Total:      {stats['total']}
  Completed:  {stats['completed']} ✓
  Questions:  {stats['questions']} ?
  Errors:     {stats['errors']} !
  Skipped:    {stats['skipped']}

"""

        if stats['question_list']:
            report += "QUESTIONS NEEDING HUMAN INPUT:\n"
            for q in stats['question_list']:
                report += f"  - {q['variable']}: {q['question']}\n"
            report += "\n"

        if stats['error_list']:
            report += "ERRORS:\n"
            for err in stats['error_list']:
                report += f"  - {err}\n"
            report += "\n"

        report += "OUTPUTS:\n"
        report += f"  - Clean script: surveys/{self.survey_name}/clean.py\n"
        report += f"  - Cleaned data: surveys/{self.survey_name}/processed/data_cleaned.csv\n"
        report += f"  - Codebook:     surveys/{self.survey_name}/processed/codebook.json\n"
        report += f"  - Process log:  surveys/{self.survey_name}/process.log\n"

        report += f"\n{'='*70}\n"

        return report

    def run(self):
        """Main orchestration workflow"""
        start_time = datetime.now()
        self.logger.info(f"Starting survey processing: {self.survey_name}")

        # Step 1: Initialize if needed
        if not self.todo_file.exists() or not self.pending_vars_file.exists():
            if not self.init_survey():
                self.logger.error("Failed to initialize survey. Exiting.")
                sys.exit(1)

        # Step 2: Get pending variables from pending_vars.txt
        pending_vars = self.get_pending_variables()

        # Also parse todo file for current status
        _, in_progress, completed, questions = self.parse_todo()

        total_vars = len(pending_vars)
        self.logger.info(f"Variables: {total_vars} total in pending_vars.txt")
        self.logger.info(f"Current status: {len(completed)} completed, {len(questions)} questions")

        # Apply limit if specified
        variables_to_process = pending_vars[:self.limit] if self.limit else pending_vars

        if self.limit:
            self.logger.info(f"Processing limited to {self.limit} variables")

        # Step 3: Process variables
        processed_count = 0
        question_count = 0
        error_count = 0
        question_list = []
        error_list = []

        for idx, variable in enumerate(variables_to_process, 1):
            self.logger.info(f"\n[{idx}/{len(variables_to_process)}] Variable: {variable}")

            status = self.process_variable(variable)

            if status == 'completed':
                processed_count += 1
            elif status == 'question':
                question_count += 1
                # Re-parse to get question text
                _, _, _, qs = self.parse_todo()
                for q in qs:
                    if q['variable'] == variable:
                        question_list.append(q)
                        break
            elif status == 'error':
                error_count += 1
                error_list.append(variable)

        # Step 4: Finalization
        if processed_count > 0 and question_count == 0 and error_count == 0 and not self.limit:
            self.logger.info("\nAll variables processed successfully. Running finalization...")
            self.finalize_survey()
        else:
            self.logger.info("\nSkipping finalization")
            if question_count > 0:
                self.logger.info("  → Questions need human input")
            if error_count > 0:
                self.logger.info("  → Errors occurred")
            if self.limit:
                self.logger.info("  → Run without --limit to process remaining variables")

        # Step 5: Generate report
        end_time = datetime.now()
        duration = end_time - start_time

        stats = {
            'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': str(duration).split('.')[0],
            'total': len(variables_to_process),
            'completed': processed_count + len(completed),
            'questions': question_count,
            'errors': error_count,
            'skipped': len(pending_vars) - len(variables_to_process) if self.limit else 0,
            'question_list': question_list,
            'error_list': error_list
        }

        report = self.generate_report(stats)
        print(report)

        # Save report
        report_file = self.survey_dir / f"cleaning_report_{start_time.strftime('%Y-%m-%d_%H-%M')}.md"
        report_file.write_text(report)
        self.logger.info(f"Report saved to {report_file}")

        # Save and display cost report
        self.cost_tracker.save_report()
        self.cost_tracker.print_summary()


def main():
    if len(sys.argv) < 2:
        print("Usage: python surveys/process_survey.py <survey_name> [--limit N]")
        print("Examples:")
        print("  python surveys/process_survey.py ces19")
        print("  python surveys/process_survey.py test --limit 5")
        sys.exit(1)

    survey_name = sys.argv[1]
    limit = None

    # Parse optional limit argument
    if len(sys.argv) > 2 and sys.argv[2] == '--limit':
        if len(sys.argv) > 3:
            limit = int(sys.argv[3])

    orchestrator = SurveyOrchestrator(survey_name, limit=limit)
    orchestrator.run()


if __name__ == "__main__":
    main()
