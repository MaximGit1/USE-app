<script setup>
import { marked } from 'marked';
import hljs from 'highlight.js';
import 'highlight.js/styles/github-dark.css';

const props = defineProps({
    content: String
});

const renderMarkdown = (text) => {
    const renderer = new marked.Renderer();
    
    renderer.code = (code, language) => {
        const codeString = String(code || '').trim();
        const lang = (language || 'plaintext').toLowerCase();
        const validLang = hljs.getLanguage(lang) ? lang : 'plaintext';
        
        try {
            const highlighted = hljs.highlight(codeString, { 
                language: validLang,
                ignoreIllegals: true 
            }).value;
            
            return `<pre><code class="hljs language-${validLang}">${highlighted}</code></pre>`;
        } catch (e) {
            return `<pre><code>${codeString}</code></pre>`;
        }
    };

    return marked(text || '', {
        renderer,
        breaks: true,
        gfm: true
    });
};
</script>

<template>
    <div class="markdown-body" v-html="renderMarkdown(content)"></div>
</template>

<style scoped>
.markdown-body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.6;
}

.markdown-body >>> pre {
    background: #1e1e1e;
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1rem 0;
}

.markdown-body >>> code {
    font-family: 'Fira Code', monospace;
    font-size: 0.9em;
}

.markdown-body >>> .hljs {
    background: transparent;
}
</style>