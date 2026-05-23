#!/usr/bin/env python3
import json
import os

def main():
    # Resolve robust paths relative to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tree_path = os.path.join(os.path.dirname(script_dir), "tasks_tree.json")
    html_path = os.path.join(os.path.dirname(script_dir), "ux_redesign_tasks.html")

    if not os.path.exists(tree_path):
        print(f"Error: {tree_path} not found. Run build_tree.py first.")
        return

    with open(tree_path, "r", encoding="utf-8") as f:
        tasks_tree = json.load(f)

    # Count total tasks and estimates dynamically
    def get_stats(node):
        count = 1
        est = int(node.get("time_estimate") or 0)
        for sub in node.get("subtasks", []):
            c, e = get_stats(sub)
            count += c
            est += e
        return count, est

    total_tasks, total_ms = get_stats(tasks_tree)
    total_hours = total_ms / (1000 * 60 * 60)

    # Create the HTML page content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product UX Improvements & UI Redesign - ClickUp Task Explorer</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', 'sans-serif'],
                        outfit: ['Outfit', 'sans-serif'],
                    }},
                    colors: {{
                        brand: {{
                            50: '#fffbeb',
                            100: '#fef3c7',
                            200: '#fde68a',
                            300: '#fcd34d',
                            400: '#fbbf24',
                            500: '#df9e38', // Sophisticated desaturated primary amber/gold
                            600: '#c68426', // Warm bronze-amber
                            700: '#a3671c',
                            800: '#854f15',
                            900: '#6c3e12',
                            950: '#1b0d02',
                        }},
                        darkbg: {{
                            card: '#151310', // Soft dark charcoal with amber undertone
                            border: '#2a2219', // Dark desaturated bronze border
                            accent: '#201810',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #0a0806;
            color: #e2e8f0;
            background-image: 
                radial-gradient(at 0% 0%, rgba(223, 158, 56, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(198, 132, 38, 0.03) 0px, transparent 50%),
                radial-gradient(at 50% 0%, rgba(59, 130, 246, 0.02) 0px, transparent 50%);
            background-attachment: fixed;
        }}
        
        .outfit-font {{
            font-family: 'Outfit', sans-serif;
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: #0f0d0b;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #2a2219;
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #c68426;
        }}
        
        .glass-effect {{
            background: rgba(21, 18, 15, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(223, 158, 56, 0.05);
        }}
        
        .glass-hover:hover {{
            background: rgba(21, 18, 15, 0.88);
            border-color: rgba(223, 158, 56, 0.2);
            box-shadow: 0 0 25px rgba(223, 158, 56, 0.08);
            transform: translateY(-1px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .task-card-active {{
            border-color: rgba(223, 158, 56, 0.5) !important;
            box-shadow: 0 0 20px rgba(223, 158, 56, 0.15) !important;
        }}
        
        /* Glow animations */
        @keyframes pulse-glow {{
            0%, 100% {{ box-shadow: 0 0 15px rgba(223, 158, 56, 0.05); }}
            50% {{ box-shadow: 0 0 25px rgba(223, 158, 56, 0.15); }}
        }}
        .glowing-border {{
            animation: pulse-glow 3s infinite;
        }}
        
        .markdown-content p {{
            margin-bottom: 0.75rem;
            line-height: 1.6;
        }}
        .markdown-content ul {{
            list-style-type: disc;
            margin-left: 1.25rem;
            margin-bottom: 0.75rem;
        }}
        .markdown-content li {{
            margin-bottom: 0.25rem;
        }}
        .markdown-content strong {{
            color: #f1f5f9;
            font-weight: 600;
        }}
        
        /* Transitions */
        .collapsible-content {{
            transition: max-height 0.4s ease-in-out, opacity 0.3s ease-in-out;
            overflow: hidden;
        }}
    </style>
</head>
<body class="min-h-screen text-slate-200">

    <!-- TOP HEADER & STATS -->
    <header class="border-b border-brand-900/20 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
            <div class="flex flex-row items-center justify-between gap-4">
                <div>
                    <!-- Left: FPV Workplan Subtitle above main parent task -->
                    <div class="flex items-center gap-2 text-brand-500 text-sm font-semibold uppercase tracking-wider outfit-font">
                        <i class="fa-solid fa-layer-group"></i> FPV Workplan
                    </div>
                    <h1 class="text-xl sm:text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-250 outfit-font tracking-tight mt-1">
                        Product UX Improvements & UI Redesign
                    </h1>
                </div>
                
                <!-- Right: Sync and ClickUp link buttons -->
                <div class="flex items-center shrink-0 gap-3">
                    <button onclick="syncWithClickUp()" id="sync-btn" class="px-3 py-1.5 bg-slate-900/60 hover:bg-brand-900/10 border border-slate-850 hover:border-brand-500/30 text-slate-400 hover:text-brand-400 text-xs font-semibold rounded-sm shadow-sm transition-all flex items-center gap-1.5 cursor-pointer">
                        <i class="fa-solid fa-arrows-rotate text-[10px]" id="sync-icon"></i> <span id="sync-text">Sync ClickUp</span>
                    </button>
                    <a href="https://sharing.clickup.com/90182683899/l/h/6-901818298165-1/63f166fd8e9157e" target="_blank" class="px-3 py-1.5 bg-slate-900/60 hover:bg-brand-900/10 border border-slate-850 hover:border-brand-500/30 text-slate-400 hover:text-slate-200 text-xs font-semibold rounded-sm shadow-sm transition-all flex items-center gap-1.5">
                        <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> Open in ClickUp
                    </a>
                </div>
            </div>
        </div>
    </header>
 
    <div class="max-w-8xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
            
            <!-- SIDEBAR: DYNAMIC TREE VIEW DIRECTORY -->
            <aside class="lg:col-span-1">
                <div class="glass-effect p-4 rounded sticky top-36 overflow-y-auto max-h-[calc(100vh-11rem)] border border-brand-900/10 shadow-xl shadow-black/20">
                    
                    <!-- Main Parent Task Title as Sidebar Header: ACTIVE PROJECT replaced with FPV WORKPLAN -->
                    <div class="mb-5 pb-4 border-b border-brand-900/20">
                        <div class="text-[9px] font-bold text-brand-500/60 uppercase tracking-widest outfit-font mb-1.5 flex items-center gap-1.5">
                            <i class="fa-solid fa-folder-tree"></i> FPV WORKPLAN
                        </div>
                        <h3 class="text-sm font-extrabold text-slate-100 outfit-font leading-snug tracking-wide">
                            Product UX Improvements & UI Redesign
                        </h3>
                    </div>

                    <!-- Quick Navigation replaced with Estimated Task List -->
                    <h2 class="text-[10px] font-bold text-slate-455 uppercase tracking-wider outfit-font mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-list-ul text-brand-500/80"></i> Estimated Task List
                    </h2>
                    
                    <div class="space-y-1" id="sidebar-tree">
                        <!-- Javascript will render this tree -->
                        <div class="animate-pulse space-y-2">
                            <div class="h-6 bg-slate-900 rounded w-3/4"></div>
                            <div class="h-6 bg-slate-900 rounded w-5/6"></div>
                            <div class="h-6 bg-slate-900 rounded w-2/3"></div>
                            <div class="h-6 bg-slate-900 rounded w-full"></div>
                        </div>
                    </div>
                </div>
            </aside>
            
            <!-- MAIN PANEL: NESTED SCROLLABLE TASK VIEW -->
            <main class="lg:col-span-3">
                <!-- Borderless, Clean Stats & Expand/Collapse Control Row at the very top of main cards -->
                <div class="flex items-center justify-between mb-4 pb-2 border-b border-slate-900">
                    <!-- Left: Desaturated, Borderless Plain Text Stats -->
                    <div class="flex items-center gap-4 text-xs text-slate-400 font-outfit">
                        <div>
                            <span class="text-slate-200 font-bold text-sm" id="total-count-stat">0</span> Total Tasks
                        </div>
                        <div class="text-slate-700">|</div>
                        <div class="flex items-center gap-1">
                            <i class="fa-solid fa-clock text-brand-500/70 text-[10px]"></i>
                            <span class="text-slate-200 font-bold text-sm" id="total-time-stat">0h</span> Estimated Time
                        </div>
                    </div>
                    
                    <!-- Right: Elegant Expand All / Collapse All controls -->
                    <div class="flex items-center gap-2">
                        <button onclick="expandAll()" class="px-3 py-1.5 bg-slate-900/60 hover:bg-brand-900/10 border border-slate-850 hover:border-brand-500/30 text-slate-350 hover:text-slate-100 text-xs font-semibold rounded-sm transition-all flex items-center gap-1.5">
                            <i class="fa-solid fa-folder-open text-[10px] text-brand-500/80"></i> Expand All
                        </button>
                        <button onclick="collapseAll()" class="px-3 py-1.5 bg-slate-900/60 hover:bg-slate-800 border border-slate-850 hover:border-slate-755 text-slate-350 hover:text-slate-205 text-xs font-semibold rounded-sm transition-all flex items-center gap-1.5">
                            <i class="fa-solid fa-folder-closed text-[10px] text-slate-500"></i> Collapse All
                        </button>
                    </div>
                </div>

                <div class="space-y-6" id="tasks-container">
                    <!-- Javascript will render the hierarchical cards here -->
                    <div class="text-center py-20">
                        <div class="inline-block animate-spin text-brand-500 text-3xl mb-4">
                            <i class="fa-solid fa-spinner"></i>
                        </div>
                        <p class="text-slate-400">Loading task data and building tree structure...</p>
                    </div>
                </div>
            </main>
            
        </div>
    </div>

    <!-- FOOTER: Premium, Minimalist Footnote Authored by Burak Ozdelice -->
    <footer class="border-t border-slate-950 py-8 mt-20 text-center text-xs text-slate-500 font-outfit tracking-wide">
        <div class="max-w-7xl mx-auto px-4">
            <p>FPV UX & UI Redesign Project Plan &bull; Burak Ozdelice &bull; 2026</p>
        </div>
    </footer>

    <!-- SYNCING STATE MODAL -->
    <div id="sync-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 flex items-center justify-center opacity-0 pointer-events-none transition-opacity duration-300">
        <div class="glass-effect max-w-md w-full p-8 rounded-2xl border border-brand-500/20 shadow-2xl text-center flex flex-col items-center">
            <div class="relative w-16 h-16 mb-6">
                <!-- Golden Loader Spinner -->
                <div class="absolute inset-0 rounded-full border-4 border-brand-900/20"></div>
                <div class="absolute inset-0 rounded-full border-4 border-t-brand-500 animate-spin"></div>
            </div>
            <h3 class="text-lg font-bold text-slate-100 outfit-font tracking-wide mb-2">Syncing Workspace Data</h3>
            <p class="text-sm text-slate-400 mb-6">Fetching latest tasks from ClickUp and rebuilding the hierarchy. Please do not close this window.</p>
            
            <!-- Real-time Status Checklist -->
            <div class="w-full text-left space-y-3 bg-slate-950/40 p-4 rounded-xl border border-brand-900/10 text-xs">
                <div id="status-step-1" class="flex items-center gap-2.5 text-slate-500 transition-colors duration-200">
                    <i class="fa-solid fa-spinner animate-spin text-[10px] hidden" id="step-1-spinner"></i>
                    <i class="fa-solid fa-circle-notch text-[10px]" id="step-1-pending"></i>
                    <i class="fa-solid fa-circle-check text-brand-500 text-[10px] hidden" id="step-1-check"></i>
                    <span>Connecting and downloading ClickUp tasks...</span>
                </div>
                <div id="status-step-2" class="flex items-center gap-2.5 text-slate-500 transition-colors duration-200">
                    <i class="fa-solid fa-spinner animate-spin text-[10px] hidden" id="step-2-spinner"></i>
                    <i class="fa-solid fa-circle-notch text-[10px]" id="step-2-pending"></i>
                    <i class="fa-solid fa-circle-check text-brand-500 text-[10px] hidden" id="step-2-check"></i>
                    <span>Analyzing dependency tree & ordering...</span>
                </div>
                <div id="status-step-3" class="flex items-center gap-2.5 text-slate-500 transition-colors duration-200">
                    <i class="fa-solid fa-spinner animate-spin text-[10px] hidden" id="step-3-spinner"></i>
                    <i class="fa-solid fa-circle-notch text-[10px]" id="step-3-pending"></i>
                    <i class="fa-solid fa-circle-check text-brand-500 text-[10px] hidden" id="step-3-check"></i>
                    <span>Compiling dynamic components...</span>
                </div>
            </div>
        </div>
    </div>

    <!-- OFFLINE GUIDANCE MODAL -->
    <div id="offline-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 flex items-center justify-center opacity-0 pointer-events-none transition-opacity duration-300">
        <div class="glass-effect max-w-lg w-full p-8 rounded-2xl border border-red-500/20 shadow-2xl">
            <div class="flex items-center gap-3.5 mb-5 pb-4 border-b border-brand-900/10">
                <div class="w-10 h-10 rounded-full bg-brand-900/10 border border-brand-500/25 flex items-center justify-center shrink-0">
                    <i class="fa-solid fa-circle-exclamation text-brand-500 text-lg"></i>
                </div>
                <div>
                    <h3 class="text-base font-bold text-slate-100 outfit-font tracking-wide">Workspace Sync Offline</h3>
                    <p class="text-xs text-slate-500">Live background sync server could not be reached.</p>
                </div>
            </div>
            
            <p class="text-sm text-slate-300 leading-relaxed mb-5">
                To sync your dashboard with ClickUp instantly, make sure the local background server is running.
            </p>
            
            <div class="space-y-4">
                <div class="text-xs font-semibold text-slate-400 outfit-font uppercase tracking-wider">How to start the server:</div>
                <div class="bg-slate-950 p-4 rounded-xl border border-brand-900/15 font-mono text-xs text-brand-400 select-all relative group">
                    <div class="text-[9px] text-slate-600 absolute right-3 top-2.5 uppercase font-sans tracking-widest group-hover:text-slate-550 transition-colors">Terminal Command</div>
                    python3 ux_task_dashboard/server.py
                </div>
                
                <div class="flex items-start gap-2.5 text-xs text-slate-400 leading-relaxed">
                    <i class="fa-solid fa-circle-info text-brand-500/80 mt-0.5 text-[10px]"></i>
                    <span>Once running, your board will be served at <a href="http://localhost:5001" target="_blank" class="text-brand-400 hover:underline">http://localhost:5001</a> and can be updated instantly from any browser tab.</span>
                </div>
            </div>
            
            <div class="flex items-center justify-end gap-3 mt-8 pt-4 border-t border-brand-900/10">
                <button onclick="closeOfflineModal()" class="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 text-xs font-semibold rounded-lg transition-all border border-slate-850 hover:border-slate-755 cursor-pointer">
                    Continue Offline
                </button>
                <button onclick="retrySync()" class="px-4 py-2 bg-brand-500/10 hover:bg-brand-500/20 text-brand-400 hover:text-brand-300 text-xs font-semibold rounded-lg transition-all border border-brand-500/30 cursor-pointer flex items-center gap-1.5">
                    <i class="fa-solid fa-arrows-rotate text-[10px]" id="retry-icon"></i> Retry Sync
                </button>
            </div>
        </div>
    </div>

    <!-- DATA BUNDLING & CLIENT APP CODE -->
    <script>
        // Bundled ClickUp Task Tree from Python
        const taskData = {json.dumps(tasks_tree)};

        // Main State
        let expandedNodes = new Set();
        let searchQuery = "";

        // Helper to format estimated time
        function formatEstimate(ms) {{
            if (!ms) return null;
            const totalMinutes = Math.floor(ms / (1000 * 60));
            const hours = Math.floor(totalMinutes / 60);
            const mins = totalMinutes % 60;
            if (hours > 0) {{
                return mins > 0 ? `${{hours}}h ${{mins}}m` : `${{hours}}h`;
            }}
            return `${{mins}}m`;
        }}

        // Simple Markdown description formatter
        function formatDescription(desc) {{
            if (!desc) return '<span class="text-slate-500 italic">No description provided.</span>';
            
            // Clean HTML escaping
            let html = desc
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");
                
            // Convert Bold
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
            
            // Convert Bullet points (lists)
            const lines = html.split('\\n');
            let inList = false;
            let resultLines = [];
            
            for (let line of lines) {{
                let trimmed = line.trim();
                if (trimmed.startsWith('- ') || trimmed.startsWith('* ') || trimmed.startsWith('• ')) {{
                    if (!inList) {{
                        resultLines.push('<ul class="list-disc pl-5 my-2 text-slate-350">');
                        inList = true;
                    }}
                    resultLines.push(`<li>${{trimmed.substring(2)}}</li>`);
                }} else {{
                    if (inList) {{
                        resultLines.push('</ul>');
                        inList = false;
                    }}
                    if (trimmed.length > 0) {{
                        resultLines.push(`<p class="mb-2">${{line}}</p>`);
                    }} else {{
                        resultLines.push('<div class="h-2"></div>');
                    }}
                }}
            }}
            if (inList) {{
                resultLines.push('</ul>');
            }}
            
            return `<div class="markdown-content text-sm text-slate-355">${{resultLines.join('')}}</div>`;
        }}

        // Recursive statistics calculator
        function calculateStats(node) {{
            let count = 1;
            let ms = parseInt(node.time_estimate || 0);
            let completed = 0;
            
            const st = (node.status || '').toLowerCase();
            if (st === 'complete' || st === 'done' || st === 'closed') completed = 1;

            if (node.subtasks && node.subtasks.length > 0) {{
                for (let sub of node.subtasks) {{
                    const subStats = calculateStats(sub);
                    count += subStats.count;
                    ms += subStats.ms;
                    completed += subStats.completed;
                }}
            }}
            return {{ count, ms, completed }};
        }}

        // Recursively build sidebar tree directory (Shows all nested levels with dynamic saturation steps)
        function renderSidebarNode(node, level = 0) {{
            if (!node) return '';
            
            const hasSub = node.subtasks && node.subtasks.length > 0;
            const stats = calculateStats(node);
            const estStr = stats.ms > 0 ? ` (${{Math.ceil(stats.ms / 3600000)}}h)` : '';
            
            let paddingLeft = level * 14;
            
            // Calculate dynamic desaturated yellow-orange color per level (+20% saturation step)
            const sat = Math.min(40 + (level * 20), 100);
            const titleColor = `hsl(38, ${{sat}}%, 60%)`;
            
            // Choose elegant icon based on level of nesting
            let icon = '';
            if (level === 0) {{
                icon = `<i class="fa-solid fa-folder" style="color: ${{titleColor}}"></i>`;
            }} else if (level === 1) {{
                icon = `<i class="fa-regular fa-folder" style="color: ${{titleColor}}"></i>`;
            }} else if (level === 2) {{
                icon = `<i class="fa-regular fa-file-lines text-slate-455"></i>`;
            }} else {{
                icon = `<i class="fa-solid fa-angle-right text-[7px]" style="color: ${{titleColor}}"></i>`;
            }}

            let html = `
                <div class="group flex items-center justify-between py-1.5 px-2 rounded-md hover:bg-slate-900/60 cursor-pointer text-xs transition-all" 
                     style="padding-left: ${{paddingLeft}}px" 
                     onclick="scrollToTask('${{node.id}}')">
                    <div class="flex items-center gap-2 truncate">
                        ${{icon}}
                        <span class="truncate font-medium transition-colors" style="color: ${{titleColor}}" title="${{node.name}}">
                            ${{node.name}}
                        </span>
                    </div>
                    <span class="text-[10px] text-slate-500 whitespace-nowrap pl-2">
                        ${{estStr}}
                    </span>
                </div>
            `;

            if (hasSub) {{
                for (let sub of node.subtasks) {{
                    html += renderSidebarNode(sub, level + 1);
                }}
            }}
            
            return html;
        }}

        // Deep Search filter
        function matchesSearch(node, query) {{
            if (!query) return true;
            const q = query.toLowerCase();
            const nameMatch = (node.name || '').toLowerCase().includes(q);
            const descMatch = (node.description || '').toLowerCase().includes(q);
            
            if (nameMatch || descMatch) return true;
            
            if (node.subtasks && node.subtasks.length > 0) {{
                return node.subtasks.some(sub => matchesSearch(sub, query));
            }}
            return false;
        }}

        // Render main tasks recursively as nested frame groups with dynamic color and saturation steps
        function renderMainNode(node, level = 0) {{
            if (!node) return '';
            
            // If searching and this branch has no matches, skip rendering
            if (searchQuery && !matchesSearch(node, searchQuery)) {{
                return '';
            }}

            const hasSub = node.subtasks && node.subtasks.length > 0;
            const isExpanded = expandedNodes.has(node.id);
            const stats = calculateStats(node);
            
            // Format estimate for this specific node or aggregate
            const selfEst = formatEstimate(node.time_estimate);
            const totalEst = formatEstimate(stats.ms);
            
            // Calculate dynamic saturation color step (+20% saturation step per level)
            const sat = Math.min(40 + (level * 20), 100);
            const titleColor = `hsl(38, ${{sat}}%, 60%)`;
            const accentBorderColor = `hsla(38, ${{sat}}%, 60%, 0.4)`;
            
            // CSS classes for nested styling
            let containerClass = "rounded border shadow-md transition-all duration-300 ";
            let headerBgClass = "p-4 flex items-center justify-between cursor-pointer ";
            let borderStyle = "";
            let styleAttr = "";
            
            if (level === 0) {{
                // Level 1: Groups (e.g. GROUP 5 — Full App Design) - Keeps thick left accent border
                containerClass += "bg-slate-900/15 border-brand-900/20 hover:border-brand-500/20 mb-5";
                headerBgClass += "bg-gradient-to-r from-brand-950/30 to-slate-950 hover:from-brand-950/50 hover:to-slate-900/80 border-b border-brand-900/10";
                borderStyle = "border-l-4 border-l-brand-900/30 hover:border-l-brand-500/90 transition-all duration-300";
            }} else {{
                // Levels 2+: Sub-categories, screens, subtasks - NO left-border accent coloring (clean slate rounded boxes)
                containerClass += "bg-slate-950/15 border-slate-900/85 hover:border-slate-855 my-2";
                headerBgClass += "bg-transparent hover:bg-slate-900/20 py-2.5 px-4";
                borderStyle = "";
                styleAttr = "";
            }}

            // Search query text highlighter
            function highlightText(text) {{
                if (!searchQuery || !text) return text || '';
                const regex = new RegExp(`(${{searchQuery.replace(/[-\/\\^$*+?.()|[\]{{}}]/g, '\\$&')}})`, 'gi');
                return text.replace(regex, '<mark class="bg-brand-500/25 text-brand-200 border-b border-brand-500/80 px-0.5 rounded-sm">$1</mark>');
            }}

            // Indented subtask frame wrapping container with custom guide lines matching hierarchy saturation
            let subtasksHtml = '';
            if (hasSub) {{
                const guideSat = Math.min(40 + ((level + 1) * 20), 100);
                const guideColor = `hsla(38, ${{guideSat}}%, 55%, 0.12)`;
                subtasksHtml = `
                    <div class="pl-4 ml-3.5 border-l space-y-2.5 collapsible-content ${{isExpanded ? 'block' : 'hidden'}}" 
                         style="border-color: ${{guideColor}}" id="children-${{node.id}}">
                        ${{node.subtasks.map(sub => renderMainNode(sub, level + 1)).join('')}}
                    </div>
                `;
            }}

            const timeBadge = totalEst 
                ? `<span class="text-xs text-slate-450 flex items-center gap-1 bg-transparent px-1 whitespace-nowrap">
                       <i class="fa-solid fa-clock text-brand-500/70 text-[10px]"></i> ${{level === 0 ? totalEst : selfEst || totalEst}}
                   </span>`
                : '';

            // Subtask count badge
            const subCountBadge = hasSub
                ? `<span class="text-[10px] text-slate-455 bg-brand-900/10 px-2 py-0.5 rounded-sm border border-brand-800/10 whitespace-nowrap flex items-center gap-1 font-medium">
                       <i class="fa-solid fa-network-wired text-brand-500/80"></i> ${{stats.count - 1}} Subtask${{(stats.count - 1) !== 1 ? 's' : ''}}
                   </span>`
                : '';

            // Expand/Collapse Indicator button on the very far right of the card header
            const toggleBtn = hasSub
                ? `<span class="p-1 text-slate-500 hover:text-slate-300 transition-colors shrink-0 ml-1">
                       <i class="fa-solid fa-chevron-down transition-transform duration-300 text-xs ${{isExpanded ? 'rotate-0' : '-rotate-90'}}"></i>
                   </span>`
                : '';

            const html = `
                <div class="task-node scroll-mt-24" id="task-card-${{node.id}}">
                    <div class="${{containerClass}} ${{borderStyle}}" style="${{styleAttr}}">
                        
                        <!-- HEADER BAR -->
                        <div class="${{headerBgClass}}" onclick="toggleNode('${{node.id}}', event)">
                            <div class="flex items-center gap-2.5 min-w-0 mr-4">
                                <h3 class="text-sm font-semibold truncate outfit-font tracking-wide" style="color: ${{titleColor}}" title="${{node.name}}">
                                    ${{highlightText(node.name)}}
                                </h3>
                            </div>
                            
                            <!-- Badges & Toggle Button - WITHOUT STATUS BADGES (TODO TAGS REMOVED) -->
                            <div class="flex items-center gap-2 shrink-0">
                                ${{subCountBadge}}
                                ${{timeBadge}}
                                ${{toggleBtn}}
                            </div>
                        </div>
                        
                        <!-- COLLAPSIBLE BODY -->
                        <div class="${{(!hasSub || isExpanded) ? 'block' : 'hidden'}}" id="body-${{node.id}}">
                            <!-- Description (Only show if present - WITHOUT section header) -->
                            ${{node.description ? `
                                <div class="px-5 py-3.5 border-t border-slate-900/60 bg-slate-950/20">
                                    ${{formatDescription(node.description)}}
                                </div>
                            ` : ''}}
                            
                            <!-- Child Subtasks Container -->
                            ${{subtasksHtml}}
                        </div>
                        
                    </div>
                </div>
            `;
            return html;
        }}

        // Toggle collapsible node
        function toggleNode(nodeId, event) {{
            const body = document.getElementById(`body-${{nodeId}}`);
            const children = document.getElementById(`children-${{nodeId}}`);
            const header = event.currentTarget;
            const chevron = header.querySelector('.fa-chevron-down');
            
            if (expandedNodes.has(nodeId)) {{
                expandedNodes.delete(nodeId);
                if (body) body.classList.add('hidden');
                if (children) children.classList.add('hidden');
                if (chevron) {{
                    chevron.classList.add('-rotate-90');
                }}
            }} else {{
                expandedNodes.add(nodeId);
                if (body) body.classList.remove('hidden');
                if (children) children.classList.remove('hidden');
                if (chevron) {{
                    chevron.classList.remove('-rotate-90');
                }}
            }}
        }}

        // Expand All
        function expandAll() {{
            const recurse = (node) => {{
                expandedNodes.add(node.id);
                if (node.subtasks) {{
                    node.subtasks.forEach(recurse);
                }}
            }};
            taskData.subtasks.forEach(recurse);
            renderUI();
        }}

        // Collapse All
        function collapseAll() {{
            expandedNodes.clear();
            renderUI();
        }}

        // Search engine that auto-expands matching branches
        function handleSearch(val) {{
            searchQuery = val.trim();
            const clearBtn = document.getElementById('clear-search-btn');
            
            if (searchQuery) {{
                clearBtn.classList.remove('hidden');
                // Auto expand matching branches
                expandedNodes.clear();
                function recurse(node) {{
                    if (matchesSearch(node, searchQuery)) {{
                        expandedNodes.add(node.id);
                        if (node.subtasks) {{
                            node.subtasks.forEach(recurse);
                        }}
                    }}
                }}
                taskData.subtasks.forEach(recurse);
            }} else {{
                clearBtn.classList.add('hidden');
                // Reset to default (expand groups only)
                initDefaultExpansion();
            }}
            renderUI();
        }}

        // Clear search input
        function clearSearch() {{
            document.getElementById('search-input').value = "";
            handleSearch("");
        }}

        // Smooth scroll to a target task element
        function scrollToTask(id) {{
            // Make sure the target and all its parent nodes are expanded so it is visible
            function expandParentOf(node, targetId, path = []) {{
                if (node.id === targetId) {{
                    path.forEach(pid => expandedNodes.add(pid));
                    expandedNodes.add(targetId);
                    return true;
                }}
                if (node.subtasks) {{
                    for (let sub of node.subtasks) {{
                        if (expandParentOf(sub, targetId, [...path, node.id])) {{
                            return true;
                        }}
                    }}
                }}
                return false;
            }}
            
            expandParentOf(taskData, id);
            renderUI();
            
            setTimeout(() => {{
                const el = document.getElementById(`task-card-${{id}}`);
                if (el) {{
                    el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    
                    // Add accent glow
                    const card = el.querySelector('.rounded');
                    if (card) {{
                        card.classList.add('task-card-active');
                        setTimeout(() => {{
                            card.classList.remove('task-card-active');
                        }}, 2000);
                    }}
                }}
            }}, 150);
        }}

        // Initialize default expansion (level 0 expanded, others collapsed)
        function initDefaultExpansion() {{
            expandedNodes.clear();
            taskData.subtasks.forEach(group => {{
                expandedNodes.add(group.id);
            }});
        }}

        // Refresh dynamic UI elements
        function renderUI() {{
            const sidebar = document.getElementById('sidebar-tree');
            const mainContainer = document.getElementById('tasks-container');
            
            // 1. Render Sidebar
            let sidebarHtml = '';
            for (let group of taskData.subtasks) {{
                sidebarHtml += renderSidebarNode(group, 0);
            }}
            sidebar.innerHTML = sidebarHtml;
            
            // 2. Render Main Cards
            let mainHtml = '';
            for (let group of taskData.subtasks) {{
                mainHtml += renderMainNode(group, 0);
            }}
            
            if (!mainHtml) {{
                mainContainer.innerHTML = `
                    <div class="text-center py-20 border border-dashed border-slate-800/80 rounded-xl bg-slate-900/10">
                        <i class="fa-solid fa-folder-open text-4xl text-slate-700 mb-3"></i>
                        <h3 class="text-base font-semibold text-slate-400 outfit-font font-medium">No Results Found</h3>
                        <p class="text-xs text-slate-500 mt-1">No tasks matched the search term "${{searchQuery}}".</p>
                    </div>
                `;
            }} else {{
                mainContainer.innerHTML = mainHtml;
            }}
        }}

        // Compute global stats
        function initStats() {{
            const stats = calculateStats(taskData);
            
            // Total tasks is stats.count - 1 (excluding root task itself)
            document.getElementById('total-count-stat').textContent = stats.count - 1;
            
            const hours = Math.round(stats.ms / 3600000);
            document.getElementById('total-time-stat').textContent = `${{hours}}h`;
        }}

        // Sync with ClickUp Functionality
        let isSyncing = false;

        function showModal(id) {{
            const el = document.getElementById(id);
            if (el) {{
                el.classList.remove('pointer-events-none');
                el.classList.remove('opacity-0');
            }}
        }}

        function hideModal(id) {{
            const el = document.getElementById(id);
            if (el) {{
                el.classList.add('pointer-events-none');
                el.classList.add('opacity-0');
            }}
        }}

        function setStepState(stepNum, state) {{
            // state can be 'pending', 'active', 'done'
            const stepEl = document.getElementById(`status-step-${{stepNum}}`);
            const pendingEl = document.getElementById(`step-${{stepNum}}-pending`);
            const spinnerEl = document.getElementById(`step-${{stepNum}}-spinner`);
            const checkEl = document.getElementById(`step-${{stepNum}}-check`);
            
            if (!stepEl) return;
            
            if (state === 'pending') {{
                stepEl.className = "flex items-center gap-2.5 text-slate-500 transition-colors duration-200";
                if (pendingEl) pendingEl.classList.remove('hidden');
                if (spinnerEl) spinnerEl.classList.add('hidden');
                if (checkEl) checkEl.classList.add('hidden');
            }} else if (state === 'active') {{
                stepEl.className = "flex items-center gap-2.5 text-brand-400 font-semibold transition-colors duration-200";
                if (pendingEl) pendingEl.classList.add('hidden');
                if (spinnerEl) spinnerEl.classList.remove('hidden');
                if (checkEl) checkEl.classList.add('hidden');
            }} else if (state === 'done') {{
                stepEl.className = "flex items-center gap-2.5 text-brand-500 transition-colors duration-200";
                if (pendingEl) pendingEl.classList.add('hidden');
                if (spinnerEl) spinnerEl.classList.add('hidden');
                if (checkEl) checkEl.classList.remove('hidden');
            }}
        }}

        async function syncWithClickUp() {{
            if (isSyncing) return;
            isSyncing = true;
            
            // UI Button syncing state
            const btn = document.getElementById('sync-btn');
            const icon = document.getElementById('sync-icon');
            const text = document.getElementById('sync-text');
            
            if (btn) btn.disabled = true;
            if (icon) icon.classList.add('fa-spin');
            if (text) text.textContent = "Syncing...";
            
            // Show loading modal and reset steps
            showModal('sync-modal');
            setStepState(1, 'active');
            setStepState(2, 'pending');
            setStepState(3, 'pending');
            
            try {{
                // Step 1: Connecting and downloading
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout
                
                // Fetch from localhost background server
                const response = await fetch('http://localhost:5001/api/refresh', {{
                    method: 'GET',
                    signal: controller.signal
                }});
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {{
                    throw new Error(`Server returned HTTP ${{response.status}}`);
                }}
                
                const data = await response.json();
                
                if (data.status === 'success') {{
                    // Update steps state dynamically with micro-delays for visual feedback
                    setStepState(1, 'done');
                    setStepState(2, 'active');
                    
                    await new Promise(resolve => setTimeout(resolve, 800));
                    setStepState(2, 'done');
                    setStepState(3, 'active');
                    
                    await new Promise(resolve => setTimeout(resolve, 800));
                    setStepState(3, 'done');
                    
                    await new Promise(resolve => setTimeout(resolve, 500));
                    // Success reload
                    window.location.reload();
                }} else {{
                    throw new Error(data.message || 'Unknown error occurred during sync');
                }}
            }} catch (err) {{
                console.error("Sync error:", err);
                // Reset loading state
                hideModal('sync-modal');
                
                if (btn) btn.disabled = false;
                if (icon) icon.classList.remove('fa-spin');
                if (text) text.textContent = "Sync ClickUp";
                
                // Show offline/error instruction modal
                showModal('offline-modal');
            }} finally {{
                isSyncing = false;
            }}
        }}

        function closeOfflineModal() {{
            hideModal('offline-modal');
        }}

        function retrySync() {{
            closeOfflineModal();
            syncWithClickUp();
        }}

        // Initialize the Web App
        window.addEventListener('DOMContentLoaded', () => {{
            initDefaultExpansion();
            renderUI();
            initStats();
        }});
    </script>
</body>
</html>
"""

    # Write HTML file robustly inside the parent folder of scripts directory
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generated ux_redesign_tasks.html successfully!")

if __name__ == "__main__":
    main()
