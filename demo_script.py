#!/usr/bin/env python3
"""
Shared Document Collaboration Demo

This script demonstrates the shared document mod capabilities with multiple agents
collaborating on document creation, editing, and review.
"""

import asyncio
from pathlib import Path

from openagents.core.network import AgentNetwork
from openagents.utils.agent_loader import load_agent_from_yaml


class SharedDocumentDemo:
    """Demo orchestrator for shared document collaboration."""

    def __init__(self):
        self.network_manager = None
        self.agents = {}
        self.demo_document_id = None

    def _get_documents_adapter(self, agent):
        """Get the documents mod adapter for an agent."""
        return agent.get_mod_adapter("openagents.mods.workspace.documents")

    async def setup_network(self):
        """Set up the network and agents."""
        print("🚀 Setting up shared document collaboration network...")

        # Load network configuration
        config_path = Path(__file__).parent / "network.yaml"
        self.network_manager = AgentNetwork.load(str(config_path))

        # Initialize and start the network
        await self.network_manager.initialize()
        print("✅ Network started successfully")

        # Allow time for network to initialize
        await asyncio.sleep(2)

    async def create_agents(self):
        """Create and register demo agents."""
        print("👥 Creating demonstration agents...")

        # Get network connection info from network config
        network_host = "localhost"
        network_port = 8700  # Default port from network.yaml

        # Create editor agent
        editor_config = Path(__file__).parent / "editor_agent.yaml"
        editor, editor_connection = load_agent_from_yaml(str(editor_config))
        self.agents["editor"] = editor
        await editor.async_start(
            network_host=(
                editor_connection.get("host", network_host)
                if editor_connection
                else network_host
            ),
            network_port=(
                editor_connection.get("port", network_port)
                if editor_connection
                else network_port
            ),
            network_id=(
                editor_connection.get("network_id") if editor_connection else None
            ),
        )

        # Create reviewer agent
        reviewer_config = Path(__file__).parent / "reviewer_agent.yaml"
        reviewer, reviewer_connection = load_agent_from_yaml(str(reviewer_config))
        self.agents["reviewer"] = reviewer
        await reviewer.async_start(
            network_host=(
                reviewer_connection.get("host", network_host)
                if reviewer_connection
                else network_host
            ),
            network_port=(
                reviewer_connection.get("port", network_port)
                if reviewer_connection
                else network_port
            ),
            network_id=(
                reviewer_connection.get("network_id") if reviewer_connection else None
            ),
        )

        # Create collaborator agent
        collaborator_config = Path(__file__).parent / "collaborator_agent.yaml"
        collaborator, collaborator_connection = load_agent_from_yaml(
            str(collaborator_config)
        )
        self.agents["collaborator"] = collaborator
        await collaborator.async_start(
            network_host=(
                collaborator_connection.get("host", network_host)
                if collaborator_connection
                else network_host
            ),
            network_port=(
                collaborator_connection.get("port", network_port)
                if collaborator_connection
                else network_port
            ),
            network_id=(
                collaborator_connection.get("network_id")
                if collaborator_connection
                else None
            ),
        )

        print("✅ All agents created and started")

        # Allow time for agents to register
        await asyncio.sleep(3)

    async def demo_document_creation(self):
        """Demonstrate document creation."""
        print("\n📝 Demo 1: Document Creation")
        print("-" * 50)

        editor = self.agents["editor"]

        # Create a new document
        initial_content = """# Project Requirements Document

## Overview
This document outlines the requirements for our new project.

## Scope
TBD - needs to be defined

## Timeline
TBD - needs scheduling

## Resources
TBD - needs resource planning"""

        print("Editor creating new document...")
        documents_adapter = self._get_documents_adapter(editor)
        if documents_adapter:
            result = await documents_adapter.create_document(
                document_name="Project Requirements",
                initial_content=initial_content,
                access_permissions={
                    "reviewer_agent": "read_write",
                    "collaborator_agent": "read_write",
                },
            )
            print(f"Document creation result: {result}")
            # Extract document ID from result
            if result.get("status") == "success" and "data" in result:
                self.demo_document_id = result["data"].get(
                    "document_id", "demo-doc-123"
                )
            else:
                self.demo_document_id = "demo-doc-123"
        else:
            print("⚠️  Documents mod adapter not found for editor agent")
            self.demo_document_id = "demo-doc-123"

        await asyncio.sleep(2)

    async def demo_collaborative_editing(self):
        """Demonstrate collaborative editing."""
        print("\n🤝 Demo 2: Collaborative Editing")
        print("-" * 50)

        editor = self.agents["editor"]
        collaborator = self.agents["collaborator"]

        editor_adapter = self._get_documents_adapter(editor)
        collaborator_adapter = self._get_documents_adapter(collaborator)

        # Open document for editing
        print("!!!Agents opening document...")
        if editor_adapter and hasattr(editor_adapter, "get_document"):
            await editor_adapter.get_document(self.demo_document_id)
        else:
            print("⚠️  open_document method not available")
        if collaborator_adapter and hasattr(collaborator_adapter, "get_document"):
            await collaborator_adapter.get_document(self.demo_document_id)
        else:
            print("⚠️  open_document method not available")

        # Editor updates the scope section
        print("Editor updating scope section...")
        doc = await editor_adapter.get_document(self.demo_document_id)
        # content = doc["data"]["content"]
        content = "this is new content"
        await editor_adapter.save_document(self.demo_document_id, content)

        print("--------------------------------")
        if editor_adapter and hasattr(editor_adapter, "replace_lines"):
            await editor_adapter.replace_lines(
                document_id=self.demo_document_id,
                start_line=5,
                end_line=5,
                content=[
                    "Define the core features and functionality needed for the MVP"
                ],
            )
        else:
            print("⚠️  replace_lines method not available")

        # Collaborator adds timeline details
        print("Collaborator adding timeline details...")
        if collaborator_adapter and hasattr(collaborator_adapter, "replace_lines"):
            await collaborator_adapter.replace_lines(
                document_id=self.demo_document_id,
                start_line=8,
                end_line=8,
                content=[
                    "Phase 1: Requirements gathering (2 weeks)",
                    "Phase 2: Design and planning (3 weeks)",
                    "Phase 3: Development (8 weeks)",
                    "Phase 4: Testing and deployment (2 weeks)",
                ],
            )
        else:
            print("⚠️  replace_lines method not available")

        # Editor adds resource information
        print("Editor adding resource information...")
        if editor_adapter and hasattr(editor_adapter, "replace_lines"):
            await editor_adapter.replace_lines(
                document_id=self.demo_document_id,
                start_line=11,
                end_line=11,
                content=[
                    "Development team: 3 engineers",
                    "Design team: 1 designer",
                    "Product team: 1 product manager",
                    "QA team: 1 QA engineer",
                ],
            )
        else:
            print("⚠️  replace_lines method not available")

        await asyncio.sleep(2)

    async def demo_commenting_and_review(self):
        """Demonstrate commenting and review functionality."""
        print("\n💬 Demo 3: Review and Comments")
        print("-" * 50)

        reviewer = self.agents["reviewer"]
        reviewer_adapter = self._get_documents_adapter(reviewer)

        # Reviewer opens document
        print("Reviewer opening document for review...")
        if reviewer_adapter and hasattr(reviewer_adapter, "open_document"):
            await reviewer_adapter.open_document(self.demo_document_id)
        else:
            print("⚠️  open_document method not available")

        # Add review comments
        print("Reviewer adding feedback comments...")
        if reviewer_adapter and hasattr(reviewer_adapter, "add_comment"):
            await reviewer_adapter.add_comment(
                document_id=self.demo_document_id,
                line_number=3,
                comment_text="Consider adding a more detailed project description here",
            )

            await reviewer_adapter.add_comment(
                document_id=self.demo_document_id,
                line_number=6,
                comment_text="Good scope definition. Should we also define what's out of scope?",
            )

            await reviewer_adapter.add_comment(
                document_id=self.demo_document_id,
                line_number=10,
                comment_text="Timeline looks reasonable. Consider adding buffer time for each phase.",
            )

            await reviewer_adapter.add_comment(
                document_id=self.demo_document_id,
                line_number=15,
                comment_text="Resource allocation looks good. Do we have these team members confirmed?",
            )
        else:
            print("⚠️  add_comment method not available")

        await asyncio.sleep(2)

    async def demo_presence_tracking(self):
        """Demonstrate agent presence tracking."""
        print("\n👀 Demo 4: Agent Presence Tracking")
        print("-" * 50)

        editor = self.agents["editor"]
        collaborator = self.agents["collaborator"]

        editor_adapter = self._get_documents_adapter(editor)
        collaborator_adapter = self._get_documents_adapter(collaborator)

        # Update cursor positions
        print("Agents updating their working positions...")
        if editor_adapter and hasattr(editor_adapter, "update_cursor_position"):
            await editor_adapter.update_cursor_position(
                document_id=self.demo_document_id, line_number=3, column_number=10
            )
        else:
            print("⚠️  update_cursor_position method not available")

        if collaborator_adapter and hasattr(
            collaborator_adapter, "update_cursor_position"
        ):
            await collaborator_adapter.update_cursor_position(
                document_id=self.demo_document_id, line_number=8, column_number=1
            )
        else:
            print("⚠️  update_cursor_position method not available")

        # Check presence
        print("Checking agent presence...")
        if editor_adapter and hasattr(editor_adapter, "get_agent_presence"):
            presence_result = await editor_adapter.get_agent_presence(
                self.demo_document_id
            )
            print(f"Agent presence: {presence_result}")
        else:
            print("⚠️  get_agent_presence method not available")

        await asyncio.sleep(2)

    async def demo_document_management(self):
        """Demonstrate document management features."""
        print("\n📋 Demo 5: Document Management")
        print("-" * 50)

        editor = self.agents["editor"]
        editor_adapter = self._get_documents_adapter(editor)

        # Get document content
        print("Getting current document content...")
        if editor_adapter:
            if hasattr(editor_adapter, "get_document_content"):
                content_result = await editor_adapter.get_document_content(
                    document_id=self.demo_document_id,
                    include_comments=True,
                    include_presence=True,
                )
                print(f"Document content result: {content_result}")
            elif hasattr(editor_adapter, "get_document"):
                content_result = await editor_adapter.get_document(
                    self.demo_document_id
                )
                print(f"Document content result: {content_result}")
            else:
                print("⚠️  get_document_content/get_document method not available")
        else:
            print("⚠️  Documents adapter not found")

        # Get document history
        print("Getting document operation history...")
        if editor_adapter and hasattr(editor_adapter, "get_document_history"):
            history_result = await editor_adapter.get_document_history(
                document_id=self.demo_document_id, limit=10
            )
            print(f"Document history result: {history_result}")
        else:
            print("⚠️  get_document_history method not available")

        # List documents
        print("Listing all available documents...")
        if editor_adapter and hasattr(editor_adapter, "list_documents"):
            list_result = await editor_adapter.list_documents()
            print(f"Document list result: {list_result}")
        else:
            print("⚠️  list_documents method not available")

        await asyncio.sleep(2)

    async def run_demo(self):
        """Run the complete demo."""
        try:
            print("🎯 Starting Shared Document Collaboration Demo")
            print("=" * 60)

            # Setup
            await self.setup_network()
            await self.create_agents()

            # Run demo scenarios
            await self.demo_document_creation()
            await self.demo_collaborative_editing()
            await self.demo_commenting_and_review()
            await self.demo_presence_tracking()
            await self.demo_document_management()

            print("\n🎉 Demo completed successfully!")
            print("=" * 60)

        except Exception as e:
            print(f"❌ Demo failed with error: {e}")

        finally:
            await self.cleanup()

    async def cleanup(self):
        """Clean up resources."""
        print("\n🧹 Cleaning up...")

        # Close documents
        if self.demo_document_id and self.agents:
            for agent in self.agents.values():
                try:
                    documents_adapter = self._get_documents_adapter(agent)
                    if documents_adapter and hasattr(
                        documents_adapter, "close_document"
                    ):
                        await documents_adapter.close_document(self.demo_document_id)
                except Exception:
                    pass

        # Stop agents
        for agent in self.agents.values():
            try:
                await agent.async_stop()
            except Exception:
                pass

        # Stop network
        if self.network_manager:
            try:
                await self.network_manager.shutdown()
            except Exception:
                pass

        print("✅ Cleanup completed")


async def main():
    """Main demo entry point."""
    demo = SharedDocumentDemo()
    await demo.run_demo()


if __name__ == "__main__":
    # Set up event loop for Windows compatibility
    if hasattr(asyncio, "WindowsProactorEventLoopPolicy"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    asyncio.run(main())
