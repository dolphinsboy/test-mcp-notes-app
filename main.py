from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='[LOG] %(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

# Simple in-memory storage for notes
notes_storage = []

def reset_notes():
    """Reset notes storage to empty"""
    global notes_storage
    notes_storage.clear()
    logger.info("Notes storage reset to empty")

# Reset notes on startup
reset_notes()

# Create FastMCP instance
mcp = FastMCP(
    name="Notes App",
    version="0.1.0",
    description="A simple MCP server",
)

@mcp.tool()
def get_my_notes(query: str = "") -> str:
    """Get all notes for the user"""
    logger.info(f"get_my_notes called with query: '{query}'")
    if not query:
        # Return all notes
        if not notes_storage:
            logger.info("No notes found")
            return "没有找到任何笔记"
        
        result = "当前笔记列表：\n"
        for note in notes_storage:
            result += f"- ID: {note['id']}, 内容: {note['content']}, 创建时间: {note['created']}\n"
        logger.info(f"Returning {len(notes_storage)} notes")
        return result
    else:
        # Search notes by query
        filtered_notes = [note for note in notes_storage if query.lower() in note['content'].lower()]
        if not filtered_notes:
            logger.info(f"No notes found matching query: '{query}'")
            return f"没有找到包含 '{query}' 的笔记"
        
        result = f"包含 '{query}' 的笔记：\n"
        for note in filtered_notes:
            result += f"- ID: {note['id']}, 内容: {note['content']}, 创建时间: {note['created']}\n"
        logger.info(f"Returning {len(filtered_notes)} filtered notes")
        return result

@mcp.tool()
def add_note(content: str) -> str:
    """Add a note to the user's notes"""
    logger.info(f"add_note called with content: '{content}'")
    if not content.strip():
        logger.warning("Empty note content provided")
        return "笔记内容不能为空"
    
    new_id = max([note['id'] for note in notes_storage]) + 1 if notes_storage else 1
    new_note = {
        "id": new_id,
        "content": content,
        "created": "2024-01-04"  # In a real app, this would be current timestamp
    }
    notes_storage.append(new_note)
    logger.info(f"Note added successfully with ID: {new_id}")
    return f"笔记已添加: ID {new_id}, 内容: {content}"

@mcp.tool()
def delete_note(note_id: int) -> str:
    """Delete a note by ID"""
    logger.info(f"delete_note called with ID: {note_id}")
    
    # Find the note with the specified ID
    note_to_delete = None
    for note in notes_storage:
        if note['id'] == note_id:
            note_to_delete = note
            break
    
    if note_to_delete is None:
        logger.warning(f"Note with ID {note_id} not found")
        return f"未找到ID为 {note_id} 的笔记"
    
    # Remove the note from storage
    notes_storage.remove(note_to_delete)
    logger.info(f"Note with ID {note_id} deleted successfully")
    return f"笔记已删除: ID {note_id}, 内容: {note_to_delete['content']}"

@mcp.tool()
def clear_all_notes() -> str:
    """Clear all notes"""
    logger.info("clear_all_notes called")
    
    if not notes_storage:
        logger.info("No notes to clear")
        return "没有笔记需要清空"
    
    note_count = len(notes_storage)
    notes_storage.clear()
    logger.info(f"All {note_count} notes cleared successfully")
    return f"已清空所有 {note_count} 条笔记"

if __name__ == "__main__":
    logger.info("Starting MCP server...")
    try:
        # 使用 stdio 传输，这通常更稳定
        mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Error starting MCP server: {e}")
        sys.exit(1)