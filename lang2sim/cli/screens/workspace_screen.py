"""
Screen 2: 80/20 Workspace Screen
File: lang2sim/cli/screens/workspace_screen.py
"""

import asyncio
<<<<<<< HEAD
from pathlib import Path
from typing import Any, List, Dict, Optional
from textual.screen import Screen
from textual.widgets import Static, Markdown
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.binding import Binding
from textual import work
=======
import json
from typing import Any, Dict, List, Optional

>>>>>>> upstream/staging
from rich.markup import escape
from textual import events, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Markdown, Static

from ...agent.nemotron_client import NemotronClient
from ...agent.react_loop import (
    SUPERVISOR_SYSTEM_PROMPT,
    ActionCompleted,
    ActionStarted,
    CommandExecuted,
    ContentChunk,
    PermissionRequested,
    PlanCreated,
    PlanStepUpdated,
    ReActSupervisor,
    ThoughtChunk,
    ThoughtCompleted,
    TurnCompleted,
)
from ...core.session_manager import ChatMessage, session_manager
from ..widgets.action_pill import ActionPill
from ..widgets.command_card import CommandCard
from ..widgets.plan_card import PlanCard
from ..widgets.prompt_card import PromptCard
from ..widgets.telemetry_sidebar import TelemetrySidebar
<<<<<<< HEAD
from ...agent.nemotron_client import NemotronClient
from ...core.session_manager import session_manager, ChatMessage

SYSTEM_PROMPT = (
    "You are Sim2Lang Copilot, an expert AI robotics simulation assistant. "
    "You help roboticists design, configure, inspect, and reason about Gazebo Harmonic "
    "simulations, SDF scene layouts, Nav2 navigation stacks, and robot sensor telemetry. "
    "Be concise, technically precise, conversational, and direct. Format your answers with clean Markdown. "
    "When a system message carries Lang2Sim simulation context, base answers about the robot, the run and the "
    "NQI score on those measured numbers. The app itself carries out simulation requests the user types in plain "
    "English (build a world, start a stress run, dim the lights, drop a crate, go to rack 2, stop the robot); when "
    "suggesting a next step, phrase it as such a sentence, never as a slash command."
)
=======
from ..widgets.thought_box import ThoughtBox

SYSTEM_PROMPT = SUPERVISOR_SYSTEM_PROMPT
>>>>>>> upstream/staging


class WorkspaceScreen(Screen):
    """The 80/20 split workspace screen featuring conversational LLM execution and live telemetry."""

    BINDINGS = [
        Binding("ctrl+s", "open_sessions", "Sessions", show=False),
    ]

    def __init__(
        self,
        initial_prompt: str = "",
        session_id: Optional[str] = None,
        workspace_name: str = "active_project",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.initial_prompt = initial_prompt
        self.client = NemotronClient()
        self.sim_session = None
        self.workspace_name = workspace_name
<<<<<<< HEAD
        self._sim_reachable = False   # a control API answered the last telemetry poll
        self.current_spec = None
=======
        self.always_allow_commands: bool = False
        self._pending_permissions: Dict[str, asyncio.Future] = {}
        self._active_command_cards: Dict[str, CommandCard] = {}
        self._active_plan_card: Optional[PlanCard] = None
        self._selected_text: Optional[str] = None
>>>>>>> upstream/staging

        # Session initialization
        if session_id:
            loaded = session_manager.get_session(session_id)
            if loaded:
                self.session = loaded
            else:
                self.session = session_manager.create_session(
                    title=initial_prompt[:40] if initial_prompt else "New Session",
                    workspace_name=workspace_name,
                    system_prompt=SYSTEM_PROMPT,
                )
        else:
            self.session = session_manager.create_session(
                title=initial_prompt[:40] if initial_prompt else "New Session",
                workspace_name=workspace_name,
                system_prompt=SYSTEM_PROMPT,
            )

        self.conversation_history: List[Dict[str, str]] = []
        for m in self.session.messages:
            if m.role == "system":
                self.conversation_history.append({"role": "system", "content": m.content})
            elif m.role == "user":
                self.conversation_history.append({"role": "user", "content": m.content})
            elif m.role == "assistant":
                self.conversation_history.append({"role": "assistant", "content": m.content})
        self.total_tokens_used: int = self.session.total_tokens
        self.is_streaming: bool = False
        from ..demo_commands import DemoRunner

        self.demo = DemoRunner(
            say=self._demo_say, show=self._demo_show, progress=self._demo_progress
        )
        self._progress_line: Optional[Static] = None

    def compose(self):
        # Top title bar
        yield Static(f"S2L | {self.session.title} — lang2sim", id="workspace-header")

        # 80/20 Horizontal body
        with Horizontal(id="workspace-body"):
            # Left Pane: 80% Width
            with Vertical(id="left-pane"):
                with VerticalScroll(id="chat-scroll"):
                    yield Static("", id="scroll-anchor")
                yield PromptCard(
<<<<<<< HEAD
                    placeholder='lang2sim > Describe a world to simulate, or tell the robot what to do',
=======
                    placeholder="lang2sim > Ask, or /mission · /stress · /benchmark · /report · /help",
>>>>>>> upstream/staging
                    card_id="sticky-prompt-input",
                    id="sticky-input-card",
                )

            # Right Sidebar: 20% Width
            yield TelemetrySidebar()

        # Bottom footer bar
        with Horizontal(id="workspace-footer"):
            yield Static("~", classes="footer-left")
            yield Static("", classes="footer-spacer")
            yield Static(
                f"[#ced6e0]{self.total_tokens_used:,} tokens (1%)[/]   "
                "[#57606f]ctrl+s sessions[/]   [#57606f]ctrl+p commands[/]   [#2ed573]●[/] [#57606f]lang2sim 2.0.0[/]",
                id="footer-status",
                classes="footer-right",
            )

    TELEMETRY_POLL_S = 1.0

    def on_mount(self) -> None:
        """Mount existing session messages, focus input, and process initial prompt."""
        self.set_interval(self.TELEMETRY_POLL_S, self.poll_telemetry)
        chat_scroll = self.query_one("#chat-scroll", VerticalScroll)

        # Restore past messages if loading an existing session
        for msg in self.session.messages:
            if msg.role == "user":
                user_card = Static(f"[bold #ffffff]{msg.content}[/]", classes="user-prompt-card")
                chat_scroll.mount(user_card)
            elif msg.role == "assistant":
                if msg.thought:
                    dur = msg.thought_duration_str or "1.2s"
                    thought_box = ThoughtBox(duration_str=dur, content=msg.thought)
                    chat_scroll.mount(thought_box)
                if msg.actions:
                    for act in msg.actions:
                        if act.tool_name == "run_command" or (
                            act.arguments and "command" in act.arguments
                        ):
                            cmd = act.arguments.get("command", "") if act.arguments else ""
                            out = (
                                act.output.get("stdout", "") if isinstance(act.output, dict) else ""
                            )
                            err = (
                                act.output.get("stderr", "") if isinstance(act.output, dict) else ""
                            )
                            rc = (
                                act.output.get("exit_code", 0)
                                if isinstance(act.output, dict)
                                else 0
                            )
                            card = CommandCard(
                                event_id="restored",
                                command=cmd,
                                tool_name=act.tool_name,
                                arguments=act.arguments,
                                permission_required=False,
                            )
                            chat_scroll.mount(card)
                            card.set_result(
                                exit_code=rc, duration_str=act.duration_str, stdout=out, stderr=err
                            )
                        else:
                            pill = ActionPill(
                                tool_name=act.tool_name,
                                duration_str=act.duration_str,
                                status=act.status,
                            )
                            chat_scroll.mount(pill)
                resp_md = Markdown(msg.content, classes="assistant-response")
                chat_scroll.mount(resp_md)

        sidebar = self.query_one(TelemetrySidebar)
        capacity_pct = min(100, max(1, self.total_tokens_used // 1000))
        sidebar.update_telemetry(
            tokens_used=self.total_tokens_used,
            context_capacity_pct=capacity_pct,
        )

        chat_scroll.scroll_end(animate=False)
        self.query_one("#sticky-input-card", PromptCard).focus_input()

        # Start periodic telemetry polling from active control server
        self.set_interval(1.5, self.poll_live_telemetry)

        if self.initial_prompt:
            self.handle_user_prompt(self.initial_prompt)

    @work(exclusive=True, group="telemetry")
    async def poll_live_telemetry(self) -> None:
        """Polls live Gazebo & ROS 2 telemetry from ControlClient or local container in real time."""
        # 1. Try ControlClient
        try:
            from lang2sim.runtime.control_api.client import ControlClient

            async with ControlClient(timeout=0.3) as client:
                status = await client.sim_status()
                if status.status in ("running", "launching"):
                    telem = await client.telemetry()
                    pose = telem.robot_pose
                    vel = telem.robot_velocity
                    rtf_str = (
                        f"{telem.real_time_factor:.2f}x"
                        if telem.real_time_factor is not None
                        else "1.0x"
                    )
                    sidebar = self.query_one(TelemetrySidebar)
                    sidebar.update_telemetry(
                        sim_state=f"Active ({status.status.capitalize()})",
                        sim_time=f"{int(telem.sim_time // 60):02d}:{int(telem.sim_time % 60):02d}",
                        rtf=rtf_str,
                        robot_x=pose.x if pose else 0.0,
                        robot_y=pose.y if pose else 0.0,
                        speed=vel.x if vel else 0.0,
                        collision_count=0,
                    )
                    return
        except Exception:
            pass

        # 2. Inspect Docker container lang2sim-sim or local ROS 2 processes
        try:
            import subprocess
            from datetime import datetime, timezone

            inspect_proc = subprocess.run(
                "docker inspect lang2sim-sim --format '{{json .State}}'",
                shell=True,
                capture_output=True,
                text=True,
                timeout=1,
            )
            sidebar = self.query_one(TelemetrySidebar)
            if inspect_proc.returncode == 0 and inspect_proc.stdout.strip():
                state_data = json.loads(inspect_proc.stdout)
                is_running = state_data.get("Running", False)
                if is_running:
                    started_at = state_data.get("StartedAt", "")
                    sim_time_str = "00:00.0"
                    if started_at:
                        try:
                            clean_ts = started_at[:26] + "Z" if "." in started_at else started_at
                            start_dt = datetime.fromisoformat(clean_ts.replace("Z", "+00:00"))
                            elapsed = (datetime.now(timezone.utc) - start_dt).total_seconds()
                            mins = int(elapsed // 60)
                            secs = elapsed % 60
                            sim_time_str = f"{mins:02d}:{secs:04.1f}"
                        except Exception:
                            pass

                    # Check if gazebo or rviz2 is running in container
                    ps_proc = subprocess.run(
                        "docker exec lang2sim-sim ps aux",
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=1,
                    )
                    out = ps_proc.stdout.lower()
                    has_gui = (
                        "rviz2" in out or "gz sim" in out or "gz-sim" in out or "ign gazebo" in out
                    )
                    sim_state = "Active (GUI)" if has_gui else "Active (Docker)"
                    rtf_str = "1.0x" if has_gui else "0.0x"

                    sidebar.update_telemetry(
                        sim_state=sim_state,
                        sim_time=sim_time_str,
                        rtf=rtf_str,
                    )
                else:
                    sidebar.update_telemetry(
                        sim_state="Idle (Offline)",
                        sim_time="00:00.0",
                        rtf="0.0x",
                    )
            else:
                sidebar.update_telemetry(
                    sim_state="Idle (Offline)",
                    sim_time="00:00.0",
                    rtf="0.0x",
                )
        except Exception:
            pass

    def action_open_sessions(self) -> None:
        """Open custom floating sessions modal."""
        from .sessions_modal import SessionsModal

        self.app.push_screen(
            SessionsModal(workspace_name=self.session.workspace_name),
            callback=self.on_session_switched,
        )

    def on_session_switched(self, session_id: Optional[str]) -> None:
        if session_id and session_id != self.session.id:
            self.load_session(session_id)

    def load_session(self, session_id: str) -> None:
        """Load and mount a selected session cleanly."""
        loaded = session_manager.get_session(session_id)
        if not loaded:
            return

        self.session = loaded
        self.conversation_history = [
            {"role": m.role, "content": m.content} for m in self.session.messages
        ]
        self.total_tokens_used = self.session.total_tokens

        chat_scroll = self.query_one("#chat-scroll", VerticalScroll)
        chat_scroll.remove_children()

        for msg in self.session.messages:
            if msg.role == "user":
                user_card = Static(f"[bold #ffffff]{msg.content}[/]", classes="user-prompt-card")
                chat_scroll.mount(user_card)
            elif msg.role == "assistant":
                if msg.thought:
                    dur = msg.thought_duration_str or "1.2s"
                    thought_box = ThoughtBox(duration_str=dur, content=msg.thought)
                    chat_scroll.mount(thought_box)
                if msg.actions:
                    for act in msg.actions:
                        if act.tool_name == "run_command" or (
                            act.arguments and "command" in act.arguments
                        ):
                            cmd = act.arguments.get("command", "") if act.arguments else ""
                            out = (
                                act.output.get("stdout", "") if isinstance(act.output, dict) else ""
                            )
                            err = (
                                act.output.get("stderr", "") if isinstance(act.output, dict) else ""
                            )
                            rc = (
                                act.output.get("exit_code", 0)
                                if isinstance(act.output, dict)
                                else 0
                            )
                            card = CommandCard(
                                event_id="restored",
                                command=cmd,
                                tool_name=act.tool_name,
                                arguments=act.arguments,
                                permission_required=False,
                            )
                            chat_scroll.mount(card)
                            card.set_result(
                                exit_code=rc, duration_str=act.duration_str, stdout=out, stderr=err
                            )
                        else:
                            pill = ActionPill(
                                tool_name=act.tool_name,
                                duration_str=act.duration_str,
                                status=act.status,
                            )
                            chat_scroll.mount(pill)
                resp_md = Markdown(msg.content, classes="assistant-response")
                chat_scroll.mount(resp_md)

        # Update header and sidebar
        self.query_one("#workspace-header", Static).update(f"S2L | {self.session.title} — lang2sim")
        sidebar = self.query_one(TelemetrySidebar)
        capacity_pct = min(100, max(1, self.total_tokens_used // 1000))
        sidebar.update_telemetry(
            tokens_used=self.total_tokens_used,
            context_capacity_pct=capacity_pct,
        )

        footer_right = self.query_one("#footer-status", Static)
        if footer_right:
            footer_right.update(
                f"[#ced6e0]{self.total_tokens_used:,} tokens ({capacity_pct}%)[/]   "
                "[#57606f]ctrl+s sessions[/]   [#57606f]ctrl+p commands[/]   [#2ed573]●[/] [#57606f]lang2sim 2.0.0[/]"
            )

        chat_scroll.scroll_end(animate=False)
        self.query_one("#sticky-input-card", PromptCard).focus_input()

    def on_prompt_card_submitted(self, message: PromptCard.Submitted) -> None:
        """When user types in sticky input card, add prompt and run execution."""
        self.handle_user_prompt(message.value)

    def _resolve_first_pending_permission(self, approved: bool, always: bool = False) -> bool:
        """Resolves the oldest pending command permission card."""
        if not self._pending_permissions:
            return False
        if always:
            self.always_allow_commands = True
        event_id, fut = next(iter(self._pending_permissions.items()))
        self._pending_permissions.pop(event_id, None)
        card = self._active_command_cards.get(event_id)
        if card:
            if approved:
                card.set_running()
            else:
                card.status = "rejected"
                card._update_classes()
                card._remove_actions_row()
                try:
                    card.query_one("#cmd-badge", Static).update(card._format_badge())
                except Exception:
                    pass
        if fut and not fut.done():
            fut.set_result(approved)
        return True

    def get_conversation_as_text(self) -> str:
        """Assembles entire active chat into clean plain text for copying."""
        lines = []
        for msg in self.session.messages:
            role_label = "USER" if msg.role == "user" else "ASSISTANT"
            lines.append(f"[{role_label}]:\n{msg.content}\n")
            if msg.thought:
                lines.append(f"[THOUGHT]:\n{msg.thought}\n")
            if msg.actions:
                for act in msg.actions:
                    lines.append(
                        f"[TOOL: {act.tool_name}]: {act.duration_str} - status: {act.status}"
                    )
        return "\n".join(lines).strip()

    def action_select_all(self) -> None:
        """Select all text in current input or select entire conversation for copying."""
        try:
            from textual.widgets import Input

            inp = self.query_one("#sticky-prompt-input", Input)
            if inp.has_focus and inp.value:
                inp.action_select_all()
                self._selected_text = inp.value
                self.app.notify("Selected input text (Ctrl+Shift+C to copy)", timeout=1.5)
                return
        except Exception:
            pass

        full_text = self.get_conversation_as_text()
        self._selected_text = full_text
        self.app.notify(
            "Selected all chat text! Press Ctrl+Shift+C to copy", title="Select All", timeout=2.0
        )

    def on_key(self, event: events.Key) -> None:
        """Global key interceptor for immediate command approval, Ctrl+A select all, and copy."""
        key = event.key.lower()

        # 1. Ctrl+A: Select All
        if key == "ctrl+a":
            event.prevent_default()
            event.stop()
            self.action_select_all()
            return

        # 2. Ctrl+Shift+C / Shift+Ctrl+C: Copy to clipboard
        if key in ("ctrl+shift+c", "shift+ctrl+c"):
            event.prevent_default()
            event.stop()
            self.app.action_copy_selection()
            return

        # 3. Pending permission card hotkeys
        if self._pending_permissions:
            try:
                from textual.widgets import Input

                inp = self.query_one("#sticky-prompt-input", Input)
                if not inp.value.strip():
                    if key in ("y", "enter"):
                        event.prevent_default()
                        event.stop()
                        self._resolve_first_pending_permission(approved=True, always=False)
                        return
                    elif key == "a":
                        event.prevent_default()
                        event.stop()
                        self._resolve_first_pending_permission(approved=True, always=True)
                        return
                    elif key in ("n", "escape"):
                        event.prevent_default()
                        event.stop()
                        self._resolve_first_pending_permission(approved=False, always=False)
                        return
            except Exception:
                pass

    def handle_user_prompt(self, prompt: str) -> None:
        """Every sentence is understood by the copilot (LLM, offline parser as fallback) and acted on.

        The user never needs a command syntax: "build a warehouse with 3 racks", "start a stress
        run", "dim the lights and drop a crate in its path", "stop the robot", "go to rack 2",
        "show me the score", "why did the score drop?" all go through intent.interpret().
        Slash commands (/sim, /stop, /mission, /stress, ...) still work as silent shortcuts.
        """
        from ..demo_commands import parse_command

        cleaned_prompt = prompt.strip()
        if not cleaned_prompt:
            return
        lowered = cleaned_prompt.lower()

<<<<<<< HEAD
        if lowered.startswith("/sim"):
            widget = self._start_turn(cleaned_prompt, "● *Building your simulation...*")
            self.run_simulation(widget, cleaned_prompt[4:].strip() or "a warehouse with 4 racks and 1 crate")
            return
        if lowered in ("/stop", "/quit-sim"):
            self.stop_simulation(self._start_turn(cleaned_prompt, "● *Stopping...*"))
            return
        command = parse_command(cleaned_prompt)
        if command is not None:
            self._mount_user(cleaned_prompt)
=======
        # 1. Natural language permission approval routing
        if self._pending_permissions:
            lowered = cleaned_prompt.lower()
            if lowered in ("y", "yes", "run", "approve", "ok", "proceed", "go"):
                self._resolve_first_pending_permission(approved=True, always=False)
                return
            elif lowered in ("a", "always", "always allow", "always_allow"):
                self._resolve_first_pending_permission(approved=True, always=True)
                return
            elif lowered in ("n", "no", "reject", "cancel", "stop", "abort"):
                self._resolve_first_pending_permission(approved=False, always=False)
                return

        # 2. Recovery for "try again" / "retry" / "restart"
        if cleaned_prompt.lower() in ("try again", "retry", "restart"):
            for _event_id, fut in list(self._pending_permissions.items()):
                if not fut.done():
                    fut.cancel()
            self._pending_permissions.clear()
            self.is_streaming = False

        # 3. Demo commands (/mission, /stress, /benchmark, ...) and plain-language stress requests
        from ..demo_commands import parse_command, parse_stress_intent

        command = parse_command(cleaned_prompt) or parse_stress_intent(cleaned_prompt)
        if command is not None:
            chat_scroll = self.query_one("#chat-scroll", VerticalScroll)
            chat_scroll.mount(
                Static(f"[bold #ffffff]{escape(cleaned_prompt)}[/]", classes="user-prompt-card")
            )
            chat_scroll.scroll_end(animate=False)
            self.session.messages.append(
                ChatMessage(
                    role="user", content=cleaned_prompt, tokens=max(1, len(cleaned_prompt) // 4)
                )
            )
            session_manager.save_session(self.session)
>>>>>>> upstream/staging
            self.run_demo_command(command)
            return
        self._mount_user(cleaned_prompt)
        self.understand_and_act(cleaned_prompt)

    @work(exclusive=False, group="intent")
    async def understand_and_act(self, text: str) -> None:
        """Natural language -> one action (intent.interpret) -> run it, saying what was understood."""
        from ..intent import interpret, situation

        line = Static("[#8b98a8]● understanding…[/]", classes="demo-line")
        self._mount_chat(line)
        mission_running = self.demo.mission_lock.locked()
        racks: List[str] = []
        spec = getattr(self, "current_spec", None)
        if spec is not None:
            racks = [o.id for o in spec.objects if "rack" in o.id]
        it = await interpret(text, self.client, sim_active=self._sim_active(), mission_running=mission_running,
                             context=situation(self._sim_active(), mission_running, racks))

        if it.action == "chat":
            line.remove()
            widget = self._start_turn(text, "● *Thinking...*", mount_prompt=False)
            self.conversation_history.append({"role": "user", "content": text})
            self.stream_response(widget, text)
            return
        line.update(f"[#8b98a8]Understood ({escape(it.source)}): {escape(it.summary)}[/]")
        if it.action == "new_sim":
            widget = self._start_turn(text, "● *Building your simulation...*", mount_prompt=False)
            self.run_simulation(widget, it.scenario or text)
            return
        if it.action == "stop_sim":
            self.stop_simulation(self._start_turn(text, "● *Stopping...*", mount_prompt=False))
            return
        if it.needs_sim and not self._sim_active():
            self._demo_say("[#f39c12]No simulation is running yet.[/] Describe a world first, e.g. "
                           "[italic]\"build a warehouse with 3 racks and 2 crates\"[/].")
            return
        command = it.command
        if command is None:
            return
        if command.name == "mission" and mission_running:
            if command.args:      # "make it harder" mid-run: stress the run that is already driving
                from ..demo_commands import Command

                command = Command("stress")
                self._demo_say("[#8b98a8]A mission is already driving, so I'm stressing it now: dim the lights "
                               "to 10% and drop a wooden crate in the robot's path.[/]")
        elif command.name == "stress" and not mission_running:
            # Nothing is being recorded: start a stress run and apply the change once the robot is moving,
            # so the request is measured against the normal run.
            from ..demo_commands import Command

            command = Command("mission", args=["stress"], then=command)
        self.run_demo_command(command)

    def _mount_user(self, text: str) -> None:
        chat_scroll = self.query_one("#chat-scroll", VerticalScroll)
<<<<<<< HEAD
        chat_scroll.mount(Static(f"[bold #ffffff]{escape(text)}[/]", classes="user-prompt-card"))
=======

        # Auto-name session if it is still "New Session"
        if self.session.title == "New Session":
            self.session.title = cleaned_prompt[:40]
            self.query_one("#workspace-header", Static).update(
                f"S2L | {self.session.title} — lang2sim"
            )

        # Mount user prompt card
        user_card = Static(f"[bold #ffffff]{cleaned_prompt}[/]", classes="user-prompt-card")
        chat_scroll.mount(user_card)
>>>>>>> upstream/staging
        chat_scroll.scroll_end(animate=False)
        if self.session.title == "New Session":
            self.session.title = text[:40]
            self.query_one("#workspace-header", Static).update(f"S2L | {self.session.title} — lang2sim")
        self.session.messages.append(ChatMessage(role="user", content=text, tokens=max(1, len(text) // 4)))
        session_manager.save_session(self.session)

<<<<<<< HEAD
    def _sim_active(self) -> bool:
        """A simulation this app started, or any control API answering (run_sim.py, replay)."""
        return self.sim_session is not None or self._sim_reachable

    def _start_turn(self, prompt: str, placeholder: str, mount_prompt: bool = True) -> Markdown:
        """Mount the user's prompt (unless already shown) and an assistant reply widget."""
        chat_scroll = self.query_one("#chat-scroll", VerticalScroll)
        if mount_prompt:
            self._mount_user(prompt)
        widget = Markdown(placeholder, classes="assistant-response")
        chat_scroll.mount(widget)
        chat_scroll.scroll_end(animate=False)
        return widget

    # ------------------------------------------------------------------ pitch wiring
    @work(exclusive=True, group="sim")
    async def run_simulation(self, widget: Markdown, prompt: str) -> None:
        """Prompt -> SimSpec (LLM or parser) -> Part 1 world + map -> Part 3 sim -> mission -> Part 4 NQI."""
        from ...pipeline import build_run, describe, launch_and_drive, make_session, prompt_to_spec

        self.is_streaming = True
        chat_scroll = self.query_one("#chat-scroll", VerticalScroll)
        sidebar = self.query_one(TelemetrySidebar)
        sticky_card = self.query_one("#sticky-input-card", PromptCard)
        lines: List[str] = ["**● Building your simulation**", ""]
        status: List[str] = [""]

        async def render() -> None:
            await widget.update("\n".join(lines + ([f"`{status[0]}`"] if status[0] else [])))
            chat_scroll.scroll_end(animate=False)

        async def add(line: str) -> None:
            lines.append(line)
            await render()

        def on_event(text: str) -> None:
            status[0] = text
            if text.startswith(("READY", "mission sent")) or ", 0." in text:
                lines.append(f"- {text}")
            asyncio.ensure_future(render())

        try:
            spec, source = await prompt_to_spec(prompt, client=self.client)
            self.current_spec = spec
            await add(f"- **1. Spec** ({source}): {describe(spec)}")
            run, steps = await asyncio.to_thread(build_run, spec)
            await add(f"- **2. World builder (Part 1):** {steps[0]}")
            await add(f"- **3. Files:** {steps[1]}")
            if self.sim_session is not None:
                await self.sim_session.stop()
                self.sim_session = None
            session, plan = make_session()
            self.sim_session = session
            await add(f"- **4. Runtime (Part 3):** {plan.describe()}, starting `{session.opts.image}`")
            sidebar.update_telemetry(sim_state="Launching")
            await session.start()
            await add(f"- {session.view_hint}")
            locked = self.demo.mission_lock.acquire(blocking=False)
            try:
                nav, report = await launch_and_drive(session, run, on_event=on_event)
            finally:
                if locked:
                    self.demo.mission_lock.release()
            status[0] = ""
            await add("")
            await add(f"**Mission {nav.status.upper()}**" + (f": {nav.message}" if nav.message else "") + "\n")
            if report and "nqi" in report:
                import json as _json
                self.demo.show_report(_json.loads(Path(report["report_path"]).read_text()))
            await add("\nThe simulation is still running. Try: *\"stress-test it: dim the lights to 10% and drop a crate "
                      "in the robot's path\"*, *\"go to rack 2\"*, *\"stop the robot\"*, *\"run the full benchmark\"*, "
                      f"*\"why did the score change?\"*, or *\"stop the simulation\"*. Logs: `{run / 'logs'}`")
        except Exception as e:  # noqa: BLE001 - show the failure in the chat, keep the app alive
            status[0] = ""
            await add(f"\n**⚠ Simulation error:** `{type(e).__name__}: {e}`")
        finally:
            self.is_streaming = False
            sticky_card.focus_input()

    @work(exclusive=True, group="sim")
    async def stop_simulation(self, widget: Markdown) -> None:
        if self.sim_session is None:
            await widget.update("No simulation is running.")
            return
        await widget.update("● Stopping simulation...")
        await self.sim_session.stop()
        self.sim_session = None
        self.query_one(TelemetrySidebar).update_telemetry(sim_state="Stopped")
        await widget.update("🛑 **Simulation and container stopped successfully.**")

    async def on_unmount(self) -> None:
        if getattr(self, "sim_session", None) is not None:
            await self.sim_session.stop()
=======
        # Mount streaming assistant Markdown widget
        response_widget = Markdown("● *Thinking...*", classes="assistant-response")
        chat_scroll.mount(response_widget)
        chat_scroll.scroll_end(animate=False)

        # Stream response asynchronously with low latency
        self.stream_response(response_widget, cleaned_prompt)
>>>>>>> upstream/staging

    def on_command_card_approved(self, message: CommandCard.Approved) -> None:
        """User approved command execution."""
        if message.always_allow:
            self.always_allow_commands = True
        fut = self._pending_permissions.pop(message.event_id, None)
        if fut and not fut.done():
            fut.set_result(True)

    def on_command_card_rejected(self, message: CommandCard.Rejected) -> None:
        """User rejected command execution."""
        fut = self._pending_permissions.pop(message.event_id, None)
        if fut and not fut.done():
            fut.set_result(False)

    # --- demo commands ------------------------------------------------------------
    @work(exclusive=False, group="demo")
    async def run_demo_command(self, command) -> None:
        await self.demo.run(command)
        self.poll_telemetry()

    def _demo_say(self, markup: str) -> None:
        self._mount_chat(Static(markup, classes="demo-line"))

    def _demo_show(self, renderable) -> None:
        self._mount_chat(Static(renderable, classes="demo-table"))

    def _demo_progress(self, markup: Optional[str]) -> None:
        """One status line updated in place (None: leave it and start a new one next time)."""
        if markup is None:
            self._progress_line = None
            return
        if self._progress_line is None or not self._progress_line.is_attached:
            self._progress_line = Static(markup, classes="demo-line demo-progress")
            self._mount_chat(self._progress_line)
        else:
            self._progress_line.update(markup)

    def _mount_chat(self, widget) -> None:
        try:
            chat_scroll = self.query_one("#chat-scroll", VerticalScroll)
        except Exception:  # noqa: BLE001 - screen gone
            return
        chat_scroll.mount(widget)
        chat_scroll.scroll_end(animate=False)

    @work(thread=True, exclusive=True, group="telemetry")
    def poll_telemetry(self) -> None:
        """Fetch live telemetry off the UI thread (GET /v1/telemetry/live) and refresh the sidebar."""
        from ...telemetry.live import fetch_live, sidebar_fields

        fields = sidebar_fields(fetch_live(timeout=0.5))
        try:
            self.app.call_from_thread(self._apply_telemetry, fields)
        except Exception:  # noqa: BLE001 - app shutting down
            pass

    def _apply_telemetry(self, fields: Dict[str, Any]) -> None:
        self._sim_reachable = fields.get("sim_state") != "No simulation"
        try:
            self.query_one(TelemetrySidebar).update_telemetry(**fields)
        except Exception:  # noqa: BLE001 - screen not mounted any more
            pass

    @work(exclusive=True, group="chat_stream")
    async def stream_response(self, response_widget: Markdown, prompt: str) -> None:
        """Stream conversational response directly from LLM / ReAct supervisor with low latency."""
        self.is_streaming = True
        chat_scroll = self.query_one("#chat-scroll", VerticalScroll)
        sidebar = self.query_one(TelemetrySidebar)
        sticky_card = self.query_one("#sticky-input-card", PromptCard)

        if not self.client.is_configured():
            await response_widget.update(
                "**● Questions need an API key**\n\n"
                "I couldn't match that to a simulation action, and free-form answers need the LLM. "
                "Requests like *\"drop a crate in front of the robot\"* or *\"show me the score\"* work without one.\n\n"
                "To enable the copilot (it also understands any phrasing of a request):\n"
                "- Run: `export NVIDIA_API_KEY='nvapi-...'`\n"
                "- Or set `OPENAI_API_KEY='sk-...'`\n"
                "- Or add `NVIDIA_API_KEY=...` to `.env` in the project root."
            )
            self.is_streaming = False
            sticky_card.focus_input()
            return

        supervisor = ReActSupervisor(client=self.client, workspace_name=self.workspace_name)
        thought_box: Optional[ThoughtBox] = None
        thought_text_parts: List[str] = []
        content_parts: List[str] = []
        active_pills: Dict[str, ActionPill] = {}

        # Ground the answer in the running simulation (live telemetry + latest NQI report)
        from ...agent.grounding import fetch_context, with_context

        try:
            context = await asyncio.wait_for(asyncio.to_thread(fetch_context), timeout=3.0)
        except Exception:  # noqa: BLE001 - no sim context is fine
            context = None
        grounded_history = with_context(self.conversation_history, context)

        async def permission_checker(
            tool_name: str, cmd_str: str, args: dict, event_id: str
        ) -> bool:
            if self.always_allow_commands:
                card = CommandCard(
                    event_id=event_id,
                    command=cmd_str,
                    tool_name=tool_name,
                    arguments=args,
                    permission_required=False,
                )
                self._active_command_cards[event_id] = card
                await chat_scroll.mount(card, before=response_widget)
                chat_scroll.scroll_end(animate=False)
                return True

            card = CommandCard(
                event_id=event_id,
                command=cmd_str,
                tool_name=tool_name,
                arguments=args,
                permission_required=True,
            )
            self._active_command_cards[event_id] = card
            await chat_scroll.mount(card, before=response_widget)
            chat_scroll.scroll_end(animate=False)

            fut = asyncio.get_event_loop().create_future()
            self._pending_permissions[event_id] = fut
            approved = await fut
            return approved

        try:
            async for event in supervisor.stream_turn(
                self.session,
                prompt,
                grounded_history,
                permission_checker=permission_checker,
            ):
                if isinstance(event, ThoughtChunk):
                    if not thought_box:
                        thought_box = ThoughtBox(duration_str="...", content="")
                        await chat_scroll.mount(thought_box, before=response_widget)
                        chat_scroll.scroll_end(animate=False)
                    thought_text_parts.append(event.chunk)
                    thought_box.update_content("".join(thought_text_parts))

                elif isinstance(event, ThoughtCompleted):
                    if not thought_box:
                        thought_box = ThoughtBox(
                            duration_str=event.duration_str, content=event.thought
                        )
                        await chat_scroll.mount(thought_box, before=response_widget)
                    else:
                        thought_box.update_content(event.thought, duration_str=event.duration_str)
                    chat_scroll.scroll_end(animate=False)

                elif isinstance(event, PlanCreated):
                    self._active_plan_card = PlanCard(steps=event.steps, title=event.title)
                    await chat_scroll.mount(self._active_plan_card, before=response_widget)
                    chat_scroll.scroll_end(animate=False)

                elif isinstance(event, PlanStepUpdated):
                    if self._active_plan_card:
                        self._active_plan_card.update_step(
                            event.step_index, event.status, event.detail
                        )
                    chat_scroll.scroll_end(animate=False)

                elif isinstance(event, PermissionRequested):
                    chat_scroll.scroll_end(animate=False)

                elif isinstance(event, CommandExecuted):
                    card = self._active_command_cards.get(event.event_id)
                    if card:
                        card.set_result(
                            exit_code=event.exit_code,
                            duration_str=event.duration_str,
                            stdout=event.stdout,
                            stderr=event.stderr,
                        )
                    chat_scroll.scroll_end(animate=False)

                elif isinstance(event, ActionStarted):
                    if event.tool_name != "run_command" and self._active_plan_card is None:
                        pill = ActionPill(
                            tool_name=event.tool_name, duration_str="0.0s", status="running"
                        )
                        active_pills[event.tool_name] = pill
                        await chat_scroll.mount(pill, before=response_widget)
                        chat_scroll.scroll_end(animate=False)

                elif isinstance(event, ActionCompleted):
                    pill = active_pills.get(event.tool_name)
                    if pill:
                        pill.set_completed(event.duration_str)
                    elif event.tool_name != "run_command" and self._active_plan_card is None:
                        pill = ActionPill(
                            tool_name=event.tool_name,
                            duration_str=event.duration_str,
                            status=event.status,
                        )
                        await chat_scroll.mount(pill, before=response_widget)

                    # Dynamically sync live telemetry metrics into sidebar
                    if event.tool_name == "query_robot_telemetry" and isinstance(
                        event.output, dict
                    ):
                        sidebar = self.query_one(TelemetrySidebar)
                        sidebar.update_telemetry(
                            robot_x=float(event.output.get("x", 0.0)),
                            robot_y=float(event.output.get("y", 0.0)),
                            speed=float(event.output.get("speed", 0.0)),
                            clearance=float(event.output.get("clearance", 0.0)),
                            bumper_force=float(event.output.get("bumper_force_newtons", 0.0)),
                            collision_count=int(event.output.get("collision_count", 0)),
                        )
                    chat_scroll.scroll_end(animate=False)

                elif isinstance(event, ContentChunk):
                    content_parts.append(event.chunk)
                    await response_widget.update("".join(content_parts))
                    chat_scroll.scroll_end(animate=False)

                elif isinstance(event, TurnCompleted):
                    full_text = event.full_content
                    if not full_text:
                        full_text = "".join(content_parts).strip()
                    if full_text:
                        await response_widget.update(full_text)
                        self.conversation_history.append(
                            {"role": "assistant", "content": full_text}
                        )
                        prompt_tokens = max(1, len(prompt) // 4)
                        resp_tokens = max(1, len(full_text) // 4)
                        self.total_tokens_used += prompt_tokens + resp_tokens
                        capacity_pct = min(100, max(1, self.total_tokens_used // 1000))

                        self.session.messages.append(
                            ChatMessage(
                                role="assistant",
                                content=full_text,
                                thought=event.thought,
                                thought_duration_str=event.thought_duration_str,
                                actions=event.actions,
                                tokens=resp_tokens,
                            )
                        )
                        self.session.total_tokens = self.total_tokens_used
                        session_manager.save_session(self.session)

                        sidebar.update_telemetry(
                            tokens_used=self.total_tokens_used,
                            context_capacity_pct=capacity_pct,
                        )

                        footer_right = self.query_one("#footer-status", Static)
                        if footer_right:
                            footer_right.update(
                                f"[#ced6e0]{self.total_tokens_used:,} tokens ({capacity_pct}%)[/]   "
                                "[#57606f]ctrl+s sessions[/]   [#57606f]ctrl+p commands[/]   [#2ed573]●[/] [#57606f]lang2sim 2.0.0[/]"
                            )
                    else:
                        await response_widget.update("*(No response received from model)*")
        except Exception as e:
            await response_widget.update(f"[bold #ef4444]⚠ Connection Error:[/] {str(e)}")
        finally:
            self.is_streaming = False
            sticky_card.focus_input()
