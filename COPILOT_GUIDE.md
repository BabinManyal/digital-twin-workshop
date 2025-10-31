# Using GitHub Copilot with agents.md

## 🎯 Overview

The `agents.md` file provides comprehensive instructions for GitHub Copilot to help build and maintain your MCP server. This guide shows you how to leverage it in VS Code.

## ✅ Prerequisites

### 1. GitHub Copilot Setup
- **VS Code Extension**: Install "GitHub Copilot" and "GitHub Copilot Chat"
- **Subscription**: Active GitHub Copilot subscription
- **Sign In**: Authenticate with your GitHub account in VS Code

### 2. Enable GitHub Copilot (if using VS Code Insiders)
1. Open VS Code Insiders
2. Install "GitHub Copilot" extension
3. Sign in with GitHub account
4. Verify Copilot is active (check status bar)

## 🚀 How to Use agents.md

### Method 1: Copilot Chat with @workspace

1. **Open Copilot Chat** (Cmd/Ctrl + I or Cmd/Ctrl + Shift + I)

2. **Reference the agents.md** using @workspace:
   ```
   @workspace /fix Review agents.md and help me implement the MCP server
   ```

3. **Specific questions**:
   ```
   @workspace How do I add a new tool to the MCP server according to agents.md?
   
   @workspace Show me how to implement error handling based on agents.md guidelines
   
   @workspace Help me test the MCP server as described in agents.md
   ```

### Method 2: Inline Copilot Suggestions

1. **Open the MCP server file**:
   ```
   digital-twin-frontend/mcp/digital-twin-server.ts
   ```

2. **Start typing a function** - Copilot will suggest code based on agents.md context:
   ```typescript
   // Type: async function addNewTool
   // Copilot will suggest implementation based on patterns in agents.md
   ```

3. **Accept suggestions**: Press Tab to accept

### Method 3: Generate from Comments

1. **Write a descriptive comment**:
   ```typescript
   // Add a new tool called get_skills that retrieves technical skills
   // from the profile using the same RAG pattern
   ```

2. **Press Enter** - Copilot will generate the implementation

3. **Review and refine** - Use Copilot Chat to iterate

## 💡 Example Prompts for Copilot Chat

### Building Features
```
@workspace Based on agents.md, help me add a new tool called "get_experience" 
that retrieves work experience details
```

### Debugging
```
@workspace The MCP server is not connecting. Check against the agents.md 
requirements and suggest fixes
```

### Testing
```
@workspace Show me how to test the query_profile tool as described in agents.md
```

### Refactoring
```
@workspace Refactor the error handling in the MCP server to match the 
standards in agents.md
```

### Documentation
```
@workspace Generate JSDoc comments for the MCP server functions based on 
agents.md documentation style
```

## 🎓 Best Practices

### 1. Keep agents.md Open
- Have `agents.md` open in a tab while coding
- Copilot uses open files for better context

### 2. Use Specific References
```
@workspace According to the "RAG Implementation" section in agents.md, 
how should I structure the query flow?
```

### 3. Iterate with Copilot
```
# First prompt
@workspace Implement the query_profile tool

# Follow-up
Can you add better error handling?

# Refinement  
Now add logging as specified in agents.md
```

### 4. Review Suggestions
- Always review Copilot's suggestions
- Ensure they match your project structure
- Test before committing

## 🔧 Common Use Cases

### 1. Adding a New Tool

**Prompt**:
```
@workspace I want to add a tool called "get_projects" that returns information 
about projects. Follow the same pattern as query_profile in agents.md
```

### 2. Improving Error Handling

**Prompt**:
```
@workspace Review the error handling in digital-twin-server.ts against the 
"Error Handling" section in agents.md and suggest improvements
```

### 3. Optimizing Performance

**Prompt**:
```
@workspace Based on agents.md best practices, how can I optimize the RAG 
query performance?
```

### 4. Building Tests

**Prompt**:
```
@workspace Generate unit tests for the MCP server based on the testing 
section in agents.md
```

## 📊 agents.md Sections Reference

### Quick Navigation for Copilot Prompts

| Section | Use For | Example Prompt |
|---------|---------|----------------|
| **Technical Requirements** | Dependencies, setup | "@workspace What dependencies are needed per agents.md?" |
| **Project Architecture** | File structure, organization | "@workspace Show me the correct file structure from agents.md" |
| **MCP Server Implementation** | Core server code | "@workspace Implement the server structure from agents.md" |
| **RAG Implementation** | Query logic | "@workspace Help me implement RAG flow from agents.md" |
| **Request Handlers** | Tool handlers | "@workspace Add a new handler following agents.md pattern" |
| **Build Configuration** | TypeScript, scripts | "@workspace Configure build per agents.md" |
| **Testing** | Test cases | "@workspace Create tests based on agents.md examples" |

## 🎯 Advanced Copilot Features

### 1. Generate from Scratch
```
@workspace Create a new MCP tool following all the guidelines in agents.md 
that allows querying education history
```

### 2. Code Review
```
@workspace Review this function against the code quality standards in agents.md
```

### 3. Documentation Generation
```
@workspace Generate a README section for the MCP server based on agents.md
```

### 4. Debugging Assistance
```
@workspace This error occurred [paste error]. Check agents.md for solutions
```

## ⚡ Quick Tips

1. **Be Specific**: Reference exact sections in agents.md
2. **Provide Context**: Include file names and error messages
3. **Iterate**: Ask follow-up questions to refine
4. **Use @workspace**: Always use @workspace for project-wide context
5. **Review Code**: Copilot is a tool, not a replacement for review

## 🚫 What Copilot Cannot Do

- **Run commands**: You still need to run build/test commands manually
- **Access APIs**: Cannot test actual API calls
- **Deploy**: Cannot push to GitHub or deploy services
- **Debug runtime**: Cannot debug running processes

## 📝 Example Workflow

### Building a New Feature

1. **Plan**:
   ```
   @workspace I want to add a feature to cache query results. 
   What's the best approach based on agents.md architecture?
   ```

2. **Implement**:
   ```
   @workspace Generate the caching implementation
   ```

3. **Test**:
   ```
   @workspace Create tests for the caching feature
   ```

4. **Document**:
   ```
   @workspace Add documentation for the caching feature
   ```

5. **Review**:
   ```
   @workspace Review this implementation against agents.md standards
   ```

## 🔍 Troubleshooting

### Copilot Not Using agents.md

**Solution**: 
- Ensure agents.md is open in a tab
- Use explicit reference: `@workspace Check agents.md and...`
- Reload VS Code window

### Poor Suggestions

**Solution**:
- Be more specific in prompts
- Reference exact sections of agents.md
- Provide more context about what you want

### Copilot Not Responding

**Solution**:
- Check GitHub Copilot status (bottom right in VS Code)
- Verify subscription is active
- Restart VS Code
- Check internet connection

## 📚 Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Copilot Chat Guide](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide)
- [Best Practices](https://docs.github.com/en/copilot/using-github-copilot/getting-started-with-github-copilot)

## ✅ Checklist

- [ ] GitHub Copilot installed and active
- [ ] agents.md file created and committed
- [ ] Understand how to use @workspace
- [ ] Know how to reference agents.md sections
- [ ] Practiced with example prompts
- [ ] Ready to build with Copilot assistance!

---

**Remember**: GitHub Copilot is your AI pair programmer. The more context you provide (like agents.md), the better suggestions you'll get!
