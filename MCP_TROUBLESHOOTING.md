# MCP 服务器故障排除指南

## 红色状态指示器问题

如果您在Cursor中看到MCP服务器显示红色状态指示器，请按照以下步骤进行故障排除：

### 1. 检查MCP服务器配置

确保您的MCP服务器配置正确：

```json
{
  "mcpServers": {
    "notes-app": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/Users/guosong/Desktop/Sina/Code/test_mcp"
    }
  }
}
```

### 2. 验证依赖项

确保所有依赖项已正确安装：

```bash
pip install fastmcp dotenv
```

### 3. 测试MCP服务器

手动启动MCP服务器以检查是否有错误：

```bash
cd /Users/guosong/Desktop/Sina/Code/test_mcp
python main.py
```

### 4. 检查日志文件

查看以下日志文件以获取错误信息：
- `mcp_server.log` - MCP服务器详细日志
- `server.log` - 通用服务器日志

### 5. 重启Cursor

1. 完全关闭Cursor
2. 重新启动Cursor
3. 检查MCP服务器状态

### 6. 验证MCP工具

确保MCP工具在Cursor中正确显示：
- 打开Cursor设置
- 导航到MCP部分
- 确认notes-app服务器已启用

### 7. 常见问题解决

**问题**: MCP服务器无法启动
**解决方案**: 检查Python路径和依赖项

**问题**: 工具不可用
**解决方案**: 确保MCP服务器正在运行且配置正确

**问题**: 连接超时
**解决方案**: 检查防火墙设置和网络连接

### 8. 调试模式

启用详细日志记录以帮助调试：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 9. 联系支持

如果问题仍然存在，请：
1. 收集所有日志文件
2. 记录错误消息
3. 提供系统信息

## 当前MCP服务器状态

- **服务器名称**: Notes App
- **版本**: 0.1.0
- **传输方式**: stdio
- **工具数量**: 2 (get_my_notes, add_note)
- **状态**: 需要验证连接 