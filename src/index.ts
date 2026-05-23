import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios, { AxiosInstance } from "axios";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

const SERVER_NAME = "clickup-mcp-server";
const SERVER_VERSION = "1.0.0";

// Standard warning if token is not defined in env
if (!process.env.CLICKUP_API_TOKEN) {
  console.error(
    "Warning: CLICKUP_API_TOKEN is not set in environment. " +
    "The server will try to fetch it dynamically at runtime if possible, " +
    "but API calls will fail without a valid token."
  );
}

/**
 * Creates an Axios client configured for ClickUp API v2.
 * Uses the personal token format directly, or Bearer token if applicable.
 */
function getClickUpClient(): AxiosInstance {
  const token = process.env.CLICKUP_API_TOKEN || "";
  
  if (!token) {
    throw new Error(
      "ClickUp API Token is not configured. " +
      "Please set the CLICKUP_API_TOKEN environment variable."
    );
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  // If the token starts with 'pk_', it is a ClickUp Personal API Token, sent raw.
  // Otherwise, if it starts with 'Bearer ', use it directly.
  // If it's a raw OAuth token, we prepend 'Bearer '.
  if (token.startsWith("pk_") || token.startsWith("Bearer ")) {
    headers["Authorization"] = token;
  } else {
    headers["Authorization"] = `Bearer ${token}`;
  }

  return axios.create({
    baseURL: "https://api.clickup.com/api/v2",
    headers,
  });
}

/**
 * Gracefully formats Axios and other runtime errors into human-readable messages.
 */
function handleApiError(error: any): string {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const data = error.response?.data;
    const message = data?.err || data?.message || error.message;
    return `ClickUp API Error (Status ${status}): ${message}`;
  }
  return error instanceof Error ? error.message : String(error);
}

// 1. Initialize the MCP Server
const server = new McpServer({
  name: SERVER_NAME,
  version: SERVER_VERSION,
});

// 2. Register tools

// List Teams / Workspaces
server.registerTool(
  "list_teams",
  {
    description: "List the ClickUp Workspaces (Teams) the authenticated user has access to.",
    inputSchema: z.object({}),
  },
  async () => {
    try {
      const client = getClickUpClient();
      const response = await client.get("/team");
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// List Spaces in a Team
server.registerTool(
  "list_spaces",
  {
    description: "List all Spaces in a specific ClickUp Workspace (Team).",
    inputSchema: z.object({
      team_id: z.string().describe("The ID of the ClickUp Workspace (Team)."),
      archived: z.boolean().optional().default(false).describe("Include archived spaces in results."),
    }),
  },
  async ({ team_id, archived }) => {
    try {
      const client = getClickUpClient();
      const response = await client.get(`/team/${team_id}/space`, {
        params: { archived },
      });
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// List Folders in a Space
server.registerTool(
  "list_folders",
  {
    description: "List all Folders in a specific ClickUp Space.",
    inputSchema: z.object({
      space_id: z.string().describe("The ID of the ClickUp Space."),
      archived: z.boolean().optional().default(false).describe("Include archived folders in results."),
    }),
  },
  async ({ space_id, archived }) => {
    try {
      const client = getClickUpClient();
      const response = await client.get(`/space/${space_id}/folder`, {
        params: { archived },
      });
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// List Lists in Folder or Space
server.registerTool(
  "list_lists",
  {
    description: "List all Lists within a Folder or Space. Must specify either folder_id or space_id.",
    inputSchema: z.object({
      folder_id: z.string().optional().describe("The ID of the Folder to list lists from."),
      space_id: z.string().optional().describe("The ID of the Space (for folderless lists)."),
      archived: z.boolean().optional().default(false).describe("Include archived lists in results."),
    }),
  },
  async ({ folder_id, space_id, archived }) => {
    try {
      if (!folder_id && !space_id) {
        throw new Error("Either 'folder_id' or 'space_id' must be provided to list lists.");
      }

      const client = getClickUpClient();
      let response;

      if (folder_id) {
        response = await client.get(`/folder/${folder_id}/list`, {
          params: { archived },
        });
      } else {
        response = await client.get(`/space/${space_id}/list`, {
          params: { archived },
        });
      }

      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// List Tasks in a List
server.registerTool(
  "list_tasks",
  {
    description: "List tasks in a specific ClickUp List with optional status, assignee, and subtask filtering.",
    inputSchema: z.object({
      list_id: z.string().describe("The ID of the ClickUp List."),
      archived: z.boolean().optional().default(false).describe("Include archived tasks."),
      statuses: z.array(z.string()).optional().describe("Filter by status names (e.g. ['to do', 'in progress'])."),
      assignees: z.array(z.string()).optional().describe("Filter by assignee user IDs."),
      subtasks: z.boolean().optional().default(false).describe("Include subtasks in results."),
      page: z.number().optional().default(0).describe("The page of tasks to retrieve (starts at 0)."),
    }),
  },
  async ({ list_id, archived, statuses, assignees, subtasks, page }) => {
    try {
      const client = getClickUpClient();
      const params: any = {
        archived,
        subtasks,
        page,
      };

      if (statuses) params.statuses = statuses;
      if (assignees) params.assignees = assignees;

      const response = await client.get(`/list/${list_id}/task`, { params });
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// Get Task Detail
server.registerTool(
  "get_task",
  {
    description: "Get comprehensive details of a single ClickUp task by its ID.",
    inputSchema: z.object({
      task_id: z.string().describe("The ID of the ClickUp Task."),
      custom_fields: z.boolean().optional().default(true).describe("Include custom fields in the response."),
    }),
  },
  async ({ task_id, custom_fields }) => {
    try {
      const client = getClickUpClient();
      const response = await client.get(`/task/${task_id}`, {
        params: { custom_fields },
      });
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// Create Task
server.registerTool(
  "create_task",
  {
    description: "Create a new task inside a ClickUp List.",
    inputSchema: z.object({
      list_id: z.string().describe("The ID of the List to create the task in."),
      name: z.string().describe("The title of the task."),
      description: z.string().optional().describe("The description of the task. Supports Markdown."),
      status: z.string().optional().describe("The task status (e.g. 'to do', 'in progress')."),
      priority: z.number().min(1).max(4).optional().describe("Priority: 1 (Urgent), 2 (High), 3 (Normal), 4 (Low)."),
      due_date: z.number().optional().describe("Due date as a Unix timestamp in milliseconds."),
      start_date: z.number().optional().describe("Start date as a Unix timestamp in milliseconds."),
      assignees: z.array(z.number().or(z.string())).optional().describe("Array of user IDs to assign the task to."),
    }),
  },
  async ({ list_id, name, description, status, priority, due_date, start_date, assignees }) => {
    try {
      const client = getClickUpClient();
      const response = await client.post(`/list/${list_id}/task`, {
        name,
        description,
        status,
        priority,
        due_date,
        start_date,
        assignees,
      });
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// Update Task
server.registerTool(
  "update_task",
  {
    description: "Update an existing ClickUp task.",
    inputSchema: z.object({
      task_id: z.string().describe("The ID of the task to update."),
      name: z.string().optional().describe("New title for the task."),
      description: z.string().optional().describe("New description for the task. Supports Markdown."),
      status: z.string().optional().describe("New task status (e.g. 'in progress', 'complete')."),
      priority: z.number().min(1).max(4).optional().describe("Priority: 1 (Urgent), 2 (High), 3 (Normal), 4 (Low)."),
      due_date: z.number().optional().describe("New due date as a Unix timestamp in milliseconds."),
      assignees: z.array(z.number().or(z.string())).optional().describe("Array of user IDs to assign. Replaces existing assignees."),
    }),
  },
  async ({ task_id, name, description, status, priority, due_date, assignees }) => {
    try {
      const client = getClickUpClient();
      const response = await client.put(`/task/${task_id}`, {
        name,
        description,
        status,
        priority,
        due_date,
        assignees,
      });
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// Add Comment to Task
server.registerTool(
  "add_task_comment",
  {
    description: "Add a new comment to a ClickUp task.",
    inputSchema: z.object({
      task_id: z.string().describe("The ID of the Task to add a comment to."),
      comment_text: z.string().describe("The text of the comment to add."),
      notify_all: z.boolean().optional().default(true).describe("Send notification to all followers of the task."),
    }),
  },
  async ({ task_id, comment_text, notify_all }) => {
    try {
      const client = getClickUpClient();
      const response = await client.post(`/task/${task_id}/comment`, {
        comment_text,
        notify_all,
      });
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// Get Comments from Task
server.registerTool(
  "get_task_comments",
  {
    description: "List comments from a specific ClickUp task.",
    inputSchema: z.object({
      task_id: z.string().describe("The ID of the Task to fetch comments from."),
      limit: z.number().optional().default(20).describe("Maximum number of comments to return (max 100)."),
    }),
  },
  async ({ task_id, limit }) => {
    try {
      const client = getClickUpClient();
      const response = await client.get(`/task/${task_id}/comment`, {
        params: { limit },
      });
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// Search Tasks Across Workspace
server.registerTool(
  "search_tasks",
  {
    description: "Search tasks across a whole Workspace (Team) with filters.",
    inputSchema: z.object({
      team_id: z.string().describe("The ID of the ClickUp Workspace (Team)."),
      query: z.string().optional().describe("Search string to find matches in task name or description."),
      statuses: z.array(z.string()).optional().describe("Filter by task status names."),
      assignees: z.array(z.string()).optional().describe("Filter by assignee user IDs."),
      include_closed: z.boolean().optional().default(true).describe("Whether to include closed tasks in results."),
      subtasks: z.boolean().optional().default(false).describe("Whether to search within subtasks."),
    }),
  },
  async ({ team_id, query, statuses, assignees, include_closed, subtasks }) => {
    try {
      const client = getClickUpClient();
      const params: any = {
        include_closed,
        subtasks,
      };

      if (query) params.search = query;
      if (statuses) params.statuses = statuses;
      if (assignees) params.assignees = assignees;

      const response = await client.get(`/team/${team_id}/task`, { params });
      return {
        content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: handleApiError(error) }],
      };
    }
  }
);

// 3. Connect to Stdio Transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("ClickUp MCP Server running on stdio transport");
}

main().catch((error) => {
  console.error("Critical error in server startup:", error);
  process.exit(1);
});
